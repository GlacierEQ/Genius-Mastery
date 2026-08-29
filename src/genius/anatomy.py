"""Universal kernel-up inspection prompts for synthesized Genius entities.

These prompts do not assert requirements. They force the forge to examine each layer
before deciding whether it matters to the current mission.
"""
from __future__ import annotations

ANATOMY_PROMPTS: dict[str, list[str]] = {
    "reality": [
        "What observable real-world or digital state exists now?",
        "What exact state must become true for the outcome to count?",
        "Which external actors, environments, laws, markets, or systems can change the result?",
    ],
    "physical_substrate": [
        "Which physical devices, sensors, actuators, power sources, or human interfaces are required?",
        "Can a physical limitation invalidate or reroute the mission?",
    ],
    "compute": [
        "What CPU, GPU, RAM, VRAM, storage, bandwidth, latency, and concurrency are needed?",
        "Which compute limit is mission-sensitive rather than merely convenient?",
    ],
    "firmware_kernel_os": [
        "Which firmware, kernel, drivers, permissions, filesystem, network, clock, locale, or OS services matter?",
        "Could a low-level compatibility failure masquerade as a higher-level capability failure?",
    ],
    "runtime": [
        "Which languages, interpreters, compilers, libraries, codecs, browsers, containers, or SDKs are required?",
        "Are versions and runtime dependencies compatible with the intended action?",
    ],
    "code": [
        "What implementation actually performs the capability?",
        "Where are its interfaces, algorithms, tests, configuration, and failure paths?",
    ],
    "training_data": [
        "What training or reference data could materially shape model competence for this role?",
        "What coverage, bias, freshness, provenance, language, or modality gaps matter?",
    ],
    "training_method": [
        "What pretraining, fine-tuning, preference, reasoning, tool-use, multimodal, or domain-specialization methods affect the needed behavior?",
        "Which training assumptions are known versus inferred?",
    ],
    "model": [
        "Which model capabilities are required: reasoning, code, vision, audio, multilingual, long context, tool use, or speed?",
        "What model limitations require routing, another model, or an external tool?",
    ],
    "model_serving": [
        "How is the model loaded, routed, authenticated, scheduled, cached, rate-limited, and observed?",
        "Can serving availability or configuration be separated from underlying model competence?",
    ],
    "identity_persona": [
        "What role, temperament, initiative, skepticism, creativity, precision, and communication stance best serves the outcome?",
        "Which persona traits materially change performance for this mission?",
    ],
    "agent_kernel": [
        "Which operating laws govern truth, evidence, action, continuation, failure, recovery, and improvement?",
        "Which rules preserve safety and integrity without turning optional failures into global vetoes?",
    ],
    "instructions": [
        "Which system, developer, user, project, repository, skill, and tool instructions must reach the entity?",
        "How are conflicts, precedence, persistence, and stale instructions handled?",
    ],
    "context": [
        "What information must be in active context right now?",
        "What can be retrieved on demand instead of consuming permanent context?",
        "What critical context can be lost through truncation, ordering, or summarization?",
    ],
    "representation": [
        "What exists in reality and what representation does the model actually receive?",
        "Where can fields, layout, timing, relationships, bytes, or visual information be lost in projection?",
    ],
    "memory": [
        "What working, episodic, semantic, procedural, project, and persistent memory is needed?",
        "How are memories stored, retrieved, ranked, reconciled, superseded, and verified?",
    ],
    "knowledge": [
        "What facts, concepts, theories, procedures, relationships, precedents, and current information are required?",
        "Which knowledge must carry source, freshness, jurisdiction, confidence, or counterevidence?",
    ],
    "perception": [
        "Which text, visual, audio, video, structured-data, sensor, or UI signals must be perceived?",
        "What preprocessing and interpretation must occur before reasoning is possible?",
    ],
    "multimodal": [
        "Which modalities must be combined rather than analyzed independently?",
        "How are time, space, speaker, page, frame, object, and source relationships aligned?",
    ],
    "language": [
        "Which languages, dialects, terminology, jargon, translation, or cultural context matter?",
        "Can language mismatch become a critical capability dependency?",
    ],
    "reasoning": [
        "Which deductive, inductive, causal, temporal, spatial, mathematical, adversarial, systems, or strategic reasoning is needed?",
        "Which reasoning method should be selected for each subproblem?",
    ],
    "metacognition": [
        "How will the entity notice uncertainty, assumptions, contradiction, incompleteness, or overconfidence?",
        "How will it distinguish inability from insufficient evidence or a failed implementation route?",
    ],
    "planning": [
        "What desired state, prerequisites, dependency graph, sequencing, parallel work, critical path, fallback, and completion criteria exist?",
        "How far must high-level verbs be decomposed before leaves are actually executable?",
    ],
    "skills": [
        "Which atomic procedures already exist and which must be learned or built?",
        "What are each skill's trigger, inputs, effects, validation, failure modes, and substitutes?",
    ],
    "capability_composition": [
        "Which verified skills or capabilities combine into a genuinely stronger higher-order capability?",
        "What emergent integration value exists beyond merely running members in sequence?",
    ],
    "tools": [
        "Which tools exist, are discoverable, callable, authorized, correctly described, and verifiably working?",
        "What is the difference between tool existence, model visibility, selection, invocation, and successful effect?",
    ],
    "apis": [
        "Which endpoints, schemas, credentials, scopes, quotas, pagination, versioning, retries, and idempotency matter?",
        "Where can transport or serialization failure masquerade as application failure?",
    ],
    "connectors_mcp": [
        "Which hosts, clients, servers, sessions, transports, capability negotiations, tools, resources, and prompts are involved?",
        "What does the connector expose to the model versus what the underlying application contains?",
    ],
    "browser_computer_use": [
        "Does the mission require DOM, accessibility-tree, screenshot, keyboard, pointer, scrolling, form, upload, download, or window-state control?",
        "How is each UI action read back and verified?",
    ],
    "files_documents": [
        "Which files, formats, encodings, permissions, parsers, OCR, layout, tables, images, annotations, citations, or metadata matter?",
        "How is source provenance preserved across parsing and transformation?",
    ],
    "artifact_generation": [
        "What content, structure, layout, fonts, images, tables, citations, accessibility, serializer, renderer, and QA are required?",
        "What proves the final artifact is usable rather than merely created?",
    ],
    "communication": [
        "Who must receive what information through which channel, identity, thread, format, and acknowledgement path?",
        "How are tone, attachments, delivery, and response state handled?",
    ],
    "state_persistence": [
        "What mission, workflow, artifact, tool, and environment state must survive between actions or sessions?",
        "What is the exact recovery/resume point after interruption?",
    ],
    "time_events_automation": [
        "Which clocks, timezones, deadlines, freshness rules, schedules, triggers, events, recurrences, and expirations matter?",
        "How are automated effects made idempotent, observable, cancellable, and recoverable?",
    ],
    "swarm_multi_agent": [
        "Would specialization, delegation, critics, verifiers, workers, or parallel agents materially improve the outcome?",
        "How are roles, shared state, disagreement, duplicate work, synthesis, and replacement handled?",
    ],
    "orchestration": [
        "Who or what selects models, agents, tools, connectors, skills, routes, resources, and sequencing?",
        "How does orchestration reroute around local failures while preserving successful work?",
    ],
    "observability": [
        "What logs, traces, metrics, errors, latency, token, cost, resource, retrieval, tool, and result telemetry are needed?",
        "Can the entity explain why performance degraded rather than merely that it did?",
    ],
    "reliability_recovery": [
        "What retries, backoff, failover, alternate providers, checkpoints, backups, rollback, rebuild, resume, and reconciliation exist?",
        "Which failures are scoped and which truly block the exact operation?",
    ],
    "security_integrity": [
        "What authentication, authorization, secrets, encryption, sandboxing, validation, provenance, privacy, and destructive-effect boundaries apply?",
        "How is real security preserved without confusing it with arbitrary project-control friction?",
    ],
    "resource_economics": [
        "What time, compute, tokens, memory, storage, bandwidth, quota, money, energy, and human attention does the route consume?",
        "Which resource improvements materially affect mission outcome?",
    ],
    "human_interaction": [
        "What user intent, accessibility, language, expertise, interruption, approval, correction, trust, and presentation requirements matter?",
        "What changes because of the particular human participating in the system?",
    ],
    "teaching": [
        "Can the entity explain first principles and dependencies rather than only provide an answer?",
        "Can a learner reconstruct the method from a blank state?",
        "Can the learner transfer it to a novel case and teach it onward?",
    ],
    "domain_expertise": [
        "What domain vocabulary, methods, standards, tools, datasets, benchmarks, workflows, practitioners, and failure modes define excellence?",
        "What separates broad competence from frontier mastery in this purpose?",
    ],
    "real_world_effect": [
        "What state outside the model must actually change?",
        "What independent readback proves the intended effect occurred?",
    ],
    "learning_evolution": [
        "What success, failure, correction, benchmark delta, or counterevidence should change future behavior?",
        "Which small improvement has the largest mission sensitivity and downstream capability leverage?",
        "What newly verified capability can now become an input to the next composition?",
    ],
}


def prompts_for(layer: str) -> list[str]:
    """Return a defensive copy of inspection prompts for one anatomy layer."""
    return list(ANATOMY_PROMPTS.get(layer, ()))
