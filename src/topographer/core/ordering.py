from __future__ import annotations

from collections.abc import Hashable

import networkx as nx

from topographer.core.uniqueness import are_scalar_values_unique


def sort_nodes_ascending(G: nx.Graph, scalar: str = "scalar") -> list[Hashable]:
    return sorted(G.nodes(), key=lambda node: (G.nodes[node][scalar], repr(node)))


def sort_nodes_descending(G: nx.Graph, scalar: str = "scalar") -> list[Hashable]:
    return sorted(
        G.nodes(),
        key=lambda node: (G.nodes[node][scalar], repr(node)),
        reverse=True,
    )


def check_scalar_uniqueness(G: nx.Graph, scalar: str = "scalar") -> bool:
    return are_scalar_values_unique(G, scalar_attr=scalar)


__all__ = [
    "sort_nodes_ascending",
    "sort_nodes_descending",
    "check_scalar_uniqueness",
]
