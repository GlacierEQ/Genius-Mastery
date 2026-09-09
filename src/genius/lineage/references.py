"""Authoritative Reference Libraries for all 26 Genius Lineage domains.

Grounds each domain in canonical standards, peer-reviewed publications,
statutory rules, and living technical documentation to maintain cutting-edge
accuracy from first principles.
"""
from __future__ import annotations
from typing import Any

DOMAIN_REFERENCES: dict[str, list[dict[str, Any]]] = {
    "aerospace": [
        {
            "title": "NASA SP-8000 Space Vehicle Flight Dynamics & Astrodynamics Series",
            "url": "https://ntrs.nasa.gov/",
            "type": "Technical Specification",
            "authority": "NASA National Technical Reports Server",
            "relevance": "Orbital trajectory propagation, perturbation modeling, and boundary value solutions."
        },
        {
            "title": "NASA Cryogenic Boil-Off Thermodynamic and Mass Loss Formulation",
            "url": "https://ntrs.nasa.gov/citations/20200001859",
            "type": "Engineering Standard",
            "authority": "NASA Marshall Space Flight Center",
            "relevance": "Cryogenic liquid hydrogen/methane boil-off rates: dm/dt = -Q_leak / Delta_H_vap."
        },
        {
            "title": "JPL HORIZONS System & Ephemeris Computation Service",
            "url": "https://ssd.jpl.nasa.gov/horizons/",
            "type": "Living API & Reference Data",
            "authority": "NASA Jet Propulsion Laboratory (JPL)",
            "relevance": "High-accuracy planetary ephemerides, state vectors, and orbital elements."
        },
        {
            "title": "Fundamentals of Astrodynamics (Bate, Mueller, White)",
            "url": "https://store.doverpublications.com/0486600610.html",
            "type": "Foundational Textbook",
            "authority": "US Air Force Academy / Dover Publications",
            "relevance": "Vis-viva equation, Kepler's laws, Lambert targeting, and orbital maneuvers."
        },
        {
            "title": "SpaceX Starship & Falcon 9 Flight Software Architecture Principles",
            "url": "https://www.spacex.com/",
            "type": "Industry Doctrine",
            "authority": "SpaceX Flight Software Group",
            "relevance": "Real-time telemetry verification, autonomous abort limits, and engine sequencing."
        }
    ],

    "microcode": [
        {
            "title": "Intel 64 and IA-32 Architectures Software Developer's Manual (Vols 1-4)",
            "url": "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html",
            "type": "Hardware Architecture Specification",
            "authority": "Intel Corporation",
            "relevance": "Instruction decoding, micro-op translation, register renaming, and execution cycles."
        },
        {
            "title": "Arm Architecture Reference Manual Armv9-A",
            "url": "https://developer.arm.com/documentation/ddi0487/latest/",
            "type": "Instruction Set Architecture Spec",
            "authority": "Arm Limited",
            "relevance": "Superscalar pipeline hazard mitigation, register dependency tracking, and SIMD."
        },
        {
            "title": "Linux Kernel eBPF Instruction Set & Verification Architecture",
            "url": "https://docs.kernel.org/bpf/",
            "type": "Kernel Architecture Documentation",
            "authority": "Linux Kernel Organization",
            "relevance": "eBPF stack bounds verification (512-byte limit), register liveness, and static analysis."
        },
        {
            "title": "Agner Fog's Instruction Tables and Microarchitecture Guides",
            "url": "https://www.agner.org/optimize/",
            "type": "Benchmark & Optimization Canon",
            "authority": "Technical University of Denmark (DTU)",
            "relevance": "Latency, throughput, and execution port dispatch for modern x86/x64 microarchitectures."
        },
        {
            "title": "LLVM Target Independent Code Generator & Instruction Scheduling",
            "url": "https://llvm.org/docs/CodeGenerator.html",
            "type": "Compiler Architecture Reference",
            "authority": "LLVM Project",
            "relevance": "DAG scheduling, RAW/WAR/WAW hazard detection, and register allocation."
        }
    ],

    "nanosphere": [
        {
            "title": "NIST Chemistry WebBook: Thermophysical Properties of Fluid Systems",
            "url": "https://webbook.nist.gov/chemistry/",
            "type": "Living Scientific Database",
            "authority": "National Institute of Standards and Technology (NIST)",
            "relevance": "Intermolecular potential parameters (epsilon, sigma) for Lennard-Jones dynamics."
        },
        {
            "title": "LAMMPS Molecular Dynamics Simulator Documentation",
            "url": "https://docs.lammps.org/",
            "type": "Computational Physics Platform",
            "authority": "Sandia National Laboratories",
            "relevance": "Symplectic integration, NVE/NVT ensembles, and interatomic force calculation."
        },
        {
            "title": "The Materials Project Database & API",
            "url": "https://materialsproject.org/",
            "type": "Materials Informatics Platform",
            "authority": "Lawrence Berkeley National Laboratory",
            "relevance": "Crystal lattice parameters (FCC, BCC, HCP) and density functional theory structures."
        },
        {
            "title": "Introduction to Solid State Physics (Charles Kittel)",
            "url": "https://www.wiley.com/en-us/Introduction+to+Solid+State+Physics%2C+8th+Edition-p-9780471415268",
            "type": "Academic Canon",
            "authority": "UC Berkeley / John Wiley & Sons",
            "relevance": "de Broglie quantum confinement, Brillouin zones, and lattice phonon vibrations."
        }
    ],

    "security": [
        {
            "title": "NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems",
            "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
            "type": "Federal Security Standard",
            "authority": "NIST Computer Security Resource Center",
            "relevance": "Cryptographic protection, boundary control, and continuous monitoring controls."
        },
        {
            "title": "OWASP Top 10 Application Security Risks & ASVS",
            "url": "https://owasp.org/www-project-top-ten/",
            "type": "Industry Security Standard",
            "authority": "Open Web Application Security Project (OWASP)",
            "relevance": "Injection prevention, data taint tracking, and sanitization verification."
        },
        {
            "title": "RFC 2104: HMAC: Keyed-Hashing for Message Authentication",
            "url": "https://datatracker.ietf.org/doc/html/rfc2104",
            "type": "Internet Standard",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "Cryptographic authentication, constant-time comparison, and integrity validation."
        },
        {
            "title": "MITRE Common Weakness Enumeration (CWE) Corpus",
            "url": "https://cwe.mitre.org/",
            "type": "Vulnerability Encyclopedia",
            "authority": "The MITRE Corporation",
            "relevance": "Formal taxonomy of memory safety, race conditions, and cryptographic flaws."
        }
    ],

    "energy": [
        {
            "title": "NERC Reliability Standards for the Bulk Power System",
            "url": "https://www.nerc.com/pa/Stand/Pages/ReliabilityStandards.aspx",
            "type": "Regulatory Standard",
            "authority": "North American Electric Reliability Corporation (NERC)",
            "relevance": "Frequency response standards, governor droop response: dP = -(1/R) * df."
        },
        {
            "title": "US DOE / Idaho National Lab Battery Test Manual for Electric Vehicles",
            "url": "https://www.energy.gov/eere/vehicles/vehicle-technologies-office",
            "type": "Technical Standard",
            "authority": "US Department of Energy (DOE) / INL",
            "relevance": "State of Charge (SoC) Coulomb counting and electrochemical cycle degradation."
        },
        {
            "title": "IEEE 1547-2018: Standard for Interconnection of Distributed Energy Resources",
            "url": "https://standards.ieee.org/ieee/1547/5911/",
            "type": "IEEE Standard",
            "authority": "Institute of Electrical and Electronics Engineers (IEEE)",
            "relevance": "Grid synchronization, voltage/frequency trip bounds, and reactive power injection."
        },
        {
            "title": "Thermodynamics and an Introduction to Thermostatistics (Herbert Callen)",
            "url": "https://www.wiley.com/en-us/Thermodynamics+and+an+Introduction+to+Thermostatistics%2C+2nd+Edition-p-9780471862567",
            "type": "Academic Canon",
            "authority": "University of Pennsylvania / John Wiley & Sons",
            "relevance": "First and Second Laws of Thermodynamics, Carnot efficiency limit: eta = 1 - Tc/Th."
        }
    ],

    "physics": [
        {
            "title": "Course of Theoretical Physics: Vol 1 Mechanics (Landau & Lifshitz)",
            "url": "https://www.elsevier.com/books/mechanics/landau/978-0-7506-2896-9",
            "type": "Theoretical Physics Canon",
            "authority": "Pergamon Press / Elsevier",
            "relevance": "Lagrangian action principle, Hamiltonian dynamics, and Noether's conservation theorems."
        },
        {
            "title": "Geometric Numerical Integration: Structure-Preserving Algorithms (Hairer et al.)",
            "url": "https://link.springer.com/book/10.1007/3-540-30666-8",
            "type": "Mathematical Monograph",
            "authority": "Springer Science & Business Media",
            "relevance": "Symplectic Velocity Verlet integration and long-term energy conservation in Hamiltonian systems."
        },
        {
            "title": "NIST Reference on Constants, Units, and Uncertainty (CODATA)",
            "url": "https://physics.nist.gov/cuu/Constants/",
            "type": "Living Scientific Standard",
            "authority": "National Institute of Standards and Technology (NIST)",
            "relevance": "Fundamental physical constants (speed of light c, Planck constant h, gravitational constant G)."
        },
        {
            "title": "CERN ROOT High Energy Physics Framework & Numerical Libraries",
            "url": "https://root.cern/",
            "type": "Scientific Software Framework",
            "authority": "European Organization for Nuclear Research (CERN)",
            "relevance": "Numerical analysis, particle kinematics, and relativistic transformation algorithms."
        }
    ],

    "chemistry": [
        {
            "title": "IUPAC Compendium of Chemical Terminology (Gold Book)",
            "url": "https://goldbook.iupac.org/",
            "type": "International Scientific Standard",
            "authority": "International Union of Pure and Applied Chemistry (IUPAC)",
            "relevance": "Standardized chemical nomenclature, thermodynamic state functions, and reaction kinetics."
        },
        {
            "title": "NIST Chemical Kinetics Database",
            "url": "https://kinetics.nist.gov/",
            "type": "Living Experimental Database",
            "authority": "National Institute of Standards and Technology (NIST)",
            "relevance": "Arrhenius kinetic rate coefficients, activation energies, and pre-exponential factors."
        },
        {
            "title": "Cantera: Software Toolkit for Chemical Kinetics and Thermodynamics",
            "url": "https://cantera.org/",
            "type": "Open-Source Simulation Suite",
            "authority": "Cantera Developers / Caltech",
            "relevance": "Gibbs free energy minimization, equilibrium composition, and stoichiometric balancing."
        },
        {
            "title": "Atkins' Physical Chemistry (Peter Atkins, Julio de Paula)",
            "url": "https://global.oup.com/academic/product/atkins-physical-chemistry-9780198814740",
            "type": "Foundational Textbook",
            "authority": "Oxford University Press",
            "relevance": "Chemical potential, reaction quotient Q, equilibrium constant K, and phase diagrams."
        }
    ],

    "biology": [
        {
            "title": "NCBI Entrez Programming Utilities (E-utilities) API",
            "url": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
            "type": "Living Genomic API",
            "authority": "National Center for Biotechnology Information (NCBI) / NIH",
            "relevance": "GenBank nucleotide sequences, protein translation tables, and codon bias lookup."
        },
        {
            "title": "Smith & Waterman (1981): Identification of Common Molecular Subsequences",
            "url": "https://doi.org/10.1016/0022-2836(81)90087-5",
            "type": "Seminal Peer-Reviewed Paper",
            "authority": "Journal of Molecular Biology",
            "relevance": "Dynamic programming formulation for optimal local sequence alignment with gap penalties."
        },
        {
            "title": "Michaelis & Menten (1913): Kinetics of Invertin Action",
            "url": "https://doi.org/10.1016/j.febslet.2013.07.015",
            "type": "Historical Scientific Canon",
            "authority": "FEBS Letters Translation",
            "relevance": "Enzyme reaction rate kinetics: v = (Vmax * [S]) / (Km + [S])."
        },
        {
            "title": "The Biopython Structural and Sequence Analysis Architecture",
            "url": "https://biopython.org/wiki/Documentation",
            "type": "Bioinformatics Platform",
            "authority": "Biopython Project",
            "relevance": "Central Dogma sequence translation, open reading frames, and biological matrices."
        }
    ],

    "law": [
        {
            "title": "Federal Rules of Evidence (FRE), Rule 902(13) & 902(14)",
            "url": "https://www.law.cornell.edu/rules/fre/rule_902",
            "type": "Federal Statutory Rule",
            "authority": "Supreme Court of the United States / Legal Information Institute",
            "relevance": "Self-authenticating electronic data generated by electronic process or system with digital hash verification."
        },
        {
            "title": "Hawaii Rules of Civil Procedure (HRCP) & District Court Rules",
            "url": "https://www.courts.state.hi.us/legal_references/court_rules",
            "type": "State Judicial Rules",
            "authority": "Hawaii State Judiciary",
            "relevance": "Pleading caption standards, certificate of service, and jurisdictional pleading requirements."
        },
        {
            "title": "Electronic Discovery Reference Model (EDRM) Standards",
            "url": "https://edrm.net/",
            "type": "Legal Technology Standard",
            "authority": "Duke Law Center for Judicial Studies / EDRM",
            "relevance": "Bates stamping continuity, chain of custody preservation, and forensic ingestion."
        },
        {
            "title": "NIST SP 800-86: Guide to Integrating Forensic Techniques into Incident Response",
            "url": "https://csrc.nist.gov/publications/detail/sp/800-86/final",
            "type": "Forensic Standard",
            "authority": "National Institute of Standards and Technology (NIST)",
            "relevance": "Cryptographic hash chaining, tamper-evident evidence custody, and forensic integrity."
        }
    ],

    "document-processing": [
        {
            "title": "ISO 32000-2:2020 (PDF 2.0 Specification)",
            "url": "https://www.pdfa.org/resource/iso-32000-2/",
            "type": "International Standard",
            "authority": "International Organization for Standardization (ISO) / PDF Association",
            "relevance": "Document structure, content streams, text operators, font encoding, and bounding boxes."
        },
        {
            "title": "Unicode Standard Annex #29: Unicode Text Segmentation",
            "url": "https://www.unicode.org/reports/tr29/",
            "type": "Unicode Technical Report",
            "authority": "The Unicode Consortium",
            "relevance": "Grapheme cluster boundaries, word segmentation, and lossless character offset preservation."
        },
        {
            "title": "W3C Document Object Model (DOM) Architecture",
            "url": "https://www.w3.org/DOM/",
            "type": "Web Architecture Standard",
            "authority": "World Wide Web Consortium (W3C)",
            "relevance": "Hierarchical document AST representation (nodes, attributes, coordinates, and bounding geometries)."
        },
        {
            "title": "LayoutLM: Pre-training of Text and Layout for Document Image Understanding",
            "url": "https://arxiv.org/abs/1912.13318",
            "type": "Frontier Research Paper",
            "authority": "Microsoft Research",
            "relevance": "2D spatial coordinate positional embeddings and tabular structure extraction."
        }
    ],

    "document-generation": [
        {
            "title": "ISO 19005-1:2005 (PDF/A-1 Specification for Archival Preservation)",
            "url": "https://www.pdfa.org/resource/iso-19005-1/",
            "type": "International Standard",
            "authority": "International Organization for Standardization (ISO)",
            "relevance": "Embedded fonts, device-independent color spaces, and XMP metadata requirements."
        },
        {
            "title": "The Elements of Typographic Style (Robert Bringhurst)",
            "url": "https://hartleyandmarks.com/books/the-elements-of-typographic-style/",
            "type": "Typographic Canon",
            "authority": "Hartley & Marks Publishers",
            "relevance": "Vertical rhythm, baseline grid mathematical alignment, and optical margins."
        },
        {
            "title": "Knuth & Plass (1981): Breaking Paragraphs into Lines",
            "url": "https://doi.org/10.1002/spe.4380111102",
            "type": "Seminal Algorithm Paper",
            "authority": "Software: Practice and Experience",
            "relevance": "Optimal dynamic programming line breaking, hyphenation penalties, and typographic aesthetics."
        },
        {
            "title": "CommonMark Specification",
            "url": "https://spec.commonmark.org/",
            "type": "Document Syntax Standard",
            "authority": "CommonMark Project",
            "relevance": "Deterministic, unambiguous AST parsing and compilation of Markdown into formatted documents."
        }
    ],

    "metadata-depth": [
        {
            "title": "RFC 7693: The BLAKE2 Cryptographic Hash and Message Authentication Code (MAC)",
            "url": "https://datatracker.ietf.org/doc/html/rfc7693",
            "type": "Internet Standard",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "High-performance cryptographic hashing (Blake2b) for dual-hash immutable receipts."
        },
        {
            "title": "FIPS PUB 180-4: Secure Hash Standard (SHS / SHA-256)",
            "url": "https://csrc.nist.gov/publications/detail/fips/180/4/final",
            "type": "Federal Information Processing Standard",
            "authority": "National Institute of Standards and Technology (NIST)",
            "relevance": "Cryptographic 256-bit collision resistance and forensic evidence verification."
        },
        {
            "title": "W3C PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "type": "W3C Recommendation",
            "authority": "World Wide Web Consortium (W3C)",
            "relevance": "Data provenance modeling: Entities, Activities, Agents, and Directed Acyclic Lineage Graphs."
        },
        {
            "title": "Lamport (1978): Time, Clocks, and the Ordering of Events in a Distributed System",
            "url": "https://doi.org/10.1145/359545.359563",
            "type": "Seminal Systems Paper",
            "authority": "Communications of the ACM",
            "relevance": "Logical clocks, partial ordering, monotonic timestamps, and causal DAG consistency."
        }
    ],

    "filesystem": [
        {
            "title": "POSIX.1-2024 (IEEE Std 1003.1-2024) Standard for Information Technology",
            "url": "https://pubs.opengroup.org/onlinepubs/9699919799/",
            "type": "POSIX Standard",
            "authority": "The Open Group / IEEE Computer Society",
            "relevance": "Atomic file rename (rename() system call), fsync durability, and file descriptor semantics."
        },
        {
            "title": "Linux Kernel Filesystem Architecture (VFS, Ext4, XFS)",
            "url": "https://docs.kernel.org/filesystems/",
            "type": "Kernel Architecture Documentation",
            "authority": "Linux Kernel Organization",
            "relevance": "Inode management, extent block allocation, journaling layers, and crash consistency."
        },
        {
            "title": "Mohan et al. (1992): ARIES: A Transaction Recovery Method",
            "url": "https://doi.org/10.1145/128765.128770",
            "type": "Seminal Database Systems Paper",
            "authority": "ACM Transactions on Database Systems",
            "relevance": "Write-ahead logging (WAL) protocol: Write log before page, compensation log records, and redo/undo recovery."
        },
        {
            "title": "SQLite Write-Ahead Logging (WAL) Architecture",
            "url": "https://sqlite.org/wal.html",
            "type": "Database System Architecture",
            "authority": "SQLite Development Team",
            "relevance": "Append-only commit logs, checkpointing algorithms, and reader/writer concurrency."
        }
    ],

    "cloud-database": [
        {
            "title": "Ongaro & Ousterhout (2014): In Search of an Understandable Consensus Algorithm (Raft)",
            "url": "https://raft.github.io/raft.pdf",
            "type": "Distributed Systems Paper",
            "authority": "Stanford University / USENIX ATC '14",
            "relevance": "Leader election, term monotonicity, log replication, and quorum safety (votes > N/2)."
        },
        {
            "title": "Berenson et al. (1995): A Critique of ANSI SQL Isolation Levels",
            "url": "https://doi.org/10.1145/223784.223785",
            "type": "Seminal Database Research",
            "authority": "ACM SIGMOD",
            "relevance": "Multi-Version Concurrency Control (MVCC) snapshot isolation and write skew anomaly detection."
        },
        {
            "title": "Corbett et al. (2013): Spanner: Google's Globally-Distributed Database",
            "url": "https://research.google/pubs/pub39966/",
            "type": "Production Systems Paper",
            "authority": "Google Research / ACM TOCS",
            "relevance": "External consistency, two-phase commit over Paxos, and distributed multi-version timestamping."
        },
        {
            "title": "Jepsen Distributed Systems Analysis and Verification Archive",
            "url": "https://jepsen.io/analyses",
            "type": "Living Systems Verification Portal",
            "authority": "Jepsen LLC (Kyle Kingsbury)",
            "relevance": "Formal verification of linearizability, serializability, and network partition failure modes."
        }
    ],

    "device": [
        {
            "title": "PCI-SIG PCI Express Base Specification Revision 6.0",
            "url": "https://pcisig.com/specifications",
            "type": "Hardware Interconnect Standard",
            "authority": "PCI-SIG",
            "relevance": "Memory-Mapped I/O (MMIO), Transaction Layer Packets (TLPs), and DMA bus mastering."
        },
        {
            "title": "Linux Kernel Driver API: Direct Memory Access (DMA) Mapping Guide",
            "url": "https://docs.kernel.org/core-api/dma-api.html",
            "type": "Kernel Architecture Documentation",
            "authority": "Linux Kernel Organization",
            "relevance": "Cache coherency maintenance (dma_sync_single_for_cpu vs dma_sync_single_for_device)."
        },
        {
            "title": "Liu & Layland (1973): Scheduling Algorithms for Hard-Real-Time Environment",
            "url": "https://doi.org/10.1145/321738.321743",
            "type": "Seminal Real-Time Systems Paper",
            "authority": "Journal of the ACM",
            "relevance": "Rate-monotonic scheduling, interrupt latency deadlines, and worst-case execution bounds."
        },
        {
            "title": "ARM CoreLink Cache Coherent Interconnect Architecture",
            "url": "https://developer.arm.com/architectures/system-architectures",
            "type": "Hardware Architecture Manual",
            "authority": "Arm Limited",
            "relevance": "Hardware snooping, memory barriers (DMB/DSB/ISB), and volatile peripheral registers."
        }
    ],

    "pc": [
        {
            "title": "Intel 64 and IA-32 Architectures Software Developer's Manual (Vol 3A: Paging)",
            "url": "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html",
            "type": "System Programming Guide",
            "authority": "Intel Corporation",
            "relevance": "4-Level paging address translation: PML4 -> PDPT -> PD -> PT -> 4KB Physical Page Offset."
        },
        {
            "title": "Advanced Configuration and Power Interface (ACPI) Specification Version 6.5",
            "url": "https://uefi.org/specs/ACPI/6.5/",
            "type": "Industry Power Specification",
            "authority": "UEFI Forum",
            "relevance": "Global system states (S0 Working, S3 Standby, S4 Hibernate, S5 Soft Off) and transition invariants."
        },
        {
            "title": "Microsoft Authenticode PE Signature & Verification Specification",
            "url": "https://learn.microsoft.com/en-us/windows-hardware/drivers/install/authenticode",
            "type": "Operating System Specification",
            "authority": "Microsoft Corporation",
            "relevance": "Portable Executable (PE) header parsing, DOS header e_lfanew, and Certificate Table parsing."
        },
        {
            "title": "UEFI Specification Version 2.10",
            "url": "https://uefi.org/specifications",
            "type": "Firmware Standard",
            "authority": "Unified Extensible Firmware Interface (UEFI) Forum",
            "relevance": "Secure Boot validation, EFI system table, and firmware handover to OS kernel."
        }
    ],

    "mac": [
        {
            "title": "Apple Developer Documentation: Mach Kernel Architecture & Port Rights",
            "url": "https://developer.apple.com/documentation/kernel",
            "type": "Operating System Architecture Guide",
            "authority": "Apple Inc.",
            "relevance": "Mach port semantics: send rights, receive rights, dead names, and port leak prevention."
        },
        {
            "title": "Apple Silicon Unified Memory Architecture & Metal Shading Guidelines",
            "url": "https://developer.apple.com/metal/",
            "type": "System Architecture Guide",
            "authority": "Apple Developer",
            "relevance": "Zero-copy shared memory between CPU, GPU, and Apple Neural Engine (ANE)."
        },
        {
            "title": "Inside Code Signing: Requirements, Rules, and Entitlements (TN3125)",
            "url": "https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles",
            "type": "Security Technical Note",
            "authority": "Apple Developer Technical Support",
            "relevance": "Code directory hashing, entitlement plist validation, App Sandbox, and hardened runtime."
        },
        {
            "title": "Darwin XNU Operating System Source Repository",
            "url": "https://github.com/apple-oss-distributions/xnu",
            "type": "Open Source Operating System",
            "authority": "Apple Open Source",
            "relevance": "Kernel task ports, IPC message passing, and virtual memory subsystem."
        }
    ],

    "linux": [
        {
            "title": "Axboe (2019): Efficient IO with io_uring",
            "url": "https://kernel.dk/io_uring.pdf",
            "type": "Systems Architecture Paper",
            "authority": "Jens Axboe (Linux Kernel IO Subsystem Maintainer)",
            "relevance": "Submission Queue (SQ) and Completion Queue (CQ) ring buffers with memory barrier coordination."
        },
        {
            "title": "Linux Control Group v2 (cgroup v2) Architecture",
            "url": "https://docs.kernel.org/admin-guide/cgroup-v2.html",
            "type": "Kernel Documentation",
            "authority": "Linux Kernel Organization",
            "relevance": "Single hierarchy tree rule, memory.max limits, and child-to-ancestor resource charging."
        },
        {
            "title": "Linux Namespaces Architecture (namespaces(7))",
            "url": "https://man7.org/linux/man-pages/man7/namespaces.7.html",
            "type": "System Programming Manual",
            "authority": "Michael Kerrisk (Linux man-pages Project)",
            "relevance": "PID, Network, Mount, IPC, and UTS isolation invariants and clone flags."
        },
        {
            "title": "The Linux Programming Interface (Michael Kerrisk)",
            "url": "https://man7.org/tlpi/",
            "type": "Definitive Systems Programming Book",
            "authority": "No Starch Press",
            "relevance": "Low-level Linux system call semantics, signals, memory locking, and process isolation."
        }
    ],

    "android": [
        {
            "title": "Android Open Source Project (AOSP) Binder IPC Architecture",
            "url": "https://source.android.com/docs/core/architecture/hidl/binder-ipc",
            "type": "Platform Architecture Documentation",
            "authority": "Google Android Open Source Project",
            "relevance": "Binder flat parcel serialization, transaction codes, and kernel /dev/binder driver."
        },
        {
            "title": "Dalvik Executable (DEX) Format Specification",
            "url": "https://source.android.com/docs/core/runtime/dex-format",
            "type": "Virtual Machine Specification",
            "authority": "Google AOSP",
            "relevance": "DEX header magic ('dex\\n039\\0'), adler32 checksum, and SHA-1 signature validation."
        },
        {
            "title": "Android Interface Definition Language (AIDL) Guide",
            "url": "https://developer.android.com/guide/components/aidl",
            "type": "Developer API Guide",
            "authority": "Google Android Developers",
            "relevance": "Interprocess communication contracts, onTransact dispatch, and proxy/stub boundaries."
        },
        {
            "title": "Android Runtime (ART) Garbage Collection and Memory Model",
            "url": "https://source.android.com/docs/core/runtime",
            "type": "Runtime Architecture Documentation",
            "authority": "Google AOSP",
            "relevance": "Concurrent copy (CC) garbage collection, ahead-of-time (AOT) compilation, and compacting heaps."
        }
    ],

    "ios": [
        {
            "title": "Swift Evolution SE-0306: Actors",
            "url": "https://github.com/swiftlang/swift-evolution/blob/main/proposals/0306-actors.md",
            "type": "Language Design Specification",
            "authority": "Swift Language Steering Group",
            "relevance": "Data race elimination, actor mailbox isolation, and asynchronous FIFO message ordering."
        },
        {
            "title": "Apple Security: Pointer Authentication on ARM64e Architecture",
            "url": "https://support.apple.com/guide/security/pointer-authentication-codes-sec2a3a5e8e3/web",
            "type": "Security Whitepaper",
            "authority": "Apple Security Engineering and Architecture (SEAR)",
            "relevance": "ARM64e Pointer Authentication Codes (PAC), context keys, and control flow integrity."
        },
        {
            "title": "Apple Developer: Optimizing ProMotion Display Refresh Rates (120Hz)",
            "url": "https://developer.apple.com/documentation/quartzcore/cadisplaylink",
            "type": "Framework API Guide",
            "authority": "Apple Developer",
            "relevance": "Frame pacing budgets (8.33ms at 120fps vs 16.66ms at 60fps), hitch detection, and CADisplayLink."
        },
        {
            "title": "The Swift Programming Language Book",
            "url": "https://www.swift.org/documentation/",
            "type": "Official Language Guide",
            "authority": "Apple / Swift.org",
            "relevance": "Structured concurrency, tasks, actors, isolation domains, and memory ownership rules."
        }
    ],

    "email": [
        {
            "title": "RFC 5322: Internet Message Format (MIME Syntax)",
            "url": "https://datatracker.ietf.org/doc/html/rfc5322",
            "type": "Internet Standard",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "Standardized email header syntax, unfolded lines, address specification, and MIME body."
        },
        {
            "title": "RFC 6376: DomainKeys Identified Mail (DKIM) Signatures",
            "url": "https://datatracker.ietf.org/doc/html/rfc6376",
            "type": "Internet Standard",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "Simple and relaxed canonicalization algorithms, SHA-256 body hash calculation (bh=)."
        },
        {
            "title": "RFC 7208: Sender Policy Framework (SPF) for Authorizing IP Addresses",
            "url": "https://datatracker.ietf.org/doc/html/rfc7208",
            "type": "Proposed Standard",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "DNS SPF record parsing, ip4/ip6 mechanisms, and qualifiers (+, -, ~, ?)."
        },
        {
            "title": "RFC 7489: Domain-based Message Authentication, Reporting, and Conformance (DMARC)",
            "url": "https://datatracker.ietf.org/doc/html/rfc7489",
            "type": "Informational RFC",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "Domain alignment evaluation, SPF/DKIM validation pass/fail policy actions (none, quarantine, reject)."
        }
    ],

    "automation": [
        {
            "title": "RFC 7231 / HTTP 1.1 Semantics: Idempotent Methods Definition",
            "url": "https://datatracker.ietf.org/doc/html/rfc7231#section-4.2.2",
            "type": "Internet Standard",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "Mathematical definition of idempotency: f(f(x)) = f(x) and side-effect invariance."
        },
        {
            "title": "Brooker (2015): Exponential Backoff And Jitter",
            "url": "https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/",
            "type": "Systems Architecture Whitepaper",
            "authority": "Amazon Web Services (AWS) Architecture",
            "relevance": "Full-jitter exponential backoff algorithm to resolve thundering herd problem in distributed systems."
        },
        {
            "title": "Garcia-Molina & Salem (1987): Sagas",
            "url": "https://doi.org/10.1145/38713.38742",
            "type": "Seminal Distributed Database Paper",
            "authority": "ACM SIGMOD",
            "relevance": "Long-lived distributed transactions, forward step execution, and backward compensating transactions."
        },
        {
            "title": "Temporal Architecture & Distributed Workflow Determinism",
            "url": "https://docs.temporal.io/temporal",
            "type": "Orchestration Architecture Manual",
            "authority": "Temporal Technologies",
            "relevance": "Stateful workflow event replay, activity idempotency, and saga failure compensation."
        }
    ],

    "model-weights": [
        {
            "title": "Dettmers et al. (2022): LLM.int8(): 8-bit Matrix Multiplication for Transformers",
            "url": "https://arxiv.org/abs/2208.07339",
            "type": "Frontier AI Research Paper",
            "authority": "University of Washington / Meta AI",
            "relevance": "Symmetric uniform INT8 quantization, outlier feature preservation, and scale factor calibration."
        },
        {
            "title": "Su et al. (2021): RoFormer: Enhanced Transformer with Rotary Position Embedding (RoPE)",
            "url": "https://arxiv.org/abs/2104.09864",
            "type": "Seminal Representation Learning Paper",
            "authority": "ArXiv / Zhuiyi Technology",
            "relevance": "Rotary position embedding 2D block-diagonal unitary rotation matrix and distance decay properties."
        },
        {
            "title": "Kwon et al. (2023): Efficient Memory Management for Large Language Model Serving with PagedAttention",
            "url": "https://arxiv.org/abs/2309.06180",
            "type": "Systems for AI Paper",
            "authority": "UC Berkeley (SOSP '23)",
            "relevance": "Paged KV-cache virtual memory allocation, zero internal fragmentation, and shared block tables."
        },
        {
            "title": "Dao et al. (2022): FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness",
            "url": "https://arxiv.org/abs/2205.14135",
            "type": "GPU Kernel Architecture Paper",
            "authority": "Stanford University (NeurIPS '22)",
            "relevance": "Tiling, SRAM IO minimization, and online softmax normalization for attention computation."
        }
    ],

    "spiritual-awareness": [
        {
            "title": "Gandhi - The Story of My Experiments with Truth (Ahimsa & Satyagraha)",
            "url": "https://www.mkgandhi.org/autobio/autobio.htm",
            "type": "Philosophical Canon",
            "authority": "Navajivan Publishing House",
            "relevance": "Ahimsa (non-harm) operational boundary and ethical adherence to truth without compromise."
        },
        {
            "title": "United Nations Universal Declaration of Human Rights (UDHR)",
            "url": "https://www.un.org/en/about-us/universal-declaration-of-human-rights",
            "type": "International Covenant",
            "authority": "United Nations General Assembly",
            "relevance": "Inviolable human dignity, sovereignty, freedom from degrading treatment, and equality."
        },
        {
            "title": "Stanford Encyclopedia of Philosophy: Epistemic Humility",
            "url": "https://plato.stanford.edu/entries/epistemology/",
            "type": "Peer-Reviewed Philosophical Compendium",
            "authority": "Stanford University",
            "relevance": "Calibration of certainty assertions against empirical evidence bounds to eliminate epistemic arrogance."
        },
        {
            "title": "IEEE Ethically Aligned Design: A Vision for Prioritizing Human Well-being in AI",
            "url": "https://standards.ieee.org/industry-connections/ec/ead-v1/",
            "type": "Technical Ethics Standard",
            "authority": "IEEE Global Initiative on Ethics of Autonomous and Intelligent Systems",
            "relevance": "Sovereignty protection, algorithmic transparency, and non-exploitative system architectures."
        }
    ],

    "scifi": [
        {
            "title": "Einstein (1905): On the Electrodynamics of Moving Bodies (Special Relativity)",
            "url": "https://einsteinpapers.press.princeton.edu/vol2-trans/154",
            "type": "Foundational Physics Paper",
            "authority": "Annalen der Physik / Princeton University Press",
            "relevance": "Lorentz transformation factor: gamma = 1 / sqrt(1 - v^2/c^2), time dilation, and cosmic speed limit."
        },
        {
            "title": "Kardashev (1964): Transmission of Information by Extraterrestrial Civilizations",
            "url": "https://ui.adsabs.harvard.edu/abs/1964SvA.....8..217K/abstract",
            "type": "Astrophysical Classification Paper",
            "authority": "Soviet Astronomy / Harvard ADS",
            "relevance": "Energy consumption scale: Type I (10^16 W), Type II (10^26 W), Type III (10^36 W), K = (log10(P) - 6)/10."
        },
        {
            "title": "Thorne (1994): Black Holes and Time Warps: Einstein's Outrageous Legacy",
            "url": "https://wwnorton.com/books/Black-Holes-and-Time-Warps/",
            "type": "Theoretical Physics Monograph",
            "authority": "W. W. Norton & Company",
            "relevance": "Causal timeline topologies, Novikov self-consistency principle, and closed timelike curves."
        },
        {
            "title": "NASA Breakthrough Propulsion Physics Project Archive",
            "url": "https://www.nasa.gov/",
            "type": "Advanced Propulsion Research",
            "authority": "NASA Glenn Research Center",
            "relevance": "Alcubierre metric bounds, negative energy densities, and horizon causality constraints."
        }
    ],

    "nerd-geek": [
        {
            "title": "MOS 6502 Microprocessor Hardware & Programming Manuals",
            "url": "http://www.6502.org/documents/manuals/",
            "type": "Historical Hardware Manual",
            "authority": "MOS Technology / 6502.org Community",
            "relevance": "Accumulator, X/Y index registers, status flags (Z, N, C), zero-page addressing, and clock cycles."
        },
        {
            "title": "IETF Request for Comments (RFC) Complete Index",
            "url": "https://www.ietf.org/standards/rfcs/",
            "type": "Internet Standard Repository",
            "authority": "Internet Engineering Task Force (IETF)",
            "relevance": "Foundational protocols of the Internet (IP, TCP, UDP, DNS, HTTP, SSH, TLS, SMTP)."
        },
        {
            "title": "The Jargon File: The Hacker's Dictionary (Eric S. Raymond)",
            "url": "http://www.catb.org/jargon/",
            "type": "Computing Cultural Canon",
            "authority": "MIT AI Lab / Eric S. Raymond",
            "relevance": "Classical computer science hacker lore, terminology, and first-principles craftsmanship."
        },
        {
            "title": "Pouët.net & Assembly Demo Archives (Demoparty Byte-Golf Heritage)",
            "url": "https://www.pouet.net/",
            "type": "Living Demoscene Archive",
            "authority": "Pouët Demoscene Community",
            "relevance": "Extreme assembly instruction byte-golf optimization (256-byte, 512-byte, 4KB executables)."
        }
    ]
}


def get_domain_references(domain_id: str) -> list[dict[str, Any]]:
    """Return the curated list of reference entries for a given domain."""
    return DOMAIN_REFERENCES.get(domain_id, [])
