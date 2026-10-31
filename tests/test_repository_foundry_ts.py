"""Executable acceptance for the standalone TypeScript taskboard profile."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import jsonschema

from genius.repository_foundry import MISSION_SCHEMA
from genius.repository_foundry_ts import PROFILE, generate_typescript_taskboard

ROOT = Path(__file__).resolve().parents[1]


def build(root: Path, *, objective="Build a local task tracker with real browser and REST behavior") -> Path:
    return generate_typescript_taskboard(objective, "Taskboard", root)


def test_versioned_mission_and_full_byte_manifest(tmp_path):
    project = build(tmp_path)
    mission = json.loads((project / "mission.json").read_text())
    schema = json.loads((ROOT / "schemas/repository-mission.schema.json").read_text())
    jsonschema.validate(mission, schema)
    assert mission["schema_version"] == MISSION_SCHEMA
    assert mission["profile"] == PROFILE
    assert mission["status"] == "GENERATED_UNVERIFIED"
    assert "arbitrary" in mission["unverified_requirements"]
    assert "npm ci" in mission["acceptance_command"]
    manifest = json.loads((project / "source-manifest.json").read_text())
    assert manifest["status"] == "GENERATED_UNVERIFIED"
    assert len(manifest["files_sha256"]) >= 12
    for relative, expected_hash in manifest["files_sha256"].items():
        assert hashlib.sha256((project / relative).read_bytes()).hexdigest() == expected_hash
    assert not any("genius-mastery" in content for content in
                   (project / "package.json").read_text().splitlines())
    assert not (project / "node_modules").exists()


def test_repeat_is_idempotent_and_preserves_durable_user_edits(tmp_path):
    project = build(tmp_path)
    file = project / "src/store.ts"
    original = file.read_bytes()
    stamp = file.stat().st_mtime_ns
    assert build(tmp_path) == project
    assert file.read_bytes() == original
    assert file.stat().st_mtime_ns == stamp
    (project / ".private-operator-note").write_text("do not alter", encoding="utf-8")
    with pytest.raises(FileExistsError, match="changed or unrelated"):
        build(tmp_path)
    assert (project / ".private-operator-note").read_text() == "do not alter"


def test_no_implicit_scope_inflation_and_original_objective_retained(tmp_path):
    objective = 'Build my tasks app </script><script>alert(1)</script> with custom business rules'
    project = build(tmp_path, objective=objective)
    mission = json.loads((project / "mission.json").read_text())
    assert mission["original_objective"] == objective
    assert mission["profile"] == "typescript-taskboard"
    assert objective not in (project / "public/index.html").read_text()
    assert "unverified_requirements" in mission
    assert (project / "src/store.ts").read_text().find("export type Task") >= 0


def test_invalid_mission_fails_before_any_publication(tmp_path):
    for objective in ("", " ", None, 123, "x" * 20_001):
        with pytest.raises(ValueError, match="objective"):
            generate_typescript_taskboard(objective, "Taskboard", tmp_path)
    assert not (tmp_path / "Genius-Taskboard").exists()


def test_cli_dispatches_new_profile_but_keeps_previous_profile(tmp_path):
    new = subprocess.run(
        [sys.executable, "-m", "genius.cli", "foundry", "new",
         "--name", "Taskboard", "--objective", "Build a persistent taskboard",
         "--profile", "typescript-taskboard", "--dest", str(tmp_path)],
        capture_output=True, text=True
    )
    assert new.returncode == 0, new.stderr
    assert "typescript-taskboard" in new.stdout
    assert "GENERATED_UNVERIFIED" in new.stdout
    assert (tmp_path / "Genius-Taskboard" / "src/server.ts").is_file()
    previous = subprocess.run(
        [sys.executable, "-m", "genius.cli", "foundry", "new",
         "--name", "Text Audit", "--objective", "Count input word frequencies",
         "--profile", "python-text-audit", "--dest", str(tmp_path)],
        capture_output=True, text=True
    )
    assert previous.returncode == 0, previous.stderr
    assert (tmp_path / "Genius-Text-Audit" / "src/genius_text_audit/app.py").is_file()


def test_generated_fullstack_application_compiles_runs_and_passes_native_http_tests(tmp_path):
    if not shutil.which("node") or not shutil.which("npm"):
        pytest.skip("Node and npm unavailable; GitHub workflow separately installs Node 22")
    version = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True).stdout.strip()
    major = int(re.match(r"v(\d+)", version).group(1))
    if major < 22:
        pytest.skip("Node 22 or newer required")
    project = build(tmp_path)
    installed = subprocess.run(["npm", "ci", "--offline", "--ignore-scripts", "--no-audit"],
                               cwd=project, capture_output=True, text=True, timeout=60)
    assert installed.returncode == 0, installed.stdout + installed.stderr
    tested = subprocess.run(["npm", "test"], cwd=project,
                            capture_output=True, text=True, timeout=100)
    assert tested.returncode == 0, tested.stdout + tested.stderr
    assert "pass 5" in tested.stdout
    assert (project / "dist/server.js").is_file()
    assert (project / "dist/store.js").is_file()
    assert not (project / "node_modules" / "genius-mastery").exists()

def test_generated_typescript_profile_has_strict_optional_compiler_contract(tmp_path):
    project = build(tmp_path)
    import json
    config = json.loads((project / "tsconfig.json").read_text())
    package = json.loads((project / "package.json").read_text())
    manifest = json.loads((project / "source-manifest.json").read_text())
    assert config["compilerOptions"]["strict"] is True
    assert config["compilerOptions"]["erasableSyntaxOnly"] is True
    assert config["compilerOptions"]["noEmit"] is True
    assert package["scripts"]["typecheck"] == "tsc --noEmit -p tsconfig.json"
    assert "tsconfig.json" in manifest["files_sha256"]
    # Preserve native no-install baseline: pin verifier tools only in the
    # optional CI typecheck lane, not in package runtime dependencies.
    assert "devDependencies" not in package
    assert "dependencies" not in package

