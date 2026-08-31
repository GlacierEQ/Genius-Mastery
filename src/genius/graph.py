"""Capability graph compiler for synthesized Genius entities."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


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

    for family_name, spec in families.items():
        fid = f"family:{_slug(family_name)}"
        family_state = str(spec.get("status") or spec.get("state") or "mapped")
        add_node(
            {
                "id": fid,
                "kind": "capability-family",
                "label": family_name,
                "state": family_state,
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
            add_node(
                {
                    "id": tid,
                    "kind": "capability-target",
                    "label": target,
                    "state": "research-and-verify",
                    "mission_impact": 0.6,
                    "metadata": {"family": family_name},
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
                "mission_impact": min(
                    1.0,
                    0.5 + 0.05 * float(match.get("match_score") or 0),
                ),
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

    graph = {
        "schema_version": 1,
        "repository": repository,
        "nodes": nodes,
        "edges": edges,
        "analysis": {
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
    }
    return analyze_capability_graph(graph)


def _families_from_plan(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    families: dict[str, dict[str, Any]] = {}
    for item in plan.get("capability_families") or []:
        if not isinstance(item, dict) or not item.get("id"):
            continue
        families[str(item["id"])] = {
            "status": item.get("status") or "mapped",
            "layers": list(item.get("layers") or []),
            "targets": list(item.get("targets") or []),
        }
    return families


def rebuild_graph(root: Path) -> Path:
    """Rebuild capabilities/GRAPH.yaml from a Genius entity's own contracts."""
    root = root.resolve()
    genius_path = root / "GENIUS.yaml"
    role_path = root / "ROLE.yaml"
    plan_path = root / "synthesis" / "PLAN.yaml"

    missing = [
        path.relative_to(root).as_posix()
        for path in (genius_path, role_path, plan_path)
        if not path.exists()
    ]
    if missing:
        raise ValueError(
            "cannot rebuild capability graph; missing: " + ", ".join(missing)
        )

    genius = yaml.safe_load(genius_path.read_text(encoding="utf-8")) or {}
    role = yaml.safe_load(role_path.read_text(encoding="utf-8")) or {}
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8")) or {}

    repository = str(genius.get("repository") or plan.get("repository") or root.name)
    role_name = str(role.get("role") or plan.get("role") or genius.get("purpose") or "")
    outcomes = list(role.get("outcomes") or plan.get("outcomes") or [])
    if not role_name or not outcomes:
        raise ValueError("role and at least one outcome are required to rebuild graph")

    graph = build_synthesis_graph(
        repository,
        role_name,
        outcomes,
        _families_from_plan(plan),
        list(plan.get("matched_live_capabilities") or []),
    )

    graph_path = root / "capabilities" / "GRAPH.yaml"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(
        yaml.safe_dump(graph, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    genius["capability_graph"] = "capabilities/GRAPH.yaml"
    genius_path.write_text(
        yaml.safe_dump(genius, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return graph_path
