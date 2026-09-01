"""Regression tests for fail-closed Buildkite receipts."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = ROOT / "tools" / "buildkite_receipt.py"


def _load_receipt_module():
    spec = importlib.util.spec_from_file_location("buildkite_receipt_tested", RECEIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fake_checkout(tmp_path: Path, sha: str) -> Path:
    root = tmp_path / "checkout"
    git = root / ".git"
    git.mkdir(parents=True)
    (git / "HEAD").write_text(sha + "\n", encoding="utf-8")
    (root / ".verification-artifacts").mkdir()
    (root / ".verification-artifacts" / "junit.xml").write_text(
        "<testsuite tests='1' failures='0'/>\n",
        encoding="utf-8",
    )
    (root / ".verification-artifacts" / "mastery-vector.yaml").write_text(
        "schema_version: 2\nintegrity:\n  clean: true\n",
        encoding="utf-8",
    )
    return root


def _env(monkeypatch: pytest.MonkeyPatch, commit: str) -> None:
    values = {
        "BUILDKITE_COMMIT": commit,
        "BUILDKITE_COMMIT_RESOLVED": "true",
        "BUILDKITE_BRANCH": "main",
        "BUILDKITE_BUILD_ID": "build-id",
        "BUILDKITE_BUILD_NUMBER": "999",
        "BUILDKITE_PIPELINE_SLUG": "genius-mastery",
        "BUILDKITE_ORGANIZATION_SLUG": "casey-1",
    }
    for key, value in values.items():
        monkeypatch.setenv(key, value)


def _run_receipt(monkeypatch: pytest.MonkeyPatch, checkout: Path):
    module = _load_receipt_module()
    monkeypatch.chdir(checkout)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "buildkite_receipt.py",
            "--repository",
            "genius-mastery",
            "--artifact",
            ".verification-artifacts/junit.xml",
            "--proof",
            ".verification-artifacts/mastery-vector.yaml",
        ],
    )
    assert module.main() == 0
    path = checkout / ".verification-artifacts" / "buildkite-verified-receipt.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_receipt_binds_exact_requested_sha(monkeypatch, tmp_path):
    sha = "a" * 40
    checkout = _fake_checkout(tmp_path, sha)
    _env(monkeypatch, sha)

    receipt = _run_receipt(monkeypatch, checkout)

    assert receipt["commit"] == sha
    assert receipt["checkout_head"] == sha
    assert receipt["requested_commit"] == sha
    assert receipt["requested_commit_is_exact"] is True
    assert receipt["verification"]["requested_exact_sha_matched"] is True
    assert receipt["verification"]["symbolic_request_recorded"] is False


def test_receipt_records_symbolic_head_and_binds_resolved_checkout(monkeypatch, tmp_path):
    sha = "b" * 40
    checkout = _fake_checkout(tmp_path, sha)
    _env(monkeypatch, "HEAD")

    receipt = _run_receipt(monkeypatch, checkout)

    assert receipt["requested_commit"] == "HEAD"
    assert receipt["requested_commit_is_exact"] is False
    assert receipt["commit"] == sha
    assert receipt["checkout_head"] == sha
    assert receipt["verification"]["requested_exact_sha_matched"] is False
    assert receipt["verification"]["symbolic_request_recorded"] is True


def test_receipt_rejects_conflicting_exact_sha(monkeypatch, tmp_path):
    checkout = _fake_checkout(tmp_path, "c" * 40)
    _env(monkeypatch, "d" * 40)
    module = _load_receipt_module()
    monkeypatch.chdir(checkout)
    monkeypatch.setattr(
        sys,
        "argv",
        ["buildkite_receipt.py", "--repository", "genius-mastery"],
    )

    with pytest.raises(RuntimeError, match="checkout mismatch"):
        module.main()


def test_receipt_rejects_unknown_symbolic_commit(monkeypatch, tmp_path):
    checkout = _fake_checkout(tmp_path, "e" * 40)
    _env(monkeypatch, "refs/heads/main")
    module = _load_receipt_module()
    monkeypatch.chdir(checkout)
    monkeypatch.setattr(
        sys,
        "argv",
        ["buildkite_receipt.py", "--repository", "genius-mastery"],
    )

    with pytest.raises(RuntimeError, match="exact SHA or the supported symbolic HEAD"):
        module.main()
