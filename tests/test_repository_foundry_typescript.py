"""Repository compiler acceptance for the TypeScript task-board product profile."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from genius.repository_foundry_typescript import PROFILE, generate_typescript_task_board


def generated(tmp_path: Path, name: str = "Task Board") -> Path:
    return generate_typescript_task_board(
        "Produce a functional task board with TypeScript backend API and browser UI",
        name, tmp_path,
    )


def test_manifest_and_mission_are_exact_and_not_self_verified(tmp_path):
    root = generated(tmp_path)
    data = json.loads((root / 'source-manifest.json').read_text())
    mission = json.loads((root / 'mission.json').read_text())
    assert mission['schema_version'] == 'glaciereq.repo-foundry.mission.v1'
    assert mission['mode'] == 'NEW' and mission['profile'] == PROFILE
    assert mission['status'] == data['status'] == 'GENERATED_UNVERIFIED'
    assert 'TypeScript backend' in mission['original_objective']
    assert len(data['files_sha256']) >= 11
    for relative, digest in data['files_sha256'].items():
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest
    assert not (root / 'src' / 'genius').exists()


def test_accepted_mission_and_native_project_files(tmp_path):
    import jsonschema
    root = generated(tmp_path)
    schema = json.loads((Path(__file__).resolve().parents[1] / 'schemas/repository-mission.schema.json').read_text())
    jsonschema.validate(json.loads((root / 'mission.json').read_text()), schema)
    package = json.loads((root / 'package.json').read_text())
    lock = json.loads((root / 'package-lock.json').read_text())
    assert package['name'] == lock['name'] == lock['packages']['']['name']
    assert package['devDependencies'] == lock['packages']['']['devDependencies']
    assert 'node_modules/typescript' in lock['packages']
    assert 'node_modules/@types/node' in lock['packages']
    assert 'node_modules/undici-types' in lock['packages']
    for file in ('src/server.ts','src/store.ts','src/public/client.ts',
                 'public/index.html','tests/task-board.test.mjs', 'tsconfig.json',
                 '.github/workflows/verify.yml'):
        assert (root / file).is_file()


def test_generation_is_repeatable_and_preserves_existing_work(tmp_path):
    first = generated(tmp_path / 'one')
    second = generated(tmp_path / 'two')
    assert (first / 'source-manifest.json').read_bytes() == (second / 'source-manifest.json').read_bytes()
    preserved = first / '.operator-asset'
    preserved.write_text('keep this user content')
    with pytest.raises(FileExistsError):
        generated(tmp_path / 'one')
    assert preserved.read_text() == 'keep this user content'


def test_generated_project_name_updates_npm_lock_without_path_dependency(tmp_path):
    project = generated(tmp_path, 'Operator Kanban')
    package = json.loads((project / 'package.json').read_text())
    lock = json.loads((project / 'package-lock.json').read_text())
    assert project.name == 'Genius-Operator-Kanban'
    assert package['name'] == lock['name'] == 'genius-operator-kanban'
    assert lock['packages']['']['name'] == 'genius-operator-kanban'
    assert '/root/projects/' not in (project / 'README.md').read_text()


def test_invalid_mission_does_not_publish(tmp_path):
    for objective in ('', ' ', None, 'a' * 20001):
        with pytest.raises(ValueError, match='objective'):
            generate_typescript_task_board(objective, 'Task Board', tmp_path)
    assert not (tmp_path / 'Genius-Task-Board').exists()


def test_existing_cli_dispatches_supported_profile(tmp_path):
    p = subprocess.run([
        sys.executable, '-m', 'genius.cli', 'foundry', 'new',
        '--profile', PROFILE, '--name', 'Task Board',
        '--objective', 'Deliver a full-stack TypeScript task board', '--dest', str(tmp_path),
    ], text=True, capture_output=True)
    assert p.returncode == 0, p.stdout + p.stderr
    assert 'GENERATED_UNVERIFIED' in p.stdout
    assert (tmp_path / 'Genius-Task-Board/src/server.ts').is_file()