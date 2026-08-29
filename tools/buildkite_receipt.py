#!/usr/bin/env python3
"""Emit a fail-closed Buildkite receipt without recording credential values."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import subprocess
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"required Buildkite environment variable missing: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--output", default=".verification-artifacts/buildkite-verified-receipt.json")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--proof", action="append", default=[])
    args = parser.parse_args()

    commit = require_env("BUILDKITE_COMMIT")
    branch = require_env("BUILDKITE_BRANCH")
    build_id = require_env("BUILDKITE_BUILD_ID")
    build_number = require_env("BUILDKITE_BUILD_NUMBER")
    pipeline = require_env("BUILDKITE_PIPELINE_SLUG")
    organization = require_env("BUILDKITE_ORGANIZATION_SLUG")

    if not SHA_RE.fullmatch(commit):
        raise RuntimeError(f"BUILDKITE_COMMIT is not an exact 40-character SHA: {commit!r}")

    actual = git("rev-parse", "HEAD")
    if actual != commit:
        raise RuntimeError(f"checkout mismatch: actual={actual} expected={commit}")

    expected_pipeline = args.repository.casefold()
    if pipeline != expected_pipeline:
        raise RuntimeError(
            f"pipeline mismatch: actual={pipeline!r} expected={expected_pipeline!r}"
        )

    subprocess.run(["git", "diff", "--exit-code"], check=True)

    artifact_digests = {}
    for raw_path in args.artifact:
        path = Path(raw_path)
        if not path.is_file():
            raise RuntimeError(f"required verification artifact missing: {path}")
        artifact_digests[path.as_posix()] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "size_bytes": path.stat().st_size,
        }

    proof_artifacts = []
    for raw_path in args.proof:
        proof_path = Path(raw_path)
        if not proof_path.is_file():
            raise RuntimeError(f"required proof artifact missing: {proof_path}")
        payload = proof_path.read_bytes()
        proof_artifacts.append(
            {
                "path": proof_path.as_posix(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "glaciereq.genius.buildkite-receipt.v2",
        "status": "PASS",
        "repository": args.repository,
        "organization": organization,
        "pipeline": pipeline,
        "branch": branch,
        "commit": commit,
        "tree": git("rev-parse", "HEAD^{tree}"),
        "build_id": build_id,
        "build_number": build_number,
        "build_url": f"https://buildkite.com/{organization}/{pipeline}/builds/{build_number}",
        "generated_at": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "verification": {
            "exact_source_checkout": True,
            "tracked_worktree_clean": True,
            "pipeline_identity_match": True,
            "artifact_count": len(artifact_digests),
            "proof_count": len(proof_artifacts),
        },
        "artifacts": artifact_digests,
        "proof_artifacts": proof_artifacts,
        "credential_values_recorded": False,
    }
    encoded = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(encoded)
    digest = hashlib.sha256(encoded).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
