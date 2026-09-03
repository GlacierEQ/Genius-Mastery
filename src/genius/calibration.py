"""Calibration and perturbation checks for mission-intelligence ranking."""
from __future__ import annotations
from copy import deepcopy
from typing import Any
from genius.intelligence import analyze_capability_graph

def _rank(graph: dict[str, Any]) -> list[str]:
    analyzed = analyze_capability_graph(graph)
    return [row["id"] for row in (analyzed.get("analysis") or {}).get("ranked_priorities") or []]

def calibrate_graph(graph: dict[str, Any]) -> dict[str, Any]:
    base = analyze_capability_graph(graph)
    rows = list((base.get("analysis") or {}).get("ranked_priorities") or [])
    scenarios: list[dict[str, Any]] = []
    for row in rows[: min(8, len(rows))]:
        node_id = row["id"]
        variant = deepcopy(graph)
        for node in variant.get("nodes") or []:
            if isinstance(node, dict) and node.get("id") == node_id:
                node["state"] = "verified"
                refs = list(node.get("evidence_refs") or [])
                refs.append(f"calibration:{node_id}")
                node["evidence_refs"] = refs
                break
        reranked = analyze_capability_graph(variant)
        by_id = {item["id"]: item for item in (reranked.get("analysis") or {}).get("ranked_priorities") or []}
        after = by_id.get(node_id) or {}
        scenarios.append({
            "node": node_id,
            "before_priority": row.get("priority"),
            "after_priority": after.get("priority"),
            "before_readiness": row.get("readiness"),
            "after_readiness": after.get("readiness"),
            "priority_not_increased_after_verification": float(after.get("priority") or 0) <= float(row.get("priority") or 0),
            "readiness_not_decreased_after_verification": float(after.get("readiness") or 0) >= float(row.get("readiness") or 0),
        })
    clean = all(
        item["priority_not_increased_after_verification"] and item["readiness_not_decreased_after_verification"]
        for item in scenarios
    )
    return {
        "schema_version": 1,
        "engine": "mission-intelligence-calibration-v1",
        "base_ranking": _rank(graph),
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
        "clean": clean,
        "truth_note": "Synthetic monotonic calibration does not prove globally optimal ranking weights.",
    }

def calibration_report(result: dict[str, Any]) -> str:
    lines = [
        "Mission-intelligence calibration",
        f"scenarios: {result.get('scenario_count', 0)}",
        f"clean: {result.get('clean')}",
    ]
    for s in result.get("scenarios") or []:
        lines.append(
            f"  - {s['node']}: priority {s['before_priority']} -> {s['after_priority']}; "
            f"readiness {s['before_readiness']} -> {s['after_readiness']}"
        )
    return "\n".join(lines)
