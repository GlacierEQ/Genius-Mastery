"""Independent, adversarial TypeScript full-stack acceptance from Mastery."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from genius.repository_foundry import MISSION_SCHEMA
from genius.repository_foundry_text_workbench import TS_PROFILE, generate_typescript_text_workbench


def build(tmp_path: Path) -> Path:
    return generate_typescript_text_workbench(
        "Build a real TypeScript frontend, JSON API and Unicode word analysis",
        "TS Workbench", tmp_path
    )


def node(*argv, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["node", *argv], cwd=cwd,
        env={"PATH": os.environ.get("PATH", ""), "HOME": str(cwd)},
        text=True, capture_output=True, timeout=40
    )


def test_generated_typescript_executes_native_api_tests_without_teacher(tmp_path):
    project = build(tmp_path)
    assert (project / "web/index.html").exists()
    assert (project / "src/server.ts").exists()
    assert (project / ".github/workflows/test.yml").exists()
    assert not (project / "src/genius").exists()
    assert shutil.which("node"), "Node >=22.16 must be provisioned in native CI"
    version = node("--version", cwd=project)
    assert version.returncode == 0
    assert int(version.stdout.strip().lstrip("v").split(".")[0]) >= 22
    result = node("--experimental-strip-types", "--test", "tests/fullstack.test.ts", cwd=project)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "# pass 2" in result.stdout
    assert "# fail 0" in result.stdout


def test_manifest_and_mission_schema_and_determinism(tmp_path):
    a = build(tmp_path / "one")
    b = build(tmp_path / "two")
    manifest = json.loads((a / "source-manifest.json").read_text())
    assert manifest["status"] == "GENERATED_UNVERIFIED"
    checksums = manifest["files_sha256"]
    assert len(checksums) >= 12
    assert checksums == json.loads((b / "source-manifest.json").read_text())["files_sha256"]
    for name, digest in checksums.items():
        assert hashlib.sha256((a / name).read_bytes()).hexdigest() == digest
    mission = json.loads((a / "mission.json").read_text())
    assert mission["schema_version"] == MISSION_SCHEMA
    assert mission["profile"] == TS_PROFILE
    assert "TypeScript frontend" in mission["original_objective"]
    assert mission["status"] == "GENERATED_UNVERIFIED"
    import jsonschema
    schema = json.loads((Path(__file__).resolve().parents[1] / "schemas/repository-mission.schema.json").read_text())
    jsonschema.validate(mission, schema)


def test_identical_rerun_preserves_bytes_and_operator_edits(tmp_path):
    target = build(tmp_path)
    original = (target / "source-manifest.json").read_bytes()
    assert build(tmp_path) == target
    assert (target / "source-manifest.json").read_bytes() == original
    (target / "operator-note.md").write_text("must not disappear", encoding="utf-8")
    with pytest.raises(FileExistsError, match="changed or unrelated"):
        build(tmp_path)
    assert (target / "operator-note.md").read_text() == "must not disappear"
    assert not list(tmp_path.glob(".Genius-TS-Workbench.stage-*"))


def test_invalid_objective_is_rejected_without_publication(tmp_path):
    for objective in ("", " ", 17):
        with pytest.raises(ValueError, match="objective"):
            generate_typescript_text_workbench(objective, "TS Workbench", tmp_path)
    with pytest.raises(ValueError, match="objective"):
        generate_typescript_text_workbench("x" * 20_001, "TS Workbench", tmp_path)
    assert not list(tmp_path.iterdir())


def test_existing_cli_supports_both_profiles_and_rejects_unsupported(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "genius.cli", "foundry", "new",
         "--name", "TS Workbench", "--objective", "A working browser and API",
         "--profile", TS_PROFILE, "--dest", str(tmp_path)],
        text=True, capture_output=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    assert "GENERATED_UNVERIFIED" in result.stdout
    assert (tmp_path / "Genius-TS-Workbench/src/server.ts").is_file()
    bad = subprocess.run(
        [sys.executable, "-m", "genius.cli", "foundry", "new",
         "--name", "Unsupported", "--objective", "unsupported",
         "--profile", "fake-profile", "--dest", str(tmp_path)],
        text=True, capture_output=True, timeout=30
    )
    assert bad.returncode != 0
    assert not (tmp_path / "Genius-Unsupported").exists()
