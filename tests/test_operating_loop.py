"""Tests for the mission-aware operating loop."""
from genius.operating_loop import build_loop, loop_report, validate_loop


def base(**overrides):
    values = dict(
        mission="Make a useful change",
        context=["A baseline exists"],
        options=["Change", "Do not change"],
        impact=["Capability may improve", "Regression is possible"],
        action="Make the smallest meaningful change",
    )
    values.update(overrides)
    return build_loop(**values)


def test_loop_preserves_retrieval_uncertainty_without_downgrading_context():
    record = base(
        mission="Preserve the strongest useful direction",
        context=["The project is new and still aspirational"],
        options=["Clip the aspiration", "Preserve the horizon"],
        impact=["Clipping reduces discovery", "Labels preserve truth"],
        action="Preserve aspirations while implementing one verifiable slice",
        evidence_state="retrieval_pending",
    )
    assert validate_loop(record) == []
    assert record["status"] == "ready_to_act"
    assert record["evidence_state"] == "retrieval_pending"


def test_string_inputs_are_single_items_not_character_lists():
    record = base(context="One context item", options="One option", impact="One impact")
    assert record["phases"]["context"] == ["One context item"]
    assert validate_loop(record) == []


def test_outcome_requires_explicit_verification_state():
    record = base(outcome="The change passed the local check")
    assert validate_loop(record) == []
    assert record["status"] == "awaiting_verification"

    verified = base(
        outcome="The change passed independent verification",
        outcome_status="verified",
        evidence_state="searched_found",
        source_refs=["ci-run-123"],
        learnings=["The contract is compatible with the existing test surface"],
        strengthened=["Add this loop to future synthesis decisions"],
    )
    assert validate_loop(verified) == []
    assert verified["status"] == "verified"


def test_verified_outcome_cannot_hide_unresolved_retrieval():
    record = base(
        outcome="It worked",
        outcome_status="verified",
        evidence_state="not_searched",
        source_refs=["local-note-1"],
    )
    assert any("unresolved retrieval" in error for error in validate_loop(record))


def test_terminal_states_require_receipts_and_truthful_evidence():
    missing_ref = base(outcome="Verified", outcome_status="verified", evidence_state="searched_found")
    assert any("source_ref" in error for error in validate_loop(missing_ref))

    contradicted = base(
        outcome="The expected result was not reproduced",
        outcome_status="contradicted",
        evidence_state="contradicted",
        source_refs=["counterevidence-1"],
    )
    assert validate_loop(contradicted) == []


def test_invalid_retrieval_state_is_rejected():
    record = base(evidence_state="google_says_no")
    assert any("evidence_state" in error for error in validate_loop(record))


def test_report_keeps_the_whole_loop_visible():
    record = base(
        mission="Keep the horizon visible",
        context=["The idea is early"],
        options=["Shrink it", "Aim at it"],
        impact=["Ambition creates a target"],
        action="Aim while labeling the current slice honestly",
    )
    report = loop_report(record)
    assert "Mission: Keep the horizon visible" in report
    assert "Action: Aim while labeling the current slice honestly" in report
    assert "Evidence: not_searched" in report
    assert "Outcome state: pending" in report
