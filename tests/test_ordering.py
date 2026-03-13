from topographer.core.ordering import (
    check_scalar_uniqueness,
    sort_nodes_ascending,
    sort_nodes_descending,
)
from topographer.examples import easy_path_graph, invalid_duplicate_scalar_graph


def test_sort_nodes_ascending_orders_by_scalar():
    graph = easy_path_graph(5)

    assert sort_nodes_ascending(graph, scalar="scalar") == [0, 1, 2, 3, 4]


def test_sort_nodes_descending_orders_by_scalar():
    graph = easy_path_graph(5)

    assert sort_nodes_descending(graph, scalar="scalar") == [4, 3, 2, 1, 0]


def test_check_scalar_uniqueness_matches_graph_data():
    assert check_scalar_uniqueness(easy_path_graph(4), scalar="scalar") is True
    assert check_scalar_uniqueness(invalid_duplicate_scalar_graph(), scalar="scalar") is False
