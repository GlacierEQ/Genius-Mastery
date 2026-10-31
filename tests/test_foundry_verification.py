"""Native evidence, counterevidence, and source-provenance acceptance for Foundry."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from genius.repository_foundry import generate_python_text_audit
from genius.repository_foundry_ts import generate_typescript_taskboard
from genius.foundry_verification import verify_generated_repository
from genius.cli import main


def python_repo(tmp_path):
    return generate_python_text_audit(
        "Build a Unicode text analysis CLI", "Text Audit", tmp_path
    )


def test_python_product_tested_with_durable_truthful_receipt(tmp_path):
    project = python_repo(tmp_path)
    result = verify_generated_repository(project)
    assert result["state"] == "TESTED", result
    assert result["profile"] == "python-text-audit"
    assert len(result["source_manifest_sha256"]) == 64
    assert result["native_executions"] and all(
        row["exit_code"] == 0 for row in result["native_executions"]
    )
    assert not result["deployment_verified"]
    assert not result["external_provider_verified"]
    path = Path(result["receipt_path"])
    assert path.is_file()
    assert project not in path.parents  # Out-of-tree evidence cannot silently alter manifest.
    assert json.loads(path.read_text())["state"] == "TESTED"


def test_source_tampering_prevents_any_execution_and_retains_counterevidence(tmp_path):
    project = python_repo(tmp_path)
    file = next((project / "src").rglob("app.py"))
    file.write_text(file.read_text() + "\n# unapproved modification\n")
    with patch("genius.foundry_verification._run", side_effect=AssertionError("never execute tampered code")):
        result = verify_generated_repository(project)
    assert result["state"] == "FAILED_INTEGRITY"
    assert result["native_executions"] == []
    assert any("source integrity mismatch" in x for x in result["integrity_problems"])
    assert Path(result["receipt_path"]).is_file()


def test_manifest_path_escape_rejected_without_execution(tmp_path):
    project = python_repo(tmp_path)
    manifest = project / "source-manifest.json"
    data = json.loads(manifest.read_text())
    data["files_sha256"]["../some-other-private-file"] = "f" * 64
    manifest.write_text(json.dumps(data))
    with patch("genius.foundry_verification._run", side_effect=AssertionError("no external execution")):
        result = verify_generated_repository(project)
    assert result["state"] == "FAILED_INTEGRITY"
    assert any("unsafe source path" in issue for issue in result["integrity_problems"])


def test_corrupt_manifest_is_failure_with_receipt_not_success(tmp_path):
    project = python_repo(tmp_path)
    (project / "source-manifest.json").write_text("{broken")
    result = verify_generated_repository(project)
    assert result["state"] == "FAILED_INTEGRITY"
    assert len(result["native_executions"]) == 0
    assert Path(result["receipt_path"]).is_file()


def test_native_regression_failure_is_not_reported_as_tested(tmp_path):
    project = python_repo(tmp_path)
    test_file = project / "tests/test_text_audit.py"
    test_file.write_text(test_file.read_text() + "\nraise AssertionError('injected failing regression')\n")
    manifest_path = project / "source-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["files_sha256"]["tests/test_text_audit.py"] = hashlib.sha256(
        test_file.read_bytes()
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest))
    result = verify_generated_repository(project)
    assert result["state"] == "FAILED_TESTS"
    assert result["native_executions"][0]["exit_code"] != 0
    assert result["native_executions"][0]["stderr_sha256"]
    assert "injected failing regression" in result["native_executions"][0]["stderr_excerpt"]


def test_no_arbitrary_manifest_command_execution(tmp_path):
    project = python_repo(tmp_path)
    mission = project / "mission.json"
    payload = json.loads(mission.read_text())
    payload["acceptance_command"] = "sh -c 'DO_NOT_RUN_THIS_UNTRUSTED_COMMAND'"
    mission.write_text(json.dumps(payload))
    manifest_path = project / "source-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["files_sha256"]["mission.json"] = hashlib.sha256(mission.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest))
    result = verify_generated_repository(project)
    assert result["state"] == "TESTED"
    assert all("DO_NOT_RUN_THIS_UNTRUSTED_COMMAND" not in " ".join(r["argv"])
               for r in result["native_executions"])


def test_cli_native_verification_exit_codes_and_json_output(tmp_path, capsys):
    project = python_repo(tmp_path)
    assert main(["foundry", "verify", "--path", str(project), "--json"]) == 0
    output = capsys.readouterr().out
    result = json.loads(output)
    assert result["state"] == "TESTED"
    assert Path(result["receipt_path"]).is_file()
    (project / "README.md").write_text("tampered")
    assert main(["foundry", "verify", "--path", str(project), "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["state"] == "FAILED_INTEGRITY"


def test_runner_timeout_is_not_mislabeled_as_native_test_failure(tmp_path):
    project = python_repo(tmp_path)
    interruption = {
        "argv": ["python", "-m", "unittest"], "exit_code": None,
        "failure": "timeout after 120s", "elapsed_ms": 120000,
    }
    with patch("genius.foundry_verification._run", return_value=interruption):
        result = verify_generated_repository(project)
    assert result["state"] == "BLOCKED_EXECUTION"
    assert result["native_executions"][0]["failure"] == "timeout after 120s"
    assert Path(result["receipt_path"]).is_file()


def test_missing_native_binary_is_separate_from_failed_tests(tmp_path):
    project = generate_typescript_taskboard(
        "Build browser taskboard", "Taskboard", tmp_path
    )
    with patch("genius.foundry_verification.shutil.which", return_value=None):
        result = verify_generated_repository(project)
    assert result["state"] == "BLOCKED_TOOLCHAIN"
    assert result["native_executions"] == []
    assert Path(result["receipt_path"]).is_file()



def test_current_typechecked_workbench_has_distinct_native_verification_path(tmp_path):
    from genius.repository_foundry_text_workbench import generate_typescript_text_workbench
    project = generate_typescript_text_workbench(
        "Build a browser/API Unicode text workbench", "Text Workbench", tmp_path
    )
    calls = []

    def completed(command, project_root, env, timeout):
        calls.append(list(command))
        return {"argv": command, "exit_code": 0, "stdout_sha256": "0" * 64,
                "stderr_sha256": "0" * 64, "elapsed_ms": 2}

    with patch("genius.foundry_verification._run", side_effect=completed):
        result = verify_generated_repository(project)
    assert result["state"] == "TESTED"
    assert result["profile"] == "typescript-text-workbench"
    assert len(calls) == 4
    assert calls[0][-1] == "test"
    assert "install" in calls[1]
    assert calls[2][-1] == "typecheck"
    assert calls[3][-1] == "build"


def test_native_execution_environment_does_not_inherit_provider_secrets(tmp_path, monkeypatch):
    project = python_repo(tmp_path)
    monkeypatch.setenv("GITHUB_TOKEN", "secret-should-not-leak")
    monkeypatch.setenv("PRIVATE_OPERATOR_PASSWORD", "secret-should-not-leak")
    inspected = []

    def completed(command, root, env, timeout):
        inspected.append(dict(env))
        return {"argv": command, "exit_code": 0, "stdout_sha256": "0" * 64,
                "stderr_sha256": "0" * 64, "elapsed_ms": 1}

    with patch("genius.foundry_verification._run", side_effect=completed):
        assert verify_generated_repository(project)["state"] == "TESTED"
    assert inspected
    assert "GITHUB_TOKEN" not in inspected[0]
    assert "PRIVATE_OPERATOR_PASSWORD" not in inspected[0]


def test_invalid_root_or_invalid_timeout_refused(tmp_path):
    with pytest.raises(ValueError, match="existing real"):
        verify_generated_repository(tmp_path / "not-found")
    repo = python_repo(tmp_path)
    for timeout in (0, True, 1201):
        with pytest.raises(ValueError, match="timeout"):
            verify_generated_repository(repo, timeout=timeout)


def test_typescript_native_execution_is_independently_verified(tmp_path):
    if not shutil.which("node") or not shutil.which("npm"):
        pytest.skip("Node/npm missing, fixed CI runner config supplies Node 22")
    import subprocess
    version = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout
    if int(version.lstrip("v").split(".")[0]) < 22:
        pytest.skip("Node 22 required")
    project = generate_typescript_taskboard(
        "Build a real local taskboard browser API", "Taskboard", tmp_path
    )
    result = verify_generated_repository(project)
    assert result["state"] == "TESTED", result
    assert result["profile"] == "typescript-taskboard"
    assert len(result["native_executions"]) == 2
    assert all(x["exit_code"] == 0 for x in result["native_executions"])
    assert not result["deployment_verified"]
