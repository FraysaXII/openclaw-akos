"""Unit tests for the 3 Layer-1/2/3 Pydantic models (Initiative 86 Wave L).

Covers:
- akos.hlk_output_type_registry_csv.OutputTypeRegistryRow (Layer 1)
- akos.hlk_artifact_class_registry_csv.ArtifactClassRegistryRow (Layer 2)
- akos.hlk_component_primitive_registry_csv.ComponentPrimitiveRegistryRow (Layer 3)

Per CONTRIBUTING.md "Python Code Standards": tests carry valid + invalid input
pairs; registered under the @pytest.mark.unit group.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from akos.hlk_artifact_class_registry_csv import (
    ARTIFACT_CLASS_REGISTRY_FIELDNAMES,
    ArtifactClassRegistryRow,
)
from akos.hlk_component_primitive_registry_csv import (
    COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES,
    ComponentPrimitiveRegistryRow,
    VALID_KINDS,
)
from akos.hlk_output_type_registry_csv import (
    OUTPUT_TYPE_REGISTRY_FIELDNAMES,
    OutputTypeRegistryRow,
    VALID_MEDIUM_CLASSES,
    VALID_RENDER_TARGETS,
)


pytestmark = pytest.mark.unit


# ---------- Layer 1: OUTPUT_TYPE_REGISTRY ----------


VALID_OT_ROW: dict[str, str] = {
    "output_type_code": "OT-PROSE-MARKDOWN",
    "name": "Plain markdown prose",
    "medium_class": "text",
    "render_targets": "web;pdf;mail;erp",
    "authoring_tool": "markdown editor",
    "accessibility_concerns": "reading-level + heading hierarchy",
    "brand_visual_anchor": "brand-voice register",
    "status": "active",
    "added_at": "2026-05-20",
    "last_review_at": "2026-05-20",
    "last_review_by": "Founder",
    "last_review_decision_id": "D-IH-86-BB",
    "methodology_version_at_review": "v3.1",
    "notes": "test row",
}


def test_output_type_fieldnames_count():
    assert len(OUTPUT_TYPE_REGISTRY_FIELDNAMES) == 14


def test_output_type_valid_row_parses():
    row = OutputTypeRegistryRow(**VALID_OT_ROW)
    assert row.output_type_code == "OT-PROSE-MARKDOWN"
    assert row.medium_class == "text"


def test_output_type_invalid_code_rejected():
    bad = dict(VALID_OT_ROW, output_type_code="ot-lowercase")
    with pytest.raises(ValidationError):
        OutputTypeRegistryRow(**bad)


def test_output_type_invalid_medium_class_rejected():
    bad = dict(VALID_OT_ROW, medium_class="not-a-valid-class")
    with pytest.raises(ValidationError):
        OutputTypeRegistryRow(**bad)


def test_output_type_invalid_status_rejected():
    bad = dict(VALID_OT_ROW, status="something-else")
    with pytest.raises(ValidationError):
        OutputTypeRegistryRow(**bad)


def test_output_type_invalid_decision_id_rejected():
    bad = dict(VALID_OT_ROW, last_review_decision_id="NOT-A-DECISION")
    with pytest.raises(ValidationError):
        OutputTypeRegistryRow(**bad)


def test_output_type_invalid_methodology_version_rejected():
    bad = dict(VALID_OT_ROW, methodology_version_at_review="3.1")
    with pytest.raises(ValidationError):
        OutputTypeRegistryRow(**bad)


def test_output_type_valid_medium_classes_complete():
    assert VALID_MEDIUM_CLASSES == frozenset(
        {"text", "visual", "multimedia", "interactive", "document"}
    )


def test_output_type_valid_render_targets_complete():
    assert VALID_RENDER_TARGETS == frozenset(
        {"pdf", "web", "erp", "mail", "slide", "broadcast"}
    )


# ---------- Layer 2: ARTIFACT_CLASS_REGISTRY ----------


VALID_AC_ROW: dict[str, str] = {
    "artifact_class_code": "AC-COVER-EMAIL",
    "name": "Cover email",
    "output_type_codes": "OT-PROSE-MARKDOWN;OT-PROSE-EMAIL-RICH",
    "typical_audience_codes": "J-IN;J-AD",
    "typical_channel_codes": "CHAN-EMAIL-OUTBOUND",
    "render_script_path": "scripts/render_cover_email.py",
    "exemplar_path": "docs/.../cover_email_en.md",
    "doctrine_owner_role": "Brand & Narrative Manager",
    "quality_fabric_invocation": "fabric.compose(audience,channel,scenario,brand,governance)",
    "status": "active",
    "added_at": "2026-05-20",
    "last_review_at": "2026-05-20",
    "last_review_by": "Founder",
    "last_review_decision_id": "D-IH-86-BB",
    "methodology_version_at_review": "v3.1",
    "notes": "test row",
}


def test_artifact_class_fieldnames_count():
    assert len(ARTIFACT_CLASS_REGISTRY_FIELDNAMES) == 16


def test_artifact_class_valid_row_parses():
    row = ArtifactClassRegistryRow(**VALID_AC_ROW)
    assert row.artifact_class_code == "AC-COVER-EMAIL"


def test_artifact_class_invalid_code_rejected():
    bad = dict(VALID_AC_ROW, artifact_class_code="cover-email")
    with pytest.raises(ValidationError):
        ArtifactClassRegistryRow(**bad)


def test_artifact_class_empty_audience_rejected():
    bad = dict(VALID_AC_ROW, typical_audience_codes="")
    with pytest.raises(ValidationError):
        ArtifactClassRegistryRow(**bad)


def test_artifact_class_render_script_optional():
    """Render script path may be empty for purely-authored artifacts."""
    ok = dict(VALID_AC_ROW, render_script_path="")
    row = ArtifactClassRegistryRow(**ok)
    assert row.render_script_path == ""


# ---------- Layer 3: COMPONENT_PRIMITIVE_REGISTRY ----------


VALID_CP_ROW: dict[str, str] = {
    "component_primitive_code": "CP-CTA",
    "name": "Call-to-action",
    "kind": "prose",
    "parent_artifact_class_codes": "AC-COVER-EMAIL;AC-INTRO-MESSAGE",
    "research_dimensions": "ask-clarity;reciprocity-fit",
    "a11y_dimensions": "reading-order;link-text",
    "brand_dimensions": "voice-register;ask-tone",
    "doctrine_path": "COMPONENT_PRIMITIVE_LIBRARY.md#cp-cta",
    "status": "active",
    "added_at": "2026-05-20",
    "last_review_at": "2026-05-20",
    "last_review_by": "Founder",
    "last_review_decision_id": "D-IH-86-BB",
    "methodology_version_at_review": "v3.1",
    "notes": "test row",
}


def test_component_primitive_fieldnames_count():
    assert len(COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES) == 15


def test_component_primitive_valid_row_parses():
    row = ComponentPrimitiveRegistryRow(**VALID_CP_ROW)
    assert row.component_primitive_code == "CP-CTA"


def test_component_primitive_multi_kind_accepted_at_pydantic_layer():
    """Pydantic layer accepts semicolon-list; validator layer FK-validates tokens."""
    multi = dict(VALID_CP_ROW, kind="prose;visual")
    row = ComponentPrimitiveRegistryRow(**multi)
    assert row.kind == "prose;visual"


def test_component_primitive_empty_kind_rejected():
    bad = dict(VALID_CP_ROW, kind="")
    with pytest.raises(ValidationError):
        ComponentPrimitiveRegistryRow(**bad)


def test_component_primitive_valid_kinds_complete():
    assert VALID_KINDS == frozenset(
        {"prose", "visual", "interactive", "mixed"}
    )


def test_component_primitive_invalid_code_rejected():
    bad = dict(VALID_CP_ROW, component_primitive_code="cp-lowercase")
    with pytest.raises(ValidationError):
        ComponentPrimitiveRegistryRow(**bad)


def test_component_primitive_frozen():
    """Pydantic frozen=True; mutation should fail."""
    row = ComponentPrimitiveRegistryRow(**VALID_CP_ROW)
    with pytest.raises(ValidationError):
        row.name = "mutated"  # type: ignore[misc]
