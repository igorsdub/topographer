from __future__ import annotations

import networkx as nx

from topographer.algorithms.contour_merge import merge_split_join_trees
from topographer.algorithms.degree_reduction import reduce_degree_two_nodes
from topographer.algorithms.join_tree import compute_join_tree
from topographer.algorithms.split_tree import compute_split_tree
from topographer.models.tree import ContourTree, JoinTree, SplitTree


def compute_contour_tree_from_split_join(
    ST: SplitTree,
    JT: JoinTree,
) -> ContourTree:
    merged_tree, merged_arc_vertices = merge_split_join_trees(ST, JT)
    reduced_tree, reduced_arc_vertices = reduce_degree_two_nodes(merged_tree, merged_arc_vertices)

    critical_nodes = sorted(set(ST.critical_nodes) | set(JT.critical_nodes), key=repr)

    node_metadata = dict(ST.node_metadata)
    node_metadata.update(JT.node_metadata)

    return ContourTree(
        graph=reduced_tree,
        scalar=ST.scalar,
        split_tree=ST,
        join_tree=JT,
        augmented=False,
        critical_nodes=critical_nodes,
        arc_vertices=reduced_arc_vertices,
        node_metadata=node_metadata,
    )


def compute_contour_tree(
    graph: nx.Graph,
    scalar: str = "scalar",
    *,
    require_connected: bool = True,
) -> ContourTree:
    ST = compute_split_tree(
        graph,
        scalar=scalar,
        require_connected=require_connected,
    )
    JT = compute_join_tree(
        graph,
        scalar=scalar,
        require_connected=require_connected,
    )

    return compute_contour_tree_from_split_join(ST, JT)


__all__ = ["compute_contour_tree", "compute_contour_tree_from_split_join"]
