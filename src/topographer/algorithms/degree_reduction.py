from __future__ import annotations

from collections.abc import Hashable

import networkx as nx


def _edge_key(a: Hashable, b: Hashable) -> tuple[Hashable, Hashable]:
    ordered = sorted((a, b), key=repr)
    return ordered[0], ordered[1]


def _orient_path(path: list[Hashable], start: Hashable, end: Hashable) -> list[Hashable]:
    if path and path[0] == start and path[-1] == end:
        return path

    if path and path[0] == end and path[-1] == start:
        return list(reversed(path))

    return [start, end]


def _dedupe_consecutive(path: list[Hashable]) -> list[Hashable]:
    if not path:
        return path

    compact = [path[0]]
    for vertex in path[1:]:
        if vertex != compact[-1]:
            compact.append(vertex)
    return compact


def _canonicalize_path(path: list[Hashable]) -> list[Hashable]:
    if len(path) <= 1:
        return path

    reversed_path = list(reversed(path))
    if tuple(map(repr, path)) <= tuple(map(repr, reversed_path)):
        return path

    return reversed_path


def reduce_degree_two_nodes(
    tree: nx.Graph,
    arc_vertices: dict[tuple[Hashable, Hashable], list[Hashable]],
) -> tuple[nx.Graph, dict[tuple[Hashable, Hashable], list[Hashable]]]:
    reduced = tree.copy()
    reduced_arc_vertices = dict(arc_vertices)

    changed = True
    while changed:
        changed = False

        for node in list(reduced.nodes()):
            if node not in reduced or reduced.degree(node) != 2:
                continue

            neighbor_a, neighbor_b = list(reduced.neighbors(node))
            key_a = _edge_key(neighbor_a, node)
            key_b = _edge_key(node, neighbor_b)

            path_a = _orient_path(
                reduced_arc_vertices.get(key_a, [neighbor_a, node]),
                start=neighbor_a,
                end=node,
            )
            path_b = _orient_path(
                reduced_arc_vertices.get(key_b, [node, neighbor_b]),
                start=node,
                end=neighbor_b,
            )

            merged_path = _dedupe_consecutive(path_a[:-1] + path_b)

            reduced.remove_node(node)
            reduced_arc_vertices.pop(key_a, None)
            reduced_arc_vertices.pop(key_b, None)

            if neighbor_a == neighbor_b:
                changed = True
                break

            key = _edge_key(neighbor_a, neighbor_b)
            reduced.add_edge(*key)
            reduced_arc_vertices[key] = _canonicalize_path(merged_path)
            changed = True
            break

    for edge in list(reduced_arc_vertices.keys()):
        if not reduced.has_edge(*edge):
            reduced_arc_vertices.pop(edge, None)

    for edge in reduced.edges():
        key = _edge_key(edge[0], edge[1])
        if key not in reduced_arc_vertices:
            reduced_arc_vertices[key] = [key[0], key[1]]

    return reduced, reduced_arc_vertices


__all__ = ["reduce_degree_two_nodes"]
