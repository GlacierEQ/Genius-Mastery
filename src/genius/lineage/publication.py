"""Portable, guarded, staged publication for generated Genius repositories.

Only completed generated directories are published. Existing destinations are
preserved by default; explicit replacements retain a rollback copy. A host/process crash may leave a hidden stage
or lock behind; inspect and recover that path before retrying.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Callable

_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _tree_signature(root: Path) -> dict[str, tuple[str, bytes]]:
    """Compare complete generated trees without following links or losing receipts.

    The forge materialization timestamp is the only volatile data excluded
    from the content identity. Additional receipts remain significant.
    """
    if root.is_symlink() or not root.is_dir():
        raise FileExistsError(f"unsafe existing generated destination: {root}")
    signature: dict[str, tuple[str, bytes]] = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise FileExistsError(f"refusing to follow generated symlink: {path}")
        key = path.relative_to(root).as_posix()
        if path.is_dir():
            signature[key] = ("directory", b"")
            continue
        if not path.is_file():
            raise FileExistsError(f"unsupported generated entry: {path}")
        data = path.read_bytes()
        if key == "evidence/RECEIPTS.jsonl":
            try:
                records = []
                for line in data.splitlines():
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    if not isinstance(entry, dict):
                        raise ValueError("receipt must be an object")
                    entry.pop("timestamp", None)
                    records.append(json.dumps(entry, sort_keys=True, separators=(",", ":")))
                data = ("\n".join(records) + "\n").encode("utf-8")
            except (ValueError, TypeError, UnicodeDecodeError) as error:
                raise FileExistsError(
                    f"cannot compare existing receipt safely: {path}"
                ) from error
        signature[key] = ("file", data)
    return signature



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
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise FileExistsError(f"refusing to overwrite existing destination: {target}")
    if any(p.name.casefold() == repo_name.casefold() and p.name != repo_name for p in root.iterdir()):
        raise FileExistsError(f"case-insensitive destination collision: {target}")

    lock = root / f".{repo_name}.genius-forge.lock"
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise FileExistsError(f"forge already active or stale lock requires recovery: {lock}") from error
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        if target.is_symlink() or (target.exists() and not target.is_dir()):
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
            if target.is_symlink():
                raise FileExistsError(f"refusing to overwrite symlink: {target}")
            backup = None
            if target.exists():
                if _tree_signature(target) == _tree_signature(expected):
                    return target  # Same intent: no write, preserving prior receipts.
                if not force:
                    raise FileExistsError(
                        f"refusing to overwrite changed or unrelated destination: {target}"
                    )
                # Explicit replacement retains the original until publication succeeds.
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
