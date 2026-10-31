"""Execution-level regression tests for staged Genius Lineage generation."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from genius.archetypes import get_archetype
from genius.lineage.forge import forge_domain
from genius.lineage.publication import publish_domain


@pytest.fixture
def aerospace():
    arch = get_archetype("aerospace")
    assert arch is not None
    return arch


def test_portable_default_resolves_at_call_time_and_emits_native_source(tmp_path, monkeypatch, aerospace):
    monkeypatch.chdir(tmp_path)
    output = forge_domain(aerospace)
    assert output == tmp_path / "Genius-Lineage" / aerospace.name
    assert output.is_dir()
    graph = yaml.safe_load((output / "capabilities/GRAPH.yaml").read_text())
    assert graph["capabilities"]
    assert all(item["verified"] is False for item in graph["capabilities"])
    assert all(item["evidence_state"] == "mapped" for item in graph["capabilities"])
    assert all(item["evidence_refs"] == [] for item in graph["capabilities"])
    assert (output / "pyproject.toml").is_file()
    assert (output / "tests/test_invariants.py").is_file()
    assert len(list((output / "src").rglob("tools.py"))) == 1
    assert not list((output.parent).glob(".*.stage-*"))
    assert not list((output.parent).glob("*.genius-forge.lock"))


def test_nonempty_target_is_untouched_even_with_hidden_files(tmp_path, aerospace):
    target = tmp_path / aerospace.name
    target.mkdir()
    sentinel = target / ".user-history"
    sentinel.write_text("retain this", encoding="utf-8")
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        forge_domain(aerospace, tmp_path)
    assert sentinel.read_text(encoding="utf-8") == "retain this"
    assert sorted(p.name for p in target.iterdir()) == [".user-history"]


def test_failed_renderer_never_publishes_incomplete_repository(tmp_path, aerospace, monkeypatch):
    # The source writes a number of files before generating the reference
    # library. Inject a late failure to verify staged partials are removed.
    import genius.lineage.forge as module

    original = module.get_domain_references
    monkeypatch.setattr(module, "get_domain_references", lambda _id: [
        {"title": "missing remaining fields"}
    ])
    with pytest.raises(KeyError):
        forge_domain(aerospace, tmp_path)
    assert not (tmp_path / aerospace.name).exists()
    assert not list(tmp_path.glob(f".{aerospace.name}.stage-*"))
    assert not list(tmp_path.glob(f".{aerospace.name}.genius-forge.lock"))
    monkeypatch.setattr(module, "get_domain_references", original)
    assert forge_domain(aerospace, tmp_path).is_dir()


def test_reject_path_escape_and_symlinked_destinations(tmp_path, aerospace):
    for name in ("../escape", "/tmp/nope", ".", "..", "Genius/escape"):
        with pytest.raises(ValueError, match="unsafe generated repository name"):
            publish_domain(tmp_path, name, lambda _stage: tmp_path)
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "linked"
    try:
        link.symlink_to(real, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable on this platform")
    with pytest.raises(ValueError, match="symlink"):
        forge_domain(aerospace, link)
    assert list(real.iterdir()) == []
    (tmp_path / aerospace.name).symlink_to(real, target_is_directory=True)
    with pytest.raises(FileExistsError):
        forge_domain(aerospace, tmp_path)


def test_forge_cli_emits_usable_independent_project(tmp_path, aerospace):
    result = subprocess.run(
        [sys.executable, "-m", "genius.cli", "archetype", "forge", "aerospace",
         "--dest", str(tmp_path)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    generated = tmp_path / aerospace.name
    assert "not verified" in result.stdout
    assert (generated / "src").is_dir()
    # Run independent generated tests from the descendant root, not a
    # test suite inside the teacher's src/ package.
    run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=generated, capture_output=True, text=True, check=False,
        env={**os.environ, "PYTHONPATH": str(generated / "src")},
    )
    assert run.returncode == 0, run.stdout + run.stderr
    receipt = json.loads((generated / "evidence/RECEIPTS.jsonl").read_text().strip())
    assert receipt["status"] == "FORGED"  # Never confused with test verification.



def test_exact_second_generation_is_idempotent_and_does_not_rewrite_files(tmp_path, aerospace):
    generated = forge_domain(aerospace, tmp_path)
    code = next((generated / "src").rglob("tools.py"))
    before = (code.read_bytes(), code.stat().st_mtime_ns)
    original_receipt = (generated / "evidence/RECEIPTS.jsonl").read_bytes()
    assert forge_domain(aerospace, tmp_path) == generated
    assert (code.read_bytes(), code.stat().st_mtime_ns) == before
    assert (generated / "evidence/RECEIPTS.jsonl").read_bytes() == original_receipt
    assert not list(tmp_path.glob(".*.stage-*"))
    assert not list(tmp_path.glob("*.genius-forge.lock"))


def test_user_modified_existing_source_never_replaced(tmp_path, aerospace):
    generated = forge_domain(aerospace, tmp_path)
    file = generated / "GENIUS.yaml"
    file.write_text(file.read_text() + "\n# retain user edit\n")
    with pytest.raises(FileExistsError, match="changed or unrelated"):
        forge_domain(aerospace, tmp_path)
    assert file.read_text().endswith("# retain user edit\n")


def test_added_receipt_record_preserved_without_jsonl_parse_failure(tmp_path, aerospace):
    generated = forge_domain(aerospace, tmp_path)
    file = generated / "evidence/RECEIPTS.jsonl"
    original = file.read_text()
    user_data = original + json.dumps({"event": "USER_ATTESTED", "verified": True}) + "\n"
    file.write_text(user_data)
    with pytest.raises(FileExistsError, match="changed or unrelated"):
        forge_domain(aerospace, tmp_path)
    assert file.read_text() == user_data


def test_malformed_existing_receipt_does_not_destroy_any_files(tmp_path, aerospace):
    generated = forge_domain(aerospace, tmp_path)
    file = generated / "evidence/RECEIPTS.jsonl"
    file.write_text("{unclosed")
    with pytest.raises(FileExistsError, match="cannot compare existing receipt"):
        forge_domain(aerospace, tmp_path)
    assert file.read_text() == "{unclosed"


def test_added_empty_directory_counts_as_changed_output(tmp_path, aerospace):
    generated = forge_domain(aerospace, tmp_path)
    (generated / "empty-user-dir").mkdir()
    with pytest.raises(FileExistsError, match="changed or unrelated"):
        forge_domain(aerospace, tmp_path)
    assert (generated / "empty-user-dir").is_dir()


def test_materialization_receipt_explicitly_lacks_verification(tmp_path, aerospace):
    generated = forge_domain(aerospace, tmp_path)
    evidence = json.loads((generated / "evidence/RECEIPTS.jsonl").read_text())
    assert evidence["status"] == "FORGED"
    assert evidence["verification_status"] == "UNVERIFIED"


def test_generated_files_reproducible_except_runtime_receipt(tmp_path, aerospace):
    first = forge_domain(aerospace, tmp_path / "one")
    second = forge_domain(aerospace, tmp_path / "two")
    for rel in ("GENIUS.yaml", "capabilities/GRAPH.yaml", "src", "tests"):
        a, b = first / rel, second / rel
        if a.is_file():
            assert a.read_bytes() == b.read_bytes()
        else:
            assert sorted(str(p.relative_to(a)) for p in a.rglob("*")) == (
                sorted(str(p.relative_to(b)) for p in b.rglob("*"))
            )
            for path in a.rglob("*"):
                if path.is_file():
                    assert path.read_bytes() == (b / path.relative_to(a)).read_bytes()
