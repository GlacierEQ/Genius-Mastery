"""Build the independent full-stack TypeScript profile from owned, reviewed templates."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from genius.lineage.publication import publish_domain
from genius.naming import genius_name
from genius.repository_foundry import MISSION_SCHEMA

TS_PROFILE = "typescript-text-workbench"
TEMPLATE_ROOT = Path(__file__).resolve().parent / "foundry_templates" / "ts_text_workbench"


def generate_typescript_text_workbench(
    objective: str, name: str, output_root: Path | str | None = None
) -> Path:
    """Compile a real local browser/API product, preserving original wording."""
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("nonempty original objective required")
    if len(objective) > 20_000:
        raise ValueError("objective exceeds 20,000 characters")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("nonempty project name required")
    repo = genius_name(name)
    mission = {
        "schema_version": MISSION_SCHEMA,
        "mode": "NEW",
        "original_objective": objective,
        "project": repo,
        "profile": TS_PROFILE,
        "implemented_behavior": [
            "Loopback Node HTTP API with working browser user interface",
            "Unicode word counts with deterministic ranking",
            "Structured input validation and error status responses",
            "Native Node test suite and TypeScript typecheck/build commands",
        ],
        "unverified_requirements":
            "This product profile does not implement arbitrary objectives or public deployment.",
        "status": "GENERATED_UNVERIFIED",
        "acceptance_command": "npm test && npm run typecheck && npm run build",
    }

    def render(staging: Path) -> Path:
        root = staging / repo
        if not TEMPLATE_ROOT.is_dir():
            raise FileNotFoundError("packaged TypeScript Foundry templates unavailable")
        files: dict[str, str] = {
            "mission.json": json.dumps(mission, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        }
        for template in sorted(TEMPLATE_ROOT.rglob("*")):
            if template.is_symlink():
                raise ValueError("unsafe symlink in Foundry template tree")
            if not template.is_file():
                continue
            name = template.relative_to(TEMPLATE_ROOT).as_posix()
            if name in files or name == "source-manifest.json":
                raise ValueError("reserved Foundry template path")
            data = template.read_text(encoding="utf-8")
            files[name] = data.replace("__PROJECT__", repo).replace("__PACKAGE__", repo.lower())
        required = {
            "src/analysis.ts", "src/server.ts", "web/index.html", "web/app.js",
            "tests/fullstack.test.ts", "package.json", "tsconfig.json",
            "tsconfig.build.json", ".github/workflows/test.yml", "README.md"
        }
        if not required.issubset(files):
            raise ValueError(f"Foundry templates incomplete: {sorted(required - files.keys())}")
        digests = {
            name: hashlib.sha256(data.encode("utf-8")).hexdigest()
            for name, data in sorted(files.items())
        }
        files["source-manifest.json"] = json.dumps({
            "schema_version": "glaciereq.repo-foundry.source-manifest.v1",
            "status": "GENERATED_UNVERIFIED",
            "files_sha256": digests,
        }, sort_keys=True, indent=2) + "\n"
        for name, data in files.items():
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(data, encoding="utf-8")
        return root

    return publish_domain(output_root, repo, render)
