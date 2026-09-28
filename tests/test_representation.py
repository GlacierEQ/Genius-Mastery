"""Regression tests for executable dynamic-adjustment doctrine."""
import json
import subprocess
import sys

from genius.instruction_engineering import compile_instruction_contract
from genius.representation import (
    compile_representation_contract,
    validate_representation_contract,
)


def test_aspiration_stays_labeled_and_cannot_be_promoted_by_rendering():
    contract = compile_representation_contract(
        "Autonomously closes every legal case.",
        maturity="aspirational",
        next_actor="person",
        purpose="orientation",
    )
    assert contract["truth"]["maturity"] == "aspirational"
    assert contract["projection"]["claim_label"] == "ASPIRATIONAL"
    assert contract["projection"]["preferred_pillar"] == "orientation"
    assert validate_representation_contract(contract) == []


def test_verified_claim_requires_source_bearing_evidence():
    contract = compile_representation_contract(
        "Provider write succeeded.",
        maturity="verified",
        next_actor="expert",
        purpose="evaluation",
    )
    assert "verified maturity requires at least one evidence_ref" in validate_representation_contract(contract)


def test_demonstrated_claim_requires_execution_receipt():
    contract = compile_representation_contract(
        "The command executed successfully.",
        maturity="demonstrated",
        evidence_refs=["src:test"],
        next_actor="expert",
        purpose="evaluation",
    )
    assert "demonstrated maturity requires at least one execution_ref" in validate_representation_contract(contract)


def test_machine_actor_selects_machine_contract_without_changing_truth():
    contract = compile_representation_contract(
        "Connector supports structured invocation.",
        maturity="designed_for",
        next_actor="machine",
        purpose="integration",
        system_state="planned",
    )
    assert contract["projection"]["preferred_pillar"] == "machine_contract"
    assert contract["projection"]["claim_label"] == "DESIGNED FOR"
    assert contract["truth"]["maturity"] == "designed_for"


def test_high_impact_external_action_requires_trusted_host_authorization():
    contract = compile_representation_contract(
        "Send an external filing.",
        maturity="verified",
        evidence_refs=["receipt:reviewed-draft"],
        next_actor="machine",
        purpose="operation",
        impact="high",
        reversibility="hard_to_reverse",
        external_action=True,
    )
    gate = contract["action_gate"]
    assert gate["requires_host_authorization"] is True
    assert gate["representation_can_authorize"] is False
    assert gate["execution_eligible"] is False


def test_weak_evidence_and_high_impact_force_strict_verification_projection():
    contract = compile_representation_contract(
        "Potentially consequential claim.",
        maturity="unknown",
        next_actor="expert",
        purpose="evaluation",
        impact="critical",
        evidence_quality="weak",
    )
    assert contract["projection"]["verification_intensity"] == "strict"
    assert contract["projection"]["restraint"] == "high"


def test_instruction_compiler_inherits_representation_integrity_policy():
    contract = compile_instruction_contract(
        "Evaluate a capability without overstating it.",
        instructions=["Preserve evidence boundaries."],
        output_contract=["Return the conclusion and maturity state."],
        verification=["Check every promoted claim against source-bearing evidence."],
    )
    policy = contract["representation_policy"]
    assert policy["truth_state_locked"] is True
    assert policy["authorization_source"] == "trusted-host-only"
    assert "Aspiration is never silently promoted" in contract["compiled_prompt"]


def test_cli_represent_emits_machine_readable_contract_and_refuses_false_verification():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "genius.cli",
            "represent",
            "--statement",
            "Provider write succeeded.",
            "--maturity",
            "verified",
            "--next-actor",
            "expert",
            "--purpose",
            "evaluation",
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["integrity"]["clean"] is False
    assert "verified maturity requires at least one evidence_ref" in payload["integrity"]["errors"]
