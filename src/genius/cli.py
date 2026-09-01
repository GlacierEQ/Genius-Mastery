"""genius CLI entry point."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from genius import __version__
from genius.doctor import doctor_report
from genius.naming import genius_name
from genius.scaffold import create_domain
from genius.synthesize import synthesize_role
from genius.validate import validate_repo
from genius.impact import impact_report
from genius.discovery import full_discovery_report
from genius.migration import migrate_genius_repo
from genius.performance import benchmark_synthesis, benchmark_validate, performance_report
from genius.challenge import generate_challenges, challenge_report
import yaml


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
            mega_skills_root=(
                Path(args.mega_skills_root).resolve()
                if args.mega_skills_root
                else None
            ),
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


def cmd_impact(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    graph_path = root / "capabilities" / "GRAPH.yaml"
    if not graph_path.exists():
        print(f"Error: No GRAPH.yaml at {graph_path}")
        return 1
    with graph_path.open("r", encoding="utf-8") as f:
        graph = yaml.safe_load(f) or {}
    print(impact_report(graph))
    return 0


def cmd_discover(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    report = full_discovery_report(root)
    for category, items in report.items():
        print(f"=== {category.upper()} ===")
        for item in items:
            print(f"  {item['name']} ({item['version']}) - {item['notes']}")
    return 0


def cmd_migrate(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    receipt = migrate_genius_repo(root)
    print("Migration Receipt:")
    for k, v in receipt.items():
        print(f"  {k}: {v}")
    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    print("Benchmarking...")
    r1 = benchmark_synthesis("TestRole", "TestOutcome", 5)
    r2 = benchmark_validate(root, 5)
    print(performance_report([r1, r2]))
    return 0


def cmd_challenge(args: argparse.Namespace) -> int:
    challenges = generate_challenges(args.role, [args.outcome], {})
    for c in challenges:
        print(f"Challenge ID: {c['id']}")
        print(f"Question: {c['question']}")
        print(f"Hint: {c['hint']}\n")
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

    p_new = sub.add_parser(
        "new",
        help="Create a bare Genius-{purpose} domain scaffold",
    )
    p_new.add_argument("purpose", help="e.g. Code | 'Distributed Systems'")
    p_new.add_argument(
        "--dest",
        default=".",
        help="Parent directory for the new repo (default: cwd)",
    )
    p_new.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing non-empty directory",
    )
    p_new.set_defaults(func=cmd_new)

    p_syn = sub.add_parser(
        "synthesize",
        help="Forge a Genius entity from a role title and desired outcomes",
    )
    p_syn.add_argument("role", help="Job title or entity purpose, e.g. Researcher")
    p_syn.add_argument(
        "--outcome",
        action="append",
        required=True,
        help="Desired outcome or directional archetype. Repeat for multiple outcomes.",
    )
    p_syn.add_argument(
        "--archetype",
        default=None,
        help="Optional explicit directional archetype/persona reference.",
    )
    p_syn.add_argument(
        "--constraint",
        action="append",
        default=[],
        help="Optional constraint. Repeat as needed.",
    )
    p_syn.add_argument(
        "--mega-skills-root",
        default=None,
        help="Optional local GlacierEQ/mega-skills checkout for real capability matching.",
    )
    p_syn.add_argument(
        "--dest",
        default=".",
        help="Parent directory for the generated repo (default: cwd)",
    )
    p_syn.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing non-empty directory",
    )
    p_syn.set_defaults(func=cmd_synthesize)

    p_imp = sub.add_parser("impact", help="Rank bottlenecks")
    p_imp.add_argument("path", nargs="?", default=".")
    p_imp.set_defaults(func=cmd_impact)

    p_disc = sub.add_parser("discover", help="Discover live capabilities")
    p_disc.add_argument("path", nargs="?", default=".")
    p_disc.set_defaults(func=cmd_discover)

    p_mig = sub.add_parser("migrate", help="Migrate repo to current version")
    p_mig.add_argument("path", nargs="?", default=".")
    p_mig.set_defaults(func=cmd_migrate)

    p_bench = sub.add_parser("benchmark", help="Benchmark performance")
    p_bench.add_argument("path", nargs="?", default=".")
    p_bench.set_defaults(func=cmd_benchmark)

    p_chal = sub.add_parser("challenge", help="Generate challenges")
    p_chal.add_argument("role")
    p_chal.add_argument("outcome")
    p_chal.set_defaults(func=cmd_challenge)


    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
