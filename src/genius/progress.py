"""Progress orchestration for Genius-Mastery.

This layer composes the existing mission-aware loop and capability intelligence
into a deterministic contract for advancing state without confusing plans,
mutations, observations, and verification.
"""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from genius.intelligence import analyze_capability_graph
from genius.operating_loop import build_loop, validate_loop
from genius.prompt_codes import DEFAULT_PROGRESS_CODES, normalize_codes


PROGRESS_PHASES = ("recover", "prioritize", "execute", "persist", "verify", "compound")

PROGRESS_INVARIANTS = (
    "Inspect current state before claiming it.",
    "Preserve verified gains unless replacement is demonstrably stronger.",
    "Choose the highest-leverage executable action, not merely the easiest action.",
    "Distinguish proposed, executed, observed, and verified state.",
    "Make durable state changes when a writable durable surface exists.",
    "Read back mutations from the destination of record.",
    "Require inspectable receipts before claiming verification.",
    "Feed verified gains and counterevidence into the next cycle.",
)


def _items(values: Iterable[str] | None) -> list[str]:
    return [str(value).strip() for value in (values or []) if str(value).strip()]


def _impact_line(row: dict[str, Any]) -> str:
    reasons = "; ".join(str(reason) for reason in (row.get("reasons") or [])[:4])
    suffix = f" — {reasons}" if reasons else ""
    return (
        f"{row.get('id', 'unknown')}: priority={float(row.get('priority') or 0):.4f}, "
        f"leverage={float(row.get('leverage') or 0):.4f}, "
        f"state={row.get('state', 'unknown')}{suffix}"
    )


def _load_ranked_actions(root: Path) -> tuple[list[dict[str, Any]], str, list[str]]:
    graph_path = root / "capabilities" / "GRAPH.yaml"
    if not graph_path.exists():
        return [], "searched_not_found", []
    graph = yaml.safe_load(graph_path.read_text(encoding="utf-8")) or {}
    analyzed = analyze_capability_graph(graph)
    rows = list((analyzed.get("analysis") or {}).get("ranked_priorities") or [])
    return rows, "searched_found", [str(graph_path)]


