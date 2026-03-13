from __future__ import annotations

import networkx as nx

from topographer.algorithms.contour_merge import merge_split_join_trees
from topographer.algorithms.degree_reduction import reduce_degree_two_nodes
from topographer.algorithms.join_tree import compute_join_tree
from topographer.algorithms.split_tree import compute_split_tree
from topographer.models.contour_tree import ContourTreeResult
from topographer.models.split_join import JoinTreeResult, SplitTreeResult


def compute_contour_tree_from_split_join(
    split_result: SplitTreeResult,
    join_result: JoinTreeResult,
) -> ContourTreeResult:
    merged_tree, merged_arc_vertices = merge_split_join_trees(split_result, join_result)
    reduced_tree, reduced_arc_vertices = reduce_degree_two_nodes(merged_tree, merged_arc_vertices)

    critical_nodes = sorted(
        set(split_result.critical_nodes) | set(join_result.critical_nodes), key=repr
    )

    return ContourTreeResult(
        tree=reduced_tree,
        scalar=split_result.scalar,
        augmented=False,
        critical_nodes=critical_nodes,
        arc_vertices=reduced_arc_vertices,
    )


def compute_contour_tree(
    graph: nx.Graph,
    scalar: str = "scalar",
    *,
    require_connected: bool = True,
) -> ContourTreeResult:
    split_result = compute_split_tree(
        graph,
        scalar=scalar,
        require_connected=require_connected,
    )
    join_result = compute_join_tree(
        graph,
        scalar=scalar,
        require_connected=require_connected,
    )

    return compute_contour_tree_from_split_join(split_result, join_result)


__all__ = ["compute_contour_tree", "compute_contour_tree_from_split_join"]
