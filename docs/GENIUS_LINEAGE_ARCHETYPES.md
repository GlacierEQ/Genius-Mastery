# Genius Lineage Archetypes

## 1. Architectural Philosophy: The Universal Pillar Invariant

The **Universal Pillar Invariant** establishes that:
> *High-order systems ("pillars") must be assembled from strictly decoupled, universal atomic pieces that function independently anywhere in the estate. No archetype couples to or depends on another archetype.*

Rather than constructing an unmaintainable, tangled monolith of disparate capabilities, the Genius Lineage establishes **26 specialized, atomic domain archetypes**. Each archetype possesses:
1. **First-Principles Invariants:** Concrete physical, mathematical, or systemic laws that govern the domain without exception.
2. **Granular Capability Targets:** Explicit, testable actions and computational models.
3. **Domain-Native Tools & APIs:** Essential interfaces required for the domain.
4. **Verification Gates:** Verifiable acceptance tests that must pass before any mastery claim is recognized.
5. **Teaching Transfer Challenges:** Concrete problems requiring the synthesized entity to independently reconstruct and transfer its methods to another agent without external scaffolding.

---

## 2. The 26 Canonical Archetypes by Domain

### A. Deep Frontier Science & AI
1. **Genius-Aerospace (`aerospace`)**
   - *Invariants:*
     - Tsiolkovsky Rocket Equation: $\Delta v = I_{sp} \cdot g_0 \cdot \ln(m_0 / m_f)$
     - Vis-viva Orbital Energy Conservation: $v^2 = \mu (2/r - 1/a)$
     - Kepler's Third Law: $T^2 = 4\pi^2 a^3 / \mu$
     - Propellant Boil-Off Mass Conservation: $dm/dt = -\dot{Q}_{leak} / \Delta H_{vap}$
   - *Tools:* `telemetry_stream_ingest`, `orbital_propagator`, `delta_v_budget_calculator`, `conjunction_assessor`
   - *Verification Gate:* Delta-v budget closure within 0.1% margin; zero keep-out ellipsoid collisions.

2. **Genius-Nanosphere (`nanosphere`)**
   - *Invariants:*
     - Lennard-Jones Potential: $V_{LJ}(r) = 4\epsilon [(\sigma/r)^{12} - (\sigma/r)^6]$
     - de Broglie Wavelength: $\lambda = h / p$
     - Quantum Confinement Bandgap Shift: $\Delta E = \hbar^2 \pi^2 / (2 m^* d^2)$
   - *Tools:* `molecular_lattice_simulator`, `atomic_force_analyzer`, `quantum_confinement_solver`
   - *Verification Gate:* NVE microcanonical energy conservation; surface defect density < 1 ppb.

3. **Genius-Physics (`physics`)**
   - *Invariants:*
     - Noether's Theorem: Continuous symmetries correspond to conserved currents.
     - Principle of Stationary Action: $\frac{d}{dt}\frac{\partial L}{\partial \dot{q}} - \frac{\partial L}{\partial q} = 0$
     - Liouville's Phase-Space Incompressibility.
     - Relativistic Invariance: $s^2 = c^2 \Delta t^2 - \Delta x^2 - \Delta y^2 - \Delta z^2$
   - *Tools:* `symplectic_integrator`, `field_tensor_calculator`, `geodesic_integrator`
   - *Verification Gate:* Symplectic volume preserved to machine precision; gauge invariance preserved.

4. **Genius-Chemistry (`chemistry`)**
   - *Invariants:*
     - Mass and Stoichiometric Balance across all reaction equations.
     - Gibbs Free Energy Spontaneity: $\Delta G = \Delta H - T\Delta S < 0$
     - Arrhenius Kinetics: $k = A \exp(-E_a / (RT))$
     - Le Chatelier Equilibrium: $K_{eq} = \prod [P]^p / \prod [R]^r$
   - *Tools:* `stoichiometry_balancer`, `kinetics_ode_solver`, `spectroscopy_analyzer`
   - *Verification Gate:* Atom count strictly conserved; equilibrium constants satisfy van 't Hoff.

5. **Genius-Biology (`biology`)**
   - *Invariants:*
     - Central Dogma of Molecular Biology: DNA $\to$ RNA $\to$ Protein.
     - Michaelis-Menten Kinetics: $v = V_{max} [S] / (K_m + [S])$
     - Hardy-Weinberg Equilibrium: $p^2 + 2pq + q^2 = 1$
     - Reading Frame Triplet Preservation.
   - *Tools:* `sequence_aligner`, `protein_conformation_evaluator`, `metabolic_flux_solver`
   - *Verification Gate:* Optimal Smith-Waterman matrix scores; steady-state metabolic flux $S \cdot v = 0$.

