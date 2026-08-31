"""genius CLI entry point."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from genius import __version__
from genius.doctor import doctor_report
from genius.family import analyze_family, family_report
from genius.intelligence import analyze_capability_graph, capability_intelligence_report
from genius.naming import genius_name
from genius.operating_loop import EVIDENCE_STATES, OUTCOME_STATUSES, build_loop, loop_report, validate_loop
from genius.scaffold import create_domain
from genius.synthesize import synthesize_role
from genius.validate import validate_repo
from genius.vector import compute_vector, vector_report, write_vector


def cmd_name(args: argparse.Namespace) -> int:
    print(genius_name(args.purpose))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    errors = validate_repo(root)
    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS — {root}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    print(doctor_report(root))
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    graph_path = target / "capabilities" / "GRAPH.yaml" if target.is_dir() else target
    if not graph_path.exists():
        print(f"ERROR: capability graph not found: {graph_path}", file=sys.stderr)
        return 1
    try:
        graph = yaml.safe_load(graph_path.read_text(encoding="utf-8")) or {}
        analyzed = analyze_capability_graph(graph)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot analyze {graph_path}: {exc}", file=sys.stderr)
        return 1
    if args.write:
        graph_path.write_text(yaml.safe_dump(analyzed, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"Updated {graph_path}")
    print(capability_intelligence_report(analyzed, top=args.top))
    return 0


def cmd_family(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    if not root.exists():
        print(f"ERROR: family root not found: {root}", file=sys.stderr)
        return 1
    try:
        analysis = analyze_family(root)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot analyze Genius family at {root}: {exc}", file=sys.stderr)
        return 1
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(yaml.safe_dump(analysis, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"Wrote {output}")
    print(family_report(analysis, top=args.top))
    return 0


def cmd_vector(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    if not root.exists():
        print(f"ERROR: Genius root not found: {root}", file=sys.stderr)
        return 1
    try:
        vector = compute_vector(root)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot compute mastery vector at {root}: {exc}", file=sys.stderr)
        return 1
    if args.write:
        target = write_vector(root)
        print(f"Updated {target}")
    print(vector_report(vector))
    return 0


def cmd_loop(args: argparse.Namespace) -> int:
    record = build_loop(
        mission=args.mission,
        context=args.context,
        options=args.option,
        impact=args.impact,
        action=args.action,
        outcome=args.outcome,
        evidence_state=args.evidence_state,
        outcome_status=args.outcome_status,
        source_refs=args.source_ref,
        learnings=args.learning,
        strengthened=args.strengthen,
    )
    errors = validate_loop(record)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1
    if args.json:
        print(json.dumps(record, indent=2, ensure_ascii=False))
    else:
        print(loop_report(record))
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    dest = Path(args.dest).resolve()
    try:
        root = create_domain(args.purpose, dest, force=args.force)
    except (ValueError, FileExistsError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"Created {root}")
    print("Next: populate claims/sources, run challenges, emit evidence receipts.")
    return 0


def cmd_synthesize(args: argparse.Namespace) -> int:
    dest = Path(args.dest).resolve()
    try:
        root = synthesize_role(
            args.role,
            list(args.outcome),
            dest,
            archetype=args.archetype,
            constraints=list(args.constraint or []),
            mega_skills_root=Path(args.mega_skills_root).resolve() if args.mega_skills_root else None,
            force=args.force,
        )
    except (ValueError, FileExistsError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"Synthesized {root}")
    print(f"Role: {args.role}")
    print("Outcomes:")
    for outcome in args.outcome:
        print(f"  - {outcome}")
    print("State: mapped hypotheses; research, challenge, execute, verify, teach.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="genius",
        description="Genius-Mastery teacher-forge — create masters, not static examples.",
    )
    parser.add_argument("--version", action="version", version=f"genius {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_name = sub.add_parser("name", help="Normalize purpose → Genius-{Purpose}")
    p_name.add_argument("purpose")
    p_name.set_defaults(func=cmd_name)

    p_val = sub.add_parser("validate", help="Validate GENIUS.yaml + core contracts")
    p_val.add_argument("path", nargs="?", default=".")
    p_val.set_defaults(func=cmd_validate)

    p_doc = sub.add_parser("doctor", help="Diagnostic strength/weakness surface")
    p_doc.add_argument("path", nargs="?", default=".")
    p_doc.set_defaults(func=cmd_doctor)

    p_analyze = sub.add_parser("analyze", help="Rank capability bottlenecks and leverage for the current mission")
    p_analyze.add_argument("path", nargs="?", default=".", help="Genius repo directory or capabilities/GRAPH.yaml path")
    p_analyze.add_argument("--top", type=int, default=10, help="Number of ranked priorities to print (default: 10)")
    p_analyze.add_argument("--write", action="store_true", help="Persist enriched analysis back to GRAPH.yaml")
    p_analyze.set_defaults(func=cmd_analyze)

    p_family = sub.add_parser("family", help="Discover Genius repositories and rank cross-family composition opportunities")
    p_family.add_argument("path", nargs="?", default=".", help="Directory containing Genius-* repositories, or one Genius repo")
    p_family.add_argument("--top", type=int, default=10, help="Number of composition candidates to print (default: 10)")
    p_family.add_argument("--output", default=None, help="Optional YAML path for the full family analysis")
    p_family.set_defaults(func=cmd_family)

    p_vector = sub.add_parser("vector", help="Compute evidence-derived multidimensional mastery state")
    p_vector.add_argument("path", nargs="?", default=".", help="Genius repository root (default: cwd)")
    p_vector.add_argument("--write", action="store_true", help="Persist computed state to mastery/VECTOR.yaml")
    p_vector.set_defaults(func=cmd_vector)

    p_loop = sub.add_parser(
        "loop",
        help="Record a mission-aware decision loop without collapsing retrieval state into truth",
    )
    p_loop.add_argument("--mission", required=True)
    p_loop.add_argument("--context", action="append", default=[])
    p_loop.add_argument("--option", action="append", required=True)
    p_loop.add_argument("--impact", action="append", required=True)
    p_loop.add_argument("--action", required=True)
    p_loop.add_argument("--outcome", default=None)
    p_loop.add_argument("--evidence-state", choices=sorted(EVIDENCE_STATES), default="not_searched")
    p_loop.add_argument("--outcome-status", choices=sorted(OUTCOME_STATUSES), default=None)
    p_loop.add_argument("--source-ref", action="append", default=[])
    p_loop.add_argument("--learning", action="append", default=[])
    p_loop.add_argument("--strengthen", action="append", default=[])
    p_loop.add_argument("--json", action="store_true", help="Emit the machine-readable record")
    p_loop.set_defaults(func=cmd_loop)

    p_new = sub.add_parser("new", help="Create a bare Genius-{purpose} domain scaffold")
    p_new.add_argument("purpose", help="e.g. Code | 'Distributed Systems'")
    p_new.add_argument("--dest", default=".", help="Parent directory for the new repo (default: cwd)")
    p_new.add_argument("--force", action="store_true", help="Allow writing into an existing non-empty directory")
    p_new.set_defaults(func=cmd_new)

    p_syn = sub.add_parser("synthesize", help="Forge a Genius entity from a role title and desired outcomes")
    p_syn.add_argument("role", help="Job title or entity purpose, e.g. Researcher")
    p_syn.add_argument("--outcome", action="append", required=True, help="Desired outcome or directional archetype. Repeat for multiple outcomes.")
    p_syn.add_argument("--archetype", default=None, help="Optional explicit directional archetype/persona reference.")
    p_syn.add_argument("--constraint", action="append", default=[], help="Optional constraint. Repeat as needed.")
    p_syn.add_argument("--mega-skills-root", default=None, help="Optional local GlacierEQ/mega-skills checkout for real capability matching.")
    p_syn.add_argument("--dest", default=".", help="Parent directory for the generated repo (default: cwd)")
    p_syn.add_argument("--force", action="store_true", help="Allow writing into an existing non-empty directory")
    p_syn.set_defaults(func=cmd_synthesize)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
