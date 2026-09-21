from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "epistemology.json"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_aspen_grove_model_preserves_domain_locality():
    epistemology = load_contract()
    assert epistemology["model"] == "ASPEN_GROVE"
    locality = epistemology["domain_locality"]
    assert locality["substantive_knowledge_domain_local_by_default"] is True
    assert locality["domain_identity_merge_by_composition"] is False
    assert locality["law"] == "SHARED_ROOTS_INDEPENDENT_TRUNKS_COMPOSABLE_BRANCHES"


def test_context_hydration_precedes_interpretation():
    hydration = load_contract()["context_hydration"]
    assert hydration["required_before_interpretation"] is True
    assert hydration["silent_prompt_only_fallback_forbidden"] is True
    assert hydration["search_hit_alone_is_not_hydration"] is True
    assert set(hydration["statuses"]) == {"VERIFIED", "PARTIAL", "UNAVAILABLE"}


def test_evidence_and_execution_axes_do_not_collapse():
    axes = load_contract()["axes"]
    assert axes["one_axis_may_not_imply_the_other"] is True
    assert "VERIFIED" in axes["evidence"]
    assert "EFFECT_VERIFIED" in axes["execution"]
    assert axes["evidence"] != axes["execution"]


def test_cross_domain_composition_is_typed_not_identity_merge():
    bridge = load_contract()["cross_domain_bridge"]
    assert bridge["typed_relation_required"] is True
    assert bridge["composition_may_create_higher_order_capability"] is True
    assert bridge["composition_may_not_merge_domain_identity"] is True
    assert bridge["donor_verification_does_not_auto_transfer"] is True
    required = set(bridge["required_fields"])
    assert {"donor_domain", "consumer_domain", "relation_type", "provenance"} <= required


def test_epistemic_promotion_law_prevents_common_inversions():
    law = load_contract()["promotion_law"]
    assert law["rhetoric_cannot_promote_state"] is True
    assert law["representation_is_not_reality"] is True
    assert law["retrieval_is_not_proof"] is True
    assert law["execution_is_not_verification"] is True
    assert law["verification_is_not_universal_truth"] is True
