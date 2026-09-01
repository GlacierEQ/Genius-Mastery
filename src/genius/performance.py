# src/genius/performance.py
"""Performance claims and benchmarking."""
from __future__ import annotations
import time
from pathlib import Path
from typing import TypedDict, Callable, Any
from genius.synthesize import synthesize_role
from genius.validate import validate_repo
from genius.graph import rebuild_graph

class PerfResult(TypedDict):
    operation: str
    n_iterations: int
    mean_ms: float
    p95_ms: float
    p99_ms: float

def benchmark(fn: Callable[[], Any], n: int = 1000) -> PerfResult:
    times = []
    for _ in range(n):
        t0 = time.perf_counter_ns()
        fn()
        t1 = time.perf_counter_ns()
        times.append((t1 - t0) / 1_000_000.0) # ms
        
    times.sort()
    mean_ms = sum(times) / len(times) if times else 0.0
    p95_idx = int(len(times) * 0.95)
    p99_idx = int(len(times) * 0.99)
    
    return {
        "operation": fn.__name__ if hasattr(fn, "__name__") else "unknown",
        "n_iterations": n,
        "mean_ms": mean_ms,
        "p95_ms": times[p95_idx] if times else 0.0,
        "p99_ms": times[p99_idx] if times else 0.0
    }

def benchmark_synthesis(role: str, outcome: str, n: int = 10) -> PerfResult:
    def _fn():
        synthesize_role(role, [outcome], Path("."))
    res = benchmark(_fn, n)
    res["operation"] = "synthesize_entity"
    return res

def benchmark_validate(root: Path, n: int = 100) -> PerfResult:
    def _fn():
        validate_repo(root)
    res = benchmark(_fn, n)
    res["operation"] = "validate_genius_yaml"
    return res

def benchmark_graph_rebuild(root: Path, n: int = 10) -> PerfResult:
    def _fn():
        rebuild_graph(root)
    res = benchmark(_fn, n)
    res["operation"] = "rebuild_graph"
    return res

def performance_report(results: list[PerfResult]) -> str:
    lines = [
        f"{'Operation':<25} | {'Iters':<6} | {'Mean (ms)':<10} | {'p95 (ms)':<10} | {'p99 (ms)':<10}",
        "-" * 70
    ]
    for r in results:
        lines.append(f"{r['operation']:<25} | {r['n_iterations']:<6} | {r['mean_ms']:<10.2f} | {r['p95_ms']:<10.2f} | {r['p99_ms']:<10.2f}")
    return "\n".join(lines)
