"""Systems & Platforms domain implementations and test suites.

Domains:
- microcode: CPU decode, register dependencies, RAW/WAR/WAW hazard detection, eBPF stack bounds.
- filesystem: Write-ahead log journal, POSIX atomic file replace, extent block allocator.
- cloud-database: Raft consensus node state machine, MVCC snapshot isolation, 2PC coordinator.
- device: MMIO register bitmask map, ISR latency validator, DMA coherency tracker.
- pc: x86_64 4-level page table calculator, ACPI power state transitions, Authenticode/PE validator.
- mac: Mach port rights tracker, Apple Silicon unified memory coherency, code sign entitlements validator.
- linux: io_uring SQ/CQ ring buffer simulator, cgroups v2 memory tree hierarchy, namespace isolator.
- android: Binder flat parcel serializer, AIDL transaction dispatcher, ART DEX header validator.
- ios: Swift actor exclusive queue, ARM64e PAC signature verifier, 120Hz ProMotion frame budget.
- email: RFC 5322 MIME parser, RFC 6376 DKIM canonicalizer, SPF/DMARC policy evaluators.
- automation: Idempotency ledger, FSM with full-jitter exponential backoff, Saga coordinator.
"""
from __future__ import annotations

SYSTEMS_DOMAINS = {
    "microcode": {
        "module_name": "genius_microcode",
        "tools_code": '''"""Genius-Microcode first-principles domain tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class MicroOp:
    opcode: str
    dst: str | None
    src1: str | None
    src2: str | None = None

def detect_hazards(instructions: Sequence[MicroOp]) -> dict[str, list[tuple[int, int, str]]]:
    """Detect RAW (Read-After-Write), WAR (Write-After-Read), and WAW (Write-After-Write) hazards."""
    raw: list[tuple[int, int, str]] = []
    war: list[tuple[int, int, str]] = []
    waw: list[tuple[int, int, str]] = []

    for i, curr in enumerate(instructions):
        for j in range(i + 1, len(instructions)):
            future = instructions[j]
            # RAW: curr writes to a reg that future reads
            if curr.dst:
                if future.src1 == curr.dst or future.src2 == curr.dst:
                    raw.append((i, j, curr.dst))
                # WAW: curr writes to reg that future also writes
                if future.dst == curr.dst:
                    waw.append((i, j, curr.dst))
            # WAR: curr reads a reg that future writes
            if future.dst:
                if curr.src1 == future.dst or curr.src2 == future.dst:
                    war.append((i, j, future.dst))

    return {"RAW": raw, "WAR": war, "WAW": waw}

class EBPFStackVerifier:
    """Verifies eBPF stack access bounds (0 to 512 bytes)."""
    MAX_STACK_SIZE = 512

    def __init__(self) -> None:
        self.allocated_slots: set[int] = set()

    def write_stack(self, offset: int, size: int) -> bool:
        """Verify stack write: offset in [-512, -1], offset + size <= 0."""
        if offset < -self.MAX_STACK_SIZE or offset >= 0:
            raise ValueError(f"eBPF stack write out of bounds: offset={offset}")
        if offset + size > 0:
            raise ValueError(f"eBPF stack write overflow: offset={offset}, size={size}")
        for b in range(offset, offset + size):
            self.allocated_slots.add(b)
        return True

    def read_stack(self, offset: int, size: int) -> bool:
        """Verify stack read: within bounds and previously written."""
        if offset < -self.MAX_STACK_SIZE or offset >= 0:
            raise ValueError(f"eBPF stack read out of bounds: offset={offset}")
        if offset + size > 0:
            raise ValueError(f"eBPF stack read overflow: offset={offset}, size={size}")
        for b in range(offset, offset + size):
            if b not in self.allocated_slots:
                raise ValueError(f"eBPF uninitialized stack read at byte {b}")
        return True
''',
        "test_code": '''"""Tests for Genius-Microcode invariants."""
import pytest
from genius_microcode.tools import MicroOp, detect_hazards, EBPFStackVerifier

def test_pipeline_hazards_detection():
    insts = [
        MicroOp("ADD", dst="R1", src1="R2", src2="R3"),
        MicroOp("SUB", dst="R4", src1="R1", src2="R5"),  # RAW on R1
        MicroOp("MUL", dst="R2", src1="R6", src2="R7"),  # WAR on R2 (inst 0 reads R2)
        MicroOp("MOV", dst="R1", src1="R8"),             # WAW on R1 (inst 0 writes R1)
    ]
    hazards = detect_hazards(insts)
    assert (0, 1, "R1") in hazards["RAW"]
    assert (0, 2, "R2") in hazards["WAR"]
    assert (0, 3, "R1") in hazards["WAW"]

def test_ebpf_stack_verifier_bounds():
    verifier = EBPFStackVerifier()
    # Legal write and read
    assert verifier.write_stack(-8, 8) is True
    assert verifier.read_stack(-8, 8) is True

    # Uninitialized read fails
    with pytest.raises(ValueError, match="uninitialized"):
        verifier.read_stack(-16, 8)

    # Out of bounds (> 512) fails
    with pytest.raises(ValueError, match="out of bounds"):
        verifier.write_stack(-520, 8)
'''
    },

    "filesystem": {
        "module_name": "genius_filesystem",
        "tools_code": '''"""Genius-Filesystem first-principles domain tools."""
from __future__ import annotations
import os
import tempfile
from dataclasses import dataclass
from typing import Any

@dataclass
class LogEntry:
    lsn: int
    tx_id: int
    op_type: str  # "INSERT", "UPDATE", "DELETE", "COMMIT"
    key: str
    value: Any

class WriteAheadLog:
    """WAL manager ensuring ACID durability and recovery replay."""
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []
        self._current_lsn = 0

    def append(self, tx_id: int, op_type: str, key: str, value: Any = None) -> int:
        self._current_lsn += 1
        entry = LogEntry(self._current_lsn, tx_id, op_type, key, value)
        self.entries.append(entry)
        return self._current_lsn

    def recover(self) -> dict[str, Any]:
        """Replay only committed transactions to restore clean state."""
        committed_txs: set[int] = set()
        for entry in self.entries:
            if entry.op_type == "COMMIT":
                committed_txs.add(entry.tx_id)

        state: dict[str, Any] = {}
        for entry in self.entries:
            if entry.tx_id in committed_txs:
                if entry.op_type in ("INSERT", "UPDATE"):
                    state[entry.key] = entry.value
                elif entry.op_type == "DELETE" and entry.key in state:
                    del state[entry.key]
        return state

def atomic_write_file(target_path: str, data: bytes) -> bool:
    """POSIX atomic file replacement via temporary write and rename."""
    target_dir = os.path.dirname(os.path.abspath(target_path))
    os.makedirs(target_dir, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target_dir, delete=False) as tf:
        tf.write(data)
        tf.flush()
        os.fsync(tf.fileno())
        temp_name = tf.name
    os.replace(temp_name, target_path)
    return True

class ExtentBlockAllocator:
    """Simple extent block allocator tracking block allocation without double-alloc."""
    def __init__(self, total_blocks: int) -> None:
        self.total_blocks = total_blocks
        self.free_bitmap = [True] * total_blocks

    def allocate_extent(self, num_blocks: int) -> tuple[int, int]:
        """Find contiguous free blocks of length num_blocks."""
        consecutive = 0
        start_idx = -1
        for i in range(self.total_blocks):
            if self.free_bitmap[i]:
                if consecutive == 0:
                    start_idx = i
                consecutive += 1
                if consecutive == num_blocks:
                    for b in range(start_idx, start_idx + num_blocks):
                        self.free_bitmap[b] = False
                    return (start_idx, num_blocks)
            else:
                consecutive = 0
                start_idx = -1
        raise MemoryError("No contiguous extent of requested size available")

    def free_extent(self, start_block: int, num_blocks: int) -> None:
        for b in range(start_block, start_block + num_blocks):
            self.free_bitmap[b] = True
''',
        "test_code": '''"""Tests for Genius-Filesystem invariants."""
import pytest
import os
import tempfile
from genius_filesystem.tools import WriteAheadLog, atomic_write_file, ExtentBlockAllocator

def test_wal_recovery_durability():
    wal = WriteAheadLog()
    # Tx 1 commits
    wal.append(1, "INSERT", "keyA", "valA")
    wal.append(1, "COMMIT", "")

    # Tx 2 crashes without commit
    wal.append(2, "INSERT", "keyB", "valB")

    state = wal.recover()
    assert "keyA" in state
    assert state["keyA"] == "valA"
    assert "keyB" not in state

def test_atomic_file_write():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "atomic_test.txt")
        data = b"Sovereign filesystem state"
        assert atomic_write_file(path, data) is True
        with open(path, "rb") as f:
            assert f.read() == data

def test_extent_block_allocator():
    alloc = ExtentBlockAllocator(total_blocks=16)
    start, count = alloc.allocate_extent(4)
    assert start == 0
    assert count == 4
    start2, count2 = alloc.allocate_extent(8)
    assert start2 == 4
    assert count2 == 8
    alloc.free_extent(start, count)
    assert all(alloc.free_bitmap[:4])
'''
    },

    "cloud-database": {
        "module_name": "genius_cloud_database",
        "tools_code": '''"""Genius-CloudDatabase first-principles domain tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class RaftVoteResponse:
    term: int
    vote_granted: bool

class RaftNode:
    """Minimalist Raft consensus node state machine."""
    def __init__(self, node_id: str, peers: list[str]) -> None:
        self.node_id = node_id
        self.peers = peers
        self.term = 0
        self.voted_for: str | None = None
        self.role = "Follower"  # "Follower", "Candidate", "Leader"

    def start_election(self) -> int:
        self.role = "Candidate"
        self.term += 1
        self.voted_for = self.node_id
        return self.term

    def request_vote(self, candidate_id: str, candidate_term: int) -> RaftVoteResponse:
        if candidate_term > self.term:
            self.term = candidate_term
            self.role = "Follower"
            self.voted_for = None

        if candidate_term == self.term and (self.voted_for is None or self.voted_for == candidate_id):
            self.voted_for = candidate_id
            return RaftVoteResponse(self.term, True)
        return RaftVoteResponse(self.term, False)

class MVCCStore:
    """Multi-Version Concurrency Control with snapshot isolation."""
    def __init__(self) -> None:
        # key -> list of (created_tx, deleted_tx, value)
        self.versions: dict[str, list[tuple[int, int | None, Any]]] = {}
        self.active_tx_counter = 0

    def begin_transaction(self) -> int:
        self.active_tx_counter += 1
        return self.active_tx_counter

    def write(self, tx_id: int, key: str, value: Any) -> None:
        if key not in self.versions:
            self.versions[key] = []
        # Mark previous version deleted at tx_id
        updated_list = []
        for c_tx, d_tx, val in self.versions[key]:
            if d_tx is None:
                updated_list.append((c_tx, tx_id, val))
            else:
                updated_list.append((c_tx, d_tx, val))
        updated_list.append((tx_id, None, value))
        self.versions[key] = updated_list

    def read_snapshot(self, tx_id: int, key: str) -> Any | None:
        """Read version visible at tx_id (created <= tx_id and (deleted is None or deleted > tx_id))."""
        if key not in self.versions:
            return None
        for c_tx, d_tx, val in reversed(self.versions[key]):
            if c_tx <= tx_id:
                if d_tx is None or d_tx > tx_id:
                    return val
        return None

class TwoPhaseCommitCoordinator:
    """2PC transaction coordinator."""
    def __init__(self, participants: list[str]) -> None:
        self.participants = participants

    def execute_transaction(self, votes: dict[str, bool]) -> str:
        """Decide COMMIT if all participants vote True, else ABORT."""
        for p in self.participants:
            if not votes.get(p, False):
                return "ABORT"
        return "COMMIT"
''',
        "test_code": '''"""Tests for Genius-CloudDatabase invariants."""
import pytest
from genius_cloud_database.tools import RaftNode, MVCCStore, TwoPhaseCommitCoordinator

def test_raft_election():
    node = RaftNode("node_1", ["node_2", "node_3"])
    assert node.role == "Follower"
    term = node.start_election()
    assert node.role == "Candidate"
    assert term == 1
    assert node.voted_for == "node_1"

    # Higher term resets candidate to follower
    resp = node.request_vote("node_2", 2)
    assert resp.vote_granted is True
    assert node.role == "Follower"
    assert node.term == 2

def test_mvcc_snapshot_isolation():
    store = MVCCStore()
    tx1 = store.begin_transaction()
    store.write(tx1, "balance", 100)

    tx2 = store.begin_transaction()
    store.write(tx2, "balance", 200)

    # tx1 reads its snapshot (100), tx2 reads (200)
    assert store.read_snapshot(tx1, "balance") == 100
    assert store.read_snapshot(tx2, "balance") == 200

def test_two_phase_commit():
    coord = TwoPhaseCommitCoordinator(["db1", "db2", "db3"])
    assert coord.execute_transaction({"db1": True, "db2": True, "db3": True}) == "COMMIT"
    assert coord.execute_transaction({"db1": True, "db2": False, "db3": True}) == "ABORT"
'''
    },

    "device": {
        "module_name": "genius_device",
        "tools_code": '''"""Genius-Device first-principles domain tools."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any

class DMACoherencyState(Enum):
    CLEAN = "CLEAN"
    DIRTY_CPU = "DIRTY_CPU"
    DIRTY_DEVICE = "DIRTY_DEVICE"

class MMIORegisterMap:
    """Memory-Mapped I/O Register bank with read-only bitmask protection."""
    def __init__(self, size_bytes: int = 256) -> None:
        self.registers: bytearray = bytearray(size_bytes)
        self.readonly_mask: bytearray = bytearray(size_bytes)

    def set_readonly_mask(self, offset: int, mask: int) -> None:
        self.readonly_mask[offset] = mask & 0xFF

    def write_byte(self, offset: int, value: int) -> None:
        ro = self.readonly_mask[offset]
        current = self.registers[offset]
        # Preserve read-only bits, allow writable bits
        writable_bits = (~ro) & 0xFF
        new_val = (current & ro) | (value & writable_bits)
        self.registers[offset] = new_val

    def read_byte(self, offset: int) -> int:
        return self.registers[offset]

def validate_isr_latency(execution_cycles: int, clock_frequency_hz: float, deadline_seconds: float) -> dict[str, Any]:
    """Verify Interrupt Service Routine latency against real-time deadline."""
    if clock_frequency_hz <= 0:
        raise ValueError("Clock frequency must be positive")
    latency_sec = execution_cycles / clock_frequency_hz
    meets_deadline = latency_sec <= deadline_seconds
    return {
        "execution_cycles": execution_cycles,
        "latency_microseconds": latency_sec * 1e6,
        "deadline_microseconds": deadline_seconds * 1e6,
        "meets_deadline": meets_deadline,
        "status": "PASS" if meets_deadline else "DEADLINE_EXCEEDED"
    }

class DMABufferTracker:
    """Tracks DMA buffer coherency state to prevent stale CPU/device caches."""
    def __init__(self, size: int) -> None:
        self.size = size
        self.state = DMACoherencyState.CLEAN

    def cpu_write(self) -> None:
        self.state = DMACoherencyState.DIRTY_CPU

    def flush_to_device(self) -> None:
        """Cache clean/flush before device initiates DMA read."""
        self.state = DMACoherencyState.CLEAN

    def device_write(self) -> None:
        self.state = DMACoherencyState.DIRTY_DEVICE

    def invalidate_cpu_cache(self) -> None:
        """Invalidate CPU cache before CPU reads device DMA write."""
        self.state = DMACoherencyState.CLEAN
''',
        "test_code": '''"""Tests for Genius-Device invariants."""
import pytest
from genius_device.tools import MMIORegisterMap, validate_isr_latency, DMABufferTracker, DMACoherencyState

def test_mmio_readonly_mask():
    mmio = MMIORegisterMap(64)
    # Bit 7 is read-only status bit
    mmio.set_readonly_mask(0, 0x80)
    mmio.registers[0] = 0x80  # initial HW status set
    mmio.write_byte(0, 0x0F)   # attempt to write 0x0F
    # Bit 7 must remain 1, lower nibble updated to 0x0F
    assert mmio.read_byte(0) == 0x8F

def test_isr_latency_verification():
    # 1000 cycles at 100MHz = 10 microseconds. Deadline = 20 microseconds.
    res = validate_isr_latency(execution_cycles=1000, clock_frequency_hz=1e8, deadline_seconds=20e-6)
    assert res["meets_deadline"] is True
    assert res["status"] == "PASS"

    # Deadline = 5 microseconds -> FAIL
    res2 = validate_isr_latency(execution_cycles=1000, clock_frequency_hz=1e8, deadline_seconds=5e-6)
    assert res2["meets_deadline"] is False
    assert res2["status"] == "DEADLINE_EXCEEDED"

def test_dma_coherency_lifecycle():
    dma = DMABufferTracker(4096)
    assert dma.state == DMACoherencyState.CLEAN
    dma.cpu_write()
    assert dma.state == DMACoherencyState.DIRTY_CPU
    dma.flush_to_device()
    assert dma.state == DMACoherencyState.CLEAN
'''
    },

    "pc": {
        "module_name": "genius_pc",
        "tools_code": '''"""Genius-PC first-principles domain tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class X86PagingDecomposition:
    pml4_index: int
    pdpt_index: int
    pd_index: int
    pt_index: int
    offset: int

def decompose_x86_canonical_address(vaddr: int) -> X86PagingDecomposition:
    """Decompose 48-bit canonical virtual address into 4-level paging indexes."""
    # Ensure canonical address (bits 48-63 match bit 47)
    bit47 = (vaddr >> 47) & 1
    high_bits = (vaddr >> 48) & 0xFFFF
    expected_high = 0xFFFF if bit47 else 0x0000
    if high_bits != expected_high:
        raise ValueError(f"Non-canonical 48-bit virtual address: 0x{vaddr:X}")

    offset = vaddr & 0xFFF
    pt_idx = (vaddr >> 12) & 0x1FF
    pd_idx = (vaddr >> 21) & 0x1FF
    pdpt_idx = (vaddr >> 30) & 0x1FF
    pml4_idx = (vaddr >> 39) & 0x1FF

    return X86PagingDecomposition(pml4_idx, pdpt_idx, pd_idx, pt_idx, offset)

class ACPIStateManager:
    """ACPI Power state machine (S0 Working -> S3 Standby -> S4 Hibernation -> S5 Soft Off)."""
    VALID_STATES = {"S0", "S1", "S2", "S3", "S4", "S5"}

    def __init__(self) -> None:
        self.current_state = "S0"

    def transition_to(self, target_state: str) -> bool:
        if target_state not in self.VALID_STATES:
            raise ValueError(f"Invalid ACPI state: {target_state}")
        # Must transit back through S0 to switch sleep modes
        if self.current_state != "S0" and target_state != "S0":
            raise RuntimeError(f"Cannot transition from {self.current_state} directly to {target_state} without waking to S0")
        self.current_state = target_state
        return True

def parse_pe_header_summary(pe_bytes: bytes) -> dict[str, Any]:
    """Validate PE (Portable Executable) DOS and NT header signatures."""
    if len(pe_bytes) < 64:
        raise ValueError("File too short for DOS header")
    if pe_bytes[:2] != b"MZ":
        raise ValueError("Invalid DOS header magic (missing MZ)")

    e_lfanew = int.from_bytes(pe_bytes[60:64], byteorder="little")
    if len(pe_bytes) < e_lfanew + 4:
        raise ValueError("Truncated PE header")

    pe_sig = pe_bytes[e_lfanew:e_lfanew+4]
    if pe_sig != b"PE\\x00\\x00":
        raise ValueError("Invalid PE signature")

    return {"is_valid_pe": True, "e_lfanew": e_lfanew}
''',
        "test_code": '''"""Tests for Genius-PC invariants."""
import pytest
from genius_pc.tools import decompose_x86_canonical_address, ACPIStateManager, parse_pe_header_summary

def test_x86_4level_paging_decomposition():
    # Canonical user address
    vaddr = 0x00007FFF80001234
    decomp = decompose_x86_canonical_address(vaddr)
    assert decomp.offset == 0x234
    assert decomp.pml4_index < 512
    assert decomp.pdpt_index < 512
    assert decomp.pd_index < 512
    assert decomp.pt_index < 512

def test_acpi_state_transitions():
    acpi = ACPIStateManager()
    assert acpi.current_state == "S0"
    acpi.transition_to("S3")
    assert acpi.current_state == "S3"
    # S3 direct to S5 fails without waking to S0
    with pytest.raises(RuntimeError):
        acpi.transition_to("S5")
    acpi.transition_to("S0")
    acpi.transition_to("S5")
    assert acpi.current_state == "S5"

def test_pe_header_validation():
    # Mock valid PE buffer
    data = bytearray(128)
    data[0:2] = b"MZ"
    data[60:64] = (64).to_bytes(4, "little")
    data[64:68] = b"PE\\x00\\x00"
    res = parse_pe_header_summary(bytes(data))
    assert res["is_valid_pe"] is True
'''
    },

    "mac": {
        "module_name": "genius_mac",
        "tools_code": '''"""Genius-Mac first-principles domain tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

class MachPortRight:
    RECEIVE = "RECEIVE"
    SEND = "SEND"
    SEND_ONCE = "SEND_ONCE"

class MachPortTracker:
    """Manages Mach port rights and detects dangling or leaking send rights."""
    def __init__(self) -> None:
        self.ports: dict[str, dict[str, Any]] = {}

    def create_port(self, name: str, owner: str) -> None:
        if name in self.ports:
            raise ValueError(f"Mach port {name} already exists")
        self.ports[name] = {
            "owner": owner,
            "has_receive_right": True,
            "send_rights": 0,
            "send_once_rights": 0,
        }

    def allocate_send_right(self, name: str) -> None:
        if name not in self.ports:
            raise KeyError(f"Port {name} not found")
        self.ports[name]["send_rights"] += 1

    def deallocate_send_right(self, name: str) -> None:
        if name not in self.ports:
            raise KeyError(f"Port {name} not found")
        if self.ports[name]["send_rights"] <= 0:
            raise ValueError(f"Port {name} has no send rights to deallocate")
        self.ports[name]["send_rights"] -= 1

    def detect_leaks(self) -> list[str]:
        leaks = []
        for name, data in self.ports.items():
            if not data["has_receive_right"] and data["send_rights"] > 0:
                leaks.append(f"Dangling send rights for deceased port {name}")
        return leaks

class AppleUnifiedMemoryBuffer:
    """Zero-copy buffer model sharing memory coherently between CPU and Neural Engine/GPU."""
    def __init__(self, size_bytes: int) -> None:
        self.size_bytes = size_bytes
        self.backing_buffer = bytearray(size_bytes)
        self.is_mapped_gpu = False

    def map_shared(self) -> None:
        """Expose unified buffer without copying."""
        self.is_mapped_gpu = True

    def write_cpu(self, offset: int, data: bytes) -> None:
        self.backing_buffer[offset:offset+len(data)] = data

    def read_shared(self, offset: int, size: int) -> bytes:
        return bytes(self.backing_buffer[offset:offset+size])

def verify_code_signature_entitlements(entitlements: dict[str, Any], required_keys: list[str]) -> bool:
    """Verify Apple code signature entitlements dictionary against security profile."""
    for k in required_keys:
        if k not in entitlements or not entitlements[k]:
            return False
    return True
''',
        "test_code": '''"""Tests for Genius-Mac invariants."""
import pytest
from genius_mac.tools import MachPortTracker, AppleUnifiedMemoryBuffer, verify_code_signature_entitlements

def test_mach_port_management():
    tracker = MachPortTracker()
    tracker.create_port("com.apple.kernel.test", "kernel")
    tracker.allocate_send_right("com.apple.kernel.test")
    assert tracker.ports["com.apple.kernel.test"]["send_rights"] == 1
    tracker.deallocate_send_right("com.apple.kernel.test")
    assert tracker.ports["com.apple.kernel.test"]["send_rights"] == 0

def test_unified_memory_zero_copy():
    buf = AppleUnifiedMemoryBuffer(1024)
    buf.map_shared()
    assert buf.is_mapped_gpu is True
    buf.write_cpu(0, b"AppleSilicon")
    assert buf.read_shared(0, 12) == b"AppleSilicon"

def test_entitlements_verification():
    ent = {
        "com.apple.security.app-sandbox": True,
        "com.apple.security.network.client": True,
    }
    assert verify_code_signature_entitlements(ent, ["com.apple.security.app-sandbox"]) is True
    assert verify_code_signature_entitlements(ent, ["com.apple.security.files.all"]) is False
'''
    },

    "linux": {
        "module_name": "genius_linux",
        "tools_code": '''"""Genius-Linux first-principles domain tools."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class SQE:
    opcode: str
    fd: int
    user_data: int

@dataclass
class CQE:
    user_data: int
    res: int

class IOUringSimulator:
    """Simulated Linux io_uring SQ (Submission Queue) and CQ (Completion Queue)."""
    def __init__(self, entries: int = 16) -> None:
        self.entries = entries
        self.sq: list[SQE] = []
        self.cq: list[CQE] = []

    def submit_sqe(self, sqe: SQE) -> None:
        if len(self.sq) >= self.entries:
            raise OverflowError("io_uring SQ full")
        self.sq.append(sqe)

    def process_submissions(self) -> int:
        completed = 0
        while self.sq:
            sqe = self.sq.pop(0)
            # Simulated instant execution: res is byte count or 0
            cqe = CQE(user_data=sqe.user_data, res=0)
            self.cq.append(cqe)
            completed += 1
        return completed

    def harvest_cqe(self) -> CQE | None:
        return self.cq.pop(0) if self.cq else None

class CgroupsV2Node:
    """Cgroups v2 unified memory hierarchy tree."""
    def __init__(self, name: str, memory_max_bytes: int, parent: CgroupsV2Node | None = None) -> None:
        self.name = name
        self.memory_max_bytes = memory_max_bytes
        self.parent = parent
        self.current_usage_bytes = 0
        self.children: list[CgroupsV2Node] = []
        if parent:
            parent.children.append(self)

    def charge_memory(self, bytes_to_add: int) -> bool:
        """Charge memory recursively up the tree; enforce limits."""
        node: CgroupsV2Node | None = self
        nodes_to_revert: list[CgroupsV2Node] = []
        while node is not None:
            if node.current_usage_bytes + bytes_to_add > node.memory_max_bytes:
                # Revert previously charged ancestors
                for r in nodes_to_revert:
                    r.current_usage_bytes -= bytes_to_add
                raise MemoryError(f"Cgroup {node.name} memory.max exceeded ({node.current_usage_bytes + bytes_to_add} > {node.memory_max_bytes})")
            node.current_usage_bytes += bytes_to_add
            nodes_to_revert.append(node)
            node = node.parent
        return True

def check_linux_namespace_isolation(ns1: set[int], ns2: set[int]) -> bool:
    """Verify two namespaces have zero overlap in isolated resources (PIDs, net interfaces)."""
    return len(ns1.intersection(ns2)) == 0
''',
        "test_code": '''"""Tests for Genius-Linux invariants."""
import pytest
from genius_linux.tools import IOUringSimulator, SQE, CgroupsV2Node, check_linux_namespace_isolation

def test_io_uring_execution():
    ring = IOUringSimulator(entries=8)
    ring.submit_sqe(SQE("READ", 3, 1001))
    ring.submit_sqe(SQE("WRITE", 4, 1002))
    assert len(ring.sq) == 2
    processed = ring.process_submissions()
    assert processed == 2
    cqe1 = ring.harvest_cqe()
    assert cqe1 is not None and cqe1.user_data == 1001

def test_cgroups_v2_hierarchy_enforcement():
    root = CgroupsV2Node("root", 1024 * 1024)
    child = CgroupsV2Node("service_a", 512 * 1024, parent=root)

    # Valid charge
    assert child.charge_memory(256 * 1024) is True
    assert child.current_usage_bytes == 256 * 1024
    assert root.current_usage_bytes == 256 * 1024

    # Exceed child limit
    with pytest.raises(MemoryError):
        child.charge_memory(300 * 1024)

def test_namespace_isolation():
    pid_ns1 = {1, 2, 3}
    pid_ns2 = {101, 102, 103}
    assert check_linux_namespace_isolation(pid_ns1, pid_ns2) is True
'''
    },

    "android": {
        "module_name": "genius_android",
        "tools_code": '''"""Genius-Android first-principles domain tools."""
from __future__ import annotations
import struct
from typing import Any

class BinderFlatParcel:
    """Android Binder flat parcel serializer and deserializer."""
    def __init__(self) -> None:
        self.buffer = bytearray()
        self.read_pos = 0

    def write_int32(self, val: int) -> None:
        self.buffer.extend(struct.pack("<i", val))

    def read_int32(self) -> int:
        if self.read_pos + 4 > len(self.buffer):
            raise IndexError("Parcel buffer underflow on int32 read")
        val = struct.unpack_from("<i", self.buffer, self.read_pos)[0]
        self.read_pos += 4
        return val

    def write_string16(self, s: str) -> None:
        encoded = s.encode("utf-16le")
        length = len(s)
        self.write_int32(length)
        self.buffer.extend(encoded)
        # 4-byte alignment padding
        rem = len(encoded) % 4
        if rem != 0:
            self.buffer.extend(b"\\x00" * (4 - rem))

    def read_string16(self) -> str:
        length = self.read_int32()
        byte_len = length * 2
        if self.read_pos + byte_len > len(self.buffer):
            raise IndexError("Parcel buffer underflow on string16 read")
        raw = bytes(self.buffer[self.read_pos:self.read_pos + byte_len])
        self.read_pos += byte_len
        # skip alignment padding
        rem = byte_len % 4
        if rem != 0:
            self.read_pos += (4 - rem)
        return raw.decode("utf-16le")

def validate_dex_header(dex_bytes: bytes) -> dict[str, Any]:
    """Validate Dalvik / ART DEX executable header magic and version."""
    if len(dex_bytes) < 40:
        raise ValueError("File too short for DEX header")
    magic = dex_bytes[:4]
    if magic != b"dex\\n":
        raise ValueError(f"Invalid DEX magic: {magic}")
    version = dex_bytes[4:7].decode("ascii", errors="ignore")
    return {"valid": True, "dex_version": version}

class AIDLDispatcher:
    """Dispatches AIDL RPC calls via transaction codes."""
    def __init__(self) -> None:
        self.handlers: dict[int, Any] = {}

    def register_transaction(self, code: int, handler: Any) -> None:
        self.handlers[code] = handler

    def dispatch(self, code: int, data: BinderFlatParcel) -> BinderFlatParcel:
        if code not in self.handlers:
            raise KeyError(f"Unknown AIDL transaction code: {code}")
        reply = BinderFlatParcel()
        self.handlers[code](data, reply)
        return reply
''',
        "test_code": '''"""Tests for Genius-Android invariants."""
import pytest
from genius_android.tools import BinderFlatParcel, validate_dex_header, AIDLDispatcher

def test_binder_flat_parcel_roundtrip():
    parcel = BinderFlatParcel()
    parcel.write_int32(42)
    parcel.write_string16("AndroidSovereignIPC")

    assert parcel.read_int32() == 42
    assert parcel.read_string16() == "AndroidSovereignIPC"

def test_dex_header_validation():
    valid_dex = b"dex\\n039\\x00" + b"\\x00" * 32
    res = validate_dex_header(valid_dex)
    assert res["valid"] is True
    assert res["dex_version"] == "039"

    with pytest.raises(ValueError, match="Invalid DEX magic"):
        validate_dex_header(b"NOTDEX\\x00\\x00" + b"\\x00" * 32)

def test_aidl_dispatcher():
    dispatcher = AIDLDispatcher()
    def handle_ping(data: BinderFlatParcel, reply: BinderFlatParcel) -> None:
        val = data.read_int32()
        reply.write_int32(val * 2)

    dispatcher.register_transaction(1, handle_ping)
    req = BinderFlatParcel()
    req.write_int32(21)
    rep = dispatcher.dispatch(1, req)
    assert rep.read_int32() == 42
'''
    },

    "ios": {
        "module_name": "genius_ios",
        "tools_code": '''"""Genius-iOS first-principles domain tools."""
from __future__ import annotations
import hmac
import hashlib
from typing import Callable, Any

class SwiftActorQueue:
    """Serial FIFO queue simulating Swift actor isolated execution preventing data races."""
    def __init__(self) -> None:
        self._queue: list[tuple[Callable[..., Any], tuple, dict]] = []
        self._is_busy = False

    def enqueue_task(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self._queue.append((func, args, kwargs))

    def drain_all(self) -> list[Any]:
        """Execute all pending actor tasks strictly sequentially."""
        results = []
        while self._queue:
            func, args, kwargs = self._queue.pop(0)
            results.append(func(*args, **kwargs))
        return results

def compute_arm64e_pac(ptr_val: int, context: int, secret_key: bytes) -> str:
    """Simulate ARM64e Pointer Authentication Code (PAC) signature."""
    msg = f"{ptr_val:X}:{context:X}".encode("utf-8")
    return hmac.new(secret_key, msg, hashlib.sha256).hexdigest()[:8]

def verify_arm64e_pac(ptr_val: int, context: int, tag: str, secret_key: bytes) -> bool:
    expected = compute_arm64e_pac(ptr_val, context, secret_key)
    return hmac.compare_digest(expected, tag)

def check_promotion_frame_budget(duration_seconds: float, target_hz: int = 120) -> dict[str, Any]:
    """Verify display frame render duration against ProMotion refresh deadline."""
    frame_budget_ms = 1000.0 / target_hz
    actual_ms = duration_seconds * 1000.0
    dropped = actual_ms > frame_budget_ms
    return {
        "target_hz": target_hz,
        "frame_budget_ms": frame_budget_ms,
        "actual_render_ms": actual_ms,
        "dropped_frame": dropped,
        "status": "PASS" if not dropped else "HITCH"
    }
''',
        "test_code": '''"""Tests for Genius-iOS invariants."""
import pytest
from genius_ios.tools import (
    SwiftActorQueue,
    compute_arm64e_pac,
    verify_arm64e_pac,
    check_promotion_frame_budget
)

def test_swift_actor_serial_execution():
    actor = SwiftActorQueue()
    counter = []
    actor.enqueue_task(lambda x: counter.append(x), 1)
    actor.enqueue_task(lambda x: counter.append(x), 2)
    actor.drain_all()
    assert counter == [1, 2]

def test_arm64e_pac_verification():
    key = b"A17ProSecretKey"
    ptr = 0x10004500
    ctx = 0x2000
    tag = compute_arm64e_pac(ptr, ctx, key)
    assert verify_arm64e_pac(ptr, ctx, tag, key) is True
    # Tampered context fails
    assert verify_arm64e_pac(ptr, 0x9999, tag, key) is False

def test_promotion_frame_budget():
    # 6.0 ms at 120Hz (budget ~8.33ms) -> PASS
    res = check_promotion_frame_budget(0.006, target_hz=120)
    assert res["status"] == "PASS"

    # 10.0 ms at 120Hz -> HITCH
    res2 = check_promotion_frame_budget(0.010, target_hz=120)
    assert res2["status"] == "HITCH"
'''
    },

    "email": {
        "module_name": "genius_email",
        "tools_code": '''"""Genius-Email first-principles domain tools."""
from __future__ import annotations
import hashlib
import re
from typing import Any

def canonicalize_dkim_relaxed_body(body: str) -> bytes:
    """Canonicalize email body according to RFC 6376 relaxed algorithm."""
    # 1. Reduce all sequences of whitespace within a line to a single space
    lines = body.splitlines()
    relaxed_lines = []
    for line in lines:
        cleaned = re.sub(r"[ \\t]+", " ", line).rstrip(" \\r\\t")
        relaxed_lines.append(cleaned)

    # 2. Remove trailing empty lines
    while relaxed_lines and relaxed_lines[-1] == "":
        relaxed_lines.pop()

    if not relaxed_lines:
        return b""
    return ("\\r\\n".join(relaxed_lines) + "\\r\\n").encode("utf-8")

def compute_dkim_body_hash(canonical_body: bytes) -> str:
    """Compute SHA-256 body hash for DKIM."""
    import base64
    digest = hashlib.sha256(canonical_body).digest()
    return base64.b64encode(digest).decode("ascii")

def evaluate_spf_ip(sender_ip: str, spf_record: str) -> str:
    """Evaluate sender IP against basic SPF record mechanisms."""
    mechanisms = spf_record.split()
    if not mechanisms or mechanisms[0] != "v=spf1":
        return "neutral"

    for mech in mechanisms[1:]:
        if mech == "+all":
            return "pass"
        elif mech == "-all":
            return "fail"
        elif mech == "~all":
            return "softfail"
        elif mech.startswith("ip4:"):
            target_ip = mech[4:]
            if sender_ip == target_ip:
                return "pass"
    return "neutral"

def evaluate_dmarc(spf_pass: bool, dkim_pass: bool, policy: str = "reject") -> dict[str, Any]:
    """Evaluate DMARC alignment and policy action."""
    passed = spf_pass or dkim_pass
    action = "pass" if passed else policy
    return {"dmarc_pass": passed, "action": action}
''',
        "test_code": '''"""Tests for Genius-Email invariants."""
import pytest
from genius_email.tools import (
    canonicalize_dkim_relaxed_body,
    compute_dkim_body_hash,
    evaluate_spf_ip,
    evaluate_dmarc
)

def test_dkim_relaxed_body_canonicalization():
    raw_body = "Hello    World!  \\nThis is a test.   \\n\\n\\n"
    canonical = canonicalize_dkim_relaxed_body(raw_body)
    assert canonical == b"Hello World!\\r\\nThis is a test.\\r\\n"
    bh = compute_dkim_body_hash(canonical)
    assert len(bh) > 0

def test_spf_evaluation():
    spf = "v=spf1 ip4:192.168.1.1 -all"
    assert evaluate_spf_ip("192.168.1.1", spf) == "pass"
    assert evaluate_spf_ip("10.0.0.1", spf) == "fail"

def test_dmarc_evaluation():
    assert evaluate_dmarc(spf_pass=True, dkim_pass=False)["dmarc_pass"] is True
    assert evaluate_dmarc(spf_pass=False, dkim_pass=True)["dmarc_pass"] is True
    failed = evaluate_dmarc(spf_pass=False, dkim_pass=False, policy="quarantine")
    assert failed["dmarc_pass"] is False
    assert failed["action"] == "quarantine"
'''
    },

    "automation": {
        "module_name": "genius_automation",
        "tools_code": '''"""Genius-Automation first-principles domain tools."""
from __future__ import annotations
import hashlib
import random
from typing import Callable, Any

class IdempotencyLedger:
    """Guarantees idempotency f(f(x)) = f(x) via cryptographic execution hashes."""
    def __init__(self) -> None:
        self.cache: dict[str, Any] = {}

    def execute_once(self, idempotency_key: str, action: Callable[[], Any]) -> Any:
        h = hashlib.sha256(idempotency_key.encode("utf-8")).hexdigest()
        if h in self.cache:
            return self.cache[h]
        result = action()
        self.cache[h] = result
        return result

def full_jitter_backoff(attempt: int, base_seconds: float = 1.0, max_seconds: float = 30.0) -> float:
    """Full-jitter exponential backoff: Uniform(0, min(max, base * 2^attempt))."""
    cap = min(max_seconds, base_seconds * (2 ** attempt))
    return random.uniform(0.0, cap)

class SagaStep:
    def __init__(self, name: str, forward: Callable[[], Any], compensate: Callable[[], Any]) -> None:
        self.name = name
        self.forward = forward
        self.compensate = compensate

class SagaCoordinator:
    """Orchestrates distributed Saga transactions with forward execution and reverse compensation."""
    def __init__(self, steps: list[SagaStep]) -> None:
        self.steps = steps
        self.executed_steps: list[SagaStep] = []

    def execute(self) -> bool:
        for step in self.steps:
            try:
                step.forward()
                self.executed_steps.append(step)
            except Exception:
                self.rollback()
                return False
        return True

    def rollback(self) -> None:
        while self.executed_steps:
            step = self.executed_steps.pop()
            try:
                step.compensate()
            except Exception:
                pass
''',
        "test_code": '''"""Tests for Genius-Automation invariants."""
import pytest
from genius_automation.tools import IdempotencyLedger, full_jitter_backoff, SagaStep, SagaCoordinator

def test_idempotency_ledger():
    ledger = IdempotencyLedger()
    call_count = 0
    def perform_action():
        nonlocal call_count
        call_count += 1
        return "order_123"

    res1 = ledger.execute_once("tx_abc", perform_action)
    res2 = ledger.execute_once("tx_abc", perform_action)
    assert res1 == "order_123"
    assert res2 == "order_123"
    assert call_count == 1

def test_full_jitter_bounds():
    delay = full_jitter_backoff(attempt=3, base_seconds=1.0, max_seconds=10.0)
    assert 0.0 <= delay <= 8.0

def test_saga_rollback_on_failure():
    compensations = []
    step1 = SagaStep("reserve_credit", lambda: None, lambda: compensations.append("refund_credit"))
    def failing_step():
        raise RuntimeError("Inventory out of stock")
    step2 = SagaStep("reserve_inventory", failing_step, lambda: compensations.append("refund_inventory"))

    saga = SagaCoordinator([step1, step2])
    success = saga.execute()
    assert success is False
    assert compensations == ["refund_credit"]
'''
    }
}
