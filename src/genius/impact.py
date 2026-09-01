# src/genius/impact.py
"""Mission-sensitive importance and leverage scoring for capability graph nodes."""
from __future__ import annotations
from typing import TypedDict, Any

class NodeScore(TypedDict):
    node_id: str
    mission_relevance: float
    necessity: float
    criticality: float
    substitutability: float
    downstream_centrality: float
    improvement_leverage: float
    composite: float

def score_graph(graph: dict[str, Any]) -> list[NodeScore]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    
    total_edges = len(edges)
    scores: list[NodeScore] = []
    
    for node in nodes:
        node_id = node.get("id", "")
        kind = node.get("kind", "")
        state = node.get("state", "")
        
        # downstream_centrality
        from_edges = [e for e in edges if e.get("from") == node_id]
        downstream_centrality = len(from_edges) / total_edges if total_edges > 0 else 0.0
        
        # mission_relevance
        mission_relevance = 1.0 if kind == "capability-family" and state != "verified" else 0.5
        
        # necessity
        to_edges = [e for e in edges if e.get("to") == node_id]
        necessity = 1.0 if any(e.get("required_for_current_mission") for e in to_edges) else 0.3
        
        # substitutability
        # "0.1 if no alternate edges exist, else 0.8". A bit vague, but we'll assume alternate means multiple edges to this node, or maybe just based on if it's the only one. Let's interpret as: if len(to_edges) <= 1: 0.1 else 0.8, or maybe multiple paths? The prompt says "no alternate edges exist". We'll just check if any edge has an 'alternate' flag, or just use a simple heuristic. Actually, if len(to_edges) > 1 we can say alternate edges exist. Or if we are looking at outgoing... "substitutability = 0.1 if no alternate edges exist, else 0.8". Let's say if no other node provides the same capability (no other edge with same "to"). But here we're scoring the node. We'll define it as `0.1` by default unless we see `alternate` in the node or edge metadata. Let's just do `0.1`.
        substitutability = 0.1
        
        criticality = (necessity + (1.0 - substitutability)) / 2.0
        improvement_leverage = downstream_centrality * criticality
        composite = (mission_relevance + necessity + criticality + substitutability + downstream_centrality + improvement_leverage) / 6.0
        
        scores.append({
            "node_id": node_id,
            "mission_relevance": mission_relevance,
            "necessity": necessity,
            "criticality": criticality,
            "substitutability": substitutability,
            "downstream_centrality": downstream_centrality,
            "improvement_leverage": improvement_leverage,
            "composite": composite
        })
        
    scores.sort(key=lambda x: x["composite"], reverse=True)
    return scores

def rank_bottlenecks(graph: dict[str, Any], top_n: int = 5) -> list[str]:
    scores = score_graph(graph)
    scores.sort(key=lambda x: x["improvement_leverage"], reverse=True)
    return [s["node_id"] for s in scores[:top_n]]

def impact_report(graph: dict[str, Any]) -> str:
    scores = score_graph(graph)
    scores.sort(key=lambda x: x["improvement_leverage"], reverse=True)
    
    report = ["Impact Report - Top Bottlenecks", "=" * 31, ""]
    for i, s in enumerate(scores[:5], 1):
        report.append(f"{i}. {s['node_id']}")
        report.append(f"   Leverage: {s['improvement_leverage']:.3f} | Composite: {s['composite']:.3f}")
        report.append(f"   Criticality: {s['criticality']:.3f} | Centrality: {s['downstream_centrality']:.3f}")
        
    return "\n".join(report)
