"""Capability graph compiler for synthesized Genius entities."""
from __future__ import annotations

import re
from typing import Any


def _slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value or "unnamed"


def build_synthesis_graph(
    repository: str,
    role: str,
    outcomes: list[str],
    families: dict[str, dict[str, Any]],
    live_matches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a recursive graph from role -> outcomes/families -> targets/capabilities."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add_node(node: dict[str, Any]) -> None:
        if node["id"] in seen:
            return
        seen.add(node["id"])
        nodes.append(node)

    role_id = f"role:{_slug(role)}"
    add_node(
        {
            "id": role_id,
            "kind": "role",
            "label": role,
            "state": "mapped",
            "mission_impact": 1.0,
            "metadata": {"repository": repository},
        }
    )

    for outcome in outcomes:
        oid = f"outcome:{_slug(outcome)}"
        add_node(
            {
                "id": oid,
                "kind": "outcome",
                "label": outcome,
                "state": "desired",
                "mission_impact": 1.0,
                "metadata": {},
            }
        )
        edges.append(
            {
                "from": role_id,
                "to": oid,
                "relation": "targets",
                "required_for_current_mission": True,
                "evidence_refs": [],
            }
        )

    target_to_families: dict[str, list[str]] = {}
    for family_name, spec in families.items():
        fid = f"family:{_slug(family_name)}"
        add_node(
            {
                "id": fid,
                "kind": "capability-family",
                "label": family_name,
                "state": "mapped",
                "mission_impact": 0.8,
                "metadata": {"layers": list(spec.get("layers") or [])},
            }
        )
        edges.append(
            {
                "from": role_id,
                "to": fid,
                "relation": "requires-capability-family",
                "required_for_current_mission": True,
                "evidence_refs": [],
            }
        )
        for target in spec.get("targets") or []:
            tid = f"target:{_slug(target)}"
            target_to_families.setdefault(target, []).append(fid)
            add_node(
                {
                    "id": tid,
                    "kind": "capability-target",
                    "label": target,
                    "state": "research-and-verify",
                    "mission_impact": 0.6,
                    "metadata": {},
                }
            )
            edges.append(
                {
                    "from": fid,
                    "to": tid,
                    "relation": "develops",
                    "required_for_current_mission": True,
                    "evidence_refs": [],
                }
            )

    for match in live_matches or []:
        mid = f"{match.get('kind', 'capability')}:{match.get('id', 'unknown')}"
        add_node(
            {
                "id": mid,
                "kind": str(match.get("kind", "capability")),
                "label": str(match.get("display_name") or match.get("id") or "unknown"),
                "state": str(match.get("maturity") or "discovered"),
                "mission_impact": min(1.0, 0.5 + 0.05 * float(match.get("match_score") or 0)),
                "metadata": {
                    "source_repository": match.get("source_repository"),
                    "source_registry": match.get("source_registry"),
                    "entrypoint": match.get("entrypoint"),
                    "version": match.get("version"),
                    "match_score": match.get("match_score"),
                    "matched_terms": match.get("matched_terms") or [],
                },
            }
        )
        edges.append(
            {
                "from": mid,
                "to": role_id,
                "relation": "candidate-supports",
                "required_for_current_mission": False,
                "evidence_refs": [],
            }
        )

    # Simple structural leverage seed: nodes used by more outgoing paths are
    # useful candidates for future centrality/sensitivity analysis.
    out_degree: dict[str, int] = {}
    for edge in edges:
        out_degree[edge["from"]] = out_degree.get(edge["from"], 0) + 1
    high_leverage = [
        node_id
        for node_id, degree in sorted(
            out_degree.items(), key=lambda item: (-item[1], item[0])
        )
        if degree > 1
    ]

    candidate_bottlenecks = [
        node["id"]
        for node in nodes
        if node["kind"] == "capability-target" and node["state"] != "verified"
    ]

    return {
        "schema_version": 1,
        "repository": repository,
        "nodes": nodes,
        "edges": edges,
        "analysis": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "candidate_bottlenecks": candidate_bottlenecks,
            "high_leverage_nodes": high_leverage,
            "note": (
                "Structural seed only. Mission sensitivity, substitution, and "
                "evidence-backed centrality remain future analysis."
            ),
        },
    }
