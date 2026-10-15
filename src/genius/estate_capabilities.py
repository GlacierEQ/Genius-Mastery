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
