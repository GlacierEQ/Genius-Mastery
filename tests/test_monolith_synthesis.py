"""Regression contract for Monolith-aware Genius role synthesis.

Synthetic catalog only: these tests must not publish private estate inventory.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys

import pytest
import yaml

from genius.synthesize import synthesize_role
from genius.validate import validate_repo


def catalog_file(tmp_path):
    path = tmp_path / "AI_DYNAMIC_CAPABILITY_INDEX.json"
    content = {
        "version": "2.0.0",
        "generated_timestamp": "2026-09-30 20:23:09 UTC",
        "intent_vectors": {
            "WORKFLOW_AUTOMATION": {
                "keywords": ["automation", "workflow", "idempotency"],
                "anchor_repositories": ["apex-control-plane", "spiral-engine"],
            },
            "MEMORY_CONTINUITY": {
                "keywords": ["memory", "context"],
                "anchor_repositories": ["aspen-grove-memory"],
            },
            "IRRELEVANT": {
                "keywords": ["aerospace"],
                "anchor_repositories": ["unrelated"],
            },
        },
    }
    path.write_text(json.dumps(content), encoding="utf-8")
    return path


def test_synthesize_bpa_resolves_monolith_pointers_without_claiming_execution(tmp_path):
    catalog = catalog_file(tmp_path)
    out = tmp_path / "output"
    out.mkdir()
    result = synthesize_role(
        "Business Process Automation",
        ["workflow automation with idempotency and context recovery"],
        out,
        monolith_catalog=catalog,
    )
    assert result.name == "Genius-Business-Process-Automation"
    assert validate_repo(result) == []
    mapping = yaml.safe_load((result / "capabilities" / "ESTATE_DISCOVERY.yaml").read_text())
    assert mapping["source_repository"] == "GlacierEQ/monolith"
    assert mapping["source_catalog"] == catalog.name
    assert mapping["catalog_sha256"] == hashlib.sha256(catalog.read_bytes()).hexdigest()
    assert mapping["catalog_generated_at"] == "2026-09-30 20:23:09 UTC"
    assert mapping["catalog_version"] == "2.0.0"
    assert mapping["matching_intents"][0]["intent_id"] == "WORKFLOW_AUTOMATION"
    assert mapping["matching_intents"][0]["repositories"] == ["apex-control-plane", "spiral-engine"]
    assert all(hit["evidence_state"] == "catalog-pointer-unverified" for hit in mapping["matching_intents"])
    assert all(hit["intent_id"] != "IRRELEVANT" for hit in mapping["matching_intents"])
    plan = yaml.safe_load((result / "synthesis" / "PLAN.yaml").read_text())
    assert plan["estate_discovery"] == "capabilities/ESTATE_DISCOVERY.yaml"
    assert plan["synthesis_state"] == "mapped"
    assert "verified" not in mapping["capability_assessment"].lower()


def test_cli_monolith_catalog_for_existing_synthesize_command(tmp_path):
    catalog = catalog_file(tmp_path)
    out = tmp_path / "cliout"
    out.mkdir()
    process = subprocess.run(
        [
            sys.executable, "-m", "genius.cli", "synthesize",
            "Business Process Automation", "--outcome", "workflow automation",
            "--monolith-catalog", str(catalog), "--dest", str(out)
        ],
        capture_output=True, text=True,
    )
    assert process.returncode == 0, process.stdout + process.stderr
    assert (out / "Genius-Business-Process-Automation" / "capabilities" / "ESTATE_DISCOVERY.yaml").is_file()


def test_invalid_catalog_rejected_before_creating_output(tmp_path):
    broken = tmp_path / "invalid.json"
    broken.write_text('{"intent_vectors": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="intent_vectors"):
        synthesize_role("Business Process Automation", ["automation"], tmp_path, monolith_catalog=broken)
    assert not (tmp_path / "Genius-Business-Process-Automation").exists()


def test_legacy_synthesis_does_not_require_catalog(tmp_path):
    result = synthesize_role("Researcher", ["Indiana Jones"], tmp_path)
    assert validate_repo(result) == []
    assert not (result / "capabilities" / "ESTATE_DISCOVERY.yaml").exists()
