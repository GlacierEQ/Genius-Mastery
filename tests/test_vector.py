"""Tests for evidence-derived mastery vectors."""
import json
from pathlib import Path

import yaml

from genius.vector import compute_vector, vector_report, write_vector


ROOT = Path(__file__).resolve().parents[1]


def _fixture(tmp_path: Path) -> Path:
    root = tmp_path / "Genius-Fixture"
    (root / "claims").mkdir(parents=True)
    (root / "evidence").mkdir()
    (root / "mastery").mkdir()

    (root / "claims" / "CLAIMS.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "claims": [
                    {
                        "id": "foundation-001",
                        "statement": "Foundation behavior is recorded and tested.",
                        "dimension": "foundations",
                        "status": "operationally_verified",
                        "evidence_refs": ["ev-1"],
                        "counterevidence_refs": [],
                    },
                    {
                        "id": "mechanism-001",
                        "statement": "Mechanism remains implemented but unverified.",
                        "dimension": "mechanisms",
                        "status": "implemented",
                        "evidence_refs": [],
                        "counterevidence_refs": [],
                    },
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (root / "evidence" / "ledger.jsonl").write_text(
        json.dumps(
            {
                "id": "ev-1",
                "claim_ids": ["foundation-001"],
                "result": "pass",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return root


def test_vector_is_evidence_derived_and_multidimensional(tmp_path):
    root = _fixture(tmp_path)
    vector = compute_vector(root)

    assert vector["representation"] == "evidence-derived-multidimensional-vector"
    assert "percentage" not in vector
    assert vector["totals"]["claims"] == 2
    assert vector["totals"]["claims_with_evidence"] == 1
    assert vector["totals"]["verified_claims"] == 1
    assert vector["dimensions"]["foundations"]["deepest_tier"] == "operationally_verified"
    assert vector["dimensions"]["mechanisms"]["deepest_tier"] == "implemented"
    assert vector["integrity"]["clean"] is True


def test_vector_detects_dangling_claim_evidence_reference(tmp_path):
    root = _fixture(tmp_path)
    claims_path = root / "claims" / "CLAIMS.yaml"
    payload = yaml.safe_load(claims_path.read_text(encoding="utf-8"))
    payload["claims"][1]["evidence_refs"] = ["ev-missing"]
    claims_path.write_text(
        yaml.safe_dump(payload, sort_keys=False),
        encoding="utf-8",
    )

    vector = compute_vector(root)

    assert vector["integrity"]["clean"] is False
    assert vector["integrity"]["unresolved_evidence_refs"] == [
        {"claim_id": "mechanism-001", "evidence_ref": "ev-missing"}
    ]


def test_vector_detects_ledger_reference_to_missing_claim(tmp_path):
    root = _fixture(tmp_path)
    ledger = root / "evidence" / "ledger.jsonl"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + json.dumps(
            {
                "id": "ev-2",
                "claim_ids": ["missing-claim"],
                "result": "pass",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    vector = compute_vector(root)

    assert vector["integrity"]["clean"] is False
    assert vector["integrity"]["ledger_claim_mismatches"] == [
        {"evidence_id": "ev-2", "claim_id": "missing-claim"}
    ]


def test_write_vector_round_trips(tmp_path):
    root = _fixture(tmp_path)
    path = write_vector(root)

    assert path == root / "mastery" / "VECTOR.yaml"
    stored = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert stored == compute_vector(root)


def test_vector_report_exposes_integrity_and_dimensions(tmp_path):
    report = vector_report(compute_vector(_fixture(tmp_path)))

    assert "integrity_clean: True" in report
    assert "foundations:" in report
    assert "mechanisms:" in report


def test_live_repository_vector_has_no_dangling_evidence_references():
    vector = compute_vector(ROOT)

    assert vector["totals"]["claims"] >= 10
    assert vector["integrity"]["unresolved_evidence_refs"] == []
    assert vector["integrity"]["ledger_claim_mismatches"] == []
    assert vector["dimensions"]["mechanisms"]["verified_claims"] >= 2
