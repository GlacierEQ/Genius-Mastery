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

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
