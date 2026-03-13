import networkx as nx
import pytest

from topographer.core.uniqueness import (
    are_scalar_values_unique,
    assert_unique_scalar_values,
)
from topographer.examples import (
    easy_path_graph,
    get_graph_options,
    invalid_duplicate_scalar_graph,
    invalid_missing_scalar_graph,
)


def test_are_scalar_values_unique_accepts_valid_graph():
    """Confirm uniqueness check passes on a valid strictly ordered graph."""
    graph = easy_path_graph(5)

    assert are_scalar_values_unique(graph) is True


def test_are_scalar_values_unique_rejects_duplicate_values():
    """Confirm uniqueness check detects duplicate scalar assignments."""
    graph = invalid_duplicate_scalar_graph()

    assert are_scalar_values_unique(graph) is False


def test_assert_unique_scalar_values_raises_on_duplicate_values():
    """Ensure strict uniqueness assertion raises on duplicate scalar values."""
    graph = invalid_duplicate_scalar_graph()

    with pytest.raises(ValueError, match="Duplicate scalar values detected"):
        assert_unique_scalar_values(graph)


def test_assert_unique_scalar_values_raises_on_missing_scalar_attribute():
    """Ensure strict uniqueness assertion raises when scalar attributes are missing."""
    graph = invalid_missing_scalar_graph()

    with pytest.raises(ValueError, match="missing scalar attribute"):
        assert_unique_scalar_values(graph)


def test_assert_unique_scalar_values_rejects_non_networkx_graph():
    """Ensure strict uniqueness assertion rejects non-graph inputs."""
    with pytest.raises(TypeError, match="Graph must be a networkx.Graph"):
        assert_unique_scalar_values({})


def test_are_scalar_values_unique_supports_custom_attribute_name():
    """Ensure uniqueness helper supports non-default scalar attribute names."""
    graph = nx.path_graph(4)

    for index, node in enumerate(graph.nodes()):
        graph.nodes[node]["height"] = float(index)

    assert are_scalar_values_unique(graph, scalar_attr="height") is True


def test_valid_example_catalog_graphs_have_unique_scalar_values():
    """Verify selected example catalog graphs maintain unique scalar fields."""
    graph_options = get_graph_options()
    valid_graph_keys = [
        "easy_path",
        "easy_star",
        "medium_binary_tree",
        "medium_grid",
        "hard_barbell",
        "hard_lollipop",
        "invalid_disconnected",
    ]

    for key in valid_graph_keys:
        assert are_scalar_values_unique(graph_options[key]) is True


def test_invalid_duplicate_example_catalog_graph_has_non_unique_scalars():
    """Verify duplicate-scalar example is correctly flagged as non-unique."""
    graph_options = get_graph_options()

    assert are_scalar_values_unique(graph_options["invalid_duplicate_scalar"]) is False
