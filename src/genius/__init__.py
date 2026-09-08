"""Genius-Mastery kernel package."""

__version__ = "1.1.0"

from genius.archetypes import (
    ARCHETYPES,
    ArchetypeDefinition,
    get_archetype,
    list_archetypes,
    match_archetypes,
)

__all__ = [
    "__version__",
    "ARCHETYPES",
    "ArchetypeDefinition",
    "get_archetype",
    "list_archetypes",
    "match_archetypes",
]