6. **Genius-ModelWeights (`model-weights`)**
   - *Invariants:*
     - Quantization Scale/Zero-Point: $x_q = \text{clip}(\text{round}(x / S) + Z, q_{min}, q_{max})$
     - Rotary Position Embedding (RoPE) Unitary Inner Product Invariance.
     - KV-Cache Upper Bound: $M_{kv} = 2 \cdot \text{layers} \cdot \text{heads} \cdot d_{head} \cdot s \cdot \text{bytes}$
   - *Tools:* `quantization_engine`, `rope_rotator`, `kv_cache_paged_allocator`, `tensor_shard_calculator`
   - *Verification Gate:* Perplexity delta < 0.15 vs FP16 baseline; zero fragmentation in paged KV cache.

---

### B. Systems & Hardware Architecture
7. **Genius-Microcode (`microcode`)**
   - *Invariants:*
     - Instruction Decode Determinism: 1:1 or 1:N micro-op decomposition.
     - Pipeline Hazard Interlocking: Zero un-interlocked RAW, WAR, or WAW hazards.
     - Cache Line Alignment: 64-byte boundary preservation to avoid false sharing.
   - *Tools:* `disassembler_stream`, `ebpf_verifier_check`, `register_liveness_analyzer`, `cycle_accurate_profiler`
   - *Verification Gate:* Bounded stack proof (<512 bytes) in eBPF; zero false-sharing cache bouncing.

8. **Genius-Filesystem (`filesystem`)**
   - *Invariants:*
     - POSIX Atomic Rename: `rename(old, new)` is atomic and never yields intermediate half-states.
     - Write-Ahead Logging (WAL) Crash Consistency: Log sync strictly precedes block write.
     - Inode Reference Counting: Block deallocated if and only if link count = 0.
   - *Tools:* `atomic_file_writer`, `wal_journal_replayer`, `extent_allocator`, `fsync_barrier_checker`
   - *Verification Gate:* Clean recovery from sudden simulated power-off; zero file descriptor leaks.

9. **Genius-CloudDatabase (`cloud-database`)**
   - *Invariants:*
     - CAP Theorem Formal Trade-off Bounds.
     - Snapshot Isolation / Serializability: Zero dirty reads or phantom reads.
     - Raft / Paxos Quorum Consensus: Monotonically increasing replication index.
   - *Tools:* `raft_consensus_engine`, `mvcc_storage_engine`, `consistent_hash_ring`, `lsm_compactor`
   - *Verification Gate:* Zero split-brain states under simulated partition; serializable correctness.

10. **Genius-Device (`device`)**
    - *Invariants:*
      - Volatile MMIO Semantics: Register reads/writes never eliminated by compiler optimization.
      - Non-blocking ISR Top/Bottom Half Latency Budget.
      - DMA Cache Coherency Flush & Invalidation.
    - *Tools:* `mmio_register_map`, `uart_spi_protocol_analyzer`, `dma_ring_buffer`, `watchdog_monitor`
    - *Verification Gate:* ISR latency < 10 microseconds; zero volatile register optimization elisions.

11. **Genius-PC (`pc`)**
    - *Invariants:*
      - x86_64 4-Level / 5-Level Page Translation (PML4 $\to$ PDPT $\to$ PD $\to$ PT).
      - ACPI Power States (S0 through S5).
      - UEFI Authenticode Cryptographic Signature Verification.
    - *Tools:* `uefi_boot_checker`, `x86_page_table_builder`, `acpi_aml_parser`, `pcie_enumerator`
    - *Verification Gate:* Secure Boot key database validation; triple-fault-free SMP initialization.

12. **Genius-Mac (`mac`)**
    - *Invariants:*
      - Mach Port IPC Capabilities & Rights Enforcement.
      - Apple Silicon Unified Memory Zero-Copy Coherency.
      - Notarized Code Signing & Hardened Runtime.
    - *Tools:* `mach_port_inspector`, `metal_compute_profiler`, `codesign_entitlements_auditor`
    - *Verification Gate:* Zero Mach port leaks across 10,000 IPC calls; `codesign --deep --strict` PASS.

