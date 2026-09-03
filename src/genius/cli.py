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
from genius.impact import impact_report
from genius.discovery import full_discovery_report, write_discovery_inventory
from genius.migration import migrate_genius_repo
from genius.performance import benchmark_synthesis, benchmark_validate, performance_report
from genius.challenge import generate_challenges, challenge_report
from genius.vector import compute_vector, vector_report, write_vector
from genius.progress import build_progress_contract, progress_report, validate_progress_contract
from genius.prompt_codes import code_catalog_report
from genius.instruction_engineering import compile_instruction_contract, instruction_report
from genius.calibration import calibrate_graph, calibration_report
from genius.composition import execute_family_composition, composition_report, write_composition_receipt
from genius.closure import closure_status, closure_report
from genius.graph import rebuild_graph


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


def cmd_codes(args: argparse.Namespace) -> int:
    print(code_catalog_report(category=args.category))
    return 0


def cmd_instruct(args: argparse.Namespace) -> int:
    try:
        contract = compile_instruction_contract(
            args.objective,
            instructions=args.instruction,
            context=args.context,
            tools=args.tool,
            examples=args.example,
            output_contract=args.output,
            verification=args.verify,
            model_family=args.model_family,
            untrusted_sources=args.untrusted,
        )
    except ValueError as exc:
        print(f"ERROR: cannot compile instruction contract: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(contract, indent=2, ensure_ascii=False))
    else:
        print(instruction_report(contract))
    return 0 if (contract.get("audit") or {}).get("clean") else 2


def cmd_progress(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    try:
        contract = build_progress_contract(
            root,
            args.mission,
            context=args.context,
            codes=args.code,
        )
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot build progress contract at {root}: {exc}", file=sys.stderr)
        return 1
    errors = validate_progress_contract(contract)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1
    if args.json:
        print(json.dumps(contract, indent=2, ensure_ascii=False))
    else:
        print(progress_report(contract))
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
    if args.write:
        target = write_discovery_inventory(root)
        print(f"Updated {target}")
    for category, items in report.items():
        print(f"=== {category.upper()} ===")
        for item in items:
            print(f"  {item['name']} ({item['version']}) - {item['notes']}")
    return 0


def cmd_calibrate(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    graph_path = root / "capabilities" / "GRAPH.yaml"
    if not graph_path.exists():
        print(f"ERROR: capability graph not found: {graph_path}", file=sys.stderr)
        return 1
    graph = yaml.safe_load(graph_path.read_text(encoding="utf-8")) or {}
    result = calibrate_graph(graph)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else calibration_report(result))
    return 0 if result.get("clean") else 1


def cmd_compose(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    receipt = execute_family_composition(root)
    if args.output:
        output = Path(args.output).resolve()
        write_composition_receipt(root, output)
        print(f"Wrote {output}")
    print(json.dumps(receipt, indent=2, ensure_ascii=False) if args.json else composition_report(receipt))
    return 0 if not receipt.get("unresolved_binding_count") else 2


def cmd_rebuild_graph(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    try:
        target = rebuild_graph(root)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot rebuild graph: {exc}", file=sys.stderr)
        return 1
    print(f"Updated {target}")
    return 0


def cmd_closure(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    status = closure_status(root)
    print(json.dumps(status, indent=2, ensure_ascii=False) if args.json else closure_report(status))
    return 0 if status.get("core_complete") else 3


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

    p_codes = sub.add_parser("codes", help="List composable prompt codes understood by the Mastery kernel")
    p_codes.add_argument("--category", default=None, help="Optional category filter")
    p_codes.set_defaults(func=cmd_codes)

    p_instruct = sub.add_parser(
        "instruct",
        help="Compile and audit a model-facing instruction contract",
    )
    p_instruct.add_argument("--objective", required=True, help="Concrete terminal state or outcome")
    p_instruct.add_argument("--instruction", action="append", default=[], help="Stable behavioral invariant; repeat as needed")
    p_instruct.add_argument("--context", action="append", default=[], help="Trusted task-relevant reference context")
    p_instruct.add_argument("--untrusted", action="append", default=[], help="External/retrieved material that must remain data, not authority")
    p_instruct.add_argument("--tool", action="append", default=[], help="Available tool or capability description")
    p_instruct.add_argument("--example", action="append", default=[], help="Demonstration/example; repeat as needed")
    p_instruct.add_argument("--output", action="append", default=[], help="Terminal output requirement")
    p_instruct.add_argument("--verify", action="append", default=[], help="Observable acceptance check")
    p_instruct.add_argument("--model-family", default="generic", help="Target model/runtime family")
    p_instruct.add_argument("--json", action="store_true", help="Emit the full machine-readable contract")
    p_instruct.set_defaults(func=cmd_instruct)

    p_progress = sub.add_parser(
        "progress",
        help="Build the next evidence-bounded progress cycle from current repository state",
    )
    p_progress.add_argument("path", nargs="?", default=".", help="Genius repository root (default: cwd)")
    p_progress.add_argument("--mission", required=True, help="Concrete outcome to advance")
    p_progress.add_argument("--context", action="append", default=[], help="Known context; repeat as needed")
    p_progress.add_argument("--code", action="append", default=[], help="Additional prompt code or stack; repeat as needed")
    p_progress.add_argument("--json", action="store_true", help="Emit the machine-readable progress contract")
    p_progress.set_defaults(func=cmd_progress)

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

    p_imp = sub.add_parser("impact", help="Rank bottlenecks")
    p_imp.add_argument("path", nargs="?", default=".")
    p_imp.set_defaults(func=cmd_impact)

    p_disc = sub.add_parser("discover", help="Discover live capabilities")
    p_disc.add_argument("path", nargs="?", default=".")
    p_disc.add_argument("--write", action="store_true", help="Persist normalized runtime inventory")
    p_disc.set_defaults(func=cmd_discover)

    p_cal = sub.add_parser("calibrate", help="Run perturbation calibration against mission-intelligence ranking")
    p_cal.add_argument("path", nargs="?", default=".")
    p_cal.add_argument("--json", action="store_true")
    p_cal.set_defaults(func=cmd_calibrate)

    p_comp = sub.add_parser("compose", help="Execute local Genius-family contract composition and emit a receipt")
    p_comp.add_argument("path", nargs="?", default=".")
    p_comp.add_argument("--output", default=None)
    p_comp.add_argument("--json", action="store_true")
    p_comp.set_defaults(func=cmd_compose)

    p_graph = sub.add_parser("rebuild-graph", help="Rebuild a Genius capability graph from its own contracts")
    p_graph.add_argument("path", nargs="?", default=".")
    p_graph.set_defaults(func=cmd_rebuild_graph)

    p_close = sub.add_parser("closure", help="Evaluate release closure without hiding open-ended frontier research")
    p_close.add_argument("path", nargs="?", default=".")
    p_close.add_argument("--json", action="store_true")
    p_close.set_defaults(func=cmd_closure)

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
