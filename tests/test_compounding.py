"""Scale FDE reusable-capability compounding tests."""
import json

import pytest
from genius.compounding import (
    extract_reusable_capability,
    register_capability,
    select_reusable_capability,
)


def _verified_receipt():
    return {
        "mission_id": "mission-1",
        "verification_status": "verified",
        "source_revision": "abc123",
        "receipt_refs": ["receipt://mission-1/verified"],
        "reusable_capability": {
            "id": "cap.provider-readback-reconcile",
            "description": "Provider readback and reconciliation after ambiguous external mutation",
            "tags": ["provider", "readback", "reconciliation", "idempotency"],
            "input_contract": {"requires": ["attempted mutation", "provider identity"]},
            "output_contract": {"emits": ["confirmed applied", "confirmed absent", "unknown"]},
        },
    }


def test_extract_reusable_capability_requires_verified_mission():
    receipt = _verified_receipt()
    receipt["verification_status"] = "executed"
    with pytest.raises(ValueError, match="verified mission"):
        extract_reusable_capability(receipt)


def test_extract_reusable_capability_preserves_explicit_contract_and_evidence():
    capability = extract_reusable_capability(_verified_receipt())
    assert capability["id"] == "cap.provider-readback-reconcile"
    assert capability["source_mission_id"] == "mission-1"
    assert capability["source_revision"] == "abc123"
    assert capability["stage"] == "verified"
    assert capability["evidence_refs"] == ["receipt://mission-1/verified"]
    assert "mission_id" not in capability["input_contract"]


def test_register_capability_is_idempotent(tmp_path):
    path = tmp_path / "capability-registry.json"
    capability = extract_reusable_capability(_verified_receipt())
    first = register_capability(path, capability)
    second = register_capability(path, capability)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert first["sha256"] == second["sha256"]
    assert len(data["capabilities"]) == 1
    assert data["capabilities"][0]["id"] == capability["id"]


def test_mission2_automatically_selects_mission1_capability():
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


def test_register_capability_preserves_previous_registry_on_interrupted_write(tmp_path, monkeypatch):
    path = tmp_path / "capability-registry.json"
    capability = extract_reusable_capability(_verified_receipt())
    register_capability(path, capability)
    previous = path.read_bytes()

    def interrupted_replace(_source, _destination):
        raise OSError("simulated process interruption before atomic replacement")

    monkeypatch.setattr("genius.compounding.os.replace", interrupted_replace)
    with pytest.raises(OSError, match="simulated process interruption"):
        register_capability(path, capability)

    assert path.read_bytes() == previous


def test_extract_reusable_capability_rejects_non_object_contract():
    receipt = _verified_receipt()
    receipt["reusable_capability"] = "not-an-object"
    with pytest.raises(TypeError, match="reusable_capability"):
        extract_reusable_capability(receipt)


def test_register_capability_rejects_invalid_registry_shape(tmp_path):
    path = tmp_path / "capability-registry.json"
    path.write_text('{"schema_version": 1, "capabilities": {}}', encoding="utf-8")
    capability = extract_reusable_capability(_verified_receipt())
    with pytest.raises(TypeError, match="capability registry"):
        register_capability(path, capability)
