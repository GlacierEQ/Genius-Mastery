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
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"required Buildkite environment variable missing: {name}")
    return value


def git_dir(root: Path = Path(".")) -> Path:
    marker = root / ".git"
    if marker.is_dir():
        return marker
    if marker.is_file():
        raw = marker.read_text(encoding="utf-8").strip()
        prefix = "gitdir:"
        if not raw.lower().startswith(prefix):
            raise RuntimeError(f"unsupported .git file: {raw!r}")
        path = Path(raw[len(prefix):].strip())
        return path if path.is_absolute() else (root / path).resolve()
    raise RuntimeError("checkout has no .git metadata")


def resolve_checkout_head(root: Path = Path(".")) -> str:
    directory = git_dir(root)
    head = (directory / "HEAD").read_text(encoding="utf-8").strip()
    if SHA_RE.fullmatch(head):
        return head
    if not head.startswith("ref: "):
        raise RuntimeError(f"unsupported Git HEAD value: {head!r}")
    ref = head[5:].strip()
    loose = directory / ref
    if loose.is_file():
        value = loose.read_text(encoding="utf-8").strip()
        if SHA_RE.fullmatch(value):
            return value
    packed = directory / "packed-refs"
    if packed.is_file():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith(("#", "^")):
                continue
            try:
                value, name = line.split(" ", 1)
            except ValueError:
                continue
            if name == ref and SHA_RE.fullmatch(value):
                return value
    raise RuntimeError(f"cannot resolve Git ref {ref!r}")


def digest_file(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size_bytes": len(payload),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument(
        "--output",
        default=".verification-artifacts/buildkite-verified-receipt.json",
    )
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
        raise RuntimeError(
            f"BUILDKITE_COMMIT is not an exact 40-character SHA: {commit!r}"
        )

    actual = resolve_checkout_head()
    if actual != commit:
        raise RuntimeError(f"checkout mismatch: actual={actual} expected={commit}")

    expected_pipeline = args.repository.casefold()
    if pipeline != expected_pipeline:
        raise RuntimeError(
            f"pipeline mismatch: actual={pipeline!r} expected={expected_pipeline!r}"
        )

    artifacts: dict[str, dict[str, object]] = {}
    for raw_path in args.artifact:
        path = Path(raw_path)
        if not path.is_file():
            raise RuntimeError(f"required verification artifact missing: {path}")
        artifacts[path.as_posix()] = digest_file(path)

    proofs: dict[str, dict[str, object]] = {}
    for raw_path in args.proof:
        path = Path(raw_path)
        if not path.is_file():
            raise RuntimeError(f"required proof artifact missing: {path}")
        proofs[path.as_posix()] = digest_file(path)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "schema": "glaciereq.genius.buildkite-receipt.v3",
        "status": "PASS",
        "repository": args.repository,
        "organization": organization,
        "pipeline": pipeline,
        "branch": branch,
        "commit": commit,
        "checkout_head": actual,
        "build_id": build_id,
        "build_number": build_number,
        "build_url": (
            f"https://buildkite.com/{organization}/{pipeline}/builds/{build_number}"
        ),
        "generated_at": (
            dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        ),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "verification": {
            "exact_source_checkout": True,
            "pipeline_identity_match": True,
            "artifact_count": len(artifacts),
            "proof_count": len(proofs),
        },
        "artifacts": artifacts,
        "proof_artifacts": proofs,
        "credential_values_recorded": False,
    }
    encoded = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(encoded)
    digest = hashlib.sha256(encoded).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n",
        encoding="utf-8",
    )
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
