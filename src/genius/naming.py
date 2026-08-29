"""Naming normalization: purpose string → Genius-{Purpose}."""
from __future__ import annotations

import re

_UNSAFE = re.compile(r"[^A-Za-z0-9._\s-]+")
_SPACES = re.compile(r"[\s_]+")


def normalize_purpose(purpose: str) -> str:
    """Turn free text into a safe hyphenated purpose segment."""
    s = purpose.strip()
    if not s:
        raise ValueError("purpose must be non-empty")
    s = _UNSAFE.sub("", s)
    s = _SPACES.sub("-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        raise ValueError("purpose normalizes to empty")
    # Title-case segments for readability while remaining valid
    parts = [p[:1].upper() + p[1:] if p else p for p in s.split("-")]
    return "-".join(parts)


def genius_name(purpose: str) -> str:
    """genius name 'Distributed Systems' → Genius-Distributed-Systems"""
    return f"Genius-{normalize_purpose(purpose)}"


def assert_valid_repo_name(name: str) -> None:
    if not re.match(r"^Genius-[A-Za-z0-9._-]+$", name):
        raise ValueError(f"invalid Genius repository name: {name!r}")
