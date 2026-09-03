"""Doctor diagnostic surface for a Genius entity."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_pointer(root: Path, genius: dict[str, Any], field: str, default: str) -> Any:
    raw = genius.get(field) or default
    return load_yaml(root / raw) if isinstance(raw, str) else None


def doctor_report(root: Path) -> str:
    genius = load_yaml(root / "GENIUS.yaml") or {}
    role = _load_pointer(root, genius, "role_brief", "ROLE.yaml") or {}
    stack = _load_pointer(root, genius, "capability_anatomy_contract", "capabilities/STACK.yaml") or {}
    graph = _load_pointer(root, genius, "capability_graph", "capabilities/GRAPH.yaml") or {}
    teaching = _load_pointer(root, genius, "teaching_contract", "teaching/TEACHING.yaml") or {}
    synthesis = _load_pointer(root, genius, "synthesis_plan", "synthesis/PLAN.yaml") or {}
    claims_data = load_yaml(root / "claims" / "CLAIMS.yaml") or {}
    claims = claims_data.get("claims") or []
    vector = load_yaml(root / "mastery" / "VECTOR.yaml") or {}
    frontier = load_yaml(root / "frontier" / "QUEUE.yaml") or {}
    composition = load_yaml(root / "interfaces" / "COMPOSITION.yaml") or {}

    lines: list[str] = []
    lines.append("=== Genius Doctor ===")
    lines.append(f"repository: {genius.get('repository', '?')}")
    lines.append(f"purpose: {genius.get('purpose', '?')}")
    lines.append(f"schema_version: {genius.get('schema_version', '?')}")
    lines.append(
        f"package_version: {genius.get('package_version', genius.get('schema_version', '?'))}"
    )
    if role:
        lines.append(f"role: {role.get('role', '?')}")
        outcomes = role.get("outcomes") or []
        lines.append(f"desired_outcomes: {len(outcomes)}")
        for outcome in outcomes[:5]:
            lines.append(f"  - {outcome}")
    lines.append("")

    layers = stack.get("layers") or {}
    interrogated = 0
    required_count = 0
    missing_count = 0
    improvement_count = 0
    for meta in layers.values():
        if not isinstance(meta, dict):
            continue
        if meta.get("inspection_prompts"):
            interrogated += 1
        required_count += len(meta.get("required") or [])
        missing_count += len(meta.get("missing") or [])
        improvement_count += len(meta.get("improvement_targets") or [])

    lines.append("Vertical capability stack:")
    lines.append(f"  state: {stack.get('state', '?')}")
    lines.append(f"  layers: {len(layers)}")
    lines.append(f"  interrogated_layers: {interrogated}/{len(layers)}")
    lines.append(f"  required_targets: {required_count}")
    lines.append(f"  explicit_missing: {missing_count}")
    lines.append(f"  improvement_targets: {improvement_count}")
    bottleneck = (stack.get("evolution") or {}).get("current_bottleneck")
    if bottleneck:
        lines.append(f"  current_bottleneck: {bottleneck}")
    impact = stack.get("mission_impact") or {}
    if impact:
        scores = []
        for key in (
            "mission_relevance",
            "necessity",
            "criticality",
            "sensitivity",
            "substitutability",
            "downstream_centrality",
            "improvement_leverage",
        ):
            if key in impact:
                scores.append(f"{key}={impact[key]}")
        if scores:
            lines.append("  mission_impact: " + ", ".join(scores))
    lines.append("")

    if graph:
        lines.append("Capability graph:")
        nodes = graph.get("nodes") or []
        edges = graph.get("edges") or []
        analysis = graph.get("analysis") or {}
        lines.append(f"  nodes: {len(nodes)}")
        lines.append(f"  edges: {len(edges)}")
        lines.append(
            f"  candidate_bottlenecks: {len(analysis.get('candidate_bottlenecks') or [])}"
        )
        high_leverage = analysis.get("high_leverage_nodes") or []
        lines.append(f"  structural_high_leverage: {len(high_leverage)}")
        for node_id in high_leverage[:5]:
            lines.append(f"    - {node_id}")
        lines.append("")

    if synthesis:
        lines.append("Synthesis:")
        lines.append(f"  state: {synthesis.get('synthesis_state', '?')}")
        families = synthesis.get("capability_families") or []
        lines.append(f"  capability_families: {len(families)}")
        lines.append(
            f"  live_capability_match: {synthesis.get('capability_match_state', 'not-recorded')}"
        )
        matches = synthesis.get("matched_live_capabilities") or []
        lines.append(f"  matched_live_capabilities: {len(matches)}")
        for item in matches[:5]:
            lines.append(
                f"    - {item.get('kind', '?')}:{item.get('id', '?')} "
                f"score={item.get('match_score', '?')}"
            )
        lines.append("")

    if teaching:
        lines.append("Teaching:")
        lines.append(f"  subject: {teaching.get('subject', '?')}")
        method = teaching.get("method") or {}
        lines.append(
            "  method_phases: "
            + ", ".join(
                phase
                for phase in ("explain", "demonstrate", "reconstruct", "transfer")
                if method.get(phase)
            )
        )
        challenges = (teaching.get("verification") or {}).get("transfer_challenges") or []
        lines.append(f"  transfer_challenges: {len(challenges)}")
        metrics = teaching.get("outcome_metrics") or {}
        if metrics:
            lines.append(
                "  outcome_metrics: "
                + ", ".join(f"{k}={v}" for k, v in metrics.items())
            )
        lines.append("")

    by_status: dict[str, int] = {}
    by_dim: dict[str, int] = {}
    for claim in claims:
        by_status[claim.get("status", "?")] = by_status.get(claim.get("status", "?"), 0) + 1
        by_dim[claim.get("dimension", "?")] = by_dim.get(claim.get("dimension", "?"), 0) + 1

    lines.append("Claims by status:")
    for key, value in sorted(by_status.items()):
        lines.append(f"  {key}: {value}")
    lines.append("Claims by dimension:")
    for key, value in sorted(by_dim.items()):
        lines.append(f"  {key}: {value}")
    lines.append("")

    lines.append("Mastery vector (diagnostic):")
    dims = vector.get("dimensions") or {}
    for name, meta in dims.items():
        if isinstance(meta, dict):
            lines.append(
                f"  {name}: mapped={meta.get('claims_mapped', 0)} "
                f"evidence={meta.get('claims_with_evidence', 0)} "
                f"tier={meta.get('deepest_tier', '-')}"
            )
    lines.append("")

    provides = composition.get("provides") or []
    lines.append(f"Capabilities provided: {len(provides)}")
    for item in provides:
        lines.append(f"  - {item.get('id')} [{item.get('stage')}]")
    lines.append("")

    items = frontier.get("items") or []
    terminal = {"resolved", "closed", "complete"}
    open_items = [
        item for item in items
        if str(item.get("status") or "open").casefold() not in terminal
    ]
    lines.append(f"Frontier unresolved: {len(open_items)}")
    for item in open_items[:8]:
        question = (item.get("question") or "")[:100]
        lines.append(f"  - {item.get('id')}: {question}")
    lines.append("")
    lines.append("NOTE: No single mastery percentage is emitted by design.")
    return "\n".join(lines)
