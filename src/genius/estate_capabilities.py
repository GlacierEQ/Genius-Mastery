"""Read-only Monolith capability routing. Catalog hits are never execution proof."""
from __future__ import annotations
import re
from typing import Any

def match_capabilities(catalog: dict[str, Any], objective: str, *, limit: int = 12) -> list[dict[str, Any]]:
    if not isinstance(catalog, dict) or not isinstance(objective, str):
        raise TypeError('catalog must be a mapping and objective must be text')
    if limit < 0:
        raise ValueError('limit must be nonnegative')
    tokens = set(re.findall(r'[a-z0-9]+', objective.casefold()))
    result = []
    vectors = catalog.get('intent_vectors', {})
    if not isinstance(vectors, dict):
        return []
    for intent_id, item in vectors.items():
        if not isinstance(item, dict):
            continue
        keywords = item.get('keywords', [])
        repos = item.get('anchor_repositories', [])
        if not isinstance(keywords, list) or not isinstance(repos, list):
            continue
        matched = [k for k in keywords if isinstance(k, str) and set(re.findall(r'[a-z0-9]+', k.casefold())) <= tokens and k.strip()]
        if not matched:
            continue
        result.append({'intent_id': str(intent_id), 'matched_keywords': sorted(set(matched)),
                       'repositories': [r for r in repos if isinstance(r, str)],
                       'evidence_state': 'catalog-pointer-unverified',
                       'next_gate': 'inspect owning repository at current head and verify implementation and execution receipts',
                       'score': len(matched)})
    result.sort(key=lambda x: (-x['score'], x['intent_id']))
    return result[:limit]


def inspect_monolith_catalog(path, objective: str, *, limit: int = 12) -> dict[str, Any]:
    """Load a local capability index and record matching repository pointers."""
    import hashlib
    import json
    from pathlib import Path

    catalog_path = Path(path)
    try:
        raw = catalog_path.read_bytes()
        catalog = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid Monolith catalog: {exc}") from exc
    if not isinstance(catalog, dict) or not isinstance(catalog.get("intent_vectors"), dict):
        raise ValueError("Monolith catalog requires an intent_vectors object")
    return {
        "schema_version": 1,
        "source_repository": "GlacierEQ/monolith",
        "source_catalog": catalog_path.name,
        "catalog_sha256": hashlib.sha256(raw).hexdigest(),
        "catalog_version": str(catalog.get("version") or "unknown"),
        "catalog_generated_at": str(catalog.get("generated_timestamp") or "unknown"),
        "query_objective": objective,
        "matching_intents": match_capabilities(catalog, objective, limit=limit),
        "capability_assessment": "Catalog references are discovery pointers; implementations and runtime results require independent verification.",
        "next_verification": [
            "Inspect the owning repository at current head",
            "Reproduce a representative execution and inspect its results",
            "Record the exact source and runtime verification receipts",
        ],
    }
