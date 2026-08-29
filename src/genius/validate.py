"""Contract validation for a Genius repository root."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REPO_NAME_RE = re.compile(r"^Genius-[A-Za-z0-9._-]+$")
SUPPORTED_SCHEMA = 2


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_repo(root: Path) -> list[str]:
    """Return list of error strings; empty means PASS."""
    errors: list[str] = []
    genius_path = root / "GENIUS.yaml"
    if not genius_path.exists():
        errors.append("GENIUS.yaml missing")
        return errors

    data = load_yaml(genius_path)
    if not isinstance(data, dict):
        errors.append("GENIUS.yaml is not a mapping")
        return errors

    if data.get("schema_version") != SUPPORTED_SCHEMA:
        errors.append(
            f"Unsupported schema_version={data.get('schema_version')}; required {SUPPORTED_SCHEMA}"
        )

    repo = data.get("repository")
    if not isinstance(repo, str) or not REPO_NAME_RE.match(repo):
        errors.append(f"repository must match ^Genius-[A-Za-z0-9._-]+$, got {repo!r}")

    if data.get("family") != "Genius":
        errors.append("family must be 'Genius'")
    if data.get("doctrine") != "mastery-not-skills":
        errors.append("doctrine must be 'mastery-not-skills'")

    # Claims uniqueness
    claims_path = root / "claims" / "CLAIMS.yaml"
    if claims_path.exists():
        claims = (load_yaml(claims_path) or {}).get("claims") or []
        ids: set[str] = set()
        for c in claims:
            cid = c.get("id")
            if not cid:
                errors.append("claim missing id")
                continue
            if cid in ids:
                errors.append(f"duplicate claim id: {cid}")
            ids.add(cid)
            if not c.get("statement") or len(str(c["statement"])) < 10:
                errors.append(f"claim {cid}: statement too short or missing")

    # Composition capability uniqueness
    comp_path = root / "interfaces" / "COMPOSITION.yaml"
    if comp_path.exists():
        comp = load_yaml(comp_path) or {}
        provides = comp.get("provides") or []
        pids: set[str] = set()
        for p in provides:
            pid = p.get("id")
            if not pid:
                errors.append("provides entry missing id")
                continue
            if pid in pids:
                errors.append(f"duplicate capability id: {pid}")
            pids.add(pid)

    return errors
