#!/usr/bin/env python3
"""Standalone Genius-Mastery contract validator."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_NAME_RE = re.compile(r"^Genius-[A-Za-z0-9._-]+$")


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    genius_path = root / "GENIUS.yaml"
    if not genius_path.exists():
        errors.append("GENIUS.yaml missing")
        genius = {}
    else:
        genius = load_yaml(genius_path) or {}
        if genius.get("schema_version") != 2:
            errors.append("GENIUS.yaml schema_version must be 2")
        repo = genius.get("repository")
        if not isinstance(repo, str) or not REPO_NAME_RE.match(repo):
            errors.append("GENIUS.yaml repository identity invalid")
        if genius.get("family") != "Genius":
            errors.append("GENIUS.yaml family must be Genius")
        if genius.get("doctrine") != "mastery-not-skills":
            errors.append("GENIUS.yaml doctrine must be mastery-not-skills")

        for field in (
            "composition_contract",
            "capability_anatomy_contract",
            "capability_graph",
            "teaching_contract",
            "role_brief",
            "synthesis_plan",
            "persona",
            "teaching_plan",
        ):
            target = genius.get(field)
            if target and not (root / target).exists():
                errors.append(f"{field} target missing: {target}")

    stack_path = root / "capabilities" / "STACK.yaml"
    if not stack_path.exists():
        errors.append("capabilities/STACK.yaml missing")
    else:
        stack = load_yaml(stack_path) or {}
        if stack.get("schema_version") != 1:
            errors.append("capabilities/STACK.yaml schema_version must be 1")
        if not stack.get("id") or not stack.get("purpose"):
            errors.append("capabilities/STACK.yaml identity incomplete")
        if not (stack.get("objective") or {}).get("desired_reality"):
            errors.append("capabilities/STACK.yaml desired_reality missing")
        if not isinstance(stack.get("layers"), dict) or not stack.get("layers"):
            errors.append("capabilities/STACK.yaml layers missing")
        if not (stack.get("verification") or {}).get("acceptance"):
            errors.append("capabilities/STACK.yaml verification.acceptance missing")
        if not isinstance(stack.get("mission_impact"), dict):
            errors.append("capabilities/STACK.yaml mission_impact missing")

    graph_target = genius.get("capability_graph")
    if graph_target:
        graph_path = root / graph_target
        if graph_path.exists():
            graph = load_yaml(graph_path) or {}
            nodes = graph.get("nodes")
            edges = graph.get("edges")
            if graph.get("schema_version") != 1:
                errors.append("capability graph schema_version must be 1")
            if not isinstance(nodes, list) or not isinstance(edges, list):
                errors.append("capability graph nodes/edges must be lists")
            else:
                ids = {
                    node.get("id")
                    for node in nodes
                    if isinstance(node, dict) and node.get("id")
                }
                if len(ids) != len(nodes):
                    errors.append("capability graph node ids must be present and unique")
                for edge in edges:
                    if (
                        not isinstance(edge, dict)
                        or edge.get("from") not in ids
                        or edge.get("to") not in ids
                        or not edge.get("relation")
                    ):
                        errors.append("capability graph contains invalid edge")
        else:
            errors.append(f"capability_graph target missing: {graph_target}")

    teaching_path = root / (
        genius.get("teaching_contract")
        if isinstance(genius.get("teaching_contract"), str)
        else "teaching/TEACHING.yaml"
    )
    if teaching_path.exists():
        teaching = load_yaml(teaching_path) or {}
        if teaching.get("schema_version") != 1:
            errors.append("teaching contract schema_version must be 1")
        if not teaching.get("teacher") or not teaching.get("subject"):
            errors.append("teaching contract teacher/subject incomplete")
        method = teaching.get("method") or {}
        for phase in ("explain", "demonstrate", "reconstruct", "transfer"):
            if not method.get(phase):
                errors.append(f"teaching contract method.{phase} missing")
        if not (teaching.get("verification") or {}).get("acceptance"):
            errors.append("teaching contract verification.acceptance missing")
    elif genius.get("teaching_contract"):
        errors.append("teaching contract missing")

    role_target = genius.get("role_brief")
    if role_target:
        role_path = root / role_target
        if role_path.exists():
            role = load_yaml(role_path) or {}
            if role.get("schema_version") != 1:
                errors.append("ROLE.yaml schema_version must be 1")
            if not role.get("role"):
                errors.append("ROLE.yaml role missing")
            if not isinstance(role.get("outcomes"), list) or not role.get("outcomes"):
                errors.append("ROLE.yaml outcomes must be non-empty")

    comp_path = root / "interfaces" / "COMPOSITION.yaml"
    if not comp_path.exists():
        errors.append("interfaces/COMPOSITION.yaml missing")

    if errors:
        print("FAIL")
        for error in errors:
            print("  -", error)
        return 1
    print("PASS: contract surfaces OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
