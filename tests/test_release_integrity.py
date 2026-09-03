from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from genius import __version__
from genius.graph import build_synthesis_graph
from genius.vector import compute_vector

ROOT = Path(__file__).resolve().parents[1]


def _yaml(path: str):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_release_identity_is_consistent():
    genius = _yaml("GENIUS.yaml")
    roadmap = _yaml("mastery/ROADMAP.yaml")
    family = json.loads((ROOT / "family/INDEX.json").read_text(encoding="utf-8"))
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"$', pyproject, flags=re.MULTILINE)
    assert match
    mastery = next(item for item in family["repositories"] if item["repository"] == "Genius-Mastery")
    assert {__version__, genius["package_version"], roadmap["release"], mastery["revision"], match.group(1)} == {__version__}
    assert genius["instruction_contract"] == "docs/INSTRUCTION_ENGINEERING.md"
    assert genius["instruction_compiler"] == "src/genius/instruction_engineering.py"
    assert "mastery.kernel.instruction-engineering" in mastery["capabilities"]


def test_tracked_graph_matches_synthesis_contract():
    role = _yaml("ROLE.yaml")
    plan = _yaml("synthesis/PLAN.yaml")
    families = {
        item["id"]: {
            "status": item.get("status") or "mapped",
            "layers": list(item.get("layers") or []),
            "targets": list(item.get("targets") or []),
        }
        for item in plan["capability_families"]
    }
    expected = build_synthesis_graph(
        "Genius-Mastery",
        role["role"],
        list(role["outcomes"]),
        families,
        list(plan.get("matched_live_capabilities") or []),
    )
    assert _yaml("capabilities/GRAPH.yaml") == expected


def test_tracked_vector_matches_claims_and_evidence():
    assert _yaml("mastery/VECTOR.yaml") == compute_vector(ROOT)
