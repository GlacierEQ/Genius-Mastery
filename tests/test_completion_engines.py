"""Completion-engine regression tests."""
from pathlib import Path
import yaml
from genius.calibration import calibrate_graph
from genius.composition import execute_family_composition

def _graph():
    return {
        "repository": "Genius-Test",
        "nodes": [
            {"id": "role:test", "kind": "role", "state": "mapped", "mission_impact": 1.0},
            {"id": "cap:weak", "kind": "capability", "state": "mapped", "mission_impact": 1.0},
            {"id": "cap:strong", "kind": "capability", "state": "verified", "mission_impact": 0.8, "evidence_refs": ["ev-1"]},
        ],
        "edges": [
            {"from": "role:test", "to": "cap:weak", "relation": "requires", "required_for_current_mission": True},
            {"from": "role:test", "to": "cap:strong", "relation": "requires", "required_for_current_mission": True},
        ],
    }

def test_calibration_is_monotonic():
    result = calibrate_graph(_graph())
    assert result["scenario_count"] > 0
    assert result["clean"] is True

def _repo(root: Path, name: str, provides: list[dict], consumes: list[dict]) -> None:
    repo = root / name
    (repo / "interfaces").mkdir(parents=True)
    (repo / "GENIUS.yaml").write_text(
        f"schema_version: 2\nrepository: {name}\npurpose: Test\nfamily: Genius\ndoctrine: mastery-not-skills\ncomposition_contract: interfaces/COMPOSITION.yaml\n",
        encoding="utf-8",
    )
    (repo / "interfaces" / "COMPOSITION.yaml").write_text(
        yaml.safe_dump({"spec_version": 1, "repository": name, "provides": provides, "consumes": consumes}, sort_keys=False),
        encoding="utf-8",
    )

def test_composition_receipt_is_deterministic_and_resolves_dependency(tmp_path):
    _repo(tmp_path, "Genius-A", [{"id": "alpha.shared", "description": "shared verification", "stage": "implemented"}], [])
    _repo(tmp_path, "Genius-B", [{"id": "beta.shared", "description": "shared research", "stage": "implemented"}], [
        {"repository": "Genius-A", "capability": "alpha.shared", "reason": "compose"}
    ])
    one = execute_family_composition(tmp_path)
    two = execute_family_composition(tmp_path)
    assert one["repository_count"] == 2
    assert one["resolved_binding_count"] == 1
    assert one["unresolved_binding_count"] == 0
    assert one["contract_composition_gain"] >= 1
    assert one["sha256"] == two["sha256"]