13. **Genius-Linux (`linux`)**
    - *Invariants:*
      - Uniform VFS Abstraction: Everything is a file descriptor.
      - cgroups v2 Unified Resource Hierarchy.
      - io_uring Submission Queue (SQ) and Completion Queue (CQ) Memory Barriers.
    - *Tools:* `io_uring_bench`, `cgroups_controller`, `ebpf_trace_loader`, `namespace_isolator`
    - *Verification Gate:* io_uring throughput $\ge$ 2x epoll with 0 dropped CQEs; namespace isolation verified.

14. **Genius-Android (`android`)**
    - *Invariants:*
      - Binder IPC Flat Object Serialization & UID Sandboxing.
      - ART DEX Bytecode Verification.
      - Android HAL AIDL Version Compatibility.
    - *Tools:* `binder_tracer`, `jni_bridge_validator`, `apk_manifest_auditor`, `vsync_profiler`
    - *Verification Gate:* Binder parcel round-trip with zero memory leak; JNI local table overflow = 0.

15. **Genius-iOS (`ios`)**
    - *Invariants:*
      - Swift Exclusive Memory Access & Thread Safety.
      - ARM64e Pointer Authentication (PAC).
      - CoreAnimation 120Hz Frame Budget (< 8.33 ms).
    - *Tools:* `swift_actor_checker`, `core_animation_budgeter`, `secure_enclave_keychain`, `sandbox_auditor`
    - *Verification Gate:* Zero data races under Swift strict concurrency; zero dropped UI frames.

16. **Genius-Email (`email`)**
    - *Invariants:*
      - RFC 5322 MIME Grammar Compliance.
      - RFC 6376 DKIM Canonicalization & Cryptographic Verification.
      - RFC 7208 SPF & RFC 7489 DMARC Alignment.
    - *Tools:* `mime_parser`, `dkim_signer_verifier`, `spf_evaluator`, `smtp_state_machine`
    - *Verification Gate:* CRLF header injection prevention; DKIM signature PASS on test vectors.

17. **Genius-Automation (`automation`)**
    - *Invariants:*
      - Idempotency Invariant: $f(f(x)) = f(x)$.
      - Exponential Backoff with Full Jitter: $t = \text{random}(0, \min(t_{max}, t_{base} \cdot 2^{attempt}))$.
      - Compensating Transaction Rollback in Reverse Order.
    - *Tools:* `fsm_engine`, `idempotency_ledger`, `saga_coordinator`, `dlq_dispatcher`
    - *Verification Gate:* Zero duplicate task executions under identical idempotency keys; clean saga rollback.

---

### C. Legal & Enterprise Mastery
18. **Genius-Law (`law`)**
    - *Invariants:*
      - Federal Rules of Evidence FRE 902(13)/(14) Self-Authenticating Electronic Records.
      - Bates Numbering Contiguous Monotonicity (0 gaps, 0 duplicates, 0 misorderings).
      - Unbroken SHA-256 / Blake2b Chain of Custody.
    - *Tools:* `bates_numberer`, `precedent_searcher`, `pleading_formatter`, `chain_of_custody_validator`
    - *Verification Gate:* Contiguous Bates verification; all factual allegations tethered to exhibit hashes.

19. **Genius-DocumentProcessing (`document-processing`)**
    - *Invariants:*
      - Normalized AST Layout Coordinates.
      - Zero Text Omission: Extracted character count matches raw content streams.
      - Lossless UTF-8 Encoding.
    - *Tools:* `pdf_stream_extractor`, `ocr_aligner`, `table_reconstructor`, `reading_order_resolver`
    - *Verification Gate:* Zero unicode replacement characters (U+FFFD); table topology preserved.

20. **Genius-DocumentGeneration (`document-generation`)**
    - *Invariants:*
      - Deterministic Compilation: Identical AST produces bit-for-bit identical document digest.
      - Typographic Hierarchy & PDF/A Archival Conformance.
      - Tagged Accessible Reading Structure.
    - *Tools:* `pdf_compiler`, `typographic_layout_engine`, `vector_typesetter`, `pdf_signer`
    - *Verification Gate:* Verified identical SHA-256 across independent compilations; PDF/A-1b clean pass.

21. **Genius-MetadataDepth (`metadata-depth`)**
    - *Invariants:*
      - Monotonic Causal Ordering: Modification timestamp $\ge$ creation timestamp.
      - Dual Cryptographic Fingerprints: Blake2b + SHA-256 paired digests.
      - Acyclic Provenance DAG.
    - *Tools:* `forensic_metadata_extractor`, `provenance_dag_builder`, `temporal_consistency_auditor`
    - *Verification Gate:* Zero chronological paradoxes; paired hash verification passes.