def build_progress_contract(
    root: str | Path,
    mission: str,
    *,
    context: Iterable[str] | None = None,
    codes: Iterable[str] | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    mission_text = str(mission).strip()
    if not mission_text:
        raise ValueError("mission must be non-empty")

    selected_codes = normalize_codes(codes, progress_defaults=True)
    ranked, evidence_state, source_refs = _load_ranked_actions(root_path)

    context_items = _items(context)
    if root_path.exists():
        context_items.insert(0, f"Repository exists: {root_path}")
    else:
        context_items.insert(0, f"Repository path is not currently present: {root_path}")

    if ranked:
        top = ranked[0]
        options = [str(row.get("id") or "unknown") for row in ranked[:3]]
        impacts = [_impact_line(row) for row in ranked[:3]]
        reasons = [str(reason) for reason in (top.get("reasons") or [])]
        action = (
            f"Advance {top.get('id')} as the current next-best action, beginning with "
            "live-state inspection and preserving its existing evidence/state labels."
        )
        next_best_action = {
            "target": top.get("id"),
            "state": top.get("state"),
            "priority": top.get("priority"),
            "leverage": top.get("leverage"),
            "reasons": reasons,
            "selection_basis": "mission-intelligence-v1 ranked priority",
        }
    else:
        options = [
            "Recover repository current state and capability graph",
            "Inspect durable evidence and recent verified state",
        ]
        impacts = [
            "Without a ranked capability graph, selecting implementation work would be guesswork.",
            "Recovery preserves prior gains and establishes a truthful next-action basis.",
        ]
        action = (
            "Recover current durable state, locate or regenerate the capability graph, "
            "then rank the next executable action before mutation."
        )
        next_best_action = {
            "target": "recover-current-state",
            "state": "required",
            "priority": None,
            "leverage": None,
            "reasons": ["no ranked capability action was available from capabilities/GRAPH.yaml"],
            "selection_basis": "recovery fallback",
        }

    loop = build_loop(
        mission=mission_text,
        context=context_items,
        options=options,
        impact=impacts,
        action=action,
        evidence_state=evidence_state,
        source_refs=source_refs,
        strengthened=[],
    )

    return {
        "schema_version": 1,
        "kind": "genius-progress-contract",
        "mission": mission_text,
        "root": str(root_path),
        "status": "ready_to_execute",
        "codes": selected_codes,
        "default_progress_stack": list(DEFAULT_PROGRESS_CODES),
        "invariants": list(PROGRESS_INVARIANTS),
        "phases": [
            {"name": "recover", "requirement": "Inspect live/durable state, prior receipts, context, and constraints before mutation.", "done_when": "Current state and uncertainty are explicitly represented."},
            {"name": "prioritize", "requirement": "Rank bottlenecks and leverage; select the strongest executable next action.", "done_when": "A specific action is selected with an inspectable basis."},
            {"name": "execute", "requirement": "Use available tools to perform the selected action rather than only describe it.", "done_when": "The target system reports an actual mutation or execution result."},
            {"name": "persist", "requirement": "Write the gain to the appropriate durable system while preserving validated prior capability.", "done_when": "The durable destination contains the intended new state."},
            {"name": "verify", "requirement": "Test and read back the destination; bind success claims to receipts.", "done_when": "Observed evidence supports the claimed post-state or records counterevidence."},
            {"name": "compound", "requirement": "Feed verified gain, counterevidence, and newly exposed bottlenecks into the next cycle.", "done_when": "The next cycle begins from the stronger verified state rather than a reset."},
        ],
        "next_best_action": next_best_action,
        "decision_loop": loop,
        "truth_contract": {
            "planned_is_not_executed": True,
            "executed_is_not_verified": True,
            "verified_requires_receipts": True,
            "counterevidence_is_retained": True,
        },
    }


def validate_progress_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if contract.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if contract.get("kind") != "genius-progress-contract":
        errors.append("kind must be 'genius-progress-contract'")
    if not isinstance(contract.get("mission"), str) or not contract["mission"].strip():
        errors.append("mission must be non-empty")
    codes = contract.get("codes")
    if not isinstance(codes, list):
        errors.append("codes must be a list")
    else:
        missing = [code for code in DEFAULT_PROGRESS_CODES if code not in codes]
        if missing:
            errors.append(f"default progress codes missing: {', '.join(missing)}")
    phase_names = [phase.get("name") for phase in (contract.get("phases") or []) if isinstance(phase, dict)]
    if tuple(phase_names) != PROGRESS_PHASES:
        errors.append(f"phases must be exactly: {', '.join(PROGRESS_PHASES)}")
    loop = contract.get("decision_loop")
    if not isinstance(loop, dict):
        errors.append("decision_loop must be a mapping")
    else:
        errors.extend(f"decision_loop: {error}" for error in validate_loop(loop))
    truth = contract.get("truth_contract") or {}
    for key in ("planned_is_not_executed", "executed_is_not_verified", "verified_requires_receipts", "counterevidence_is_retained"):
        if truth.get(key) is not True:
            errors.append(f"truth_contract.{key} must be true")
    return errors


def progress_report(contract: dict[str, Any]) -> str:
    action = contract["next_best_action"]
    lines = [
        f"Progress contract: {contract['mission']}",
        f"status: {contract['status']}",
        f"root: {contract['root']}",
        "codes: " + " + ".join(contract["codes"]),
        "",
        "Next best action:",
        f"  target: {action.get('target')}",
        f"  state: {action.get('state')}",
        f"  priority: {action.get('priority')}",
        f"  leverage: {action.get('leverage')}",
    ]
    for reason in action.get("reasons") or []:
        lines.append(f"  reason: {reason}")
    lines.extend(["", "Progress cycle:"])
    for phase in contract["phases"]:
        lines.append(f"  {phase['name'].upper()}: {phase['requirement']}")
    lines.extend(["", "Truth contract: plan != execution; execution != verification; verification requires receipts."])
    return "\n".join(lines)
