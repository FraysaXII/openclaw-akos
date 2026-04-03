"""Ollama embedding client for AKOS semantic routing.

Uses the locally running ``nomic-embed-text`` model (already deployed for
OpenClaw memory search) to produce embeddings without any additional
dependencies beyond ``urllib``.
"""

from __future__ import annotations

import json
import logging
import math
import os
import urllib.error
import urllib.request
from typing import Any

logger = logging.getLogger("akos.embeddings")

_DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
_DEFAULT_MODEL = "nomic-embed-text"


def _ollama_embed(texts: list[str], *, model: str | None = None, base_url: str | None = None) -> list[list[float]]:
    """Call the Ollama ``/api/embed`` endpoint and return embedding vectors."""
    url = (base_url or os.environ.get("OLLAMA_BASE_URL", _DEFAULT_OLLAMA_URL)).rstrip("/")
    mdl = model or os.environ.get("AKOS_EMBED_MODEL", _DEFAULT_MODEL)
    payload = json.dumps({"model": mdl, "input": texts}).encode("utf-8")
    req = urllib.request.Request(
        f"{url}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("embeddings", [])


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class EmbeddingClassifier:
    """Classify queries by cosine similarity against a bank of route exemplars.

    Exemplar embeddings are computed once at construction and cached for the
    process lifetime.  Each call to ``classify()`` embeds the input query and
    returns the best-matching route with a confidence score.
    """

    def __init__(self, exemplar_bank: dict[str, list[str]], *, model: str | None = None, base_url: str | None = None) -> None:
        self._model = model
        self._base_url = base_url
        self._route_names: list[str] = []
        self._route_embeddings: list[list[float]] = []
        self._available = False
        try:
            self._build_cache(exemplar_bank)
            self._available = True
        except Exception as exc:
            logger.warning("Embedding classifier unavailable (Ollama unreachable?): %s", exc)

    @property
    def available(self) -> bool:
        return self._available

    def _build_cache(self, exemplar_bank: dict[str, list[str]]) -> None:
        all_texts: list[str] = []
        route_map: list[str] = []
        for route, examples in exemplar_bank.items():
            for text in examples:
                all_texts.append(text)
                route_map.append(route)

        if not all_texts:
            return

        embeddings = _ollama_embed(all_texts, model=self._model, base_url=self._base_url)
        self._route_names = route_map
        self._route_embeddings = embeddings

    def classify(self, query: str, *, threshold: float = 0.3) -> dict[str, Any]:
        """Return the best-matching route for *query*.

        Returns ``{"route": str, "confidence": float, "method": "embedding"}``
        or ``{"route": "other", "confidence": 0.0, "method": "embedding"}``
        when no exemplar exceeds *threshold*.
        """
        if not self._available or not self._route_embeddings:
            return {"route": "other", "confidence": 0.0, "method": "embedding_unavailable"}

        try:
            query_emb = _ollama_embed([query], model=self._model, base_url=self._base_url)[0]
        except Exception as exc:
            logger.debug("Failed to embed query: %s", exc)
            return {"route": "other", "confidence": 0.0, "method": "embedding_error"}

        best_route = "other"
        best_score = 0.0
        route_scores: dict[str, float] = {}

        for name, emb in zip(self._route_names, self._route_embeddings):
            sim = _cosine_similarity(query_emb, emb)
            if name not in route_scores or sim > route_scores[name]:
                route_scores[name] = sim
            if sim > best_score:
                best_score = sim
                best_route = name

        if best_score < threshold:
            return {"route": "other", "confidence": best_score, "method": "embedding"}

        return {"route": best_route, "confidence": round(best_score, 4), "method": "embedding"}
