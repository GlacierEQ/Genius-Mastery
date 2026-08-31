"""Mission-to-learning loop primitives for Genius-Mastery."""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any

PHASES = ("mission", "context", "options", "impact", "action", "outcome")
EVIDENCE_STATES = {
    "known_from_context",
    "operator_reported",
    "retrieval_pending",
    "not_searched",
    "searched_found",
    "searched_not_found",
    "unavailable",
    "contradicted",
}
OUTCOME_STATUSES = {"pending", "observed", "verified", "contradicted"}


def _items(value: Iterable[str] | None) -> list[str]:
    return [str(item).strip() for item in (value or []) if str(item).strip()]


def build_loop(
    mission: str,
    context: Iterable[str],
    options: Iterable[str],
    impact: Iterable[str],
    action: str,
    outcome: str | None = None,
    *,
    evidence_state: str = "not_searched",
    outcome_status: str | None = None,
    source_refs: Iterable[str] | None = None,
    learnings: Iterable[str] | None = None,
    strengthened: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Build a serializable loop record without claiming more than it knows."""
    cleaned_outcome = str(outcome).strip() if outcome and str(outcome).strip() else None
    if outcome_status is None:
        outcome_status = "pending" if cleaned_outcome is None else "observed"
    return {
        "schema_version": 1,
        "phases": {
            "mission": str(mission).strip(),
            "context": _items(context),
            "options": _items(options),
            "impact": _items(impact),
            "action": str(action).strip(),
            "outcome": cleaned_outcome,
        },
        "evidence_state": evidence_state,
        "outcome_status": outcome_status,
        "source_refs": _items(source_refs),
        "learnings": _items(learnings),
        "strengthened": _items(strengthened),
        "status": (
            "ready_to_act"
            if cleaned_outcome is None
            else {
                "verified": "verified",
                "contradicted": "contradicted",
            }.get(outcome_status, "awaiting_verification")
        ),
    }


def validate_loop(record: dict[str, Any]) -> list[str]:
    """Return contract errors; an empty list means the loop is structurally valid."""
    errors: list[str] = []
    if record.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    phases = record.get("phases")
    if not isinstance(phases, dict):
        return ["phases must be a mapping"]
    for name in PHASES:
        if name not in phases:
            errors.append(f"phase missing: {name}")
    for name in ("mission", "action"):
        if not isinstance(phases.get(name), str) or not phases.get(name).strip():
            errors.append(f"phase {name} must be non-empty")
    for name in ("context", "options", "impact"):
        values = phases.get(name)
        if not isinstance(values, list) or not values or not all(
            isinstance(item, str) and item.strip() for item in values
        ):
            errors.append(f"phase {name} must be a non-empty string list")
    outcome = phases.get("outcome")
    if outcome is not None and (not isinstance(outcome, str) or not outcome.strip()):
        errors.append("phase outcome must be null or a non-empty string")
    if record.get("evidence_state") not in EVIDENCE_STATES:
        errors.append(f"invalid evidence_state: {record.get('evidence_state')!r}")
    if record.get("outcome_status") not in OUTCOME_STATUSES:
        errors.append(f"invalid outcome_status: {record.get('outcome_status')!r}")
    if outcome is None and record.get("outcome_status") != "pending":
        errors.append("outcome_status must be pending when outcome is null")
    if outcome is not None and record.get("outcome_status") == "pending":
        errors.append("outcome_status cannot be pending when outcome exists")
    for name in ("source_refs", "learnings", "strengthened"):
        values = record.get(name)
        if not isinstance(values, list) or not all(
            isinstance(item, str) and item.strip() for item in values
        ):
            errors.append(f"{name} must be a string list")
    expected_status = {
        "pending": "ready_to_act",
        "observed": "awaiting_verification",
        "verified": "verified",
        "contradicted": "contradicted",
    }.get(record.get("outcome_status"))
    if expected_status and record.get("status") != expected_status:
        errors.append(f"status must be {expected_status!r} for current outcome state")
    return errors


def loop_report(record: dict[str, Any]) -> str:
    """Render a compact human-readable report."""
    phases = record["phases"]
    lines = [f"Status: {record['status']}", f"Mission: {phases['mission']}"]
    for name in ("context", "options", "impact"):
        lines.append(f"{name.title()}:")
        lines.extend(f"  - {item}" for item in phases[name])
    lines.append(f"Action: {phases['action']}")
    lines.append(f"Outcome: {phases['outcome'] or '[pending]'}")
    lines.append(f"Evidence: {record['evidence_state']}")
    if record.get("learnings"):
        lines.append("Learnings:")
        lines.extend(f"  - {item}" for item in record["learnings"])
    if record.get("strengthened"):
        lines.append("Strengthened:")
        lines.extend(f"  - {item}" for item in record["strengthened"])
    return "\n".join(lines)
