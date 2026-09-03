"""Capability-source adapters for Genius synthesis."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

MEGA_REGISTRIES = {"skill": "registry/skills.json", "combo-skill": "registry/combo-skills.json", "mega-skill": "registry/mega-skills.json"}

def _tokens(value: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", value.casefold()))
    expanded = set(tokens)
    for token in tokens:
        if "-" in token:
            expanded.update(token.split("-"))
    return expanded

def _token_overlap(query_tokens: set[str], target_tokens: set[str]) -> set[str]:
    matched = set()
    for q in query_tokens:
        for t in target_tokens:
            if q == t or (len(q) >= 4 and len(t) >= 4 and (q.startswith(t) or t.startswith(q))):
                matched.add(q)
    return matched

def _flatten_text(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            out.append(str(key)); out.extend(_flatten_text(item))
    elif isinstance(value, list):
        for item in value:
            out.extend(_flatten_text(item))
    return out

def normalize_dependency_ids(entry: dict[str, Any]) -> list[str]:
    ids: set[str] = set()
    def visit(value: Any) -> None:
        if isinstance(value, str) and value.strip():
            ids.add(value.strip())
        elif isinstance(value, list):
            for item in value: visit(item)
        elif isinstance(value, dict):
            if value.get("id"): ids.add(str(value["id"]).strip())
            else:
                for item in value.values(): visit(item)
    for key in ("dependencies", "requires", "depends_on", "skills", "components"):
        if entry.get(key) is not None:
            visit(entry[key])
    ids.discard(str(entry.get("id") or ""))
    return sorted(item for item in ids if item)

def load_mega_skills_registry(root: Path) -> list[dict[str, Any]]:
    capabilities = []
    for kind, rel in MEGA_REGISTRIES.items():
        path = root.resolve() / rel
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for entry in payload.get("entries") or []:
            if isinstance(entry, dict):
                capabilities.append({"kind": kind, "id": entry.get("id", ""), "display_name": entry.get("display_name", ""), "maturity": entry.get("maturity", ""), "version": entry.get("version", ""), "entrypoint": entry.get("entrypoint", ""), "dependencies": normalize_dependency_ids(entry), "source_repository": "GlacierEQ/mega-skills", "source_registry": rel, "_raw": entry})
    return capabilities

def match_mega_skills(role: str, outcomes: list[str], root: Path, *, limit: int = 16) -> list[dict[str, Any]]:
    query_tokens = _tokens(" ".join([role, *outcomes]))
    ranked = []
    for capability in load_mega_skills_registry(root):
        raw = capability["_raw"]
        identity = _tokens(" ".join(str(raw.get(k, "")) for k in ("id", "display_name")))
        body = _tokens(" ".join(_flatten_text(raw)))
        id_matches = _token_overlap(query_tokens, identity)
        body_matches = _token_overlap(query_tokens, body)
        score = len(id_matches) * 5 + len(body_matches)
        if score <= 0: continue
        clean = {k: v for k, v in capability.items() if k != "_raw"}
        clean["match_score"] = score
        clean["matched_terms"] = sorted(body_matches.union(id_matches))
        ranked.append((score, str(clean.get("id", "")), clean))
    ranked.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in ranked[:limit]]
