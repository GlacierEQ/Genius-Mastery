"""Legal & Enterprise domain implementations and test suites.

Domains:
- law: FRE 902(13)/(14) electronic record verification, contiguous Bates stamping, custody chain.
- document-processing: Layout coordinate AST, lossless UTF-8 token extractor, tabular grid reconstructor.
- document-generation: Deterministic compilation hash, typographic baseline grid, PDF/A metadata checker.
- metadata-depth: Dual Blake2b + SHA-256 paired hashing, monotonic timestamps, provenance DAG validator.
"""
from __future__ import annotations

LEGAL_DOMAINS = {
    "law": {
        "module_name": "genius_law",
        "tools_code": '''"""Genius-Law first-principles domain tools."""
from __future__ import annotations
import hashlib
import time
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class FRE902Certificate:
    record_id: str
    sha256_hash: str
    certified_timestamp: float
    certifier: str
    compliant_rule: str  # "FRE 902(13)" or "FRE 902(14)"

def generate_fre902_certificate(data: bytes, record_id: str, certifier: str, rule: str = "FRE 902(14)") -> FRE902Certificate:
    """Generate self-authenticating electronic record certificate under FRE 902(13)/(14)."""
    h = hashlib.sha256(data).hexdigest()
    return FRE902Certificate(
        record_id=record_id,
        sha256_hash=h,
        certified_timestamp=time.time(),
        certifier=certifier,
        compliant_rule=rule,
    )

def verify_fre902_data(data: bytes, cert: FRE902Certificate) -> bool:
    """Verify data integrity against FRE 902 certificate."""
    return hashlib.sha256(data).hexdigest() == cert.sha256_hash

class BatesStampSequencer:
    """Generates contiguous, monotonic Bates numbering without gaps or duplicates."""
    def __init__(self, prefix: str, start_index: int = 1, padding: int = 6) -> None:
        self.prefix = prefix
        self.current_index = start_index
        self.padding = padding
        self.issued_numbers: list[str] = []

    def next_stamp(self) -> str:
        num_str = str(self.current_index).zfill(self.padding)
        stamp = f"{self.prefix}-{num_str}"
        self.issued_numbers.append(stamp)
        self.current_index += 1
        return stamp

    def verify_contiguity(self) -> bool:
        """Verify issued stamps are strictly sequential with no gaps."""
        if not self.issued_numbers:
            return True
        for i in range(len(self.issued_numbers) - 1):
            curr_num = int(self.issued_numbers[i].split("-")[-1])
            next_num = int(self.issued_numbers[i + 1].split("-")[-1])
            if next_num != curr_num + 1:
                return False
        return True

@dataclass
class CustodyTransfer:
    transfer_id: int
    from_custodian: str
    to_custodian: str
    timestamp: float
    prev_hash: str
    transfer_hash: str

class ExhibitChainOfCustody:
    """Cryptographic hash chain of evidentiary custody transfers."""
    def __init__(self, exhibit_id: str) -> None:
        self.exhibit_id = exhibit_id
        self.transfers: list[CustodyTransfer] = []

    def record_transfer(self, from_custodian: str, to_custodian: str) -> CustodyTransfer:
        prev_h = self.transfers[-1].transfer_hash if self.transfers else "0" * 64
        t_id = len(self.transfers) + 1
        now = time.time()
        payload = f"{t_id}:{self.exhibit_id}:{from_custodian}:{to_custodian}:{now}:{prev_h}"
        t_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        transfer = CustodyTransfer(t_id, from_custodian, to_custodian, now, prev_h, t_hash)
        self.transfers.append(transfer)
        return transfer

    def verify_chain_integrity(self) -> bool:
        for i in range(1, len(self.transfers)):
            if self.transfers[i].prev_hash != self.transfers[i - 1].transfer_hash:
                return False
        return True
''',
        "test_code": '''"""Tests for Genius-Law invariants."""
import pytest
from genius_law.tools import (
    generate_fre902_certificate,
    verify_fre902_data,
    BatesStampSequencer,
    ExhibitChainOfCustody
)

def test_fre902_self_authentication():
    evidence = b"Authentic court record data"
    cert = generate_fre902_certificate(evidence, "EXHIBIT-001", "Qualified Forensics Agent")
    assert verify_fre902_data(evidence, cert) is True
    assert verify_fre902_data(b"Tampered court record", cert) is False

def test_bates_sequencer_contiguity():
    seq = BatesStampSequencer("BARTON", start_index=1, padding=4)
    s1 = seq.next_stamp()
    s2 = seq.next_stamp()
    s3 = seq.next_stamp()
    assert s1 == "BARTON-0001"
    assert s2 == "BARTON-0002"
    assert s3 == "BARTON-0003"
    assert seq.verify_contiguity() is True

def test_chain_of_custody_tamper_detection():
    chain = ExhibitChainOfCustody("EX-A")
    t1 = chain.record_transfer("Intake", "ForensicLab")
    t2 = chain.record_transfer("ForensicLab", "Vault")
    assert chain.verify_chain_integrity() is True

    # Tamper with prev_hash of t2
    chain.transfers[1].prev_hash = "corrupted_hash"
    assert chain.verify_chain_integrity() is False
'''
    },

    "document-processing": {
        "module_name": "genius_document_processing",
        "tools_code": '''"""Genius-DocumentProcessing first-principles domain tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class BoundingBox:
    x0: float
    y0: float
    x1: float
    y1: float

    def __post_init__(self) -> None:
        if self.x0 > self.x1 or self.y0 > self.y1:
            raise ValueError(f"Invalid bounding box coordinates: ({self.x0},{self.y0}) to ({self.x1},{self.y1})")

    def intersects(self, other: BoundingBox) -> bool:
        return not (self.x1 < other.x0 or self.x0 > other.x1 or self.y1 < other.y0 or self.y0 > other.y1)

@dataclass(frozen=True)
class LayoutToken:
    text: str
    bbox: BoundingBox
    char_start: int
    char_end: int

def extract_tokens_lossless(raw_text: str) -> list[tuple[str, int, int]]:
    """Extract tokens while preserving exact character offsets."""
    import re
    tokens: list[tuple[str, int, int]] = []
    for match in re.finditer(r"\\S+", raw_text):
        tokens.append((match.group(0), match.start(), match.end()))
    return tokens

class TabularGridReconstructor:
    """Reconstructs 2D grid matrix from cell bounding boxes and content."""
    def __init__(self, row_threshold: float = 5.0) -> None:
        self.row_threshold = row_threshold

    def reconstruct_grid(self, cells: Sequence[tuple[BoundingBox, str]]) -> list[list[str]]:
        if not cells:
            return []
        # Sort cells vertically (y0) then horizontally (x0)
        sorted_cells = sorted(cells, key=lambda c: (c[0].y0, c[0].x0))
        rows: list[list[tuple[BoundingBox, str]]] = []

        current_row: list[tuple[BoundingBox, str]] = [sorted_cells[0]]
        for cell in sorted_cells[1:]:
            last_y0 = current_row[0][0].y0
            if abs(cell[0].y0 - last_y0) <= self.row_threshold:
                current_row.append(cell)
            else:
                rows.append(sorted(current_row, key=lambda c: c[0].x0))
                current_row = [cell]
        if current_row:
            rows.append(sorted(current_row, key=lambda c: c[0].x0))

        return [[c[1] for c in row] for row in rows]
''',
        "test_code": '''"""Tests for Genius-DocumentProcessing invariants."""
import pytest
from genius_document_processing.tools import (
    BoundingBox,
    LayoutToken,
    extract_tokens_lossless,
    TabularGridReconstructor
)

def test_bounding_box_geometry():
    b1 = BoundingBox(10.0, 10.0, 50.0, 50.0)
    b2 = BoundingBox(40.0, 40.0, 80.0, 80.0)
    b3 = BoundingBox(60.0, 60.0, 90.0, 90.0)
    assert b1.intersects(b2) is True
    assert b1.intersects(b3) is False

    with pytest.raises(ValueError):
        BoundingBox(50.0, 50.0, 10.0, 10.0)

def test_lossless_token_extraction():
    text = "Section 4.1 Legal Precedent"
    tokens = extract_tokens_lossless(text)
    assert len(tokens) == 4
    assert tokens[0] == ("Section", 0, 7)
    assert tokens[1] == ("4.1", 8, 11)
    # verify substring slice matches exactly
    for tok, s, e in tokens:
        assert text[s:e] == tok

def test_tabular_grid_reconstruction():
    reconstructor = TabularGridReconstructor(row_threshold=2.0)
    # 2 rows, 2 cols
    cells = [
        (BoundingBox(0, 0, 10, 5), "R0C0"),
        (BoundingBox(15, 0, 25, 5), "R0C1"),
        (BoundingBox(0, 10, 10, 15), "R1C0"),
        (BoundingBox(15, 10, 25, 15), "R1C1"),
    ]
    grid = reconstructor.reconstruct_grid(cells)
    assert len(grid) == 2
    assert grid[0] == ["R0C0", "R0C1"]
    assert grid[1] == ["R1C0", "R1C1"]
'''
    },

    "document-generation": {
        "module_name": "genius_document_generation",
        "tools_code": '''"""Genius-DocumentGeneration first-principles domain tools."""
from __future__ import annotations
import hashlib
from typing import Any

def deterministic_compile(sections: list[tuple[str, str]]) -> tuple[str, str]:
    """Deterministically compile document sections into unified text and SHA-256 digest."""
    # sections: list of (heading, content)
    output_lines: list[str] = []
    for heading, body in sections:
        output_lines.append(f"# {heading.strip()}")
        output_lines.append(body.strip())
        output_lines.append("")
    compiled = "\\n".join(output_lines)
    digest = hashlib.sha256(compiled.encode("utf-8")).hexdigest()
    return compiled, digest

def validate_vertical_baseline_grid(y_offsets: list[float], baseline_grid_pt: float = 12.0, tol: float = 1e-4) -> bool:
    """Verify that all typographic baseline offsets align to integer multiples of the grid."""
    if baseline_grid_pt <= 0:
        raise ValueError("Baseline grid spacing must be positive")
    for y in y_offsets:
        rem = y % baseline_grid_pt
        if rem > tol and abs(rem - baseline_grid_pt) > tol:
            return False
    return True

def validate_pdfa_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Check required PDF/A archival conformance keys."""
    required = ["pdfaid_part", "pdfaid_conformance", "title", "creator"]
    missing = [k for k in required if k not in metadata or not metadata[k]]
    return {
        "compliant": len(missing) == 0,
        "missing_keys": missing,
        "conformance_level": f"PDF/A-{metadata.get('pdfaid_part', '')}{metadata.get('pdfaid_conformance', '')}"
    }
''',
        "test_code": '''"""Tests for Genius-DocumentGeneration invariants."""
import pytest
from genius_document_generation.tools import (
    deterministic_compile,
    validate_vertical_baseline_grid,
    validate_pdfa_metadata
)

def test_deterministic_compilation():
    sec = [("Introduction", "Case background and doctrine."), ("Analysis", "Invariants hold.")]
    doc1, h1 = deterministic_compile(sec)
    doc2, h2 = deterministic_compile(sec)
    assert doc1 == doc2
    assert h1 == h2
    assert len(h1) == 64

def test_baseline_grid_alignment():
    # Multiples of 12.0
    valid_offsets = [0.0, 12.0, 24.0, 48.0, 120.0]
    assert validate_vertical_baseline_grid(valid_offsets, baseline_grid_pt=12.0) is True

    # Misaligned offset 15.5
    invalid_offsets = [0.0, 12.0, 15.5, 24.0]
    assert validate_vertical_baseline_grid(invalid_offsets, baseline_grid_pt=12.0) is False

def test_pdfa_metadata_validation():
    meta = {
        "pdfaid_part": "1",
        "pdfaid_conformance": "B",
        "title": "Sovereign Pleading",
        "creator": "Genius-Law"
    }
    res = validate_pdfa_metadata(meta)
    assert res["compliant"] is True
    assert res["conformance_level"] == "PDF/A-1B"
'''
    },

    "metadata-depth": {
        "module_name": "genius_metadata_depth",
        "tools_code": '''"""Genius-MetadataDepth first-principles domain tools."""
from __future__ import annotations
import hashlib
from typing import Any

def compute_dual_hashes(data: bytes) -> dict[str, str]:
    """Compute paired SHA-256 and Blake2b cryptographic hashes."""
    sha256_hash = hashlib.sha256(data).hexdigest()
    blake2b_hash = hashlib.blake2b(data).hexdigest()
    return {"sha256": sha256_hash, "blake2b": blake2b_hash}

def validate_monotonic_timestamps(timestamps: list[float]) -> bool:
    """Verify event timestamps strictly progress monotonically without causality reversal."""
    for i in range(len(timestamps) - 1):
        if timestamps[i + 1] < timestamps[i]:
            return False
    return True

class ProvenanceDAG:
    """Validates directed acyclic provenance graph for evidence lineage."""
    def __init__(self) -> None:
        # node -> set of ancestor nodes
        self.adjacency: dict[str, set[str]] = {}

    def add_edge(self, parent: str, child: str) -> None:
        if parent not in self.adjacency:
            self.adjacency[parent] = set()
        if child not in self.adjacency:
            self.adjacency[child] = set()
        self.adjacency[parent].add(child)

    def has_cycle(self) -> bool:
        """Tarjan/DFS cycle detector for provenance DAG."""
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.adjacency.get(node, ()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.adjacency:
            if node not in visited:
                if dfs(node):
                    return True
        return False
''',
        "test_code": '''"""Tests for Genius-MetadataDepth invariants."""
import pytest
from genius_metadata_depth.tools import (
    compute_dual_hashes,
    validate_monotonic_timestamps,
    ProvenanceDAG
)

def test_dual_hashing():
    data = b"Evidentiary record content"
    hashes = compute_dual_hashes(data)
    assert len(hashes["sha256"]) == 64
    assert len(hashes["blake2b"]) == 128

def test_monotonic_timestamps():
    valid = [100.0, 101.5, 102.0, 105.0]
    assert validate_monotonic_timestamps(valid) is True
    # Inverted causality
    invalid = [100.0, 102.0, 101.0, 105.0]
    assert validate_monotonic_timestamps(invalid) is False

def test_provenance_dag_cycles():
    dag = ProvenanceDAG()
    dag.add_edge("SourceDoc", "ExhibitA")
    dag.add_edge("ExhibitA", "Pleading1")
    assert dag.has_cycle() is False

    # Introduce circular dependency
    dag.add_edge("Pleading1", "SourceDoc")
    assert dag.has_cycle() is True
'''
    }
}
