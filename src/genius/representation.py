"""Executable dynamic-adjustment and four-pillar representation doctrine.

The representation layer may adapt expression, routing, and verification intensity,
but it may never promote truth state or mint execution authority.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

PILLARS = ("orientation", "mastery", "machine_contract", "mesh")
MATURITY_STATES = (
    "demonstrated",
    "verified",
    "designed_for",
    "aspirational",
    "unknown",
    "contradicted",
)
NEXT_ACTORS = ("person", "expert", "machine", "mesh")
IMPACT_LEVELS = ("low", "medium", "high", "critical")
EVIDENCE_QUALITY = ("none", "weak", "mixed", "strong")
REVERSIBILITY = ("reversible", "hard_to_reverse", "irreversible")
EMOTIONAL_WEIGHT = ("low", "medium", "high")
SYSTEM_STATES = ("live", "tested", "partial", "degraded", "simulated", "planned", "unavailable", "unknown")

REPRESENTATION_INVARIANTS = (
    "Dynamic adjustment may change expression, depth, routing, and verification intensity; it may not change the underlying truth state.",
    "Aspiration is never silently promoted to demonstrated or verified capability.",
    "Verified claims require source-bearing evidence; demonstrated claims require execution evidence.",
    "Contradictions and uncertainty remain visible across every pillar.",
    "Machine contracts must describe actual interfaces and boundaries rather than polished promises.",
    "Mesh relationships must identify a meaningful dependency, contribution, constraint, or proof relationship.",
    "Consequential external action requires authorization from a trusted host; representation logic cannot mint that authority.",
)


def _items(values: Iterable[str] | None) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    cleaned: list[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in cleaned:
            cleaned.append(text)
    return cleaned


def _enum(name: str, value: str, allowed: tuple[str, ...]) -> str:
    normalized = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in allowed:
        raise ValueError(f"{name} must be one of: {', '.join(allowed)}")
    return normalized


def _preferred_pillar(next_actor: str, purpose: str) -> str:
    purpose_key = str(purpose).strip().lower()
    if next_actor == "machine" or any(token in purpose_key for token in ("integration", "api", "automation", "operation")):
        return "machine_contract"
    if next_actor == "mesh" or any(token in purpose_key for token in ("ecosystem", "composition", "dependency", "orchestration")):
        return "mesh"
    if next_actor == "expert" or any(token in purpose_key for token in ("evaluation", "audit", "mastery", "technical")):
        return "mastery"
    return "orientation"


def _claim_label(maturity: str) -> str:
    return {"designed_for": "DESIGNED FOR"}.get(
        maturity,
        maturity.replace("_", " ").upper(),
    )


def compile_representation_contract(
    statement: str,
    *,
    maturity: str,
    next_actor: str,
    purpose: str,
    evidence_refs: Iterable[str] | None = None,
    execution_refs: Iterable[str] | None = None,
    counterevidence_refs: Iterable[str] | None = None,
    impact: str = "medium",
    evidence_quality: str = "mixed",
    reversibility: str = "reversible",
    emotional_weight: str = "medium",
    system_state: str = "unknown",
    external_action: bool = False,
) -> dict[str, Any]:
    """Compile a representation contract without granting execution authority."""

    clean_statement = str(statement).strip()
    clean_purpose = str(purpose).strip()
    if not clean_statement:
        raise ValueError("statement must be non-empty")
    if not clean_purpose:
        raise ValueError("purpose must be non-empty")

    maturity = _enum("maturity", maturity, MATURITY_STATES)
    next_actor = _enum("next_actor", next_actor, NEXT_ACTORS)
    impact = _enum("impact", impact, IMPACT_LEVELS)
    evidence_quality = _enum("evidence_quality", evidence_quality, EVIDENCE_QUALITY)
    reversibility = _enum("reversibility", reversibility, REVERSIBILITY)
    emotional_weight = _enum("emotional_weight", emotional_weight, EMOTIONAL_WEIGHT)
    system_state = _enum("system_state", system_state, SYSTEM_STATES)

    evidence = _items(evidence_refs)
    executions = _items(execution_refs)
    counterevidence = _items(counterevidence_refs)

    high_consequence = impact in {"high", "critical"} or reversibility in {"hard_to_reverse", "irreversible"}
    requires_host_authorization = bool(external_action and high_consequence)
    strict_verification = impact in {"high", "critical"} or evidence_quality in {"none", "weak", "mixed"}
    high_restraint = impact in {"high", "critical"} or emotional_weight == "high"

    contract: dict[str, Any] = {
        "schema_version": 1,
        "kind": "genius-representation-contract",
        "statement": clean_statement,
        "truth": {
            "maturity": maturity,
            "evidence_refs": evidence,
            "execution_refs": executions,
            "counterevidence_refs": counterevidence,
            "system_state": system_state,
        },
        "signals": {
            "next_actor": next_actor,
            "purpose": clean_purpose,
            "impact": impact,
            "evidence_quality": evidence_quality,
            "reversibility": reversibility,
            "emotional_weight": emotional_weight,
            "external_action": bool(external_action),
        },
        "projection": {
            "preferred_pillar": _preferred_pillar(next_actor, clean_purpose),
            "claim_label": _claim_label(maturity),
            "verification_intensity": "strict" if strict_verification else "standard",
            "restraint": "high" if high_restraint else "normal",
            "truth_state_locked": True,
        },
        "action_gate": {
            "requires_host_authorization": requires_host_authorization,
            "representation_can_authorize": False,
            "execution_eligible": False,
            "rule": (
                "A trusted host must validate real authorization before consequential external execution. "
                "This representation contract never grants execution authority."
            ),
        },
        "pillars": list(PILLARS),
        "invariants": list(REPRESENTATION_INVARIANTS),
    }
    errors = validate_representation_contract(contract)
    contract["integrity"] = {"clean": not errors, "errors": errors}
    return contract


def validate_representation_contract(contract: Mapping[str, Any]) -> list[str]:
    """Validate cross-pillar truth and authorization invariants."""
    errors: list[str] = []
    if contract.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if contract.get("kind") != "genius-representation-contract":
        errors.append("kind must be genius-representation-contract")

    truth = contract.get("truth") or {}
    projection = contract.get("projection") or {}
    gate = contract.get("action_gate") or {}
    signals = contract.get("signals") or {}

    maturity = truth.get("maturity")
    if maturity not in MATURITY_STATES:
        errors.append(f"invalid maturity: {maturity!r}")
    evidence_refs = truth.get("evidence_refs") or []
    execution_refs = truth.get("execution_refs") or []
    counterevidence_refs = truth.get("counterevidence_refs") or []

    if maturity == "verified" and not evidence_refs:
        errors.append("verified maturity requires at least one evidence_ref")
    if maturity == "demonstrated" and not execution_refs:
        errors.append("demonstrated maturity requires at least one execution_ref")
    if maturity == "contradicted" and not counterevidence_refs:
        errors.append("contradicted maturity requires at least one counterevidence_ref")

    expected_label = _claim_label(maturity) if maturity in MATURITY_STATES else None
    if expected_label and projection.get("claim_label") != expected_label:
        errors.append("projection claim_label must preserve underlying maturity")
    if projection.get("preferred_pillar") not in PILLARS:
        errors.append("projection preferred_pillar must be a recognized pillar")
    if projection.get("truth_state_locked") is not True:
        errors.append("projection must lock truth state")

    if gate.get("representation_can_authorize") is not False:
        errors.append("representation layer must never grant execution authority")
    high_consequence = signals.get("impact") in {"high", "critical"} or signals.get("reversibility") in {"hard_to_reverse", "irreversible"}
    if signals.get("external_action") and high_consequence and gate.get("requires_host_authorization") is not True:
        errors.append("consequential external action requires host authorization")
    if gate.get("execution_eligible") is not False:
        errors.append("representation contract alone cannot make execution eligible")
    return errors


def representation_report(contract: Mapping[str, Any]) -> str:
    truth = contract.get("truth") or {}
    projection = contract.get("projection") or {}
    gate = contract.get("action_gate") or {}
    integrity = contract.get("integrity") or {}
    lines = [
        "Genius representation contract",
        f"statement: {contract.get('statement')}",
        f"maturity: {truth.get('maturity')}",
        f"pillar: {projection.get('preferred_pillar')}",
        f"verification: {projection.get('verification_intensity')}",
        f"restraint: {projection.get('restraint')}",
        f"host_authorization_required: {gate.get('requires_host_authorization')}",
        f"integrity_clean: {integrity.get('clean')}",
    ]
    for error in integrity.get("errors") or []:
        lines.append(f"  error: {error}")
    return "\n".join(lines)
