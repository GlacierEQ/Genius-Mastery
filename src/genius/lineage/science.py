"""Frontier Science & AI domain implementations and test suites.

Domains:
- aerospace: Orbital dynamics, rocket propulsion, Lambert targeting, telemetry.
- nanosphere: Molecular lattice, Lennard-Jones dynamics, de Broglie confinement.
- physics: Hamiltonian dynamics, Noether invariants, symplectic integration.
- chemistry: Reaction kinetics, Gibbs equilibrium, stoichiometry.
- biology: Sequence alignment, enzyme kinetics, central dogma translation.
- model-weights: Symmetric INT8 quantization, RoPE embeddings, paged KV-cache.
"""
from __future__ import annotations

SCIENCE_DOMAINS = {
    "aerospace": {
        "module_name": "genius_aerospace",
        "tools_code": '''"""Genius-Aerospace first-principles domain tools."""
from __future__ import annotations
import math
from typing import Any

G0 = 9.80665
MU_EARTH = 398600.4418  # km^3 / s^2

def tsiolkovsky_delta_v(isp: float, m0: float, mf: float, g0: float = G0) -> float:
    """Compute ideal velocity increment via Tsiolkovsky rocket equation."""
    if m0 <= 0 or mf <= 0:
        raise ValueError("masses must be strictly positive")
    if mf > m0:
        raise ValueError("final mass cannot exceed initial mass")
    return isp * g0 * math.log(m0 / mf)

def vis_viva_velocity(r: float, a: float, mu: float = MU_EARTH) -> float:
    """Compute orbital speed via Vis-viva equation: v^2 = mu * (2/r - 1/a)."""
    if r <= 0:
        raise ValueError("radius must be strictly positive")
    diff = 2.0 / r - 1.0 / a
    if diff < 0:
        raise ValueError("hyperbolic escape state below boundary")
    return math.sqrt(mu * diff)

def orbital_period(a: float, mu: float = MU_EARTH) -> float:
    """Compute Keplerian orbital period in seconds: T = 2*pi*sqrt(a^3 / mu)."""
    if a <= 0:
        raise ValueError("semi-major axis must be strictly positive")
    return 2.0 * math.pi * math.sqrt((a ** 3) / mu)

def propellant_boil_off_loss(q_leak_watts: float, delta_h_vap_j_per_kg: float, dt_seconds: float) -> float:
    """Calculate boil-off mass loss (kg): dm = (Q_leak * dt) / Delta_H_vap."""
    if delta_h_vap_j_per_kg <= 0:
        raise ValueError("heat of vaporization must be positive")
    return (q_leak_watts * dt_seconds) / delta_h_vap_j_per_kg

def check_conjunction(distance_km: float, keep_out_km: float = 5.0) -> dict[str, Any]:
    """Check collision conjunction against keep-out ellipsoid boundary."""
    violates = distance_km < keep_out_km
    return {
        "distance_km": distance_km,
        "keep_out_km": keep_out_km,
        "conjunction_risk": violates,
        "status": "CONJUNCTION_WARNING" if violates else "CLEAR"
    }

def propagate_two_body(r: float, v: float, dt: float, mu: float = MU_EARTH) -> tuple[float, float]:
    """Simple 1D radial-tangential energy-conserving state propagation."""
    energy_initial = 0.5 * (v ** 2) - mu / r
    r_next = r + v * dt
    v_next = math.sqrt(2.0 * (energy_initial + mu / r_next))
    return r_next, v_next
''',
        "test_code": '''"""Tests for Genius-Aerospace invariants."""
import pytest
import math
from genius_aerospace.tools import (
    tsiolkovsky_delta_v,
    vis_viva_velocity,
    orbital_period,
    propellant_boil_off_loss,
    check_conjunction,
    propagate_two_body,
    G0,
    MU_EARTH
)

def test_tsiolkovsky_equation():
    # 300s Isp, 100t initial, 10t final -> ~6773 m/s
    dv = tsiolkovsky_delta_v(300.0, 100000.0, 10000.0)
    expected = 300.0 * G0 * math.log(10.0)
    assert math.isclose(dv, expected, rel_tol=1e-5)

def test_vis_viva_circular_leo():
    # Circular LEO at r = a = 6778 km (400 km altitude)
    r = 6778.0
    v = vis_viva_velocity(r, r)
    expected = math.sqrt(MU_EARTH / r)
    assert math.isclose(v, expected, rel_tol=1e-5)
    assert 7.6 < v < 7.7  # ~7.67 km/s

def test_kepler_third_law():
    r_geo = 42164.0  # Geostationary radius in km
    period = orbital_period(r_geo)
    hours = period / 3600.0
    assert math.isclose(hours, 24.0, abs_tol=0.2)

def test_boil_off_conservation():
    mass_loss = propellant_boil_off_loss(1000.0, 500000.0, 3600.0)
    assert math.isclose(mass_loss, 7.2, rel_tol=1e-5)

def test_conjunction_assessment():
    safe = check_conjunction(10.0, 5.0)
    assert not safe["conjunction_risk"]
    assert safe["status"] == "CLEAR"

    risk = check_conjunction(3.2, 5.0)
    assert risk["conjunction_risk"]
    assert risk["status"] == "CONJUNCTION_WARNING"

def test_propagate_two_body_energy_conservation():
    r0, v0 = 7000.0, 7.5
    e0 = 0.5 * (v0 ** 2) - MU_EARTH / r0
    r1, v1 = propagate_two_body(r0, v0, 10.0)
    e1 = 0.5 * (v1 ** 2) - MU_EARTH / r1
    assert math.isclose(e0, e1, rel_tol=1e-5)
'''
    },

    "nanosphere": {
        "module_name": "genius_nanosphere",
        "tools_code": '''"""Genius-Nanosphere atomic and molecular dynamics tools."""
from __future__ import annotations
import math

H_PLANCK = 6.62607015e-34  # J*s

def lennard_jones_potential(r: float, epsilon: float = 1.0, sigma: float = 1.0) -> float:
    """Calculate Lennard-Jones potential V(r) = 4*eps * ((sig/r)^12 - (sig/r)^6)."""
    if r <= 0:
        raise ValueError("interatomic distance must be strictly positive")
    sr6 = (sigma / r) ** 6
    sr12 = sr6 ** 2
    return 4.0 * epsilon * (sr12 - sr6)

def lennard_jones_force(r: float, epsilon: float = 1.0, sigma: float = 1.0) -> float:
    """Calculate Lennard-Jones interatomic force F(r) = -dV/dr."""
    if r <= 0:
        raise ValueError("interatomic distance must be strictly positive")
    inv_r = 1.0 / r
    sr6 = (sigma / r) ** 6
    sr12 = sr6 ** 2
    return 24.0 * (epsilon * inv_r) * (2.0 * sr12 - sr6)

def de_broglie_wavelength(momentum: float, h: float = H_PLANCK) -> float:
    """Calculate de Broglie matter wavelength: lambda = h / p."""
    if momentum <= 0:
        raise ValueError("momentum must be strictly positive")
    return h / momentum

def verify_nve_energy(kinetic: float, potential: float, reference_total: float, tolerance: float = 1e-4) -> bool:
    """Verify energy conservation in a microcanonical (NVE) ensemble."""
    total = kinetic + potential
    return math.isclose(total, reference_total, rel_tol=tolerance)

def lattice_parameter_cubic(volume_nm3: float, atoms_per_unit_cell: int = 4) -> float:
    """Calculate FCC cubic lattice constant a = (V_unit)^(1/3)."""
    if volume_nm3 <= 0 or atoms_per_unit_cell <= 0:
        raise ValueError("volume and atom count must be positive")
    return (volume_nm3) ** (1.0 / 3.0)
''',
        "test_code": '''"""Tests for Genius-Nanosphere invariants."""
import pytest
import math
from genius_nanosphere.tools import (
    lennard_jones_potential,
    lennard_jones_force,
    de_broglie_wavelength,
    verify_nve_energy,
    lattice_parameter_cubic,
    H_PLANCK
)

def test_lennard_jones_equilibrium():
    # Minimum of LJ potential occurs at r_min = 2^(1/6) * sigma
    r_min = 2.0 ** (1.0 / 6.0)
    v_min = lennard_jones_potential(r_min, epsilon=1.5, sigma=1.0)
    assert math.isclose(v_min, -1.5, rel_tol=1e-5)
    f_min = lennard_jones_force(r_min, epsilon=1.5, sigma=1.0)
    assert math.isclose(f_min, 0.0, abs_tol=1e-5)

def test_de_broglie_wavelength():
    # Electron with momentum 1e-24 kg*m/s
    p = 1e-24
    wl = de_broglie_wavelength(p)
    assert math.isclose(wl, H_PLANCK / p, rel_tol=1e-6)

def test_nve_energy_conservation():
    ref = 100.0
    assert verify_nve_energy(40.0, 60.0, ref)
    assert not verify_nve_energy(45.0, 60.0, ref, tolerance=1e-4)

def test_lattice_parameter():
    a = lattice_parameter_cubic(0.064)
    assert math.isclose(a, 0.4, rel_tol=1e-5)
'''
    },

    "physics": {
        "module_name": "genius_physics",
        "tools_code": '''"""Genius-Physics classical, relativistic, and symplectic dynamics tools."""
from __future__ import annotations
import math
from typing import Callable

def harmonic_hamiltonian(q: float, p: float, mass: float = 1.0, k: float = 1.0) -> float:
    """Harmonic oscillator Hamiltonian: H(q, p) = p^2 / (2m) + 0.5 * k * q^2."""
    return (p ** 2) / (2.0 * mass) + 0.5 * k * (q ** 2)

def verlet_step(q: float, p: float, force_fn: Callable[[float], float], dt: float, mass: float = 1.0) -> tuple[float, float]:
    """Symplectic Velocity Verlet integration step preserving phase space volume."""
    f0 = force_fn(q)
    q_next = q + (p / mass) * dt + 0.5 * (f0 / mass) * (dt ** 2)
    f1 = force_fn(q_next)
    p_next = p + 0.5 * (f0 + f1) * dt
    return q_next, p_next

def lagrangian_action(trajectory_q: list[float], dt: float, mass: float = 1.0, k: float = 1.0) -> float:
    """Calculate discretized action S = sum(L * dt) where L = T - V."""
    action = 0.0
    for i in range(len(trajectory_q) - 1):
        v = (trajectory_q[i + 1] - trajectory_q[i]) / dt
        t_kin = 0.5 * mass * (v ** 2)
        v_pot = 0.5 * k * (trajectory_q[i] ** 2)
        action += (t_kin - v_pot) * dt
    return action

def lorentz_factor(v_over_c: float) -> float:
    """Relativistic Lorentz factor gamma = 1 / sqrt(1 - (v/c)^2)."""
    if abs(v_over_c) >= 1.0:
        raise ValueError("velocity ratio must be strictly less than 1.0")
    return 1.0 / math.sqrt(1.0 - (v_over_c ** 2))
''',
        "test_code": '''"""Tests for Genius-Physics invariants."""
import pytest
import math
from genius_physics.tools import (
    harmonic_hamiltonian,
    verlet_step,
    lagrangian_action,
    lorentz_factor
)

def test_symplectic_energy_preservation():
    # Harmonic oscillator: F(q) = -k*q
    q, p = 1.0, 0.0
    h0 = harmonic_hamiltonian(q, p)
    force = lambda x: -1.0 * x

    # Step for 100 iterations
    dt = 0.01
    for _ in range(100):
        q, p = verlet_step(q, p, force, dt)
    h_final = harmonic_hamiltonian(q, p)
    # Symplectic Verlet should conserve energy within O(dt^2)
    assert math.isclose(h0, h_final, rel_tol=1e-3)

def test_lagrangian_action():
    traj = [0.0, 0.5, 1.0, 0.5, 0.0]
    action = lagrangian_action(traj, 0.1)
    assert isinstance(action, float)

def test_lorentz_factor():
    assert math.isclose(lorentz_factor(0.0), 1.0)
    assert math.isclose(lorentz_factor(0.6), 1.25, rel_tol=1e-5)
    with pytest.raises(ValueError):
        lorentz_factor(1.0)
'''
    },

    "chemistry": {
        "module_name": "genius_chemistry",
        "tools_code": '''"""Genius-Chemistry stoichiometry and reaction kinetics tools."""
from __future__ import annotations
import math

R_GAS = 8.314462618  # J / (mol * K)

def gibbs_free_energy(delta_h_joules: float, delta_s_joules_per_k: float, temp_k: float) -> float:
    """Calculate Gibbs free energy: Delta G = Delta H - T * Delta S."""
    if temp_k <= 0:
        raise ValueError("temperature in Kelvin must be strictly positive")
    return delta_h_joules - temp_k * delta_s_joules_per_k

def arrhenius_rate_constant(pre_exponential_a: float, activation_energy_j: float, temp_k: float) -> float:
    """Calculate reaction rate constant: k = A * exp(-E_a / (R * T))."""
    if temp_k <= 0:
        raise ValueError("temperature in Kelvin must be strictly positive")
    return pre_exponential_a * math.exp(-activation_energy_j / (R_GAS * temp_k))

def check_stoichiometric_balance(reactants: dict[str, dict[str, int]], products: dict[str, dict[str, int]]) -> bool:
    """Verify strict atom conservation across a chemical reaction."""
    atom_count: dict[str, int] = {}
    for compound, formula in reactants.items():
        for element, count in formula.items():
            atom_count[element] = atom_count.get(element, 0) + count
    for compound, formula in products.items():
        for element, count in formula.items():
            atom_count[element] = atom_count.get(element, 0) - count
    return all(count == 0 for count in atom_count.values())

def reaction_quotient_q(concentrations: dict[str, float], coefficients: dict[str, int]) -> float:
    """Calculate reaction quotient Q = product([A]^a)."""
    q = 1.0
    for species, conc in concentrations.items():
        coeff = coefficients.get(species, 0)
        q *= (conc ** coeff)
    return q
''',
        "test_code": '''"""Tests for Genius-Chemistry invariants."""
import pytest
import math
from genius_chemistry.tools import (
    gibbs_free_energy,
    arrhenius_rate_constant,
    check_stoichiometric_balance,
    reaction_quotient_q
)

def test_gibbs_spontaneity():
    # Exothermic with positive entropy -> spontaneous (Delta G < 0)
    dg = gibbs_free_energy(-50000.0, 100.0, 298.15)
    assert dg < 0
    assert math.isclose(dg, -50000.0 - (298.15 * 100.0), rel_tol=1e-5)

def test_arrhenius_kinetics():
    k = arrhenius_rate_constant(1e7, 50000.0, 300.0)
    assert k > 0
    # Higher temp -> faster rate
    k_higher = arrhenius_rate_constant(1e7, 50000.0, 400.0)
    assert k_higher > k

def test_stoichiometry_water_synthesis():
    # 2 H2 + O2 -> 2 H2O
    reactants = {"H2_1": {"H": 2}, "H2_2": {"H": 2}, "O2": {"O": 2}}
    products = {"H2O_1": {"H": 2, "O": 1}, "H2O_2": {"H": 2, "O": 1}}
    assert check_stoichiometric_balance(reactants, products)

    # Imbalanced test
    imbalanced = {"H2O_1": {"H": 2, "O": 1}}
    assert not check_stoichiometric_balance(reactants, imbalanced)

def test_reaction_quotient():
    concs = {"A": 2.0, "B": 3.0}
    coeffs = {"A": -1, "B": 2}
    # Q = (B^2) / (A^1) = 9 / 2 = 4.5
    q = reaction_quotient_q(concs, coeffs)
    assert math.isclose(q, 4.5, rel_tol=1e-5)
'''
    },

    "biology": {
        "module_name": "genius_biology",
        "tools_code": '''"""Genius-Biology bioinformatics and biochemical dynamics tools."""
from __future__ import annotations

CODON_TABLE = {
    "ATA":"I", "ATC":"I", "ATT":"I", "ATG":"M",
    "ACA":"T", "ACC":"T", "ACG":"T", "ACT":"T",
    "AAC":"N", "AAT":"N", "AAA":"K", "AAG":"K",
    "AGC":"S", "AGT":"S", "AGA":"R", "AGG":"R",
    "CTA":"L", "CTC":"L", "CTG":"L", "CTT":"L",
    "CCA":"P", "CCC":"P", "CCG":"P", "CCT":"P",
    "CAC":"H", "CAT":"H", "CAA":"Q", "CAG":"Q",
    "CGA":"R", "CGC":"R", "CGG":"R", "CGT":"R",
    "GTA":"V", "GTC":"V", "GTG":"V", "GTT":"V",
    "GCA":"A", "GCC":"A", "GCG":"A", "GCT":"A",
    "GAC":"D", "GAT":"D", "GAA":"E", "GAG":"E",
    "GGA":"G", "GGC":"G", "GGG":"G", "GGT":"G",
    "TCA":"S", "TCC":"S", "TCG":"S", "TCT":"S",
    "TTC":"F", "TTT":"F", "TTA":"L", "TTG":"L",
    "TAC":"Y", "TAT":"Y", "TAA":"_", "TAG":"_",
    "TGC":"C", "TGT":"C", "TGA":"_", "TGG":"W",
}

def translate_dna(dna: str) -> str:
    """Translate nucleotide sequence into peptide sequence via standard genetic code."""
    dna = dna.upper().replace("U", "T")
    peptide = []
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i+3]
        aa = CODON_TABLE.get(codon, "X")
        if aa == "_":
            break
        peptide.append(aa)
    return "".join(peptide)

def michaelis_menten_rate(vmax: float, substrate: float, km: float) -> float:
    """Calculate enzymatic velocity v = (Vmax * [S]) / (Km + [S])."""
    if substrate < 0 or km <= 0 or vmax < 0:
        raise ValueError("substrate, Km, and Vmax must be non-negative with Km > 0")
    return (vmax * substrate) / (km + substrate)

def smith_waterman_align(seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1) -> int:
    """Calculate maximum local alignment score via dynamic programming."""
    m, n = len(seq1), len(seq2)
    h = [[0] * (n + 1) for _ in range(m + 1)]
    max_score = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            score_diag = h[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            score_del = h[i - 1][j] + gap
            score_ins = h[i][j - 1] + gap
            val = max(0, score_diag, score_del, score_ins)
            h[i][j] = val
            if val > max_score:
                max_score = val
    return max_score

def metabolic_flux_balance(s_matrix: list[list[float]], flux_vector: list[float]) -> bool:
    """Verify steady-state stoichiometric constraint: S * v = 0."""
    for row in s_matrix:
        row_sum = sum(coeff * v for coeff, v in zip(row, flux_vector))
        if abs(row_sum) > 1e-5:
            return False
    return True
''',
        "test_code": '''"""Tests for Genius-Biology invariants."""
import pytest
import math
from genius_biology.tools import (
    translate_dna,
    michaelis_menten_rate,
    smith_waterman_align,
    metabolic_flux_balance
)

def test_central_dogma_translation():
    dna = "ATGGCCAAGTTTTAA"
    peptide = translate_dna(dna)
    # ATG -> M, GCC -> A, AAG -> K, TTT -> F, TAA -> stop
    assert peptide == "MAKF"

def test_michaelis_menten_saturation():
    # At [S] = Km, v = Vmax / 2
    v = michaelis_menten_rate(vmax=10.0, substrate=5.0, km=5.0)
    assert math.isclose(v, 5.0, rel_tol=1e-5)

def test_smith_waterman_local_alignment():
    score = smith_waterman_align("HEAGAWGHEE", "PAWHEAE")
    assert score > 0

def test_metabolic_flux_balance():
    # Stoichiometry S = [[1, -1], [-1, 1]]
    s = [[1.0, -1.0], [-1.0, 1.0]]
    v_balanced = [2.5, 2.5]
    assert metabolic_flux_balance(s, v_balanced)
    v_unbalanced = [2.5, 1.0]
    assert not metabolic_flux_balance(s, v_unbalanced)
'''
    },

    "model-weights": {
        "module_name": "genius_model_weights",
        "tools_code": '''"""Genius-ModelWeights LLM quantization and inference architecture tools."""
from __future__ import annotations
import math

def quantize_symmetric_int8(tensor: list[float]) -> tuple[list[int], float]:
    """Perform symmetric uniform INT8 quantization."""
    if not tensor:
        return [], 1.0
    max_val = max(abs(x) for x in tensor)
    if max_val == 0.0:
        return [0] * len(tensor), 1.0
    scale = max_val / 127.0
    quantized = [min(127, max(-127, round(x / scale))) for x in tensor]
    return quantized, scale

def dequantize_symmetric_int8(quantized: list[int], scale: float) -> list[float]:
    """Dequantize INT8 back to FP32."""
    return [q * scale for q in quantized]

def apply_rope_2d(x0: float, x1: float, theta: float) -> tuple[float, float]:
    """Apply Rotary Position Embedding (RoPE) 2D unitary rotation."""
    cos_th = math.cos(theta)
    sin_th = math.sin(theta)
    out0 = x0 * cos_th - x1 * sin_th
    out1 = x0 * sin_th + x1 * cos_th
    return out0, out1

class PagedKVCacheAllocator:
    """Manages non-contiguous paged memory blocks for KV caching."""
    def __init__(self, block_size: int = 16, total_blocks: int = 64):
        self.block_size = block_size
        self.total_blocks = total_blocks
        self.free_blocks = set(range(total_blocks))
        self.allocated_sequences: dict[int, list[int]] = {}

    def allocate_tokens(self, seq_id: int, num_tokens: int) -> list[int]:
        needed_blocks = math.ceil(num_tokens / self.block_size)
        if len(self.free_blocks) < needed_blocks:
            raise MemoryError("Out of KV-cache memory blocks")
        blocks = []
        for _ in range(needed_blocks):
            b = self.free_blocks.pop()
            blocks.append(b)
        self.allocated_sequences[seq_id] = blocks
        return blocks

    def free_sequence(self, seq_id: int) -> None:
        if seq_id in self.allocated_sequences:
            for b in self.allocated_sequences[seq_id]:
                self.free_blocks.add(b)
            del self.allocated_sequences[seq_id]
''',
        "test_code": '''"""Tests for Genius-ModelWeights invariants."""
import pytest
import math
from genius_model_weights.tools import (
    quantize_symmetric_int8,
    dequantize_symmetric_int8,
    apply_rope_2d,
    PagedKVCacheAllocator
)

def test_symmetric_int8_roundtrip():
    tensor = [-1.0, -0.5, 0.0, 0.5, 1.0]
    quantized, scale = quantize_symmetric_int8(tensor)
    assert len(quantized) == len(tensor)
    assert max(quantized) == 127
    assert min(quantized) == -127
    deq = dequantize_symmetric_int8(quantized, scale)
    for orig, reconstructed in zip(tensor, deq):
        assert math.isclose(orig, reconstructed, abs_tol=0.02)

def test_rope_rotation_isometry():
    # RoPE is a unitary rotation: norm(x) == norm(RoPE(x))
    x0, x1 = 3.0, 4.0
    norm_before = math.sqrt(x0**2 + x1**2)
    r0, r1 = apply_rope_2d(x0, x1, math.pi / 4.0)
    norm_after = math.sqrt(r0**2 + r1**2)
    assert math.isclose(norm_before, norm_after, rel_tol=1e-5)

def test_paged_kv_cache_allocator():
    alloc = PagedKVCacheAllocator(block_size=16, total_blocks=4)
    blocks = alloc.allocate_tokens(seq_id=1, num_tokens=32)
    assert len(blocks) == 2
    assert len(alloc.free_blocks) == 2
    alloc.free_sequence(seq_id=1)
    assert len(alloc.free_blocks) == 4
'''
    }
}
