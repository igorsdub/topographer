from __future__ import annotations

"""Merge-tree construction (split and join) from a scalar graph."""

from collections.abc import Hashable
from typing import Literal

import networkx as nx

from topographer.algorithms._merge_rules import (
    SweepContext,
    finalize_components,
    handle_join_event,
    handle_split_event,
)
from topographer.algorithms._sweep import sweep_ascending, sweep_descending
from topographer.algorithms.augmentation import augment_join_tree, augment_split_tree
from topographer.core.graph_check import check_graph
from topographer.models.tree import MergeTree


def _compute_scalar_tree(
    G: nx.Graph,
    *,
    kind: Literal["split", "join"],
    scalar: str = "scalar",
    require_connected: bool = True,
    augment: bool = True,
) -> MergeTree:
    check_graph(G, scalar_attr=scalar, require_connected=require_connected)

    context = SweepContext()

    def _visit(node: Hashable, seen: set[Hashable]) -> None:
        seen_neighbors = [neighbor for neighbor in G.neighbors(node) if neighbor in seen]
        if kind == "split":
            handle_split_event(context, node=node, seen_neighbors=seen_neighbors)
        else:
            handle_join_event(context, node=node, seen_neighbors=seen_neighbors)

    if kind == "split":
        sweep_descending(G, scalar=scalar, visit_fn=_visit)
    else:
        sweep_ascending(G, scalar=scalar, visit_fn=_visit)

    roots = finalize_components(context)

    if require_connected and len(roots) != 1:
        raise RuntimeError(f"Expected exactly one root for a connected graph, got {len(roots)}")

    root = roots[0] if roots else None

    reverse = kind == "split"
    critical_nodes = sorted(
        context.critical_nodes,
        key=lambda node: G.nodes[node][scalar],
        reverse=reverse,
    )

    node_metadata = {node: {scalar: G.nodes[node][scalar]} for node in G.nodes()}

    base_result = MergeTree(
        graph=context.tree,
        root=root,
        critical_nodes=critical_nodes,
        scalar=scalar,
        kind=kind,
        augmented=False,
        arc_vertices=context.arc_vertices,
        node_metadata=node_metadata,
    )

    if not augment:
        return base_result

    if kind == "split":
        return augment_split_tree(base_result)
    return augment_join_tree(base_result)


def compute_split_tree(
    G: nx.Graph,
    scalar: str = "scalar",
    *,
    require_connected: bool = True,
    augment: bool = True,
) -> MergeTree:
    """Compute the split tree using a descending scalar sweep."""
    return _compute_scalar_tree(
        G,
        kind="split",
        scalar=scalar,
        require_connected=require_connected,
        augment=augment,
    )


def compute_join_tree(
    G: nx.Graph,
    scalar: str = "scalar",
    *,
    require_connected: bool = True,
    augment: bool = True,
) -> MergeTree:
    """Compute the join tree using an ascending scalar sweep."""
    return _compute_scalar_tree(
        G,
        kind="join",
        scalar=scalar,
        require_connected=require_connected,
        augment=augment,
    )


__all__ = ["compute_split_tree", "compute_join_tree"]
