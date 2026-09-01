"""Mission-sensitive capability intelligence for Genius graphs.

This module turns a structural capability graph into an action model.  It does
not claim mastery from topology alone: every score is an explainable heuristic
that preserves the underlying evidence/state fields and can be recomputed.
"""
from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any


VERIFIED_STATES = {"verified", "operationally_verified"}
_STATE_READINESS = {
    "operationally_verified": 1.00,
    "verified": 0.95,
    "operational": 0.85,
    "active": 0.80,
    "available": 0.75,
    "implemented": 0.72,
    "discovered": 0.55,
    "mapped": 0.40,
    "research-and-verify": 0.25,
    "desired": 0.10,
    "blocked": 0.05,
    "failed": 0.00,
}
_CAPABILITY_KINDS = {
    "capability",
    "capability-family",
    "capability-target",
    "skill",
    "combo-skill",
    "mega-skill",
    "tool",
    "model",
    "api",
    "connector",
    "mcp",
    "runtime",
}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _readiness(state: str) -> float:
    return _STATE_READINESS.get(str(state).casefold(), 0.35)


def _evidence_strength(node: dict[str, Any], incident_edges: list[dict[str, Any]]) -> float:
    """Estimate evidence strength without inventing proof.

    Explicit numeric metadata wins. Otherwise references increase confidence
    gradually, capped below certainty because reference count is not proof
    quality.
    """
    metadata = node.get("metadata") or {}
    for key in ("evidence_confidence", "confidence", "verification_confidence"):
        raw = metadata.get(key)
        if isinstance(raw, (int, float)):
            return _clamp(float(raw))

    refs = set()
    for ref in node.get("evidence_refs") or []:
        if ref:
            refs.add(str(ref))
    for edge in incident_edges:
        for ref in edge.get("evidence_refs") or []:
            if ref:
                refs.add(str(ref))
    return min(0.85, 0.18 * len(refs))


def _bfs_distances(
    starts: list[str],
    adjacency: dict[str, list[str]],
) -> dict[str, int]:
    distances: dict[str, int] = {}
    queue: deque[tuple[str, int]] = deque((node_id, 0) for node_id in starts)
    while queue:
        node_id, distance = queue.popleft()
        if node_id in distances and distances[node_id] <= distance:
            continue
        distances[node_id] = distance
        for nxt in adjacency.get(node_id, []):
            queue.append((nxt, distance + 1))
    return distances


def _reachable_count(start: str, adjacency: dict[str, list[str]]) -> int:
    seen = {start}
    queue = deque(adjacency.get(start, []))
    while queue:
        node_id = queue.popleft()
        if node_id in seen:
            continue
        seen.add(node_id)
        queue.extend(adjacency.get(node_id, []))
    return max(0, len(seen) - 1)


