"""Reusable-capability compounding contracts.

These tests intentionally exercise evidence fidelity, negative constraints,
selection eligibility, registry integrity, atomicity, and concurrent writers.
"""
from concurrent.futures import ThreadPoolExecutor
import json

import pytest

from genius.compounding import (
    extract_reusable_capability,
    register_capability,
    score_capability_for_mission,
    select_reusable_capability,
)


def _verified_receipt(*, capability_id="cap.provider-readback-reconcile"):
    return {
        "mission_id": "mission-1",
        "verification_status": "verified",
        "source_revision": "abc123",
        "receipt_refs": ["receipt://mission-1/verified"],
        "reusable_capability": {
            "id": capability_id,
            "description": "Provider readback and reconciliation after ambiguous external mutation",
            "tags": ["provider", "readback", "reconciliation", "idempotency"],
            "input_contract": {
                "requires": ["attempted mutation", "provider identity"]
            },
            "output_contract": {
                "emits": ["confirmed applied", "confirmed absent", "unknown"]
            },
        },
    }


def test_extract_reusable_capability_requires_verified_mission():
    receipt = _verified_receipt()
    receipt["verification_status"] = "executed"
    with pytest.raises(ValueError, match="verified mission"):
        extract_reusable_capability(receipt)


def test_extract_preserves_contract_evidence_and_stage():
    receipt = _verified_receipt()
    capability = extract_reusable_capability(receipt)
    assert capability["id"] == "cap.provider-readback-reconcile"
    assert capability["source_mission_id"] == "mission-1"
    assert capability["source_revision"] == "abc123"
    assert capability["stage"] == "verified"
    assert capability["evidence_refs"] == ["receipt://mission-1/verified"]
    assert capability["input_contract"] == receipt["reusable_capability"]["input_contract"]
    assert capability["output_contract"] == receipt["reusable_capability"]["output_contract"]


def test_extract_preserves_operationally_verified_stage():
    receipt = _verified_receipt()
    receipt["verification_status"] = "operationally_verified"
    capability = extract_reusable_capability(receipt)
    assert capability["stage"] == "operationally_verified"


def test_extract_normalizes_scalar_tags_and_references_as_single_items():
    receipt = _verified_receipt()
    receipt["receipt_refs"] = "receipt://single"
    receipt["reusable_capability"]["tags"] = "readback"
    receipt["reusable_capability"]["evidence_refs"] = "evidence://single"
    capability = extract_reusable_capability(receipt)
    assert capability["tags"] == ["readback"]
    assert capability["evidence_refs"] == ["evidence://single", "receipt://single"]


def test_scoring_uses_values_not_schema_wrapper_keys():
    capability = {
        "id": "cap.alpha",
        "description": "alpha beta",
        "tags": [],
        "input_contract": {"requires": []},
        "output_contract": {"emits": []},
        "stage": "verified",
        "evidence_refs": ["ev-1"],
    }
    mission = {
        "mission_id": "mission-x",
        "objective": "gamma delta",
        "requirements": [],
        "constraints": [],
    }
    score = score_capability_for_mission(capability, mission)
    assert score["matched_terms"] == []
    assert score["fit"] == 0.0


def test_negative_constraint_cannot_increase_positive_fit_or_select_forbidden_capability():
    capability = extract_reusable_capability(_verified_receipt())
    mission = {
        "mission_id": "mission-negative",
        "objective": "Resolve the mutation safely",
        "requirements": ["provider confirmation"],
        "constraints": ["must not use readback"],
    }
    score = score_capability_for_mission(capability, mission)
    assert "readback" in score["prohibited_terms"]
    assert "readback" not in score["matched_terms"]
    selection = select_reusable_capability(mission, [capability], minimum_score=0.1)
    assert selection["selected"] is None


def test_zero_overlap_verified_capability_is_not_auto_selected():
    capability = extract_reusable_capability(_verified_receipt())
    mission = {
        "mission_id": "mission-unrelated",
        "objective": "Render a typography specimen",
        "requirements": ["font kerning", "glyph spacing"],
        "constraints": [],
    }
    selection = select_reusable_capability(mission, [capability], minimum_score=0.0)
    assert selection["ranked"][0]["fit"] == 0.0
    assert selection["selected"] is None


def test_empty_registry_returns_no_selection():
    mission = {"mission_id": "mission-empty", "objective": "Anything"}
    selection = select_reusable_capability(mission, [], minimum_score=0.0)
    assert selection["selected"] is None
    assert selection["ranked"] == []


def test_mission2_automatically_selects_matching_mission1_capability():
    capability = extract_reusable_capability(_verified_receipt())
    mission2 = {
        "mission_id": "mission-2",
        "objective": "Safely reconcile an ambiguous provider mutation using provider readback",
        "requirements": ["idempotency", "provider confirmation", "readback"],
    }
    selection = select_reusable_capability(mission2, [capability], minimum_score=0.35)
    assert selection["selected"] is not None
    assert selection["selected"]["capability"]["id"] == capability["id"]
    assert selection["selected"]["score"] >= 0.35
    assert {"provider", "readback"} & set(selection["selected"]["matched_terms"])


def test_register_capability_is_idempotent(tmp_path):
    path = tmp_path / "capability-registry.json"
    capability = extract_reusable_capability(_verified_receipt())
    first = register_capability(path, capability)
    second = register_capability(path, capability)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert first["sha256"] == second["sha256"]
    assert len(data["capabilities"]) == 1
    assert data["capabilities"][0]["id"] == capability["id"]


def test_register_rejects_malformed_existing_entries_without_data_loss(tmp_path):
    path = tmp_path / "capability-registry.json"
    original = '{"schema_version":1,"capabilities":[{"description":"missing id"}]}\n'
    path.write_text(original, encoding="utf-8")
    with pytest.raises(ValueError, match="registry entry"):
        register_capability(path, extract_reusable_capability(_verified_receipt()))
    assert path.read_text(encoding="utf-8") == original


def test_register_rejects_conflicting_same_id_without_erasing_evidence(tmp_path):
    path = tmp_path / "capability-registry.json"
    capability = extract_reusable_capability(_verified_receipt())
    register_capability(path, capability)
    before = path.read_text(encoding="utf-8")
    conflicting = dict(capability)
    conflicting["evidence_refs"] = ["different-evidence"]
    with pytest.raises(ValueError, match="conflicting capability"):
        register_capability(path, conflicting)
    assert path.read_text(encoding="utf-8") == before


def test_register_persists_normalized_id(tmp_path):
    path = tmp_path / "capability-registry.json"
    capability = extract_reusable_capability(
        _verified_receipt(capability_id="  cap.normalized  ")
    )
    register_capability(path, capability)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["capabilities"][0]["id"] == "cap.normalized"


def test_concurrent_registration_preserves_all_capabilities(tmp_path):
    path = tmp_path / "capability-registry.json"
    capabilities = [
        extract_reusable_capability(_verified_receipt(capability_id=f"cap.concurrent-{i}"))
        for i in range(8)
    ]
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda cap: register_capability(path, cap), capabilities))
    data = json.loads(path.read_text(encoding="utf-8"))
    assert [item["id"] for item in data["capabilities"]] == [
        f"cap.concurrent-{i}" for i in range(8)
    ]
    assert not list(tmp_path.glob("*.tmp"))


def test_registry_write_is_valid_json_and_reports_digest(tmp_path):
    path = tmp_path / "capability-registry.json"
    result = register_capability(path, extract_reusable_capability(_verified_receipt()))
    payload = path.read_bytes()
    json.loads(payload)
    import hashlib
    assert result["sha256"] == hashlib.sha256(payload).hexdigest()
