"""Composable prompt-code language for Genius-Mastery."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class PromptCode:
    name: str
    category: str
    instruction: str
    aliases: tuple[str, ...] = ()


_CODES = (
    PromptCode("ELI5", "explanation", "Explain plainly with concrete examples."),
    PromptCode("TLDR", "explanation", "Lead with the shortest useful summary."),
    PromptCode("DEEP DIVE", "explanation", "Explore the subject comprehensively, including edge cases and implications."),
    PromptCode("FIRST PRINCIPLES", "explanation", "Reduce the problem to fundamental facts, then rebuild the solution."),
    PromptCode("STEP-BY-STEP", "explanation", "Present an ordered sequence of actionable steps or checkpoints."),
    PromptCode("MENTAL MODEL", "explanation", "Teach the reusable model underneath the answer."),
    PromptCode("REASONING SUMMARY", "reasoning", "Expose assumptions, evidence, checks, decision points, and conclusion without requiring private reasoning traces.", aliases=("CHAIN OF THOUGHT", "COT")),
    PromptCode("MULTI-PERSPECTIVE", "reasoning", "Analyze materially different viewpoints."),
    PromptCode("SOCRATIC MODE", "reasoning", "Use targeted questions to develop understanding when dialogue is appropriate."),
    PromptCode("PRE-MORTEM", "reasoning", "Assume failure and identify the most plausible causes."),
    PromptCode("POST-MORTEM", "reasoning", "Analyze outcomes, root causes, contributing factors, and corrective actions."),
    PromptCode("SWOT", "reasoning", "Analyze strengths, weaknesses, opportunities, and threats."),
    PromptCode("TRADEOFFS", "reasoning", "Make competing benefits, costs, risks, and consequences explicit."),
    PromptCode("COUNTERARGUE", "reasoning", "Construct the strongest serious case against the current position."),
    PromptCode("STEELMAN", "reasoning", "Construct the strongest defensible version of the argument before evaluation."),
    PromptCode("RED TEAM", "reasoning", "Actively search for weaknesses, contradictions, failure modes, and blind spots."),
    PromptCode("DEVIL'S ADVOCATE", "reasoning", "Challenge the current conclusion with credible alternatives."),
    PromptCode("SECOND-ORDER", "reasoning", "Analyze downstream consequences and consequences of those consequences."),
    PromptCode("SYSTEMS THINKING", "reasoning", "Analyze dependencies, feedback loops, bottlenecks, incentives, and emergent effects."),
    PromptCode("VERIFY", "quality", "Verify material claims and distinguish confirmed facts from assumptions."),
    PromptCode("SOURCE-FIRST", "quality", "Prefer primary or authoritative sources before interpretation."),
    PromptCode("FACT / INFERENCE / HYPOTHESIS", "quality", "Separate observed facts, reasonable inferences, and unverified hypotheses.", aliases=("FACT-INFERENCE-HYPOTHESIS",)),
    PromptCode("EVIDENCE MATRIX", "quality", "Map claims to supporting evidence, contradiction, confidence, and missing proof."),
    PromptCode("EVAL-SELF", "quality", "Check the proposed answer for errors, omissions, weak assumptions, and improvements before finalizing."),
    PromptCode("CONTRADICTION CHECK", "quality", "Search specifically for internal inconsistencies and conflicts with evidence."),
    PromptCode("EDGE CASES", "quality", "Identify boundary conditions, exceptions, and unusual failure states."),
    PromptCode("CONFIDENCE", "quality", "State confidence for material conclusions and what would change it."),
    PromptCode("ASSUMPTIONS", "quality", "Surface material assumptions the result depends on."),
    PromptCode("EXECUTE", "execution", "Use available tools and take the requested action instead of only describing it."),
    PromptCode("TOOL-FIRST", "execution", "Inspect applicable tools, connectors, files, repos, and live state before guessing."),
    PromptCode("BUILD", "execution", "Produce the implementation or artifact, not only architecture or advice."),
    PromptCode("FIX", "execution", "Diagnose, repair, test, and verify the resulting state."),
    PromptCode("CONTINUE", "execution", "Recover the last valid state and advance it rather than restarting."),
    PromptCode("MAXIMUM ADVANCE", "execution", "Advance the strongest coherent reversible increment rather than a token minimum."),
    PromptCode("PRODUCTION-GRADE", "execution", "Optimize for correctness, reliability, security, observability, maintainability, and recovery."),
    PromptCode("READBACK", "execution", "Inspect the resulting state after mutation and report what actually became true."),
    PromptCode("TEST", "execution", "Validate behavior at the appropriate layer with meaningful tests."),
    PromptCode("SHIP", "execution", "Complete implementation, verification, and deployable delivery."),
    PromptCode("PRIORITIZE", "strategy", "Rank options by leverage, impact, urgency, dependencies, risk, and cost."),
    PromptCode("80/20", "strategy", "Identify the smallest set of actions producing most of the desired result."),
    PromptCode("LEVERAGE", "strategy", "Find actions that unlock disproportionate downstream capability."),
    PromptCode("BOTTLENECK", "strategy", "Find the constraint currently limiting the system."),
    PromptCode("NEXT BEST ACTION", "strategy", "Select the highest-value executable action from current state."),
    PromptCode("DECISION MATRIX", "strategy", "Compare alternatives against explicit criteria."),
    PromptCode("SCENARIO PLAN", "strategy", "Prepare responses for multiple plausible future conditions."),
    PromptCode("WAR GAME", "strategy", "Model moves, countermoves, escalation paths, and strategic responses."),
    PromptCode("ARCHITECT", "engineering", "Design the system, interfaces, state flows, dependencies, and operational boundaries."),
    PromptCode("CODE REVIEW", "engineering", "Review correctness, maintainability, security, performance, and architecture."),
    PromptCode("DEBUG", "engineering", "Trace symptoms to root cause and repair the defect."),
    PromptCode("SECURITY REVIEW", "engineering", "Analyze trust boundaries, permissions, attack surfaces, secrets, abuse cases, and mitigations."),
    PromptCode("PERFORMANCE", "engineering", "Find computational, I/O, database, network, concurrency, and architectural bottlenecks."),
    PromptCode("REFACTOR", "engineering", "Improve structure while preserving or increasing functionality."),
    PromptCode("INTEGRATE", "engineering", "Connect existing components into a coherent operational system."),
    PromptCode("HARDEN", "engineering", "Increase reliability, security, fault tolerance, validation, recovery, and observability."),
    PromptCode("BENCHMARK", "engineering", "Define measurable criteria and compare implementations empirically."),
    PromptCode("HUMANIZE", "style", "Use natural, direct, readable language."),
    PromptCode("JARGONIZE", "style", "Use precise professional or domain-specific terminology."),
    PromptCode("EXECUTIVE", "style", "Write for a decision-maker: conclusion, impact, risk, and recommendation."),
    PromptCode("TECHNICAL", "style", "Use implementation-level precision for an expert audience."),
    PromptCode("NO-FLUFF", "style", "Remove filler, repetition, and ceremonial commentary."),
    PromptCode("DENSE", "style", "Maximize useful information density without sacrificing clarity."),
    PromptCode("TEACH", "style", "Explain so the reader can independently apply the concept."),
    PromptCode("TABLE", "output", "Prefer a structured comparison table when appropriate."),
    PromptCode("CHECKLIST", "output", "Convert the result into executable checks."),
    PromptCode("PLAYBOOK", "output", "Produce triggers, actions, verification, and recovery steps."),
    PromptCode("BLUEPRINT", "output", "Produce a complete architecture or implementation design."),
    PromptCode("MATRIX", "output", "Represent relationships across multiple dimensions."),
    PromptCode("TIMELINE", "output", "Organize events or actions chronologically."),
    PromptCode("TREE", "output", "Represent the problem hierarchically."),
    PromptCode("ONE-PAGER", "output", "Compress the result into a high-density single-page structure."),
    PromptCode("FULL FIELD", "modifier", "Do not prematurely prune plausible options; surface and rank the relevant field."),
    PromptCode("RANKED", "modifier", "Order findings strongest or highest-value first."),
    PromptCode("NO ASSUMPTIONS", "modifier", "Retrieve or verify wherever practical instead of silently guessing."),
    PromptCode("PRESERVE GAINS", "modifier", "Keep validated existing capability unless replacement is demonstrably stronger."),
    PromptCode("COMPOSE", "modifier", "Combine existing capabilities where their interaction creates additional value."),
    PromptCode("DURABLE", "modifier", "Prefer persistent state changes in the appropriate durable system."),
    PromptCode("RECEIPTS", "modifier", "Bind execution claims to inspectable evidence."),
    PromptCode("MAXIMUM", "modifier", "Optimize for the strongest coherent result within real constraints."),
    PromptCode("PROGRESS", "orchestration", "Convert current state into a measurably stronger verified state: recover, prioritize, act, persist, verify, and compound."),
)

CODE_REGISTRY = {code.name: code for code in _CODES}
_ALIAS_TO_NAME = {alias: code.name for code in _CODES for alias in (code.name, *code.aliases)}

DEFAULT_PROGRESS_CODES = (
    "PROGRESS",
    "CONTINUE",
    "TOOL-FIRST",
    "NEXT BEST ACTION",
    "MAXIMUM ADVANCE",
    "EXECUTE",
    "DURABLE",
    "TEST",
    "READBACK",
    "RECEIPTS",
    "PRESERVE GAINS",
)


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip().upper().replace("_", " "))


def canonical_code(value: str) -> str:
    cleaned = _clean(value)
    try:
        return _ALIAS_TO_NAME[cleaned]
    except KeyError as exc:
        raise ValueError(f"unknown prompt code: {value!r}") from exc


def _expand_one(value: str) -> list[str]:
    cleaned = _clean(value)
    if cleaned in _ALIAS_TO_NAME:
        return [cleaned]
    if "+" in cleaned:
        return [part.strip() for part in cleaned.split("+") if part.strip()]
    if "/" in cleaned:
        return [part.strip() for part in cleaned.split("/") if part.strip()]
    return [cleaned]


def normalize_codes(codes: Iterable[str] | None, *, progress_defaults: bool = False) -> list[str]:
    ordered: list[str] = []
    raw_values: list[str] = list(DEFAULT_PROGRESS_CODES if progress_defaults else ())
    raw_values.extend(str(code) for code in (codes or []))
    for raw in raw_values:
        for token in _expand_one(raw):
            canonical = canonical_code(token)
            if canonical not in ordered:
                ordered.append(canonical)
    return ordered


def parse_coded_prompt(prompt: str) -> tuple[list[str], str]:
    text = str(prompt).strip()
    prefix, separator, body = text.partition(":")
    if not separator:
        return [], text
    try:
        codes = normalize_codes([prefix])
    except ValueError:
        return [], text
    return codes, body.strip()


def code_catalog(*, category: str | None = None) -> list[PromptCode]:
    if category is None:
        return list(_CODES)
    wanted = str(category).strip().casefold()
    return [code for code in _CODES if code.category.casefold() == wanted]


def code_catalog_report(*, category: str | None = None) -> str:
    rows = code_catalog(category=category)
    if not rows:
        return f"No prompt codes found for category {category!r}."
    lines: list[str] = []
    current = None
    for code in rows:
        if code.category != current:
            current = code.category
            lines.append(f"[{current}]")
        aliases = f" (aliases: {', '.join(code.aliases)})" if code.aliases else ""
        lines.append(f"{code.name}{aliases} — {code.instruction}")
    return "\n".join(lines)
