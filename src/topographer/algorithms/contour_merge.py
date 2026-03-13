from __future__ import annotations

from collections.abc import Hashable

import networkx as nx

from topographer.models.split_join import JoinTreeResult, SplitTreeResult


def _edge_key(a: Hashable, b: Hashable) -> tuple[Hashable, Hashable]:
    ordered = sorted((a, b), key=repr)
    return ordered[0], ordered[1]


def _canonicalize_path(path: list[Hashable]) -> list[Hashable]:
    if len(path) <= 1:
        return path

    reversed_path = list(reversed(path))
    if tuple(map(repr, path)) <= tuple(map(repr, reversed_path)):
        return path

    return reversed_path


def merge_split_join_trees(
    split_result: SplitTreeResult,
    join_result: JoinTreeResult,
) -> tuple[nx.Graph, dict[tuple[Hashable, Hashable], list[Hashable]]]:
    if split_result.scalar != join_result.scalar:
        raise ValueError("Split tree and join tree must use the same scalar attribute")

    merged_tree = nx.Graph()
    merged_tree.add_nodes_from(split_result.tree.nodes())
    merged_tree.add_nodes_from(join_result.tree.nodes())
    merged_tree.add_edges_from(_edge_key(a, b) for a, b in split_result.tree.edges())
    merged_tree.add_edges_from(_edge_key(a, b) for a, b in join_result.tree.edges())

    merged_arc_vertices: dict[tuple[Hashable, Hashable], list[Hashable]] = {}

    for source in (split_result.arc_vertices, join_result.arc_vertices):
        for edge, path in source.items():
            key = _edge_key(edge[0], edge[1])
            canonical_path = _canonicalize_path(path)

            existing = merged_arc_vertices.get(key)
            if existing is None or len(canonical_path) > len(existing):
                merged_arc_vertices[key] = canonical_path

    for edge in merged_tree.edges():
        key = _edge_key(edge[0], edge[1])
        if key not in merged_arc_vertices:
            merged_arc_vertices[key] = [key[0], key[1]]

    return merged_tree, merged_arc_vertices


__all__ = ["merge_split_join_trees"]
