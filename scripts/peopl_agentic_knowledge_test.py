#!/usr/bin/env python3
"""People Agentic Knowledge Test runbook (Initiative 79 P3a).

Paired runbook for ``SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`` per
[`akos-executable-process-catalog.mdc`](../.cursor/rules/akos-executable-process-catalog.mdc)
Rule 1 (paired SOP plus runbook). Implements the monthly knowledge-test cadence
described in the SOP §3.

Design intent: minimal Python with zero framework dependencies. People's tooling
stays portable across whichever underlying agent infrastructure Tech Lab chooses
(governed by ``AGENTIC_FRAMEWORK_LANDSCAPE.md``). This runbook reads canonicals
as plain text, presents questions one at a time to whichever agent (or human
operator) is running it, records answers as plain text, and writes structured
results under
``docs/wip/planning/79-people-manifesto-and-pattern-library/reports/knowledge-tests/<YYYY-MM>/<agent-name>.md``.

Usage::

    py scripts/peopl_agentic_knowledge_test.py --agent-name madeira --bank default
    py scripts/peopl_agentic_knowledge_test.py --agent-name madeira --bank default --interactive
    py scripts/peopl_agentic_knowledge_test.py --list-banks
    py scripts/peopl_agentic_knowledge_test.py --validate-bank default

Modes:

- Default (non-interactive): writes a result-file template that the operator
  fills in by hand or that an agent shell auto-fills when invoked. Useful for
  scheduled CI runs that prepare the result file in advance of the session.
- ``--interactive``: prompts the operator question by question; collects answers
  on stdin; emits a populated result file. Useful for an unattended agent run
  or a hands-on operator session.
- ``--validate-bank``: checks that every question in the bank has a citation
  resolving to a real canonical line range. Useful before the cadence runs.

Per ``CONTRIBUTING.md`` Python Code Standards: type hints + structured logging
via ``akos.log.setup_logging`` + ``pathlib`` paths + no shell-specific
constructs.

Cross-references:

- ``SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`` (paired SOP).
- ``HOLISTIKA_AGENTIC_DOCTRINE.md`` (doctrine the cadence operationalises).
- ``akos-executable-process-catalog.mdc`` Rule 1 (pairing rule).
- ``process_list.csv`` row ``tbi_peopl_dtp_agentic_ops_mtnce_001`` (this is the
  paired runbook for that scheduled cadence row).
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import logging
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.peopl_agentic_knowledge_test")

REPORTS_ROOT = (
    REPO_ROOT
    / "docs" / "wip" / "planning" / "79-people-manifesto-and-pattern-library"
    / "reports" / "knowledge-tests"
)


@dataclasses.dataclass(frozen=True)
class KnowledgeTestQuestion:
    """One question in a knowledge-test bank.

    Attributes:
        question_id: Stable slug; matches ``^q[0-9]+_[a-z0-9_]+$``.
        prompt: The plain-language question put to the agent.
        canonical_path: Repo-relative path to the canonical that holds the answer.
        canonical_line_range: Hint such as ``"§3"`` or ``"L42-L58"``; informational.
        expected_answer_keywords: Tokens the agent's answer should contain to
            score Pass. Match is case-insensitive substring; the operator
            still applies judgement on the final mark.
    """

    question_id: str
    prompt: str
    canonical_path: str
    canonical_line_range: str
    expected_answer_keywords: tuple[str, ...]


# Default bank: 7 questions grounded in the People canonicals.
# Banks are extensible by adding new ``KnowledgeTestQuestion`` tuples or by
# loading from a JSON file via ``--bank-path``. The default bank is enough
# to run the first session cleanly; additional banks per agent role-class
# may be authored later.
DEFAULT_BANK: tuple[KnowledgeTestQuestion, ...] = (
    KnowledgeTestQuestion(
        question_id="q1_people_dod",
        prompt="What does it mean to say People is a discipline of disciplines?",
        canonical_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md",
        canonical_line_range="§2",
        expected_answer_keywords=("design pattern", "other areas", "consulting"),
    ),
    KnowledgeTestQuestion(
        question_id="q2_singularity",
        prompt="What does process singularity mean and how is it made countable?",
        canonical_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md",
        canonical_line_range="§1, §4",
        expected_answer_keywords=("inherited_pattern_id", "process_list", "pattern"),
    ),
    KnowledgeTestQuestion(
        question_id="q3_kb_stewardship",
        prompt="Who owns the knowledge-base accessibility responsibility at Holistika?",
        canonical_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md",
        canonical_line_range="§3",
        expected_answer_keywords=("People", "every role"),
    ),
    KnowledgeTestQuestion(
        question_id="q4_jargon_split",
        prompt="Where do framework names and infrastructure jargon belong, and where do they not belong?",
        canonical_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md",
        canonical_line_range="§7",
        expected_answer_keywords=("Tech Lab", "framework", "People canonicals"),
    ),
    KnowledgeTestQuestion(
        question_id="q5_agent_in_charge",
        prompt="What does the Agent-in-Charge frame mean for SOPs?",
        canonical_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md",
        canonical_line_range="§2",
        expected_answer_keywords=("SOP", "role", "human", "agent"),
    ),
    KnowledgeTestQuestion(
        question_id="q6_knowledge_test_cadence",
        prompt="What is the People-side knowledge-test cadence and what does Drift mean?",
        canonical_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md",
        canonical_line_range="§3",
        expected_answer_keywords=("monthly", "canonical", "drift"),
    ),
    KnowledgeTestQuestion(
        question_id="q7_madeira_role_class",
        prompt="What is Madeira and what survives an underlying infrastructure upgrade?",
        canonical_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md",
        canonical_line_range="§4",
        expected_answer_keywords=("role", "archetype"),
    ),
)


def _load_bank(bank_name: str, bank_path: Path | None) -> tuple[KnowledgeTestQuestion, ...]:
    """Load a knowledge-test bank by name or by path.

    Currently supports ``default`` (the in-module bank) plus arbitrary JSON
    files via ``--bank-path``. JSON files are arrays of objects with the
    ``KnowledgeTestQuestion`` field names.
    """
    if bank_path is not None:
        if not bank_path.is_file():
            raise FileNotFoundError(f"bank path not found: {bank_path}")
        raw = json.loads(bank_path.read_text(encoding="utf-8"))
        return tuple(
            KnowledgeTestQuestion(
                question_id=row["question_id"],
                prompt=row["prompt"],
                canonical_path=row["canonical_path"],
                canonical_line_range=row.get("canonical_line_range", ""),
                expected_answer_keywords=tuple(row.get("expected_answer_keywords", ())),
            )
            for row in raw
        )
    if bank_name == "default":
        return DEFAULT_BANK
    raise ValueError(f"unknown bank name: {bank_name}; pass --bank-path for a JSON bank")


def _validate_bank(bank: tuple[KnowledgeTestQuestion, ...]) -> int:
    """Check that every canonical_path in the bank resolves to a file."""
    failures: list[str] = []
    seen_ids: set[str] = set()
    slug_re = re.compile(r"^q[0-9]+_[a-z0-9_]+$")
    for q in bank:
        if not slug_re.match(q.question_id):
            failures.append(f"{q.question_id}: question_id must match {slug_re.pattern}")
        if q.question_id in seen_ids:
            failures.append(f"{q.question_id}: duplicate question_id")
        seen_ids.add(q.question_id)
        canonical = REPO_ROOT / q.canonical_path
        if not canonical.is_file():
            failures.append(f"{q.question_id}: canonical_path not a file: {q.canonical_path}")
    if failures:
        for f in failures:
            print(f"  FAIL: {f}")
        return 1
    print(f"  PASS: bank validated ({len(bank)} questions; all canonical_paths resolve)")
    return 0


def _emit_result_template(
    *,
    agent_name: str,
    bank: tuple[KnowledgeTestQuestion, ...],
    interactive: bool,
) -> Path:
    """Write a result-file template (or populated file in interactive mode) and return its path."""
    today = dt.date.today()
    month_dir = REPORTS_ROOT / f"{today.year:04d}-{today.month:02d}"
    month_dir.mkdir(parents=True, exist_ok=True)
    out_path = month_dir / f"{agent_name}.md"
    lines: list[str] = []
    lines.append(f"# Knowledge-test result — {agent_name} — {today.isoformat()}")
    lines.append("")
    lines.append(f"- agent_name: {agent_name}")
    lines.append(f"- session_date: {today.isoformat()}")
    lines.append("- session_operator: <fill-in operator handle>")
    lines.append(f"- bank_size: {len(bank)}")
    lines.append("- bank_name: default")
    lines.append("- verdict: <PASS/FAIL/DRIFT-only — fill after scoring>")
    lines.append("")
    lines.append("## Questions and answers")
    lines.append("")
    for i, q in enumerate(bank, start=1):
        lines.append(f"### Q{i}. {q.question_id}")
        lines.append("")
        lines.append(f"**Canonical:** [`{q.canonical_path}`]({_relative_link_to_repo(q.canonical_path)}) — {q.canonical_line_range or 'whole file'}")
        lines.append("")
        lines.append(f"**Prompt:** {q.prompt}")
        lines.append("")
        if interactive:
            print(f"\nQ{i}. {q.prompt}")
            print(f"   (answer should reference: {', '.join(q.expected_answer_keywords)})")
            try:
                answer = input("Answer: ").strip()
            except EOFError:
                answer = "<no answer recorded; stdin closed>"
            lines.append(f"**Agent answer:** {answer}")
        else:
            lines.append("**Agent answer:** <fill in agent answer>")
        lines.append("")
        lines.append("**Expected answer keywords:** " + ", ".join(q.expected_answer_keywords))
        lines.append("")
        lines.append("**Operator mark:** <Pass / Fail / Drift>")
        lines.append("")
        lines.append("**Notes:** <optional drift signal or escalation pointer>")
        lines.append("")
    lines.append("## Outcomes")
    lines.append("")
    lines.append("- Pass count: <fill>")
    lines.append("- Fail count: <fill>")
    lines.append("- Drift count: <fill>")
    lines.append("- Verdict: <PASS / FAIL>")
    lines.append("- Canonical-revision tickets opened: <list or none>")
    lines.append("- Escalation records: <list or none>")
    lines.append("")
    lines.append("## Cross-references")
    lines.append("")
    lines.append("- [SOP-PEOPLE_AGENTIC_OPERATIONS_001.md](../../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md)")
    lines.append("- [HOLISTIKA_AGENTIC_DOCTRINE.md](../../../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md)")
    lines.append("")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def _relative_link_to_repo(repo_relative_path: str) -> str:
    """Compute a Markdown link from the result-file location to a repo-root path.

    The result file lives 5 levels deep under the repo root
    (``docs/wip/planning/79-.../reports/knowledge-tests/<YYYY-MM>/``). So the
    relative path back is six ``../`` segments before the repo-relative path.
    """
    return "../../../../../../" + repo_relative_path


def main(argv: list[str] | None = None) -> int:
    setup_logging()
    parser = argparse.ArgumentParser(description="People Agentic Knowledge Test runbook (I79 P3a)")
    parser.add_argument("--agent-name", type=str, help="Stable slug for the agent under test (e.g. 'madeira')")
    parser.add_argument("--bank", type=str, default="default", help="Bank name (default: 'default')")
    parser.add_argument("--bank-path", type=Path, help="Optional JSON path with a custom bank")
    parser.add_argument("--interactive", action="store_true", help="Prompt question by question on stdin")
    parser.add_argument("--list-banks", action="store_true", help="List known banks and exit")
    parser.add_argument("--validate-bank", type=str, help="Validate the named bank and exit")
    args = parser.parse_args(argv)

    if args.list_banks:
        print("  default (in-module; 7 questions; covers People manifesto + agentic doctrine)")
        return 0

    bank = _load_bank(args.validate_bank or args.bank, args.bank_path)

    if args.validate_bank:
        return _validate_bank(bank)

    if not args.agent_name:
        parser.error("--agent-name is required when not validating a bank")

    slug_re = re.compile(r"^[a-z][a-z0-9_-]*$")
    if not slug_re.match(args.agent_name):
        parser.error(f"--agent-name must match {slug_re.pattern}; got {args.agent_name!r}")

    out_path = _emit_result_template(agent_name=args.agent_name, bank=bank, interactive=args.interactive)
    print(f"\n  Wrote knowledge-test result template at:\n    {out_path}")
    if not args.interactive:
        print("\n  Run again with --interactive for question-by-question prompts,")
        print("  or fill in the template by hand and commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
