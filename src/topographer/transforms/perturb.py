from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from typing import TYPE_CHECKING

import networkx as nx

if TYPE_CHECKING:
    GraphType = nx.Graph[Hashable]
else:
    GraphType = nx.Graph


@dataclass
class PerturbationResult:
    graph: GraphType
    input_scalar: str
    output_scalar: str
    ties_found: bool
    tied_groups: dict[float, list[Hashable]]
    perturbed_nodes: list[Hashable]
    epsilon: float
    method: str


def _group_nodes_by_value(G: GraphType, scalar: str) -> dict[float, list[Hashable]]:
    grouped: dict[float, list[Hashable]] = {}
    for node, attrs in G.nodes(data=True):
        value = float(attrs[scalar])
        grouped.setdefault(value, []).append(node)
    return grouped


def _default_output_scalar(scalar: str) -> str:
    return f"{scalar}_perturbed"


def _choose_epsilon(values: list[float]) -> float:
    if not values:
        return 1e-12

    unique_values = sorted(set(values))
    gaps = [right - left for left, right in zip(unique_values, unique_values[1:]) if right > left]
    if gaps:
        min_gap = min(gaps)
        return min_gap / (2.0 * (len(values) + 1))

    scale = max(abs(value) for value in values)
    return max(scale, 1.0) * 1e-12


def _stable_node_order(nodes: list[Hashable]) -> list[Hashable]:
    return sorted(nodes, key=lambda node: (type(node).__qualname__, repr(node)))


def _perturb_group(
    nodes: list[Hashable], base_value: float, epsilon: float
) -> dict[Hashable, float]:
    return {node: base_value + index * epsilon for index, node in enumerate(nodes)}


def _copy_or_inplace(G: GraphType, inplace: bool) -> GraphType:
    if inplace:
        return G
    return G.copy()


def has_ties(G: GraphType, scalar: str) -> bool:
    return any(len(nodes) > 1 for nodes in _group_nodes_by_value(G, scalar).values())


def find_ties(G: GraphType, scalar: str) -> dict[float, list[Hashable]]:
    grouped = _group_nodes_by_value(G, scalar)
    return {value: nodes for value, nodes in grouped.items() if len(nodes) > 1}


def is_strictly_ordered(G: GraphType, scalar: str) -> bool:
    values = [float(attrs[scalar]) for _, attrs in G.nodes(data=True)]
    return len(values) == len(set(values))


def perturb_ties(
    G: GraphType,
    scalar: str,
    *,
    output_scalar: str | None = None,
    inplace: bool = False,
    epsilon: float | None = None,
    method: str = "lexicographic",
) -> PerturbationResult:
    if method != "lexicographic":
        raise ValueError(f"Unsupported perturbation method: {method}")

    graph = _copy_or_inplace(G, inplace=inplace)
    target_scalar = output_scalar or _default_output_scalar(scalar)
    ties = find_ties(graph, scalar)
    ties_found = bool(ties)

    original_values = {node: float(attrs[scalar]) for node, attrs in graph.nodes(data=True)}

    if target_scalar != scalar:
        for node, value in original_values.items():
            graph.nodes[node][target_scalar] = value

    if not ties_found:
        return PerturbationResult(
            graph=graph,
            input_scalar=scalar,
            output_scalar=target_scalar,
            ties_found=False,
            tied_groups={},
            perturbed_nodes=[],
            epsilon=0.0,
            method=method,
        )

    effective_epsilon = (
        epsilon if epsilon is not None else _choose_epsilon(list(original_values.values()))
    )
    if effective_epsilon <= 0:
        raise ValueError("epsilon must be positive")

    perturbed_nodes: list[Hashable] = []
    for value in sorted(ties):
        ordered_nodes = _stable_node_order(ties[value])
        assignments = _perturb_group(ordered_nodes, value, effective_epsilon)
        for node, perturbed_value in assignments.items():
            graph.nodes[node][target_scalar] = perturbed_value
        perturbed_nodes.extend(ordered_nodes)

    return PerturbationResult(
        graph=graph,
        input_scalar=scalar,
        output_scalar=target_scalar,
        ties_found=True,
        tied_groups=ties,
        perturbed_nodes=perturbed_nodes,
        epsilon=effective_epsilon,
        method=method,
    )


__all__ = [
    "PerturbationResult",
    "find_ties",
    "has_ties",
    "is_strictly_ordered",
    "perturb_ties",
]
