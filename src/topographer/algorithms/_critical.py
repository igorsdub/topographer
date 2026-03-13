from __future__ import annotations

from collections.abc import Hashable

import networkx as nx


def lower_link(G: nx.Graph, node: Hashable, scalar: str = "scalar") -> list[Hashable]:
    node_value = G.nodes[node][scalar]
    return [neighbor for neighbor in G.neighbors(node) if G.nodes[neighbor][scalar] < node_value]


def upper_link(G: nx.Graph, node: Hashable, scalar: str = "scalar") -> list[Hashable]:
    node_value = G.nodes[node][scalar]
    return [neighbor for neighbor in G.neighbors(node) if G.nodes[neighbor][scalar] > node_value]


def is_split_critical(G: nx.Graph, node: Hashable, scalar: str = "scalar") -> bool:
    return len(upper_link(G, node=node, scalar=scalar)) != 1


def is_join_critical(G: nx.Graph, node: Hashable, scalar: str = "scalar") -> bool:
    return len(lower_link(G, node=node, scalar=scalar)) != 1


__all__ = ["lower_link", "upper_link", "is_split_critical", "is_join_critical"]
