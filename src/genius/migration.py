"""Lossless migration engine for Genius-family repositories."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, TypedDict
import yaml

CURRENT_SCHEMA_VERSION = 2

class MigrationReceipt(TypedDict, total=False):
    from_version: int
    to_version: int
    migrated_files: list[str]
    created_files: list[str]
    preserved_ids: list[str]
    warnings: list[str]
    sha256_before: dict[str, str]
    sha256_after: dict[str, str]

def _sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def _yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data

def _atomic_yaml(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    os.replace(tmp, path)

def _preserved_ids(root: Path) -> list[str]:
    ids: set[str] = set()
    claims = root / "claims" / "CLAIMS.yaml"
    if claims.exists():
        for row in (_yaml(claims).get("claims") or []):
            if isinstance(row, dict) and row.get("id"):
                ids.add(str(row["id"]))
    graph = root / "capabilities" / "GRAPH.yaml"
    if graph.exists():
        for row in (_yaml(graph).get("nodes") or []):
            if isinstance(row, dict) and row.get("id"):
                ids.add(str(row["id"]))
    ledger = root / "evidence" / "ledger.jsonl"
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict) and row.get("id"):
                ids.add(str(row["id"]))
    return sorted(ids)

def _create(root: Path, rel: str, content: str, receipt: MigrationReceipt) -> None:
    path = root / rel
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    receipt.setdefault("created_files", []).append(rel)
    receipt.setdefault("sha256_after", {})[rel] = _sha256_file(path)

def _backfill(root: Path, data: dict[str, Any], receipt: MigrationReceipt) -> None:
    repo = str(data.get("repository") or root.name)
    purpose = str(data.get("purpose") or repo.removeprefix("Genius-"))
    for key, value in {
        "composition_contract": "interfaces/COMPOSITION.yaml",
        "capability_anatomy_contract": "capabilities/STACK.yaml",
        "teaching_contract": "teaching/TEACHING.yaml",
        "capability_graph": "capabilities/GRAPH.yaml",
    }.items():
        data.setdefault(key, value)
    _create(root, "claims/CLAIMS.yaml", "schema_version: 1\nclaims: []\n", receipt)
    _create(root, "evidence/ledger.jsonl", "", receipt)
    _create(root, "frontier/QUEUE.yaml", "schema_version: 1\nitems: []\n", receipt)
    _create(root, "mastery/ROADMAP.yaml", "schema_version: 1\nnear_term: []\nmid_term: []\nfrontier: []\n", receipt)
    _create(root, "interfaces/COMPOSITION.yaml",
        "spec_version: 1\n" + f"repository: {repo}\n" + "provides: []\nconsumes:\n  - repository: Genius-Mastery\n    capability: mastery.kernel.schemas\n    reason: Shared Genius-family contracts.\n", receipt)
    _create(root, "teaching/TEACHING.yaml",
        "schema_version: 1\n" + f"teacher: {repo}\nsubject: {purpose} mastery\n" +
        "method:\n  explain: [first principles]\n  demonstrate: [one evidence-backed example]\n  reconstruct: [rebuild from blank state]\n  transfer: [apply to a novel case]\n" +
        "verification:\n  acceptance: [learner reconstructs and transfers the method]\n  evidence_refs: []\n  transfer_challenges: []\n", receipt)

def migrate_genius_repo(root: Path) -> MigrationReceipt:
    root = root.resolve()
    path = root / "GENIUS.yaml"
    if not path.exists():
        raise FileNotFoundError("GENIUS.yaml not found.")
    data = _yaml(path)
    current = int(data.get("schema_version", 1))
    if current > CURRENT_SCHEMA_VERSION:
        raise ValueError(f"repository schema_version={current} is newer than supported {CURRENT_SCHEMA_VERSION}")
    receipt: MigrationReceipt = {
        "from_version": current, "to_version": CURRENT_SCHEMA_VERSION,
        "migrated_files": [], "created_files": [], "preserved_ids": _preserved_ids(root),
        "warnings": [], "sha256_before": {"GENIUS.yaml": _sha256_file(path)}, "sha256_after": {},
    }
    if current == 1:
        data.setdefault("package_version", "0.4.0")
        data["schema_version"] = 2
        receipt["migrated_files"].append("GENIUS.yaml")
    _backfill(root, data, receipt)
    rendered = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    if rendered != path.read_text(encoding="utf-8"):
        _atomic_yaml(path, data)
        if "GENIUS.yaml" not in receipt["migrated_files"]:
            receipt["migrated_files"].append("GENIUS.yaml")
    receipt["sha256_after"]["GENIUS.yaml"] = _sha256_file(path)
    return receipt