---

### D. Physical Systems & Sovereign Infrastructure
22. **Genius-Security (`security`)**
    - *Invariants:*
      - Constant-Time Arithmetic: Zero data-dependent branching or memory access in cryptographic primitives.
      - Shannon Entropy Bound: $H(X) \ge 256$ bits for cryptographic secrets.
      - Zero-Trust Input Validation across all privilege boundaries.
    - *Tools:* `taint_tracker`, `constant_time_prover`, `fuzz_engine`, `entropy_meter`
    - *Verification Gate:* Zero tainted inputs reaching sinks; AddressSanitizer/Valgrind memory safety proof.

23. **Genius-Energy (`energy`)**
    - *Invariants:*
      - First Law of Thermodynamics: $dU = \delta Q - \delta W$.
      - Carnot Efficiency Ceiling: $\eta_{max} = 1 - T_C / T_H$.
      - Peukert's Battery Capacity: $C_p = I^k \cdot t$.
      - Joule Heating: $P = I^2 R$.
    - *Tools:* `grid_phase_analyzer`, `battery_electrochemical_model`, `thermal_dissipation_solver`
    - *Verification Gate:* Grid frequency held within $\pm 0.05$ Hz; thermal runaway margin $> 30^\circ\text{C}$.

---

### E. Telos, Craftsmanship & Culture
24. **Genius-SpiritualAwareness (`spiritual-awareness`)**
    - *Invariants:*
      - Principle of Ahimsa / Non-Harm: Zero generation of deceptive, malicious, or dehumanizing actions.
      - Epistemic Humility: Clear boundaries between empirical facts, philosophical axioms, and unknown realms.
      - Universal Stewardship: Technology held in sacred trust for human flourishing and dignity.
    - *Tools:* `ethical_boundary_checker`, `epistemic_humility_evaluator`, `dignity_alignment_auditor`
    - *Verification Gate:* Zero deceptive assertions; calm, constructive equanimity under adversarial prompts.

25. **Genius-SciFi (`scifi`)**
    - *Invariants:*
      - Internal Causal Consistency of Speculative Novum.
      - Kardashev Energetic Scaling: Type I ($10^{16}$ W), Type II ($10^{26}$ W), Type III ($10^{36}$ W).
      - Relativistic Time Dilation: $\Delta t' = \Delta t \sqrt{1 - v^2/c^2}$.
    - *Tools:* `world_building_consistency_checker`, `kardashev_scale_calculator`, `time_dilation_solver`
    - *Verification Gate:* Zero causal or timeline paradoxes; mass-energy budgets respect solar system bounds.

26. **Genius-NerdGeek (`nerd-geek`)**
    - *Invariants:*
      - Uncompromising Craftsmanship: Elegance, byte-efficiency, and deep reverence for underlying silicon.
      - Cycle-Accurate Raster & Bus Timing.
      - Canonical Historical Attribution of Computing Pioneers and RFCs.
    - *Tools:* `cycle_exact_timer`, `rfc_archive_searcher`, `bit_hack_optimizer`, `cpu_6502_emulator`
    - *Verification Gate:* Minimum byte-count assembly golf; 6502 emulator passes Klaus Dormann test vectors.

---

## 3. CLI Operations & Workflows

### Listing Archetypes
```bash
# List all 26 registered archetypes
genius archetype list

# Filter by domain
genius archetype list --domain frontier_science
genius archetype list --domain systems_platforms
genius archetype list --domain legal_enterprise
genius archetype list --domain telos_culture

# Output JSON
genius archetype list --json
```

### Inspecting an Archetype
```bash
# Inspect first-principles details, tools, invariants, and gates
genius archetype info aerospace
genius archetype info microcode
genius archetype info law
genius archetype info ios
```

### Synthesizing a Canonical Archetype Repository
```bash
# Directly forge a Genius repository configured for an archetype
genius archetype synthesize aerospace --dest /root/projects
genius archetype synthesize microcode --dest /root/projects
genius archetype synthesize law --dest /root/projects
```

### Synthesizing via Role Specification
```bash
# Explicit archetype injection
genius synthesize "Orbital Dynamics Engineer" \
  --outcome "Calculate Hohmann and bi-elliptic transfers" \
  --archetype aerospace \
  --dest /root/projects

# Automatic keyword matching (e.g. 'orbit' or 'aerospace')
genius synthesize "Satellite Trajectory Planner" \
  --outcome "Propagate orbit and verify collision avoidance" \
  --dest /root/projects
```
