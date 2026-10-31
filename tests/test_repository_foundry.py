"""Real application acceptance for the first GENIUS Repository Foundry profile."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from genius.repository_foundry import generate_python_text_audit, MISSION_SCHEMA
from genius.lineage.publication import checked_root

ROOT = Path(__file__).resolve().parents[1]


def build(tmp_path: Path) -> Path:
    return generate_python_text_audit(
        "Build a UTF-8 text analyzer with deterministic word counts and JSON CLI output",
        "Text Audit", tmp_path,
    )


def test_python_application_runs_independent_native_tests_and_cli(tmp_path):
    project = build(tmp_path)
    assert project.name == "Genius-Text-Audit"
    env = {
        "PYTHONPATH": str(project / "src"),
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(tmp_path),
    }
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=project, env=env, text=True, capture_output=True,
    )
    assert tests.returncode == 0, tests.stdout + tests.stderr
    assert "Ran 4 tests" in tests.stderr

    cli = subprocess.run(
        [sys.executable, "-m", "genius_text_audit", "--json"],
        cwd=project, env=env, text=True, input="One one two",
        capture_output=True,
    )
    assert cli.returncode == 0, cli.stderr
    assert json.loads(cli.stdout)["top_words"][0] == {"word": "one", "count": 2}
    assert not (project / "src" / "genius").exists()


def test_generated_manifest_matches_all_source_bytes(tmp_path):
    project = build(tmp_path)
    manifest = json.loads((project / "source-manifest.json").read_text())
    assert manifest["status"] == "GENERATED_UNVERIFIED"
    checks = manifest["files_sha256"]
    assert len(checks) >= 8
    assert all(
        hashlib.sha256((project / filename).read_bytes()).hexdigest() == expected
        for filename, expected in checks.items()
    )
    mission = json.loads((project / "mission.json").read_text())
    assert mission["schema_version"] == MISSION_SCHEMA
    assert mission["status"] == "GENERATED_UNVERIFIED"
    assert mission["mode"] == "NEW"
    assert "Build a UTF-8" in mission["original_objective"]
    assert "unsupported_objective" not in mission


def test_repeat_generation_is_deterministic_and_does_not_overwrite(tmp_path):
    first = build(tmp_path / "one")
    second = build(tmp_path / "two")
    source_a = json.loads((first / "source-manifest.json").read_text())["files_sha256"]
    source_b = json.loads((second / "source-manifest.json").read_text())["files_sha256"]
    assert source_a == source_b
    original = (first / "README.md").read_bytes()
    (first / ".user-data").write_text("keep")
    with pytest.raises(FileExistsError):
        build(tmp_path / "one")
    assert (first / ".user-data").read_text() == "keep"
    assert (first / "README.md").read_bytes() == original


def test_invalid_objective_does_not_create_project(tmp_path):
    for value in ("", " ", 7):
        with pytest.raises(ValueError, match="objective"):
            generate_python_text_audit(value, "Text Audit", tmp_path)
    assert not (tmp_path / "Genius-Text-Audit").exists()


def test_cli_generates_project_but_does_not_claim_verification(tmp_path):
    process = subprocess.run(
        [sys.executable, "-m", "genius.cli", "foundry", "new",
         "--name", "Text Audit", "--objective", "Analyze text files with JSON output",
         "--dest", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert process.returncode == 0, process.stdout + process.stderr
    assert "GENERATED_UNVERIFIED" in process.stdout
    assert (tmp_path / "Genius-Text-Audit" / "source-manifest.json").is_file()
    bad = subprocess.run(
        [sys.executable, "-m", "genius.cli", "foundry", "new",
         "--name", "Other", "--objective", "arbitrary", "--profile", "unsupported",
         "--dest", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert bad.returncode == 1
    assert not (tmp_path / "Genius-Other").exists()


def test_generated_mission_validates_against_versioned_schema(tmp_path):
    import jsonschema

    generated = build(tmp_path)
    schema = json.loads((ROOT / "schemas/repository-mission.schema.json").read_text())
    mission = json.loads((generated / "mission.json").read_text())
    jsonschema.validate(mission, schema)
