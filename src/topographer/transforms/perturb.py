from __future__ import annotations

"""Deterministic tie-breaking for node scalar fields.

The perturbation keeps the original ordering between distinct scalar values and
splits ties by adding tiny offsets in a stable node order.
"""

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
    """Summary of a perturbation run.

    Attributes capture whether ties were found, which nodes changed, and where
    perturbed values were written.
    """

    graph: GraphType
    input_scalar: str
    output_scalar: str
    ties_found: bool
    tied_groups: dict[float, list[Hashable]]
    perturbed_nodes: list[Hashable]
    epsilon: float
    method: str


def _group_nodes_by_value(G: GraphType, scalar: str) -> dict[float, list[Hashable]]:
    """Group graph nodes by identical scalar value."""
    grouped: dict[float, list[Hashable]] = {}
    for node, attrs in G.nodes(data=True):
        value = float(attrs[scalar])
        grouped.setdefault(value, []).append(node)
    return grouped


def _default_output_scalar(scalar: str) -> str:
    """Return default output attribute name for perturbed scalars."""
    return f"{scalar}_perturbed"


def _choose_epsilon(values: list[float]) -> float:
    """Choose a small positive perturbation step from observed values.

    When at least two distinct values exist, epsilon is chosen small enough to
    avoid changing their relative order.
    """
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
    """Sort nodes deterministically for repeatable perturbations."""
    return sorted(nodes, key=lambda node: (type(node).__qualname__, repr(node)))


def _perturb_group(
    nodes: list[Hashable], base_value: float, epsilon: float
) -> dict[Hashable, float]:
    """Assign monotone offsets to tied nodes."""
    return {node: base_value + index * epsilon for index, node in enumerate(nodes)}


def _copy_or_inplace(G: GraphType, inplace: bool) -> GraphType:
    """Return either the original graph or a shallow copy."""
    if inplace:
        return G
    return G.copy()


def has_ties(G: GraphType, scalar: str) -> bool:
    """Return ``True`` when at least one scalar value appears multiple times."""
    return any(len(nodes) > 1 for nodes in _group_nodes_by_value(G, scalar).values())


def find_ties(G: GraphType, scalar: str) -> dict[float, list[Hashable]]:
    """Return scalar-value groups that contain ties only."""
    grouped = _group_nodes_by_value(G, scalar)
    return {value: nodes for value, nodes in grouped.items() if len(nodes) > 1}


def is_strictly_ordered(G: GraphType, scalar: str) -> bool:
    """Return ``True`` when all node scalar values are unique."""
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
    """Break scalar ties deterministically via tiny additive offsets.

    Parameters
    ----------
    G:
        Input graph.
    scalar:
        Source scalar attribute used to detect ties.
    output_scalar:
        Destination attribute for perturbed values. Defaults to
        ``f"{scalar}_perturbed"``.
    inplace:
        If ``True``, mutate ``G`` directly. Otherwise operate on a copy.
    epsilon:
        Optional perturbation step. If omitted, an order-preserving value is
        estimated from existing scalar spacing.
    method:
        Tie-breaking strategy. Currently only ``"lexicographic"`` is supported.
    """
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
