"""Independent, source-bound native acceptance for GENIUS Foundry outputs.

Only two known profiles have executable adapters. This verifies manifest bytes
before running code and records native test results, without promoting a local
test to provider deployment or arbitrary objective satisfaction.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

MISSION_SCHEMA = "glaciereq.repo-foundry.mission.v1"
MANIFEST_SCHEMA = "glaciereq.repo-foundry.source-manifest.v1"
PROFILES = {"python-text-audit", "typescript-taskboard", "typescript-text-workbench"}
SHA = re.compile(r"[0-9a-f]{64}\Z")


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _verify_integrity(root: Path) -> tuple[dict[str, Any] | None, str | None, list[str]]:
    """Verify trusted source identity before executing even the first test."""
    problems: list[str] = []
    try:
        mission_path = root / "mission.json"
        manifest_path = root / "source-manifest.json"
        if mission_path.is_symlink() or manifest_path.is_symlink():
            raise ValueError("mission and manifest must be regular files, not symlinks")
        mission = json.loads(mission_path.read_text(encoding="utf-8"))
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
        if not isinstance(mission, dict) or not isinstance(manifest, dict):
            raise ValueError("mission and manifest must be JSON objects")
        if mission.get("schema_version") != MISSION_SCHEMA:
            raise ValueError("mission schema does not match Foundry v1")
        if mission.get("project") != root.name:
            raise ValueError("mission project does not match target directory")
        if mission.get("profile") not in PROFILES:
            raise ValueError("profile is not supported by native verification")
        if mission.get("status") != "GENERATED_UNVERIFIED":
            raise ValueError("unexpected initial mission evidence state")
        if manifest.get("schema_version") != MANIFEST_SCHEMA:
            raise ValueError("unsupported source manifest schema")
        if manifest.get("status") != "GENERATED_UNVERIFIED":
            raise ValueError("manifest claims an unsupported evidence state")
        files = manifest.get("files_sha256")
        if not isinstance(files, dict) or not files or len(files) > 500:
            raise ValueError("source manifest must contain 1-500 file digests")
        if "mission.json" not in files:
            raise ValueError("original objective is not covered by the source manifest")
        for relative, expected in files.items():
            if not isinstance(relative, str) or not isinstance(expected, str) or not SHA.fullmatch(expected):
                problems.append(f"invalid manifest entry: {relative!r}")
                continue
            parts = PurePosixPath(relative)
            if (parts.is_absolute() or relative.startswith("./") or ":" in relative
                    or "\\" in relative or any(p in ("..", ".", "") for p in relative.split("/"))):
                problems.append(f"unsafe source path: {relative}")
                continue
            file = root.joinpath(*parts.parts)
            if file.is_symlink() or any(parent.is_symlink() for parent in file.parents if parent != root and root in parent.parents):
                problems.append(f"symlink source refused: {relative}")
                continue
            try:
                if not file.is_file() or _hash(file.read_bytes()) != expected:
                    problems.append(f"source integrity mismatch: {relative}")
            except OSError:
                problems.append(f"source unavailable: {relative}")
        return mission, _hash(manifest_bytes), problems
    except (OSError, ValueError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        return None, None, [f"unreadable or untrusted mission/manifest: {type(exc).__name__}: {exc}"]


def _run(command: list[str], root: Path, env: dict[str, str], timeout: int) -> dict[str, Any]:
    """Run fixed profile-specific native commands, never commands from a manifest."""
    started = time.monotonic()
    try:
        process = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=timeout)
        return {
            "argv": command, "exit_code": process.returncode,
            "stdout_sha256": _hash(process.stdout.encode("utf-8")),
            "stderr_sha256": _hash(process.stderr.encode("utf-8")),
            "stdout_excerpt": process.stdout[-3000:], "stderr_excerpt": process.stderr[-3000:],
            "elapsed_ms": round((time.monotonic() - started) * 1000),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "argv": command, "exit_code": None, "failure": f"timeout after {timeout}s",
            "elapsed_ms": round((time.monotonic() - started) * 1000),
        }
    except OSError as exc:
        return {
            "argv": command, "exit_code": None, "failure": f"tool invocation error: {type(exc).__name__}",
            "elapsed_ms": round((time.monotonic() - started) * 1000),
        }


def _save_receipt(root: Path, report: dict[str, Any], receipt_dir: Path | None) -> Path:
    folder = (root.parent / ".foundry-receipts" / root.name if receipt_dir is None
              else Path(receipt_dir).expanduser().absolute())
    if folder.is_symlink() or any(parent.is_symlink() for parent in folder.parents):
        raise ValueError("refusing symlinked verification receipt destination")
    folder.mkdir(parents=True, exist_ok=True)
    receipt = folder / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}-{uuid.uuid4().hex}.json"
    data = (json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    fd, temp = tempfile.mkstemp(prefix=".foundry-receipt-", dir=folder)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, receipt)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    return receipt


def verify_generated_repository(root: Path | str, *, receipt_dir: Path | str | None = None,
                                timeout: int = 120) -> dict[str, Any]:
    """Run accepted native product behavior and preserve an external receipt.

    Explicit invocation executes code from the supplied checkout. Only run
    against trusted worktrees. `TESTED` means these commands passed, not
    deployed, enterprise compliant, or fully satisfying arbitrary objectives.
    """
    project = Path(root).expanduser().absolute()
    if project.is_symlink() or not project.is_dir():
        raise ValueError(f"Foundry output must be an existing real directory: {project}")
    if type(timeout) is not int or not 1 <= timeout <= 1200:
        raise ValueError("timeout must be an integer from 1 to 1200 seconds")
    mission, manifest_hash, problems = _verify_integrity(project)
    report: dict[str, Any] = {
        "schema_version": "glaciereq.repo-foundry.verification-receipt.v1",
        "project": project.name, "profile": mission.get("profile") if mission else None,
        "source_manifest_sha256": manifest_hash,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": sys.version.split()[0], "platform": sys.platform},
        "state": "FAILED_INTEGRITY" if problems else "UNTESTED",
        "integrity_problems": problems,
        "execution_problems": [],
        "native_executions": [],
        "external_provider_verified": False,
        "deployment_verified": False,
    }
    if not problems:
        # Do not leak arbitrary provider tokens or operator secrets inherited
        # from the invoking shell into generated native test processes.
        allowed = {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "TEMP",
                   "TMP", "SYSTEMROOT", "USERPROFILE"}
        env = {key: value for key, value in os.environ.items() if key in allowed}
        env["PYTHONPATH"] = str(project / "src")
        profile = mission["profile"]
        if profile == "python-text-audit":
            commands = [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]]
        else:
            npm = shutil.which("npm")
            if not npm:
                commands = []
            elif profile == "typescript-taskboard":
                commands = [
                    [npm, "ci", "--offline", "--ignore-scripts", "--no-audit", "--no-fund"],
                    [npm, "test"],
                ]
            else:
                # Current owned text-workbench template intentionally uses
                # exact-pinned developer dependencies without an npm lockfile.
                # Native tests run first, then npm installs with scripts disabled
                # before static typecheck and build. No command comes from input.
                commands = [
                    [npm, "test"],
                    [npm, "install", "--ignore-scripts", "--no-audit", "--no-fund"],
                    [npm, "run", "typecheck"],
                    [npm, "run", "build"],
                ]
        if not commands:
            report["state"] = "BLOCKED_TOOLCHAIN"
            report["execution_problems"].append(
                "npm is unavailable on the current execution host"
            )
        else:
            for command in commands:
                result = _run(command, project, env, timeout)
                report["native_executions"].append(result)
                if result["exit_code"] is None:
                    # Timeout/tool startup is an execution-environment failure,
                    # not proof that the product's tests themselves failed.
                    report["state"] = "BLOCKED_EXECUTION"
                    report["execution_problems"].append(
                        result.get("failure", "native tool exited without a result")
                    )
                    break
                if result["exit_code"] != 0:
                    report["state"] = "FAILED_TESTS"
                    break
            else:
                report["state"] = "TESTED"
    saved = _save_receipt(project, report, Path(receipt_dir) if receipt_dir is not None else None)
    return {**report, "receipt_path": str(saved)}