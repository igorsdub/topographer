from topographer.algorithms._critical import (
    is_join_critical,
    is_split_critical,
    lower_link,
    upper_link,
)
from topographer.algorithms._sweep import sweep_ascending, sweep_descending
from topographer.examples import easy_path_graph


def test_critical_helpers_on_path_graph():
    graph = easy_path_graph(3)

    assert lower_link(graph, 1, scalar="scalar") == [0]
    assert upper_link(graph, 1, scalar="scalar") == [2]

    assert is_join_critical(graph, 1, scalar="scalar") is False
    assert is_split_critical(graph, 1, scalar="scalar") is False

    assert is_join_critical(graph, 0, scalar="scalar") is True
    assert is_split_critical(graph, 2, scalar="scalar") is True


def test_sweep_ascending_visits_low_to_high():
    graph = easy_path_graph(4)
    seen_orders: list[tuple[int, set[int]]] = []

    def _visit(node, seen):
        seen_orders.append((node, set(seen)))

    sweep_ascending(graph, scalar="scalar", visit_fn=_visit)

    assert [node for node, _ in seen_orders] == [0, 1, 2, 3]
    assert seen_orders[0][1] == set()
    assert seen_orders[-1][1] == {0, 1, 2}


def test_sweep_descending_visits_high_to_low():
    graph = easy_path_graph(4)
    visited: list[int] = []

    def _visit(node, seen):
        _ = seen
        visited.append(node)

    sweep_descending(graph, scalar="scalar", visit_fn=_visit)

    assert visited == [3, 2, 1, 0]
