from __future__ import annotations

from pathlib import Path

from genius.vector import repository_identity


def test_repository_identity_prefers_genius_yaml_over_checkout_dirname(tmp_path: Path) -> None:
    slug = tmp_path / "genius-mastery"
    slug.mkdir()
    (slug / "GENIUS.yaml").write_text("repository: Genius-Mastery\n", encoding="utf-8")
    assert slug.name == "genius-mastery"
    assert repository_identity(slug) == "Genius-Mastery"


def test_repository_identity_falls_back_to_directory_name(tmp_path: Path) -> None:
    folder = tmp_path / "Genius-Orphan"
    folder.mkdir()
    assert repository_identity(folder) == "Genius-Orphan"
