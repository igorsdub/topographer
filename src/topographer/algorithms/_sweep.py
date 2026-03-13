from __future__ import annotations

"""Shared scalar-sweep traversal utilities.

These helpers visit graph nodes in scalar order and expose a callback that can
update algorithm-specific state (for example split/join sweep contexts).
"""

from collections.abc import Callable, Hashable, Iterable

import networkx as nx

from topographer.core.ordering import sort_nodes_ascending, sort_nodes_descending

VisitFn = Callable[[Hashable, set[Hashable]], None]


def sweep_ascending(
    G: nx.Graph,
    scalar: str,
    visit_fn: VisitFn,
    nodes: Iterable[Hashable] | None = None,
):
    """Visit nodes from low to high scalar value.

    The callback receives ``(node, seen)`` where ``seen`` contains previously
    visited nodes.
    """
    ordered_nodes = list(nodes) if nodes is not None else sort_nodes_ascending(G, scalar=scalar)
    seen: set[Hashable] = set()

    for node in ordered_nodes:
        visit_fn(node, seen)
        seen.add(node)


def sweep_descending(
    G: nx.Graph,
    scalar: str,
    visit_fn: VisitFn,
    nodes: Iterable[Hashable] | None = None,
):
    """Visit nodes from high to low scalar value.

    The callback receives ``(node, seen)`` where ``seen`` contains previously
    visited nodes.
    """
    ordered_nodes = list(nodes) if nodes is not None else sort_nodes_descending(G, scalar=scalar)
    seen: set[Hashable] = set()

    for node in ordered_nodes:
        visit_fn(node, seen)
        seen.add(node)


__all__ = ["sweep_ascending", "sweep_descending", "VisitFn"]
