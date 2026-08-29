#!/usr/bin/env python3
"""Genius-Mastery local contract validator."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_NAME_RE = re.compile(r"^Genius-[A-Za-z0-9._-]+$")
SUPPORTED_SCHEMA = 2
SUPPORTED_CAPABILITY_SCHEMA = 1


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def validate_identity(root: Path, errors: list[str]) -> dict | None:
    genius_path = root / "GENIUS.yaml"
    if not genius_path.exists():
        fail("GENIUS.yaml missing", errors)
        return None
    data = load_yaml(genius_path)
    if not isinstance(data, dict):
        fail("GENIUS.yaml is not a mapping", errors)
        return None
    if data.get("schema_version") != SUPPORTED_SCHEMA:
        fail(
            f"Unsupported schema_version={data.get('schema_version')}; required {SUPPORTED_SCHEMA}",
            errors,
        )
    repo = data.get("repository")
    if not isinstance(repo, str) or not REPO_NAME_RE.match(repo):
        fail(f"repository must match ^Genius-[A-Za-z0-9._-]+$, got {repo!r}", errors)
    if data.get("family") != "Genius":
        fail("family must be 'Genius'", errors)
    if data.get("doctrine") != "mastery-not-skills":
        fail("doctrine must be 'mastery-not-skills'", errors)
    return data


def validate_claims(root: Path, errors: list[str]) -> None:
    path = root / "claims" / "CLAIMS.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    claims = data.get("claims") or []
    ids = set()
    for c in claims:
        cid = c.get("id")
        if not cid:
            fail("claim missing id", errors)
            continue
        if cid in ids:
            fail(f"duplicate claim id: {cid}", errors)
        ids.add(cid)
        if not c.get("statement") or len(str(c["statement"])) < 10:
            fail(f"claim {cid}: statement too short or missing", errors)
        if not c.get("dimension"):
            fail(f"claim {cid}: dimension required", errors)
        if not c.get("status"):
            fail(f"claim {cid}: status required", errors)


def validate_composition(root: Path, errors: list[str]) -> None:
    path = root / "interfaces" / "COMPOSITION.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    if data.get("repository") and not REPO_NAME_RE.match(str(data["repository"])):
        fail("COMPOSITION.yaml repository identity invalid", errors)
    provides = data.get("provides") or []
    ids = set()
    for p in provides:
        pid = p.get("id")
        if not pid:
            fail("provides entry missing id", errors)
            continue
        if pid in ids:
            fail(f"duplicate capability id: {pid}", errors)
        ids.add(pid)


def validate_capability_stack(root: Path, errors: list[str]) -> None:
    path = root / "capabilities" / "STACK.yaml"
    if not path.exists():
        return
    data = load_yaml(path)
    if not isinstance(data, dict):
        fail("capabilities/STACK.yaml is not a mapping", errors)
        return
    if data.get("schema_version") != SUPPORTED_CAPABILITY_SCHEMA:
        fail(
            f"capabilities/STACK.yaml schema_version must be {SUPPORTED_CAPABILITY_SCHEMA}",
            errors,
        )
    if not data.get("id"):
        fail("capabilities/STACK.yaml id missing", errors)
    if not data.get("purpose"):
        fail("capabilities/STACK.yaml purpose missing", errors)
    objective = data.get("objective")
    if not isinstance(objective, dict) or not objective.get("desired_reality"):
        fail("capabilities/STACK.yaml objective.desired_reality missing", errors)
    layers = data.get("layers")
    if not isinstance(layers, dict) or not layers:
        fail("capabilities/STACK.yaml layers must be a non-empty mapping", errors)
    verification = data.get("verification")
    if not isinstance(verification, dict):
        fail("capabilities/STACK.yaml verification missing", errors)
    else:
        acceptance = verification.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance:
            fail(
                "capabilities/STACK.yaml verification.acceptance must be non-empty",
                errors,
            )
    if not isinstance(data.get("mission_impact"), dict):
        fail("capabilities/STACK.yaml mission_impact missing", errors)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    print(f"Validating: {root}")
    validate_identity(root, errors)
    validate_claims(root, errors)
    validate_composition(root, errors)
    validate_capability_stack(root, errors)
    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS: contract surfaces OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
