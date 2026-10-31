"""Genius Repository Foundry: independent Python product profile.

This compiles one explicitly supported product profile, not arbitrary objectives.
Generated projects have no Genius-Mastery runtime dependency.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from genius.naming import genius_name
from genius.lineage.publication import publish_domain

MISSION_SCHEMA = "glaciereq.repo-foundry.mission.v1"
PROFILE = "python-text-audit"

_APP = '''"""Unicode text statistics with an independent CLI."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

_WORD = re.compile(r"[^\\W_]+(?:['’][^\\W_]+)*", flags=re.UNICODE)


def analyze_text(text: str, top: int = 10) -> dict:
    """Return Unicode-aware, casefolded frequencies and stable statistics."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if type(top) is not int or not 1 <= top <= 100:
        raise ValueError("top must be an integer from 1 to 100")
    words = [match.group().casefold() for match in _WORD.finditer(text)]
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top]
    return {
        "characters": len(text),
        "lines": len(text.splitlines()),
        "words": len(words),
        "unique_words": len(counts),
        "top_words": [{"word": word, "count": count} for word, count in ranked],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Unicode text statistics (files or stdin).")
    parser.add_argument("file", nargs="?", default="-", help="UTF-8 input or - for stdin")
    parser.add_argument("--top", type=int, default=10, help="Top 1-100 frequent tokens")
    parser.add_argument("--json", action="store_true", help="Print deterministic JSON")
    args = parser.parse_args(argv)
    if not 1 <= args.top <= 100:
        parser.error("--top must be 1 through 100")
    try:
        text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"text-audit: {error}", file=sys.stderr)
        return 1
    result = analyze_text(text, args.top)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"Lines: {result['lines']} | Words: {result['words']} | "
              f"Unique: {result['unique_words']} | Characters: {result['characters']}")
        for row in result["top_words"]:
            print(f"{row['word']}: {row['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

_TESTS = '''"""Independent native tests for the generated application."""
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
app = importlib.import_module("__MODULE__.app")


class ProductTests(unittest.TestCase):
    def test_unicode_and_order(self):
        result = app.analyze_text("Hawaiʻi HAWAIʻI\\nhello hello\\n")
        self.assertEqual(result["words"], 4)
        self.assertEqual(result["lines"], 2)
        self.assertEqual(result["top_words"], [{"word": "hawaiʻi", "count": 2}, {"word": "hello", "count": 2}])

    def test_empty_and_bounds(self):
        self.assertEqual(app.analyze_text("")["words"], 0)
        self.assertEqual(app.analyze_text("")["lines"], 0)
        for limit in (0, 101, True):
            with self.assertRaises(ValueError):
                app.analyze_text("text", limit)

    def test_stdin_cli_json(self):
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        proc = subprocess.run([sys.executable, "-m", "__MODULE__", "--json"],
                              input="One one two", capture_output=True, text=True,
                              cwd=ROOT, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["words"], 3)
        self.assertEqual(report["top_words"][0], {"word": "one", "count": 2})

    def test_missing_file_fails(self):
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        proc = subprocess.run([sys.executable, "-m", "__MODULE__", "not-found-9876.txt"],
                              capture_output=True, text=True, cwd=ROOT, env=env)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("text-audit:", proc.stderr)
'''

_CI = '''name: Native Python product tests
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: PYTHONPATH=src python -m unittest discover -s tests -v
      - run: python -m compileall -q src
'''

_LICENSE = '''MIT License

Copyright (c) 2026 GlacierEQ contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


def generate_python_text_audit(objective: str, name: str, output_root: Path | str | None = None) -> Path:
    """Generate a working Python text-audit application without teacher imports."""
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("nonempty original objective required")
    if len(objective) > 20_000:
        raise ValueError("objective exceeds 20,000 characters")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("nonempty project name required")
    repo = genius_name(name)
    module = re.sub(r"[^a-z0-9_]", "_", repo.lower().replace("-", "_"))
    package = repo.lower()
    mission = {
        "schema_version": MISSION_SCHEMA,
        "mode": "NEW", "original_objective": objective,
        "project": repo, "profile": PROFILE,
        "implemented_behavior": ["UTF-8 file and stdin input", "Unicode word frequency and text counts",
                                 "JSON/human-readable output", "deterministic ranking"],
        "unverified_requirements": "This profile does not establish arbitrary objective satisfaction.",
        "status": "GENERATED_UNVERIFIED",
        "acceptance_command": "PYTHONPATH=src python -m unittest discover -s tests -v",
    }

    def render(staging: Path) -> Path:
        root = staging / repo
        files = {
            "mission.json": json.dumps(mission, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            f"src/{module}/__init__.py": "from .app import analyze_text\n",
            f"src/{module}/__main__.py": "from .app import main\n\nraise SystemExit(main())\n",
            f"src/{module}/app.py": _APP,
            "tests/test_text_audit.py": _TESTS.replace("__MODULE__", module),
            ".github/workflows/test.yml": _CI,
            ".gitignore": "__pycache__/\n*.pyc\n.venv/\ndist/\n*.egg-info/\n",
            "LICENSE": _LICENSE,
            "pyproject.toml": (
                "[build-system]\nrequires = [\"setuptools>=68\"]\n"
                "build-backend = \"setuptools.build_meta\"\n\n"
                f"[project]\nname = \"{package}\"\nversion = \"0.1.0\"\n"
                "description = \"Deterministic Unicode text statistics CLI\"\n"
                "requires-python = \">=3.10\"\ndependencies = []\n\n"
                f"[project.scripts]\ntext-audit = \"{module}.app:main\"\n\n"
                "[tool.setuptools.packages.find]\nwhere = [\"src\"]\n"
            ),
            "README.md": (
                f"# {repo}\n\nFunctional Python text-analysis CLI. Original goal in `mission.json`.\n\n"
                "## Clean checkout operation\n\n"
                f"`PYTHONPATH=src python -m {module} --json < sample.txt`\n\n"
                "`PYTHONPATH=src python -m unittest discover -s tests -v`\n\n"
                "Optional installation: `python -m pip install .` and `text-audit --help`.\n\n"
                "Generated code is not automatically tested or deployed. This profile supports text analysis only.\n"
            ),
        }
        checksums = {name: hashlib.sha256(text.encode("utf-8")).hexdigest()
                     for name, text in sorted(files.items())}
        files["source-manifest.json"] = json.dumps({
            "schema_version": "glaciereq.repo-foundry.source-manifest.v1",
            "status": "GENERATED_UNVERIFIED", "files_sha256": checksums,
        }, sort_keys=True, indent=2) + "\n"
        for relative, data in files.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(data, encoding="utf-8")
        return root

    return publish_domain(output_root, repo, render)