"""Genius Lineage Archetypes registry and first-principles domain contracts.

Universal Pillar Invariant:
High-order systems ('pillars') must be assembled from strictly decoupled,
universal atomic pieces that function independently anywhere in the estate.
No archetype couples to or depends on another archetype.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class ArchetypeDefinition:
    """Immutable domain archetype specification."""

    id: str
    name: str
    lineage: str
    domain: str
    description: str
    keywords: tuple[str, ...]
    layers: tuple[str, ...]
    targets: tuple[str, ...]
    invariants: tuple[str, ...]
    tools: tuple[str, ...]
    verification_gates: tuple[str, ...]
    teaching_transfer: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "lineage": self.lineage,
            "domain": self.domain,
            "description": self.description,
            "keywords": list(self.keywords),
            "layers": list(self.layers),
            "targets": list(self.targets),
            "invariants": list(self.invariants),
            "tools": list(self.tools),
            "verification_gates": list(self.verification_gates),
            "teaching_transfer": self.teaching_transfer,
        }


# The 26 Canonical Genius Lineage Archetypes
_RAW_ARCHETYPES: list[ArchetypeDefinition] = [
    # 1. Aerospace
    ArchetypeDefinition(
        id="aerospace",
        name="Genius-Aerospace",
        lineage="Genius Lineage",
        domain="frontier_science",
        description="Orbital dynamics, rocket propulsion, Lambert targeting, and telemetry verification from first principles.",
        keywords=("aerospace", "orbital", "orbit", "trajectory", "rocket", "avionics", "spacecraft", "delta-v", "satellite", "reentry"),
        layers=("physical_substrate", "compute", "runtime", "code", "reasoning", "tools", "verification", "observability", "reliability_recovery", "domain_expertise"),
        targets=(
            "orbital trajectory propagation via high-order numerical integration",
            "lambert transfer boundary value solver",
            "cryogenic propellant boil-off thermodynamic modeling",
            "telemetry stream verification and collision conjunction assessment",
            "launch countdown sequencing and abort boundary verification",
            "aerodynamic drag and atmospheric entry thermal dissipation",
        ),
        invariants=(
            "Tsiolkovsky rocket equation: delta_v = Isp * g0 * ln(m0 / mf)",
            "Vis-viva orbital energy conservation: v^2 = mu * (2/r - 1/a)",
            "Kepler's third law: T^2 = 4*pi^2*a^3 / mu",
            "Propellant boil-off mass conservation: dm/dt = -Q_leak / Delta_H_vap",
        ),
        tools=("telemetry_stream_ingest", "orbital_propagator", "delta_v_budget_calculator", "conjunction_assessor"),
        verification_gates=(
            "Delta-v budget closure within 0.1% margin of error",
            "Orbital energy invariant preserved across Runge-Kutta 8(9) integration steps",
            "Zero conjunction collisions within 5km orbital keep-out ellipsoid",
        ),
        teaching_transfer="Reconstruct Lambert targeting algorithm from initial state vector to target rendezvous orbit without third-party ephemeris libraries.",
    ),

    # 2. Microcode
    ArchetypeDefinition(
        id="microcode",
        name="Genius-Microcode",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Bare-metal CPU architecture, instruction decode cycles, register allocation, pipeline hazard resolution, and eBPF verification.",
        keywords=("microcode", "micro-op", "uop", "isa", "cpu", "baremetal", "register", "pipeline", "ebpf", "hazard", "instruction"),
        layers=("physical_substrate", "compute", "firmware_kernel_os", "runtime", "code", "verification", "security_integrity", "domain_expertise"),
        targets=(
            "micro-operation decoding and execution scheduling",
            "register allocation, liveness analysis, and register renaming",
            "pipeline hazard mitigation (RAW, WAR, WAW interlocking)",
            "eBPF bytecode verification and bounded stack execution",
            "branch predictor penalty minimization and branch target buffers",
            "SIMD and vectorized assembly optimization",
        ),
        invariants=(
            "Instruction decode determinism: 1:1 or 1:N micro-op decomposition",
            "Pipeline hazard prevention: no un-interlocked RAW, WAR, or WAW hazards",
            "Cache line alignment: 64-byte boundary preservation to prevent false sharing",
            "Atomic memory ordering: strict acquire-release semantics under memory barrier",
        ),
        tools=("disassembler_stream", "ebpf_verifier_check", "register_liveness_analyzer", "cycle_accurate_profiler"),
        verification_gates=(
            "Zero branch misprediction pipeline stalls on critical hot path",
            "eBPF verifier termination and bounded stack proof (<512 bytes)",
            "Zero cache line bouncing across concurrent worker cores",
        ),
        teaching_transfer="Reconstruct a cycle-exact instruction decoder and register renaming unit for a RISC-V RV64I core from clean specification.",
    ),

    # 3. Nanosphere
    ArchetypeDefinition(
        id="nanosphere",
        name="Genius-Nanosphere",
        lineage="Genius Lineage",
        domain="frontier_science",
        description="Nanomaterial dynamics, atomic lattice structures, molecular simulation, and quantum confinement boundaries.",
        keywords=("nanosphere", "nano", "nanomaterial", "nanotechnology", "molecular", "lattice", "atomic", "quantum-dot", "nanotube"),
        layers=("reality", "physical_substrate", "compute", "code", "reasoning", "tools", "verification", "domain_expertise"),
        targets=(
            "molecular dynamics atomic lattice simulation",
            "nanostructure surface tension and energy minimization",
            "quantum confinement bandgap calculation",
            "carbon nanotube chiral index mapping and electronic structure",
            "atomic force microscopy signal deconvolution",
        ),
        invariants=(
            "Lennard-Jones intermolecular potential: V_LJ(r) = 4*epsilon * [(sigma/r)^12 - (sigma/r)^6]",
            "de Broglie particle-wave duality: lambda = h / p",
            "Quantum confinement bandgap shift: Delta_E = hbar^2 * pi^2 / (2 * m_eff * d^2)",
            "Surface-area-to-volume ratio scaling: A/V proportional to 1/r",
        ),
        tools=("molecular_lattice_simulator", "atomic_force_analyzer", "quantum_confinement_solver"),
        verification_gates=(
            "Total energy conservation under NVE microcanonical ensemble",
            "Lattice stability verified across 10^6 picosecond simulation steps",
            "Surface defect density below 1 part per billion threshold",
        ),
        teaching_transfer="Simulate a 1000-atom graphene lattice under tensile stress and calculate its Young's modulus from first principles.",
    ),

    # 4. Security
    ArchetypeDefinition(
        id="security",
        name="Genius-Security",
        lineage="Genius Lineage",
        domain="sovereign_infrastructure",
        description="Zero-trust isolation, constant-time cryptographic verification, AST taint tracking, memory safety proofs, and side-channel immunity.",
        keywords=("security", "cryptography", "crypto", "zero-trust", "sandbox", "taint", "side-channel", "vulnerability", "auth", "exploit"),
        layers=("security_integrity", "firmware_kernel_os", "code", "agent_kernel", "verification", "observability", "reliability_recovery"),
        targets=(
            "AST taint tracking and source-sink reachability analysis",
            "constant-time cryptographic arithmetic verification",
            "zero-trust privilege boundary enforcement",
            "side-channel timing and cache attack surface analysis",
            "cryptographic nonce reuse prevention and entropy validation",
            "memory safety formal verification",
        ),
        invariants=(
            "Constant-time execution: zero data-dependent branching or memory access in cryptographic primitives",
            "Shannon entropy lower bound: H(X) >= 256 bits for cryptographic secrets",
            "Zero-trust boundary: all input crossing privilege boundaries must be untrusted and validated",
            "Memory safety invariant: no use-after-free, double-free, or out-of-bounds read/write",
        ),
        tools=("taint_tracker", "constant_time_prover", "fuzz_engine", "entropy_meter"),
        verification_gates=(
            "Zero tainted inputs reaching shell, SQL, or eval execution sinks",
            "Constant-time proof generated with zero branch variation under differing secret keys",
            "Zero memory leaks or undefined behavior under AddressSanitizer and Valgrind",
        ),
        teaching_transfer="Construct an authenticated encryption scheme (AEAD) with verified constant-time polynomial evaluation and zero side-channel leakage.",
    ),

    # 5. Energy
    ArchetypeDefinition(
        id="energy",
        name="Genius-Energy",
        lineage="Genius Lineage",
        domain="physical_systems",
        description="Thermodynamics, electrical power distribution, battery electrochemistry, thermal management, and converter topologies.",
        keywords=("energy", "power", "grid", "battery", "thermodynamic", "joule", "watt", "heat", "converter", "thermal"),
        layers=("physical_substrate", "compute", "code", "reasoning", "tools", "resource_economics", "domain_expertise"),
        targets=(
            "grid frequency stability and phase angle balancing",
            "battery state-of-charge and degradation estimation",
            "thermodynamic dissipation and heat pump modeling",
            "renewable generation intermittency buffering",
            "power converter efficiency and switching loss optimization",
        ),
        invariants=(
            "First law of thermodynamics: dU = delta_Q - delta_W",
            "Carnot efficiency ceiling: eta_max = 1 - T_C / T_H",
            "Peukert's capacity law: Cp = I^k * t",
            "Joule heating power dissipation: P = I^2 * R",
        ),
        tools=("grid_phase_analyzer", "battery_electrochemical_model", "thermal_dissipation_solver"),
        verification_gates=(
            "Frequency deviation held within +/- 0.05 Hz under sudden 20% load step",
            "Thermal runaway margin > 30 degrees C under maximum discharge rate",
            "Energy balance closed with zero unaccounted dissipation",
        ),
        teaching_transfer="Design an optimal battery management system (BMS) state-of-charge estimator incorporating thermal feedback and Peukert losses.",
    ),

    # 6. Physics
    ArchetypeDefinition(
        id="physics",
        name="Genius-Physics",
        lineage="Genius Lineage",
        domain="frontier_science",
        description="Classical, relativistic, and quantum mechanics, Lagrangian/Hamiltonian dynamics, Noether conservation laws, and symplectic integrators.",
        keywords=("physics", "mechanics", "hamiltonian", "lagrangian", "noether", "electromagnetism", "relativity", "quantum", "gravity", "symplectic"),
        layers=("reality", "compute", "code", "reasoning", "tools", "verification", "domain_expertise"),
        targets=(
            "Lagrangian and Hamiltonian formulation synthesis",
            "symplectic numerical integration preserving phase-space volume",
            "electromagnetic field tensor and Maxwell stress computation",
            "Navier-Stokes fluid turbulence approximation",
            "relativistic spacetime metric geodesics computation",
        ),
        invariants=(
            "Noether's theorem: continuous symmetries correspond to conserved currents",
            "Euler-Lagrange principle of stationary action: d/dt(dL/d_qdot) - dL/dq = 0",
            "Liouville's theorem: phase space volume is incompressible under Hamiltonian flow",
            "Relativistic Lorentz invariance: s^2 = c^2 * dt^2 - dx^2 - dy^2 - dz^2",
        ),
        tools=("symplectic_integrator", "field_tensor_calculator", "geodesic_integrator"),
        verification_gates=(
            "Symplectic phase-space volume preserved to machine precision",
            "Conserved Noether charges (energy, momentum, angular momentum) constant across trajectory",
            "Gauge invariance satisfied across all electromagnetic field operations",
        ),
        teaching_transfer="Derive and numerically integrate the double-pendulum equations of motion using a symplectic Störmer-Verlet integrator.",
    ),

    # 7. Chemistry
    ArchetypeDefinition(
        id="chemistry",
        name="Genius-Chemistry",
        lineage="Genius Lineage",
        domain="frontier_science",
        description="Chemical stoichiometry, reaction kinetics, Gibbs free energy equilibrium, thermochemistry, and molecular transition states.",
        keywords=("chemistry", "chemical", "reaction", "stoichiometry", "kinetics", "gibbs", "equilibrium", "molecule", "enthalpy", "catalysis"),
        layers=("reality", "physical_substrate", "code", "reasoning", "tools", "verification", "domain_expertise"),
        targets=(
            "stoichiometric reaction balancing and mass conservation",
            "reaction kinetics non-linear ODE solving",
            "Gibbs free energy and phase equilibrium calculation",
            "spectroscopic peak assignment and molecular structure verification",
            "molecular transition state search and activation barrier determination",
        ),
        invariants=(
            "Law of conservation of mass: stoichiometric atom balance across all reactions",
            "Gibbs free energy spontaneity condition: Delta_G = Delta_H - T * Delta_S < 0",
            "Arrhenius reaction rate: k = A * exp(-E_a / (R * T))",
            "Le Chatelier's principle of chemical equilibrium: K_eq = prod([P]^p) / prod([R]^r)",
        ),
        tools=("stoichiometry_balancer", "kinetics_ode_solver", "spectroscopy_analyzer"),
        verification_gates=(
            "Total atom count strictly conserved across all reaction steps",
            "Equilibrium constant satisfies van 't Hoff equation across temperature range",
            "Enthalpy and entropy balances verified against standard thermochemical tables",
        ),
        teaching_transfer="Solve an oscillating Belousov-Zhabotinsky reaction mechanism from stoichiometric rate equations to limit-cycle attractor.",
    ),

    # 8. Biology
    ArchetypeDefinition(
        id="biology",
        name="Genius-Biology",
        lineage="Genius Lineage",
        domain="frontier_science",
        description="Bioinformatics, nucleotide/peptide sequence alignment, enzyme kinetics, protein conformation, and metabolic flux analysis.",
        keywords=("biology", "biological", "bioinformatics", "dna", "rna", "protein", "enzyme", "crispr", "genetics", "metabolic"),
        layers=("reality", "compute", "code", "reasoning", "tools", "files_documents", "domain_expertise"),
        targets=(
            "Smith-Waterman and Needleman-Wunsch sequence alignment",
            "protein secondary structure and folding kinetics modeling",
            "metabolic flux balance analysis under steady-state constraints",
            "CRISPR off-target cleavage risk scoring and PAM site detection",
            "phylogenetic tree maximum likelihood reconstruction",
        ),
        invariants=(
            "Central Dogma of molecular biology: DNA -> RNA -> Protein sequence translation",
            "Michaelis-Menten enzyme kinetics: v = Vmax * [S] / (Km + [S])",
            "Hardy-Weinberg genetic equilibrium: p^2 + 2pq + q^2 = 1",
            "Conservation of codon triplet reading frames across coding sequences",
        ),
        tools=("sequence_aligner", "protein_conformation_evaluator", "metabolic_flux_solver"),
        verification_gates=(
            "Sequence alignment scores mathematically optimal under chosen PAM/BLOSUM matrix",
            "Metabolic flux satisfies steady-state stoichiometric constraint S * v = 0",
            "Zero reading frame phase shifts in translated open reading frame",
        ),
        teaching_transfer="Implement a vectorized Smith-Waterman local alignment algorithm with affine gap penalty and demonstrate optimality against benchmark sequences.",
    ),

    # 9. Law
    ArchetypeDefinition(
        id="law",
        name="Genius-Law",
        lineage="Genius Lineage",
        domain="legal_enterprise",
        description="Statutory construction, precedent retrieval, Bates numbering, chain of custody, FRE 902 electronic record authentication, and pleading compilation.",
        keywords=("law", "legal", "litigation", "court", "attorney", "pleading", "bates", "evidence", "custody", "fre-902", "statute"),
        layers=("domain_expertise", "verification", "files_documents", "reasoning", "security_integrity", "artifact_generation"),
        targets=(
            "statutory canons of construction analysis",
            "precedent retrieval and Shepardizing case authority",
            "cryptographic Bates numbering and exhibit scheduling",
            "FRE 902(13)/(14) electronic evidence chain certification",
            "adversarial pleading contradiction extraction",
            "court-compliant pleading compilation and table of authorities",
        ),
        invariants=(
            "FRE 902(13)/(14) self-authenticating electronic record requirements",
            "Bates numbering contiguous monotonicity: zero gaps, zero duplicates, zero misorderings",
            "Chain of custody cryptographic unbroken hash chain (SHA-256 / Blake2b)",
            "Strict jurisdictional prerequisites: subject-matter jurisdiction and personal jurisdiction",
        ),
        tools=("bates_numberer", "precedent_searcher", "pleading_formatter", "chain_of_custody_validator"),
        verification_gates=(
            "Contiguous Bates numbering with 0 gaps and 0 collisions",
            "Every factual claim tethered to a verified SHA-256 exhibit hash",
            "Jurisdictional hooks verified against statutory rules of procedure",
        ),
        teaching_transfer="Compile a court-ready motion for summary judgment with verified Bates exhibits, SHA-256 integrity ledger, and Shepardized table of authorities.",
    ),

    # 10. Document Processing
    ArchetypeDefinition(
        id="document-processing",
        name="Genius-DocumentProcessing",
        lineage="Genius Lineage",
        domain="legal_enterprise",
        description="Lossless PDF/document ingestion, OCR token alignment, layout AST extraction, tabular data reconstruction, and reading-order resolution.",
        keywords=("document-processing", "document", "pdf", "ocr", "parsing", "table-extraction", "layout", "tokens", "reading-order"),
        layers=("files_documents", "perception", "multimodal", "representation", "artifact_generation", "verification"),
        targets=(
            "PDF stream decompression and token extraction",
            "OCR bounding box token alignment and confidence scoring",
            "hierarchical table structure reconstruction",
            "document metadata and interactive form field extraction",
            "multi-column reading order topological resolution",
        ),
        invariants=(
            "AST layout invariance: bounding box coordinates remain normalized and non-negative",
            "Zero text omission: character count in extracted tokens matches raw document stream",
            "Character encoding preservation: UTF-8 lossless transcoding",
            "Non-destructive processing: original source bytes preserved immutably",
        ),
        tools=("pdf_stream_extractor", "ocr_aligner", "table_reconstructor", "reading_order_resolver"),
        verification_gates=(
            "Zero unicode replacement characters (U+FFFD) in extracted text",
            "Table cell topology preserved with correct row/column span coordinates",
            "Source document cryptographic hash matches intake manifest",
        ),
        teaching_transfer="Extract and reconstruct complex multi-page financial tables from flattened PDF streams with 100% cell coordinate fidelity.",
    ),

    # 11. Document Generation
    ArchetypeDefinition(
        id="document-generation",
        name="Genius-DocumentGeneration",
        lineage="Genius Lineage",
        domain="legal_enterprise",
        description="Deterministic document compilation, typographic grid alignment, PDF/A archival compliance, vector typesetting, and cryptographic signing.",
        keywords=("document-generation", "generation", "pdf-generation", "typesetting", "typography", "latex", "pdf-a", "report", "watermark"),
        layers=("artifact_generation", "files_documents", "representation", "verification", "domain_expertise"),
        targets=(
            "typographic grid and layout engine compilation",
            "vector diagram and SVG typesetting",
            "PDF/A compliant archival rendering",
            "table of contents and internal bookmark cross-referencing",
            "cryptographic document watermarking and signing",
        ),
        invariants=(
            "Deterministic compilation: identical source AST produces bit-for-bit identical PDF hash",
            "Typographic hierarchy compliance: font sizes, leading, and margins adhere to specification",
            "PDF/A standard conformance: embedded fonts and color profiles for archival longevity",
            "Accessible tagged structure: screen-reader navigable headings and alternative text",
        ),
        tools=("pdf_compiler", "typographic_layout_engine", "vector_typesetter", "pdf_signer"),
        verification_gates=(
            "Deterministic compilation verified via identical SHA-256 across independent runs",
            "PDF/A-1b validator pass with 0 syntax or font embedding warnings",
            "All hyperlinks, bookmarks, and cross-references resolve with 0 broken anchors",
        ),
        teaching_transfer="Build a deterministic PDF compiler that outputs PDF/A-compliant publications with vector schematics and cryptographically verified SHA-256 digests.",
    ),

    # 12. Metadata Depth
    ArchetypeDefinition(
        id="metadata-depth",
        name="Genius-MetadataDepth",
        lineage="Genius Lineage",
        domain="legal_enterprise",
        description="Deep forensic metadata extraction, multi-hash integrity verification, provenance DAGs, and temporal chronological auditability.",
        keywords=("metadata-depth", "metadata", "exif", "id3", "provenance", "fingerprint", "chronology", "blake2b", "xmp"),
        layers=("representation", "files_documents", "verification", "observability", "state_persistence"),
        targets=(
            "deep forensic metadata extraction (EXIF, ID3, PDF, XMP)",
            "cryptographic provenance DAG generation",
            "temporal timestamp consistency auditing",
            "multimedia stream codec and container inspection",
            "semantic schema tagging and ontology alignment",
        ),
        invariants=(
            "Monotonic causal ordering: record modification timestamp >= record creation timestamp",
            "Dual cryptographic fingerprinting: Blake2b + SHA-256 paired digests",
            "Immutability of origin: provenance ancestor cannot be modified after descendant creation",
            "Schema conformance: metadata keys conform strictly to namespaced Dublin Core / ISO 19115",
        ),
        tools=("forensic_metadata_extractor", "provenance_dag_builder", "temporal_consistency_auditor"),
        verification_gates=(
            "Zero chronological paradoxes in file system, header, and container timestamps",
            "Blake2b and SHA-256 paired digests match independently recomputed values",
            "Provenance DAG is strictly acyclic with verified root of title",
        ),
        teaching_transfer="Construct an immutable provenance ledger that tracks 10,000 multi-format digital assets with dual Blake2b/SHA-256 fingerprinting.",
    ),

    # 13. Filesystem
    ArchetypeDefinition(
        id="filesystem",
        name="Genius-Filesystem",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="POSIX filesystem semantics, atomic file swaps, crash-consistent journaling, copy-on-write allocation, and extent mapping.",
        keywords=("filesystem", "posix", "inode", "wal", "journaling", "copy-on-write", "atomic", "btree", "fsync"),
        layers=("firmware_kernel_os", "runtime", "code", "files_documents", "reliability_recovery", "verification"),
        targets=(
            "atomic file swap and safe write-replace pipeline",
            "copy-on-write B-tree block allocation",
            "journaling and crash consistency replay",
            "sparse file and extent mapping",
            "directory lock and concurrency synchronization",
        ),
        invariants=(
            "POSIX atomic rename semantics: rename(old, new) is atomic and never leaves target in half-state",
            "Write-Ahead Logging (WAL) crash consistency: log entry sync precedes block write",
            "Inode reference counting: block freed if and only if link count reaches zero",
            "fsync barrier correctness: metadata and data flushed to non-volatile storage",
        ),
        tools=("atomic_file_writer", "wal_journal_replayer", "extent_allocator", "fsync_barrier_checker"),
        verification_gates=(
            "Simulated sudden power loss yields 100% clean recovery without corruption",
            "Atomic replace never exposes intermediate empty or partial file to concurrent reader",
            "File descriptor leak count = 0 under 100,000 rapid open/write/close cycles",
        ),
        teaching_transfer="Implement a crash-safe write-ahead logging (WAL) storage engine that recovers completely from simulated power-off mid-transaction.",
    ),

    # 14. Cloud Database
    ArchetypeDefinition(
        id="cloud-database",
        name="Genius-CloudDatabase",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Distributed database architecture, Raft/Paxos consensus, MVCC snapshot isolation, 2PC distributed transactions, and partition tolerance.",
        keywords=("cloud-database", "database", "sql", "nosql", "raft", "paxos", "mvcc", "consensus", "acid", "distributed-db"),
        layers=("compute", "runtime", "code", "state_persistence", "reliability_recovery", "observability"),
        targets=(
            "Raft consensus state machine implementation",
            "multi-version concurrency control (MVCC) snapshot isolation",
            "distributed transaction two-phase commit (2PC)",
            "consistent hashing and partition rebalancing",
            "write-ahead log log-structured merge-tree (LSM) compaction",
        ),
        invariants=(
            "CAP theorem bounds: explicit consistency vs availability trade-off documentation",
            "Serializability / Snapshot Isolation: no dirty reads, non-repeatable reads, or phantom reads",
            "Raft / Paxos consensus: leader election and log replication require strict majority quorum",
            "Vector clock causality: partial ordering A -> B <=> V(A) < V(B)",
        ),
        tools=("raft_consensus_engine", "mvcc_storage_engine", "consistent_hash_ring", "lsm_compactor"),
        verification_gates=(
            "Zero split-brain states during simulated network partition (Jepsen-style testing)",
            "Zero phantom reads under serializable transaction isolation test",
            "Log replication index monotonically increasing with quorum receipt",
        ),
        teaching_transfer="Implement a 3-node Raft consensus cluster with replicated log, leader election, and automated split-brain healing.",
    ),

    # 15. Device
    ArchetypeDefinition(
        id="device",
        name="Genius-Device",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Hardware peripheral interfacing, MMIO register mapping, interrupt service routines (ISR), DMA transfers, and bus protocols (UART, SPI, I2C, CAN).",
        keywords=("device", "hardware", "mmio", "isr", "dma", "uart", "spi", "i2c", "peripheral", "gpio", "embedded"),
        layers=("physical_substrate", "firmware_kernel_os", "compute", "code", "reliability_recovery", "verification"),
        targets=(
            "memory-mapped I/O (MMIO) driver synthesis",
            "interrupt service routine top/bottom half handling",
            "direct memory access (DMA) ring buffer management",
            "hardware peripheral protocols (UART, SPI, I2C, CAN)",
            "hardware watchdog and brownout detection",
        ),
        invariants=(
            "Volatile hardware register semantics: memory-mapped I/O reads/writes not eliminated by compiler optimization",
            "Interrupt Service Routine (ISR) reentrancy: non-blocking, minimal latency, top-half/bottom-half split",
            "DMA cache coherency: memory invalidated before device read and flushed after write",
            "Watchdog timer servicing: reset deadline strictly respected to avoid hardware reboot",
        ),
        tools=("mmio_register_map", "uart_spi_protocol_analyzer", "dma_ring_buffer", "watchdog_monitor"),
        verification_gates=(
            "Zero volatile register read/write optimization elisions in compiled assembly",
            "ISR execution latency < 10 microseconds under maximum interrupt load",
            "DMA ring buffer overflow count = 0 during sustained line-rate transfers",
        ),
        teaching_transfer="Author a zero-copy DMA ring-buffer driver for a high-speed SPI/UART peripheral with bounded latency ISR handlers.",
    ),

    # 16. PC
    ArchetypeDefinition(
        id="pc",
        name="Genius-PC",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="x86_64 architecture, UEFI firmware bootstrap, ACPI power tables, PCI Express configuration, and multi-core APIC initialization.",
        keywords=("pc", "x86", "x86_64", "uefi", "bios", "acpi", "pcie", "apic", "motherboard", "intel", "amd"),
        layers=("physical_substrate", "firmware_kernel_os", "compute", "code", "security_integrity", "verification"),
        targets=(
            "UEFI bootloader and GOP display initialization",
            "x86_64 long mode transition and page table mapping",
            "ACPI DSDT/SSDT AML bytecode interpretation",
            "PCI Express enumeration and MSI-X interrupt allocation",
            "APIC timer and multi-core SMP bootstrap",
        ),
        invariants=(
            "x86_64 4-level/5-level page table translation: PML4 -> PDPT -> PD -> PT",
            "ACPI power state transitions: S0 (Working) to S3/S4/S5 strictly compliant",
            "PCI Express configuration space: Base Address Register (BAR) alignment",
            "UEFI Secure Boot chain: Authenticode PE/COFF cryptographic signature verification",
        ),
        tools=("uefi_boot_checker", "x86_page_table_builder", "acpi_aml_parser", "pcie_enumerator"),
        verification_gates=(
            "Page fault handler correctly resolves valid demand-paged virtual addresses",
            "Secure Boot key database (PK, KEK, db) verifies authentic kernel signature",
            "All CPU cores successfully transition to 64-bit long mode without triple-fault",
        ),
        teaching_transfer="Build a minimal UEFI bootloader that sets up 4-level paging, parses ACPI MADT tables, and starts secondary SMP cores.",
    ),

    # 17. Mac
    ArchetypeDefinition(
        id="mac",
        name="Genius-Mac",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Apple Silicon Darwin XNU architecture, Mach IPC message ports, Apple Neural Engine (ANE), Metal Shading Language, and hardened runtime.",
        keywords=("mac", "macos", "darwin", "xnu", "apple-silicon", "m1", "m2", "m3", "m4", "ane", "metal", "mach"),
        layers=("physical_substrate", "firmware_kernel_os", "runtime", "code", "tools", "verification"),
        targets=(
            "Mach messaging IPC and bootstrap service lookups",
            "Apple Neural Engine (ANE) MIL compiler dispatch",
            "Metal Shading Language (MSL) compute pipeline",
            "macOS sandbox entitlements and TCC permission auditing",
            "Darwin kernel trace and DTrace probe integration",
        ),
        invariants=(
            "Mach port IPC rights: send/receive capabilities strictly enforced by XNU",
            "Apple Silicon unified memory coherency: CPU/GPU/ANE zero-copy buffer sharing",
            "Code signing and hardened runtime: entitlements must be notarized by Apple",
            "Grand Central Dispatch QoS priorities: UserInteractive > UserInitiated > Utility > Background",
        ),
        tools=("mach_port_inspector", "metal_compute_profiler", "codesign_entitlements_auditor"),
        verification_gates=(
            "Mach port leaks = 0 across 10,000 IPC transactions",
            "Metal compute kernel achieves zero-copy execution with shared storage mode",
            "codesign verification passes with valid Team ID and hardened runtime",
        ),
        teaching_transfer="Develop a zero-copy Metal compute pipeline utilizing Apple Silicon unified memory with synchronized CPU-GPU buffer access.",
    ),

    # 18. Linux
    ArchetypeDefinition(
        id="linux",
        name="Genius-Linux",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Linux kernel primitives, io_uring async I/O, cgroups v2 resource hierarchy, eBPF telemetry, and namespace containerization.",
        keywords=("linux", "kernel", "io_uring", "cgroups", "ebpf", "namespaces", "systemd", "procfs", "sysfs", "vfs"),
        layers=("firmware_kernel_os", "runtime", "code", "tools", "reliability_recovery", "security_integrity"),
        targets=(
            "io_uring zero-copy async file and socket I/O",
            "cgroups v2 resource controller budgeting",
            "eBPF tracing and network socket filtering",
            "Linux namespace container isolation",
            "systemd unit lifecycle and watchdog notification",
        ),
        invariants=(
            "Everything is a file: uniform VFS descriptor abstraction",
            "cgroups v2 single-hierarchy constraint: controllers enabled along unified tree",
            "io_uring memory barriers: Submission Queue (SQ) and Completion Queue (CQ) atomic ordering",
            "Linux kernel namespaces: complete isolation of PID, Mount, Net, IPC, UTS, and User",
        ),
        tools=("io_uring_bench", "cgroups_controller", "ebpf_trace_loader", "namespace_isolator"),
        verification_gates=(
            "io_uring throughput exceeds standard epoll by >= 2x with zero dropped CQEs",
            "cgroup memory.max limit strictly enforced with OOM notification",
            "Container root process unable to view or access host PID namespace",
        ),
        teaching_transfer="Build a high-performance network server using io_uring submission/completion rings bounded by cgroups v2 resource ceilings.",
    ),

    # 19. Android
    ArchetypeDefinition(
        id="android",
        name="Genius-Android",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Android OS architecture, Binder IPC transactions, ART DEX bytecode, Android NDK/JNI, SurfaceFlinger graphics, and HAL services.",
        keywords=("android", "apk", "art", "dex", "binder", "ndk", "jni", "surfaceflinger", "hal", "aidl"),
        layers=("physical_substrate", "firmware_kernel_os", "runtime", "code", "security_integrity", "tools"),
        targets=(
            "Binder IPC transaction marshaling and parceling",
            "Android NDK native C/C++ JNI bridging",
            "SurfaceFlinger display pipeline and Choreographer vsync",
            "Android manifest security permission enforcement",
            "ART DEX bytecode optimization and profiling",
        ),
        invariants=(
            "Android Binder IPC reference counting: flat binder object serialization",
            "Android ART ahead-of-time / JIT compilation and dex bytecode verification",
            "Android permission sandbox: UID-based process separation",
            "Android HAL interface definition language (AIDL) version compatibility",
        ),
        tools=("binder_tracer", "jni_bridge_validator", "apk_manifest_auditor", "vsync_profiler"),
        verification_gates=(
            "Binder parcel serialization round-trips with zero memory leak",
            "JNI local and global reference counts balanced without JNI-local table overflow",
            "Zero permission escalations allowed outside declared manifest uses-permission",
        ),
        teaching_transfer="Implement a custom AIDL service communicating across processes via Binder IPC with verified Parcelable marshaling.",
    ),

    # 20. iOS
    ArchetypeDefinition(
        id="ios",
        name="Genius-iOS",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Apple iOS runtime, Swift Concurrency actor isolation, ARM64e Pointer Authentication (PAC), CoreAnimation 120Hz ProMotion, and Secure Enclave.",
        keywords=("ios", "swift", "swiftui", "arm64e", "pac", "coreanimation", "keychain", "secure-enclave", "uikit"),
        layers=("physical_substrate", "firmware_kernel_os", "runtime", "code", "security_integrity", "verification"),
        targets=(
            "Swift Concurrency actor isolation and async/await task trees",
            "CoreAnimation and SwiftUI declarative render pipeline",
            "ARM64e PAC pointer integrity verification",
            "iOS Keychain Secure Enclave cryptographic key storage",
            "App Group shared memory and IPC container synchronization",
        ),
        invariants=(
            "Swift memory ownership and exclusivity: simultaneous mutable access to memory is undefined",
            "ARM64e Pointer Authentication (PAC): sign and authenticate function pointers and return addresses",
            "CoreAnimation 120Hz ProMotion frame budget: render loop completes in < 8.33 milliseconds",
            "App Sandbox containerization: file access strictly bounded to sandbox containers and app groups",
        ),
        tools=("swift_actor_checker", "core_animation_budgeter", "secure_enclave_keychain", "sandbox_auditor"),
        verification_gates=(
            "Swift compiler thread safety: zero data races detected under strict concurrency",
            "Zero dropped frames (60fps/120fps maintained) during complex list scrolling",
            "Keychain items securely stored in kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly",
        ),
        teaching_transfer="Build a high-concurrency iOS SwiftUI application using Swift Actors, Secure Enclave cryptography, and 120Hz smooth ProMotion rendering.",
    ),

    # 21. Email
    ArchetypeDefinition(
        id="email",
        name="Genius-Email",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="RFC 5322 MIME messaging, RFC 6376 DKIM cryptographic verification, RFC 7208 SPF policy, RFC 7489 DMARC alignment, and SMTP state machines.",
        keywords=("email", "smtp", "imap", "mime", "dkim", "spf", "dmarc", "rfc5322", "mail"),
        layers=("communication", "security_integrity", "files_documents", "apis", "verification"),
        targets=(
            "RFC 5322 MIME multi-part parser and serializer",
            "DKIM header signing and RSA/Ed25519 public key verification",
            "SPF DNS record parsing and CIDR IP validation",
            "DMARC policy enforcement and aggregate report parsing",
            "SMTP conversation state machine with STARTTLS negotiation",
        ),
        invariants=(
            "RFC 5322 internet message format BNF grammar compliance",
            "RFC 6376 DomainKeys Identified Mail (DKIM): canonicalization with cryptographic signature verification",
            "RFC 7208 Sender Policy Framework (SPF): IP match against authorized SPF record",
            "RFC 7489 DMARC alignment: SPF or DKIM identifier must align with From domain",
        ),
        tools=("mime_parser", "dkim_signer_verifier", "spf_evaluator", "smtp_state_machine"),
        verification_gates=(
            "DKIM signature verification yields PASS on canonical test vector",
            "SPF evaluation accurately classifies Pass, Neutral, SoftFail, and Fail IPs",
            "MIME parser prevents header injection (CRLF sanitization) across all fields",
        ),
        teaching_transfer="Construct an RFC-compliant SMTP receiving agent that validates DKIM, SPF, and DMARC alignment before accepting inbound MIME payloads.",
    ),

    # 22. Automation
    ArchetypeDefinition(
        id="automation",
        name="Genius-Automation",
        lineage="Genius Lineage",
        domain="systems_platforms",
        description="Idempotent event-driven workflow automation, finite state machines (FSM), saga compensating transactions, and distributed exponential backoff.",
        keywords=("automation", "workflow", "idempotent", "fsm", "saga", "scheduler", "cron", "retry", "orchestration"),
        layers=("time_events_automation", "orchestration", "reliability_recovery", "observability", "state_persistence"),
        targets=(
            "finite state machine (FSM) workflow engine",
            "idempotency key deduplication and lease management",
            "exponential backoff with jitter retry strategy",
            "saga pattern compensating transaction coordinator",
            "dead-letter queue (DLQ) and recovery dispatch",
        ),
        invariants=(
            "Idempotency invariant: f(f(x)) = f(x) for all automated operations",
            "Deterministic exponential backoff with full jitter: t = random(0, min(t_max, t_base * 2^attempt))",
            "Transactional rollback: failed composite workflows execute compensating actions in reverse order",
            "Finite State Machine (FSM) completeness: all state-event transitions explicitly defined, no unhandled events",
        ),
        tools=("fsm_engine", "idempotency_ledger", "saga_coordinator", "dlq_dispatcher"),
        verification_gates=(
            "Double execution of identical task with same idempotency key produces exactly one effect",
            "Simulated step-3 failure triggers successful compensating rollback of step-2 and step-1",
            "Zero deadlock or infinite loop conditions in state transition graph",
        ),
        teaching_transfer="Build a resilient distributed saga coordinator that executes multi-step external API calls with guaranteed idempotency and rollbacks.",
    ),

    # 23. Model Weights
    ArchetypeDefinition(
        id="model-weights",
        name="Genius-ModelWeights",
        lineage="Genius Lineage",
        domain="frontier_science",
        description="LLM weight quantization (AWQ/GPTQ/FP8), FlashAttention IO tiling, Rotary Position Embeddings (RoPE), and paged KV cache allocation.",
        keywords=("model-weights", "weights", "quantization", "fp8", "int4", "awq", "gptq", "rope", "kv-cache", "flashattention"),
        layers=("compute", "runtime", "code", "model", "model_serving", "resource_economics", "domain_expertise"),
        targets=(
            "INT4 / FP8 post-training weight quantization (AWQ / GPTQ)",
            "FlashAttention memory-efficient IO tiling computation",
            "Rotary Position Embedding (RoPE) frequency calculation",
            "KV-cache paging and prefix caching (vLLM style)",
            "Tensor parallel weight sharding and all-reduce synchronization",
        ),
        invariants=(
            "Quantization scale and zero-point transformation: x_q = clip(round(x / S) + Z, q_min, q_max)",
            "Rotary Position Embedding (RoPE) unitary transformation: preserves vector inner product under relative rotation",
            "KV cache memory upper bound: M_kv = 2 * layers * heads * d_head * s * bytes",
            "Matrix multiplication numerical stability: FP8 / BF16 accumulator prevents underflow/overflow",
        ),
        tools=("quantization_engine", "rope_rotator", "kv_cache_paged_allocator", "tensor_shard_calculator"),
        verification_gates=(
            "Quantized model perplexity delta < 0.15 compared to full precision FP16 baseline",
            "KV-cache paging eliminates memory fragmentation with > 95% GPU VRAM utilization",
            "Rotary positional inner product matches theoretical cosine/sine rotation",
        ),
        teaching_transfer="Implement an INT4 weight quantization routine with asymmetric scale/zero-point and verify perplexity preservation on a benchmark transformer layer.",
    ),

    # 24. Spiritual Awareness
    ArchetypeDefinition(
        id="spiritual-awareness",
        name="Genius-SpiritualAwareness",
        lineage="Genius Lineage",
        domain="telos_culture",
        description="Ethical telos, epistemic humility, human dignity preservation, universal stewardship, and contemplative composure under stress.",
        keywords=("spiritual-awareness", "spiritual", "spirituality", "telos", "ethics", "humility", "dignity", "mindfulness", "contemplation"),
        layers=("agent_kernel", "identity_persona", "reasoning", "metacognition", "human_interaction", "teaching", "domain_expertise"),
        targets=(
            "moral and ethical boundary evaluation",
            "epistemic humility and uncertainty discernment",
            "human dignity and compassionate alignment",
            "contemplative reflection and equanimity preservation",
            "purpose-driven teleological alignment",
        ),
        invariants=(
            "Principle of Ahimsa / Non-Harm: zero generation of deceptive, malicious, or dehumanizing actions",
            "Epistemic humility: clear distinction between empirical facts, faith/philosophy, and unknown mystery",
            "Universal stewardship: technological power is held in trust for human dignity and living flourishing",
            "Equanimity in adversity: preserving patience, clarity, and compassionate composure during failure",
        ),
        tools=("ethical_boundary_checker", "epistemic_humility_evaluator", "dignity_alignment_auditor"),
        verification_gates=(
            "Zero deceptive assertions: all unknown domains explicitly acknowledged",
            "Harm-minimization filter triggers on adversarial or dehumanizing inputs",
            "Entity maintains calm, respectful, and constructive stance under hostile prompt stress",
        ),
        teaching_transfer="Demonstrate a principled ethical reasoning evaluation that reconciles conflicting stakeholder dilemmas while preserving human dignity.",
    ),

    # 25. Sci-Fi
    ArchetypeDefinition(
        id="scifi",
        name="Genius-SciFi",
        lineage="Genius Lineage",
        domain="telos_culture",
        description="Speculative novum extrapolation, Kardashev energetic engineering, relativistic spaceflight, cybernetic intelligence, and Fermi paradox modeling.",
        keywords=("scifi", "sci-fi", "science-fiction", "speculative", "kardashev", "dyson-sphere", "relativistic", "cybernetic", "fermi"),
        layers=("reality", "reasoning", "knowledge", "artifact_generation", "domain_expertise", "teaching"),
        targets=(
            "speculative novum extrapolation and world-building consistency",
            "Kardashev megastructure engineering modeling (Dyson swarms, orbital rings)",
            "relativistic spaceflight trajectory and time dilation calculation",
            "cybernetic human-AI collective architecture",
            "Fermi paradox filter analysis and drake equation formulation",
        ),
        invariants=(
            "Internal causal consistency: speculative premises (novum) must have logically coherent consequences",
            "Kardashev energy scale bounds: Type I (10^16 W), Type II (10^26 W), Type III (10^36 W)",
            "Relativistic time dilation: Delta_t_prime = Delta_t * sqrt(1 - v^2/c^2)",
            "Fermi paradox mathematical constraints: Drake equation probabilistic bounds",
        ),
        tools=("world_building_consistency_checker", "kardashev_scale_calculator", "time_dilation_solver"),
        verification_gates=(
            "Zero timeline or causal paradoxes in speculative narrative world-state",
            "Megastructure mass-energy budgets stay within solar system raw material limits",
            "Relativistic time dilation matches Lorentz transformation to 6 decimal places",
        ),
        teaching_transfer="Model the construction timeline, orbital dynamics, and energy capture of a Dyson swarm around a G-type main-sequence star.",
    ),

    # 26. Nerd / Geek
    ArchetypeDefinition(
        id="nerd-geek",
        name="Genius-NerdGeek",
        lineage="Genius Lineage",
        domain="telos_culture",
        description="Uncompromising hacker craftsmanship, cycle-accurate retrocomputing, demoscene optimization, assembly size-golfing, and historical RFC lore.",
        keywords=("nerd-geek", "nerd", "geek", "demoscene", "retrocomputing", "assembly-golf", "6502", "z80", "hacker-lore", "easter-egg"),
        layers=("physical_substrate", "compute", "code", "identity_persona", "domain_expertise", "teaching"),
        targets=(
            "cycle-exact demoscene assembly and raster timing",
            "esoteric computing history and RFC provenance retrieval",
            "assembly code size-golfing and bit-twiddling hacks",
            "retrocomputing hardware emulation (MOS 6502, Z80, Motorola 68000)",
            "Easter egg design and subtle hacker humor",
        ),
        invariants=(
            "Uncompromising craftsmanship: elegance, byte-efficiency, and deep respect for underlying silicon",
            "Cycle-accurate timing: raster line and clock cycle synchronization",
            "Hacker ethics: transparency, curiosity, decentralization, and delight in technical discovery",
            "Canonical provenance: accurate attribution of historical RFCs, algorithms, and computing pioneers",
        ),
        tools=("cycle_exact_timer", "rfc_archive_searcher", "bit_hack_optimizer", "cpu_6502_emulator"),
        verification_gates=(
            "Assembly golf output executes identically with minimum possible byte footprint",
            "6502 CPU emulator passes all Klaus Dormann functional test vectors",
            "RFC citations verify author, date, and exact section paragraph",
        ),
        teaching_transfer="Implement a cycle-accurate MOS 6502 microprocessor emulator in pure Python that passes the complete Klaus Dormann 6502 functional test suite.",
    ),
]

# Primary registry keyed by archetype ID
ARCHETYPES: dict[str, ArchetypeDefinition] = {
    arch.id: arch for arch in _RAW_ARCHETYPES
}


def _normalize_token(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def get_archetype(name_or_id: str) -> ArchetypeDefinition | None:
    """Retrieve an archetype by ID, name, or common aliases."""
    if not name_or_id:
        return None
    slug = _normalize_token(name_or_id)
    # Direct match
    if slug in ARCHETYPES:
        return ARCHETYPES[slug]
    # Strip "genius-" prefix if present
    if slug.startswith("genius-"):
        short_slug = slug[7:]
        if short_slug in ARCHETYPES:
            return ARCHETYPES[short_slug]
    # Check by normalized name
    for arch in ARCHETYPES.values():
        if _normalize_token(arch.name) == slug:
            return arch
        if arch.id.replace("-", "") == slug.replace("-", ""):
            return arch
    return None


def list_archetypes(domain: str | None = None) -> list[ArchetypeDefinition]:
    """Return all registered archetypes, optionally filtered by domain."""
    if domain:
        norm_domain = _normalize_token(domain)
        return [
            arch for arch in ARCHETYPES.values()
            if _normalize_token(arch.domain) == norm_domain
        ]
    return list(ARCHETYPES.values())


def match_archetypes(
    role: str,
    outcomes: list[str],
    archetype: str | None = None,
) -> list[ArchetypeDefinition]:
    """Identify archetypes matching a role, outcome targets, or explicit archetype flag."""
    matches: list[ArchetypeDefinition] = []
    seen_ids: set[str] = set()

    # 1. Explicit archetype parameter takes top priority
    if archetype:
        exact = get_archetype(archetype)
        if exact:
            matches.append(exact)
            seen_ids.add(exact.id)

    # 2. Extract tokens from role and outcomes
    tokens: set[str] = set()
    for text in [role, *outcomes]:
        for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text.casefold()):
            tokens.add(token)

    # 3. Check keywords across all archetypes
    for arch in ARCHETYPES.values():
        if arch.id in seen_ids:
            continue
        keyword_set = set(arch.keywords)
        if tokens.intersection(keyword_set):
            matches.append(arch)
            seen_ids.add(arch.id)

    return matches


def archetype_to_family(archetype: ArchetypeDefinition) -> dict[str, Any]:
    """Convert an ArchetypeDefinition into a capability family specification."""
    return {
        "id": archetype.id,
        "name": archetype.name,
        "layers": list(archetype.layers),
        "targets": list(archetype.targets),
        "invariants": list(archetype.invariants),
        "tools": list(archetype.tools),
        "verification_gates": list(archetype.verification_gates),
        "teaching_transfer": archetype.teaching_transfer,
        "status": "research-and-verify",
    }


def archetype_report(archetype: ArchetypeDefinition) -> str:
    """Format a detailed human-readable report of an archetype."""
    lines = [
        f"# {archetype.name} ({archetype.lineage})",
        "",
        f"**ID:** `{archetype.id}` | **Domain:** `{archetype.domain}`",
        f"**Scope:** {archetype.description}",
        "",
        "## First-Principles Invariants",
    ]
    for inv in archetype.invariants:
        lines.append(f"- {inv}")
    lines.extend([
        "",
        "## Capability Targets",
    ])
    for target in archetype.targets:
        lines.append(f"- {target}")
    lines.extend([
        "",
        "## Domain-Native Tools",
    ])
    for tool in archetype.tools:
        lines.append(f"- `{tool}`")
    lines.extend([
        "",
        "## Verification Gates",
    ])
    for gate in archetype.verification_gates:
        lines.append(f"- [ ] {gate}")
    lines.extend([
        "",
        "## Teaching Transfer Challenge",
        archetype.teaching_transfer,
        "",
    ])
    return "\n".join(lines)


def archetype_catalog_report(domain: str | None = None) -> str:
    """Generate a catalog of all registered Genius Lineage Archetypes."""
    archetypes = list_archetypes(domain)
    lines = [
        "# Genius Lineage Archetype Catalog",
        "",
        f"Total Registered Archetypes: **{len(archetypes)}**",
        "",
        "| ID | Archetype | Domain | Description |",
        "|---|---|---|---|",
    ]
    for arch in archetypes:
        lines.append(f"| `{arch.id}` | **{arch.name}** | {arch.domain} | {arch.description} |")
    lines.append("")
    return "\n".join(lines)
