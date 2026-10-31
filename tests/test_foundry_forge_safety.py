"""Adversarial Phase 2 regression tests for the canonical Lineage forge."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import pytest
import yaml

from genius.archetypes import get_archetype
from genius.lineage import forge as foundry


@pytest.fixture
def arch():
    return get_archetype("aerospace")


def test_default_is_portable_current_workspace(monkeypatch, tmp_path, arch):
    monkeypatch.chdir(tmp_path)
    root = foundry.forge_domain(arch)
    assert root == tmp_path / 'Genius-Lineage' / arch.name
    assert (root / "src").is_dir()
    assert (root / "pyproject.toml").is_file()
    assert not list((tmp_path / 'Genius-Lineage').glob('.*.stage-*'))


def test_generated_capabilities_are_mapped_not_prematurely_verified(tmp_path, arch):
    root = foundry.forge_domain(arch, tmp_path)
    graph = yaml.safe_load((root / "capabilities/GRAPH.yaml").read_text())
    assert graph["capabilities"], "archetype targets must remain preserved"
    assert all(item["state"] == "mapped" and item["verified"] is False
               and item["evidence_refs"] == [] for item in graph["capabilities"])
    stack = yaml.safe_load((root / "capabilities/STACK.yaml").read_text())
    assert all(layer["status"] == "MAPPED" for layer in stack["stack_layers"].values())
    receipt = json.loads((root / "evidence/RECEIPTS.jsonl").read_text())
    assert receipt["status"] == "FORGED", "forge receipt never means independent verification"


def test_reproducible_manifest_and_content_hashes(tmp_path, arch):
    first = foundry.forge_domain(arch, tmp_path / "one")
    second = foundry.forge_domain(arch, tmp_path / "two")
    one = (first / "evidence/MANIFEST.json").read_bytes()
    two = (second / "evidence/MANIFEST.json").read_bytes()
    assert one == two
    manifest = json.loads(one)
    assert manifest["schema_version"] == "genius.foundry.manifest.v1"
    assert manifest["verification_state"] == "generated_unverified"
    assert manifest["files"]
    assert "evidence/RECEIPTS.jsonl" not in [entry["path"] for entry in manifest["files"]]
    for entry in manifest["files"]:
        assert hashlib.sha256((first / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]


def test_existing_files_and_user_edits_are_untouched_by_default(tmp_path, arch):
    existing = tmp_path / arch.name
    existing.mkdir()
    marker = existing / "original-user-work.txt"
    marker.write_text("do not touch", encoding="utf-8")
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        foundry.forge_domain(arch, tmp_path)
    assert marker.read_text(encoding="utf-8") == "do not touch"
    assert set(p.name for p in tmp_path.iterdir()) == {arch.name}


def test_different_input_cannot_silently_overwrite_a_completed_generation(tmp_path, arch):
    first = foundry.forge_domain(arch, tmp_path)
    unchanged = (first / "GENIUS.yaml").read_bytes()
    with pytest.raises(FileExistsError):
        foundry.forge_domain(replace(arch, description="changed specification"), tmp_path)
    assert (first / "GENIUS.yaml").read_bytes() == unchanged


def test_unsafe_names_and_casefold_collisions_rejected(tmp_path, arch):
    for bad in ("Genius-../escape", "Genius-../../unsafe", "Genius-.hidden", "Genius-"):
        with pytest.raises(ValueError, match="unsafe Genius repository"):
            foundry.forge_domain(replace(arch, name=bad), tmp_path)
    alias = tmp_path / arch.name.lower()
    alias.mkdir()
    with pytest.raises(FileExistsError, match="case-insensitive"):
        foundry.forge_domain(arch, tmp_path)
    assert alias.exists()


def test_symlink_destination_is_rejected_without_following_it(tmp_path, arch):
    outside = tmp_path / "protected"
    outside.mkdir()
    (outside / "keep.txt").write_text("keep", encoding="utf-8")
    (tmp_path / arch.name).symlink_to(outside, target_is_directory=True)
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        foundry.forge_domain(arch, tmp_path, force=True)
    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"


def test_interrupted_generation_leaves_no_partial_target_or_stage(monkeypatch, tmp_path, arch):
    original = foundry._render_domain

    def crash(spec, staging):
        target = staging / spec.name
        target.mkdir(parents=True)
        (target / "partial.txt").write_text("interrupted")
        raise RuntimeError("simulated interrupted write")

    monkeypatch.setattr(foundry, "_render_domain", crash)
    with pytest.raises(RuntimeError, match="simulated"):
        foundry.forge_domain(arch, tmp_path)
    assert not (tmp_path / arch.name).exists()
    assert list(tmp_path.iterdir()) == []
    monkeypatch.setattr(foundry, "_render_domain", original)
    assert foundry.forge_domain(arch, tmp_path).exists(), "lock must be cleaned after a failure"


def test_explicit_force_replaces_existing_directory_without_silent_default(tmp_path, arch):
    first = foundry.forge_domain(arch, tmp_path)
    (first / "custom.txt").write_text("operator edit")
    updated = foundry.forge_domain(replace(arch, description="updated description"), tmp_path, force=True)
    assert "updated description" in (updated / "GENIUS.yaml").read_text()
    assert not (updated / "custom.txt").exists()
    assert not any(path.name.startswith(".Genius-") for path in tmp_path.iterdir())


def test_existing_lock_does_not_mutate_target(tmp_path, arch):
    lock = tmp_path / f".{arch.name}.genius-forge.lock"
    lock.write_text("other process", encoding="utf-8")
    with pytest.raises(FileExistsError, match="forge already active"):
        foundry.forge_domain(arch, tmp_path)
    assert lock.read_text() == "other process"
    assert not (tmp_path / arch.name).exists()


def test_cli_forge_executes_existing_archetype_and_preserves_repeated_output(tmp_path):
    import subprocess
    import sys

    command = [sys.executable, "-m", "genius.cli", "forge", "aerospace",
               "--dest", str(tmp_path)]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "generated_unverified" in result.stdout
    assert (tmp_path / "Genius-Aerospace" / "evidence/MANIFEST.json").exists()

    rerun = subprocess.run(command, capture_output=True, text=True)
    assert rerun.returncode != 0
    assert "refusing to overwrite" in rerun.stderr
    assert (tmp_path / "Genius-Aerospace" / "GENIUS.yaml").is_file()


def test_force_publication_failure_restores_every_existing_user_byte(tmp_path, monkeypatch, arch):
    target = foundry.forge_domain(arch, tmp_path)
    original = target / "user-work.md"
    original.write_text("important uncommitted edits", encoding="utf-8")
    before = original.read_bytes()
    import genius.lineage.publication as publication
    real_rename = publication.os.rename

    def fail_staged_publish(source, destination):
        source = Path(source)
        if (source.name == arch.name
                and source.parent.name.startswith(f".{arch.name}.stage-")
                and Path(destination) == target):
            raise OSError("injected atomic publish failure")
        return real_rename(source, destination)

    monkeypatch.setattr(publication.os, "rename", fail_staged_publish)
    with pytest.raises(OSError, match="injected atomic publish failure"):
        foundry.forge_domain(replace(arch, description="new build"), tmp_path, force=True)

    assert original.read_bytes() == before
    assert not list(tmp_path.glob(f".{arch.name}.backup-*"))
    assert not list(tmp_path.glob(f".{arch.name}.stage-*"))
    assert not list(tmp_path.glob(f".{arch.name}.genius-forge.lock"))
