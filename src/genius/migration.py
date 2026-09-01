# src/genius/migration.py
"""Lossless migration engine for Genius-Mastery repositories."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import TypedDict, Any
import yaml

CURRENT_SCHEMA_VERSION = 2

class MigrationReceipt(TypedDict):
    from_version: int
    to_version: int
    migrated_files: list[str]
    preserved_ids: list[str]
    warnings: list[str]
    sha256_before: dict[str, str]
    sha256_after: dict[str, str]

def _sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def migrate_genius_repo(root: Path) -> MigrationReceipt:
    genius_yaml_path = root / "GENIUS.yaml"
    if not genius_yaml_path.exists():
        raise FileNotFoundError("GENIUS.yaml not found.")
        
    with genius_yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        
    current_version = data.get("schema_version", 1)
    
    receipt: MigrationReceipt = {
        "from_version": current_version,
        "to_version": CURRENT_SCHEMA_VERSION,
        "migrated_files": [],
        "preserved_ids": [],
        "warnings": [],
        "sha256_before": {},
        "sha256_after": {}
    }
    
    if current_version == CURRENT_SCHEMA_VERSION:
        return receipt
        
    if current_version == 1:
        _migrate_v1_to_v2(root, receipt, data, genius_yaml_path)
        
    return receipt

def _migrate_v1_to_v2(root: Path, receipt: MigrationReceipt, data: dict[str, Any], path: Path) -> None:
    receipt["sha256_before"][path.name] = _sha256_file(path)
    
    if "package_version" not in data:
        data["package_version"] = "0.4.0"
        
    if "capability_graph" not in data:
        data["capability_graph"] = "capabilities/GRAPH.yaml"
        
    teaching_plan = root / "teaching" / "TEACHING_PLAN.md"
    if teaching_plan.exists() and "teaching_plan" not in data:
        data["teaching_plan"] = "teaching/TEACHING_PLAN.md"
        
    data["schema_version"] = 2
    
    receipt["migrated_files"].append(path.name)
    receipt["preserved_ids"].extend(data.keys())
    
    tmp_path = path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)
        
    os.replace(tmp_path, path)
    
    receipt["sha256_after"][path.name] = _sha256_file(path)
