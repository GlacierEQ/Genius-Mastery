"""Genius Lineage domain implementations registry.

Aggregates all 26 canonical domain tools and test suites.
"""
from __future__ import annotations

from typing import Any

from .science import SCIENCE_DOMAINS
from .systems import SYSTEMS_DOMAINS
from .legal import LEGAL_DOMAINS
from .telos import TELOS_DOMAINS

LINEAGE_DOMAINS: dict[str, dict[str, Any]] = {}
LINEAGE_DOMAINS.update(SCIENCE_DOMAINS)
LINEAGE_DOMAINS.update(SYSTEMS_DOMAINS)
LINEAGE_DOMAINS.update(LEGAL_DOMAINS)
LINEAGE_DOMAINS.update(TELOS_DOMAINS)


def get_domain_implementation(domain_id: str) -> dict[str, Any] | None:
    """Retrieve the domain tools and test code implementation for a given archetype ID."""
    return LINEAGE_DOMAINS.get(domain_id)


def list_domain_implementations() -> list[str]:
    """Return all registered domain implementation IDs."""
    return sorted(LINEAGE_DOMAINS.keys())