def analyze_capability_graph(graph: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of *graph* with explainable mission intelligence.

    The graph's existing state remains authoritative. Scores prioritize what to
    investigate/build next; they do not promote nodes to verified/mastered.
    """
    enriched = deepcopy(graph)
    nodes = [node for node in enriched.get("nodes") or [] if isinstance(node, dict)]
    edges = [edge for edge in enriched.get("edges") or [] if isinstance(edge, dict)]
    by_id = {str(node.get("id")): node for node in nodes if node.get("id")}

    required_out: dict[str, list[str]] = {}
    required_in: dict[str, list[str]] = {}
    all_out: dict[str, list[str]] = {}
    all_in: dict[str, list[str]] = {}
    incident: dict[str, list[dict[str, Any]]] = {node_id: [] for node_id in by_id}
    substitutes: dict[str, set[str]] = {node_id: set() for node_id in by_id}

    for edge in edges:
        src = str(edge.get("from") or "")
        dst = str(edge.get("to") or "")
        if not src or not dst:
            continue
        all_out.setdefault(src, []).append(dst)
        all_in.setdefault(dst, []).append(src)
        incident.setdefault(src, []).append(edge)
        incident.setdefault(dst, []).append(edge)

        relation = str(edge.get("relation") or "").casefold()
        required = bool(edge.get("required_for_current_mission"))
        if required:
            required_out.setdefault(src, []).append(dst)
            required_in.setdefault(dst, []).append(src)
        if relation in {"substitutes", "substitute-for", "alternative-to"}:
            substitutes.setdefault(src, set()).add(dst)
            substitutes.setdefault(dst, set()).add(src)

    mission_roots = [
        node_id
        for node_id, node in by_id.items()
        if node.get("kind") in {"role", "mission"}
    ]
    if not mission_roots:
        mission_roots = [
            node_id
            for node_id, node in by_id.items()
            if float(node.get("mission_impact") or 0.0) >= 0.95
        ]

    distance_from_mission = _bfs_distances(mission_roots, required_out)
    max_dependents = max(
        [_reachable_count(node_id, required_in) for node_id in by_id] or [1]
    )
    max_dependencies = max(
        [_reachable_count(node_id, required_out) for node_id in by_id] or [1]
    )

    score_rows: list[dict[str, Any]] = []
    for node_id, node in by_id.items():
        state = str(node.get("state") or "unknown")
        mission_impact = _clamp(float(node.get("mission_impact") or 0.0))
        readiness = _readiness(state)
        evidence_strength = _evidence_strength(node, incident.get(node_id, []))

        depth = distance_from_mission.get(node_id)
        mission_proximity = 0.0 if depth is None else 1.0 / (1.0 + depth)

        dependent_count = _reachable_count(node_id, required_in)
        dependency_count = _reachable_count(node_id, required_out)
        dependent_centrality = (
            dependent_count / max_dependents if max_dependents else 0.0
        )
        dependency_reach = (
            dependency_count / max_dependencies if max_dependencies else 0.0
        )

        metadata = node.get("metadata") or {}
        declared_alternatives = metadata.get("substitutes") or metadata.get("alternatives") or []
        alternative_count = len(substitutes.get(node_id, set())) + (
            len(declared_alternatives) if isinstance(declared_alternatives, list) else 0
        )
        substitutability = min(1.0, alternative_count / 3.0)

        required_here = bool(required_in.get(node_id))
        unresolved = state.casefold() not in VERIFIED_STATES
        capability_like = str(node.get("kind") or "") in _CAPABILITY_KINDS

        priority = (
            0.28 * mission_impact
            + 0.17 * mission_proximity
            + 0.20 * dependent_centrality
            + 0.20 * (1.0 - readiness)
            + 0.10 * (1.0 - substitutability)
            + 0.05 * (1.0 - evidence_strength)
        )
        if required_here:
            priority += 0.05
        priority = _clamp(priority)

        leverage = _clamp(
            0.35 * mission_impact
            + 0.30 * dependent_centrality
            + 0.20 * dependency_reach
            + 0.15 * (1.0 - substitutability)
        )

        row = {
            "id": node_id,
            "kind": str(node.get("kind") or "unknown"),
            "label": str(node.get("label") or node_id),
            "state": state,
            "priority": round(priority, 4),
            "leverage": round(leverage, 4),
            "mission_impact": round(mission_impact, 4),
            "mission_proximity": round(mission_proximity, 4),
            "readiness": round(readiness, 4),
            "evidence_strength": round(evidence_strength, 4),
            "dependent_count": dependent_count,
            "dependency_count": dependency_count,
            "substitute_count": alternative_count,
            "required_for_current_mission": required_here,
            "candidate_bottleneck": bool(capability_like and unresolved and required_here),
            "reasons": [],
        }

        reasons = row["reasons"]
        if mission_impact >= 0.75:
            reasons.append("high mission impact")
        if dependent_centrality >= 0.5 and dependent_count:
            reasons.append(f"supports {dependent_count} upstream dependent(s)")
        if readiness <= 0.4:
            reasons.append(f"low readiness state: {state}")
        if evidence_strength < 0.25:
            reasons.append("weak or absent evidence references")
        if required_here:
            reasons.append("required by current mission path")
        if alternative_count == 0:
            reasons.append("no recorded substitute")
        score_rows.append(row)

    ranked = sorted(
        score_rows,
        key=lambda row: (-row["priority"], -row["leverage"], row["id"]),
    )
    bottlenecks = [row for row in ranked if row["candidate_bottleneck"]]
    high_leverage = sorted(
        score_rows,
        key=lambda row: (-row["leverage"], -row["priority"], row["id"]),
    )

    existing = enriched.get("analysis") or {}
    enriched["analysis"] = {
        **existing,
        "engine": "mission-intelligence-v1",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "mission_roots": mission_roots,
        "candidate_bottlenecks": [row["id"] for row in bottlenecks],
        "high_leverage_nodes": [row["id"] for row in high_leverage[:10]],
        "ranked_priorities": ranked,
        "top_next_actions": [
            {
                "id": row["id"],
                "priority": row["priority"],
                "reasons": row["reasons"][:4],
            }
            for row in bottlenecks[:10]
        ],
        "truth_note": (
            "Scores prioritize investigation and capability work; they do not "
            "promote mapped/discovered capability to verified or mastered."
        ),
    }
    return enriched


def capability_intelligence_report(
    graph: dict[str, Any],
    *,
    top: int = 10,
) -> str:
    """Render a compact human-readable priority report."""
    analyzed = analyze_capability_graph(graph)
    analysis = analyzed["analysis"]
    rows = analysis.get("ranked_priorities") or []

    lines = [
        f"Capability intelligence: {analyzed.get('repository', 'unknown')}",
        f"engine: {analysis.get('engine')}",
        f"nodes: {analysis.get('node_count', 0)}",
        f"edges: {analysis.get('edge_count', 0)}",
        "",
        "Top priorities:",
    ]
    for index, row in enumerate(rows[: max(1, top)], 1):
        reasons = "; ".join(row.get("reasons") or []) or "structural priority"
        lines.append(
            f"{index:>2}. {row['id']} priority={row['priority']:.4f} "
            f"leverage={row['leverage']:.4f} state={row['state']} — {reasons}"
        )
    if not rows:
        lines.append("  (no graph nodes)")
    return "\n".join(lines)
