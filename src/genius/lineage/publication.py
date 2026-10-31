"""Portable, guarded, staged publication for generated Genius repositories.

Only completed generated directories are published. Existing destinations are
never intentionally overwritten. A host/process crash may leave a hidden stage
or lock behind; inspect and recover that path before retrying.
"""
from __future__ import annotations

import os
import re
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Callable

_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def checked_root(value: Path | str | None) -> Path:
    """Resolve a target without following an existing symlink in its ancestry."""
    raw = Path.cwd() / "Genius-Lineage" if value is None else Path(value).expanduser()
    root = Path(os.path.abspath(raw))
    for part in (root, *root.parents):
        if part.is_symlink():
            raise ValueError(f"output path contains a symlink: {part}")
        if part.exists() and not part.is_dir():
            raise NotADirectoryError(f"output parent is not a directory: {part}")
    return root


def publish_domain(
    output_root: Path | str | None,
    repo_name: str,
    render: Callable[[Path], Path],
    *,
    force: bool = False,
) -> Path:
    """Render a complete tree in a hidden sibling stage before publication.

    The exclusive name lock serializes cooperating local forge processes.
    Uncooperative filesystem writers need external coordination; no
    cross-machine atomic transaction is claimed.
    """
    if (not isinstance(repo_name, str) or not repo_name.startswith("Genius-")
            or not _NAME.fullmatch(repo_name) or ".." in repo_name
            or repo_name.endswith((".", "-")) or repo_name.startswith("Genius-.")):
        raise ValueError("unsafe generated repository name")
    root = checked_root(output_root)
    root.mkdir(parents=True, exist_ok=True)
    root = checked_root(root)
    target = root / repo_name
    if target.is_symlink() or (target.exists() and (not force or not target.is_dir())):
        raise FileExistsError(f"refusing to overwrite existing destination: {target}")
    if any(p.name.casefold() == repo_name.casefold() and p.name != repo_name for p in root.iterdir()):
        raise FileExistsError(f"case-insensitive destination collision: {target}")

    lock = root / f".{repo_name}.genius-forge.lock"
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        if target.is_symlink() or (target.exists() and (not force or not target.is_dir())):
            raise FileExistsError(f"refusing to overwrite existing destination: {target}")
        staging = Path(tempfile.mkdtemp(prefix=f".{repo_name}.stage-", dir=root))
        try:
            generated = render(staging)
            expected = staging / repo_name
            if generated != expected or not expected.is_dir() or expected.is_symlink():
                raise ValueError("forge did not produce the expected staging tree")
            for entry in expected.rglob("*"):
                if entry.is_symlink():
                    raise ValueError(f"forge emitted an unsafe symlink: {entry}")
            if target.exists() or target.is_symlink():
                raise FileExistsError(f"refusing to overwrite existing destination: {target}")
            # Force replacement is explicit, with the old tree kept until
            # the newly staged tree has been published successfully.
            backup = None
            if target.exists():
                backup = root / f".{repo_name}.backup-{uuid.uuid4().hex}"
                target.rename(backup)
            try:
                os.rename(expected, target)
            except Exception:
                if backup is not None:
                    backup.rename(target)
                raise
            if backup is not None:
                shutil.rmtree(backup)
        finally:
            shutil.rmtree(staging)
    finally:
        os.close(descriptor)
        lock.unlink(missing_ok=True)
    return target
