import pytest

from topographer import compute_join_tree, compute_split_tree
from topographer.examples import easy_path_graph, invalid_disconnected_graph


def test_compute_join_tree_non_augmented_path_graph():
    graph = easy_path_graph(6)

    result = compute_join_tree(graph, scalar="scalar", augmented=False)

    assert result.root == 5
    assert result.scalar == "scalar"
    assert result.critical_nodes == [0, 5]
    assert set(result.tree.nodes()) == {0, 5}
    assert set(result.tree.edges()) == {(0, 5)}
    assert result.arc_vertices[(0, 5)] == [0, 1, 2, 3, 4, 5]


def test_compute_split_tree_non_augmented_path_graph():
    graph = easy_path_graph(6)

    result = compute_split_tree(graph, scalar="scalar", augmented=False)

    assert result.root == 0
    assert result.scalar == "scalar"
    assert result.critical_nodes == [5, 0]
    assert set(result.tree.nodes()) == {0, 5}
    normalized_edges = {tuple(sorted(edge)) for edge in result.tree.edges()}
    assert normalized_edges == {(0, 5)}
    assert result.arc_vertices[(0, 5)] == [5, 4, 3, 2, 1, 0]


@pytest.mark.parametrize("fn", [compute_join_tree, compute_split_tree])
def test_augmented_split_join_tree_keeps_all_vertices(fn):
    graph = easy_path_graph(6)

    result = fn(graph, scalar="scalar", augmented=True)

    assert set(graph.nodes()).issubset(result.tree.nodes())
    assert result.tree.number_of_edges() == graph.number_of_edges()
    assert result.augmented is True


@pytest.mark.parametrize("fn", [compute_join_tree, compute_split_tree])
def test_split_join_support_disconnected_when_requested(fn):
    graph = invalid_disconnected_graph()

    result = fn(graph, scalar="scalar", require_connected=False)

    assert result.tree.number_of_nodes() > 0


@pytest.mark.parametrize("fn", [compute_join_tree, compute_split_tree])
def test_split_join_reject_disconnected_by_default(fn):
    graph = invalid_disconnected_graph()

    with pytest.raises(ValueError, match="Graph must be connected"):
        fn(graph, scalar="scalar")
