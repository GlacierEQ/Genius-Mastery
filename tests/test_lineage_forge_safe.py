"""Regression checks for the previously unsafe Genius Lineage forge."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from genius.archetypes import get_archetype
from genius.cli import main
from genius.lineage import forge_domain
from genius.lineage import forge as forge_module


ARCH = get_archetype("aerospace")


def test_safe_relative_default_and_no_root_projects_assumption(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    generated = forge_domain(ARCH)
    assert generated == tmp_path / "Genius-Lineage" / ARCH.name
    assert generated.is_dir()
    assert not Path("/root/projects/Genius-Lineage") == generated


def test_generated_capabilities_are_unverified_until_execution(tmp_path):
    repo = forge_domain(ARCH, output_root=tmp_path)
    graph = yaml.safe_load((repo / "capabilities/GRAPH.yaml").read_text())
    assert graph["capabilities"]
    assert all(cap["verified"] is False for cap in graph["capabilities"])
    assert all(cap["status"] == "mapped" and cap["evidence_refs"] == []
               for cap in graph["capabilities"])
    receipt = json.loads((repo / "evidence/RECEIPTS.jsonl").read_text())
    assert receipt["status"] == "GENERATED_UNVERIFIED"
    assert receipt["event"] == "FORGE_MATERIALIZATION"


def test_retry_is_read_only_for_identical_intent(tmp_path):
    repo = forge_domain(ARCH, output_root=tmp_path)
    file = repo / "src" / "genius_aerospace" / "tools.py"
    # Actual implementation module name may differ per archetype.
    if not file.exists():
        file = next((repo / "src").rglob("tools.py"))
    prior_bytes = file.read_bytes()
    prior_stamp = file.stat().st_mtime_ns
    receipt = (repo / "evidence/RECEIPTS.jsonl").read_bytes()
    assert forge_domain(ARCH, output_root=tmp_path) == repo
    assert file.read_bytes() == prior_bytes
    assert file.stat().st_mtime_ns == prior_stamp
    assert (repo / "evidence/RECEIPTS.jsonl").read_bytes() == receipt
    assert not list(tmp_path.glob(".genius-forge-stage-*"))


def test_conflicting_existing_user_content_is_not_replaced(tmp_path):
    repo = tmp_path / ARCH.name
    repo.mkdir()
    (repo / ".important").write_text("keep my work", encoding="utf-8")
    with pytest.raises(FileExistsError, match="preserving user work"):
        forge_domain(ARCH, output_root=tmp_path)
    assert (repo / ".important").read_text() == "keep my work"
    assert list(repo.iterdir()) == [repo / ".important"]
    assert not list(tmp_path.glob(".genius-forge-stage-*"))


def test_modified_generated_file_is_preserved(tmp_path):
    repo = forge_domain(ARCH, output_root=tmp_path)
    file = repo / "GENIUS.yaml"
    file.write_text(file.read_text() + "\n# user change\n")
    with pytest.raises(FileExistsError, match="preserving user work"):
        forge_domain(ARCH, output_root=tmp_path)
    assert file.read_text().endswith("# user change\n")


def test_directory_symlink_not_followed(tmp_path):
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    symlink = tmp_path / ARCH.name
    try:
        symlink.symlink_to(foreign, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable on this platform")
    with pytest.raises(FileExistsError, match="symlink"):
        forge_domain(ARCH, output_root=tmp_path)
    assert list(foreign.iterdir()) == []


def test_output_root_symlink_not_followed(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    root = tmp_path / "linked"
    try:
        root.symlink_to(real, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable on this platform")
    with pytest.raises(ValueError, match="symlink"):
        forge_domain(ARCH, output_root=root)
    assert list(real.iterdir()) == []


def test_failed_render_leaves_no_partial_destination_or_stage(tmp_path, monkeypatch):
    def damaged_renderer(arch, root):
        partial = root / arch.name
        partial.mkdir()
        (partial / "part").write_text("incomplete")
        raise RuntimeError("injected disk writer failure")
    monkeypatch.setattr(forge_module, "_render_domain", damaged_renderer)
    with pytest.raises(RuntimeError, match="injected"):
        forge_domain(ARCH, output_root=tmp_path)
    assert not (tmp_path / ARCH.name).exists()
    assert not list(tmp_path.glob(".genius-forge-stage-*"))


def test_cli_archetype_forge_portable_and_refuses_conflicts(tmp_path, capsys):
    args = ["archetype", "forge", "aerospace", "--output-root", str(tmp_path)]
    assert main(args) == 0
    assert (tmp_path / ARCH.name / "GENIUS.yaml").is_file()
    assert "unverified" in capsys.readouterr().out.lower()
    assert main(args) == 0
    (tmp_path / ARCH.name / ".hidden").write_text("preserved")
    assert main(args) == 1
    assert (tmp_path / ARCH.name / ".hidden").read_text() == "preserved"


def test_independent_descendant_package_and_real_native_tests(tmp_path):
    repo = forge_domain(ARCH, output_root=tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo / "src")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=repo, env=env, capture_output=True, text=True, timeout=90,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    # The output suite must not import the teacher checkout for application code.
    packages = [p for p in (repo / "src").iterdir() if p.is_dir()]
    assert len(packages) == 1
    imported = subprocess.run(
        [sys.executable, "-c",
         "import importlib; m=importlib.import_module(%r); print(m.__file__)" % packages[0].name],
        cwd=repo, env=env, capture_output=True, text=True, timeout=30,
    )
    assert imported.returncode == 0, imported.stderr
    assert str(repo / "src") in imported.stdout
