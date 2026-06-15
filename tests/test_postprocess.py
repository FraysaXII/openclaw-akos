from akos.postprocess import (
    check_brand_lint_gate,
    check_citation_gate,
    check_secret_pii_gate,
    run_postprocess_chain,
)


def test_citation_gate_passes_with_src_id():
    r = check_citation_gate("See SRC-EXT-001 for detail.", require_citation=True)
    assert r.ok


def test_citation_gate_passes_with_vault_path():
    r = check_citation_gate(
        "Per docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md",
        require_citation=True,
    )
    assert r.ok


def test_citation_gate_blocks_when_required_and_missing():
    r = check_citation_gate("No sources here.", require_citation=True)
    assert not r.ok
    assert r.blocked_gates == ("citation",)


def test_chain_skips_citation_when_not_required():
    r = run_postprocess_chain("plain operator summary", require_citation=False)
    assert r.ok


def test_brand_lint_blocks_internal_codename():
    r = check_brand_lint_gate("We use AKOS internally but this is external prose.")
    assert not r.ok
    assert r.blocked_gates == ("brand_lint",)


def test_secret_pii_blocks_api_key_pattern():
    r = check_secret_pii_gate("Here is the key: sk-live-abc123notreal")
    assert not r.ok
    assert r.blocked_gates == ("secret_pii",)


def test_secret_pii_blocks_real_looking_email():
    r = check_secret_pii_gate("Contact me at operator.real@company.com today.")
    assert not r.ok


def test_chain_runs_all_gates_in_order():
    r = run_postprocess_chain(
        "Clean external summary with no leaks.",
        require_citation=False,
    )
    assert r.ok


def test_channel_truncate_gate_blocks_oversized_output():
    r = run_postprocess_chain("x" * 50, max_channel_chars=10)
    assert not r.ok
    assert "channel_truncate" in r.blocked_gates
