"""Live runtime capability discovery with normalized provenance."""
from __future__ import annotations
import importlib.metadata
import json
import os
import shutil
from pathlib import Path
from typing import Any, TypedDict
import yaml

class DiscoveredCapability(TypedDict, total=False):
    kind: str
    name: str
    version: str
    available: bool
    path: str
    provider: str
    provenance: str
    notes: str

def discover_python_packages(limit: int = 50) -> list[DiscoveredCapability]:
    rows: list[DiscoveredCapability] = []
    seen: set[str] = set()
    try:
        distributions = sorted(importlib.metadata.distributions(), key=lambda d: (d.metadata.get("Name") or "").casefold())
    except Exception:
        distributions = []
    for dist in distributions:
        name = str(dist.metadata.get("Name") or "").strip()
        if not name or name.casefold() in seen:
            continue
        seen.add(name.casefold())
        rows.append({"kind": "python-package", "name": name, "version": str(dist.version or "unknown"), "available": True, "path": "", "provider": "python-environment", "provenance": "importlib.metadata", "notes": "Installed distribution."})
        if len(rows) >= limit:
            break
    return rows

def discover_cli_tools(tools: list[str]) -> list[DiscoveredCapability]:
    rows = []
    for tool in tools:
        path = shutil.which(tool)
        rows.append({"kind": "cli", "name": tool, "version": "unknown", "available": path is not None, "path": path or "", "provider": "PATH", "provenance": "shutil.which", "notes": "Found in PATH." if path else "Not found in PATH."})
    return rows

def _server_names(path: Path) -> list[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(payload, dict):
        return []
    containers = [payload.get("mcpServers"), payload.get("servers")]
    if isinstance(payload.get("mcp"), dict):
        containers.append(payload["mcp"].get("servers"))
    names: set[str] = set()
    for container in containers:
        if isinstance(container, dict):
            names.update(str(name) for name in container)
    return sorted(names)

def discover_mcp_servers(config_root: Path) -> list[DiscoveredCapability]:
    candidates: list[Path] = []
    if config_root.exists():
        if config_root.is_file():
            candidates.append(config_root)
        else:
            for rel in ("mcp.json", ".mcp.json", ".vscode/mcp.json", ".cursor/mcp.json", ".claude/mcp.json"):
                path = config_root / rel
                if path.exists():
                    candidates.append(path)
    rows = []
    for path in sorted(set(candidates)):
        for name in _server_names(path):
            rows.append({"kind": "mcp", "name": name, "version": "unknown", "available": True, "path": str(path), "provider": "configured-mcp", "provenance": str(path), "notes": "Server name only; secret values are not inspected or emitted."})
    return rows

def discover_local_models(model_dirs: list[Path], limit: int = 50) -> list[DiscoveredCapability]:
    rows = []
    for directory in model_dirs:
        if not directory.exists() or not directory.is_dir():
            continue
        for file_path in sorted(directory.rglob("*")):
            if file_path.is_file() and file_path.suffix.casefold() in {".gguf", ".safetensors", ".pt", ".onnx"}:
                rows.append({"kind": "model", "name": file_path.name, "version": "unknown", "available": True, "path": str(file_path), "provider": "local-filesystem", "provenance": str(directory), "notes": "Local model artifact."})
                if len(rows) >= limit:
                    return rows
    return rows

def discover_environment_integrations() -> list[DiscoveredCapability]:
    families = {"OPENAI": "openai", "ANTHROPIC": "anthropic", "GOOGLE": "google", "GITHUB": "github", "BUILDKITE": "buildkite", "SLACK": "slack", "DROPBOX": "dropbox", "NOTION": "notion", "SUPABASE": "supabase"}
    keys = [key.upper() for key in os.environ]
    present = sorted(provider for prefix, provider in families.items() if any(key.startswith(prefix + "_") for key in keys))
    return [{"kind": "integration-signal", "name": provider, "version": "unknown", "available": True, "path": "", "provider": provider, "provenance": "environment-variable-name", "notes": "Signal inferred from variable names only; values were not read."} for provider in present]

def full_discovery_report(root: Path) -> dict[str, list[DiscoveredCapability]]:
    root = root.resolve()
    return {
        "python": discover_python_packages(),
        "cli": discover_cli_tools(["python3", "git", "go", "node", "docker", "bk"]),
        "mcp": discover_mcp_servers(root),
        "models": discover_local_models([Path.home() / ".cache" / "huggingface" / "hub", root / "models"]),
        "integrations": discover_environment_integrations(),
    }

def write_discovery_inventory(root: Path) -> Path:
    target = root / "capabilities" / "RUNTIME_INVENTORY.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": 1, "repository": root.name, "inventory": full_discovery_report(root), "truth_note": "Only capabilities observable from this runtime are recorded; absence is not proof of global absence."}
    target.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return target

def bind_discoveries_to_synthesis(plan: dict[str, Any], discoveries: dict[str, list[DiscoveredCapability]]) -> dict[str, Any]:
    plan["matched_live_capabilities"] = discoveries
    return plan
