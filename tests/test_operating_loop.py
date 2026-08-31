"""Tests for the mission-aware operating loop."""
from genius.operating_loop import build_loop, loop_report, validate_loop


def test_loop_preserves_retrieval_uncertainty_without_downgrading_context():
    record = build_loop(
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


def test_outcome_requires_explicit_verification_state():
    record = build_loop(
        mission="Make a useful change",
        context=["A baseline exists"],
        options=["Change", "Do not change"],
        impact=["Capability may improve", "Regression is possible"],
        action="Make the smallest meaningful change",
        outcome="The change passed the local check",
    )
    assert validate_loop(record) == []
    assert record["status"] == "awaiting_verification"

    verified = build_loop(
        mission="Make a useful change",
        context=["A baseline exists"],
        options=["Change"],
        impact=["Capability may improve"],
        action="Make the smallest meaningful change",
        outcome="The change passed independent verification",
        outcome_status="verified",
        evidence_state="searched_found",
        source_refs=["ci-run-123"],
        learnings=["The contract is compatible with the existing test surface"],
        strengthened=["Add this loop to future synthesis decisions"],
    )
    assert validate_loop(verified) == []
    assert verified["status"] == "verified"


def test_invalid_retrieval_state_is_rejected():
    record = build_loop(
        mission="Test state handling",
        context=["Context"],
        options=["Option"],
        impact=["Impact"],
        action="Act",
        evidence_state="google_says_no",
    )
    assert any("evidence_state" in error for error in validate_loop(record))


def test_report_keeps_the_whole_loop_visible():
    record = build_loop(
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
