import networkx as nx
import pytest

from topographer.transforms.perturb import (
    find_ties,
    has_ties,
    is_strictly_ordered,
    perturb_ties,
)


def test_find_ties_and_has_ties_detect_duplicates() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            ("a", {"f": 1.0}),
            ("b", {"f": 1.0}),
            ("c", {"f": 2.0}),
        ]
    )

    ties = find_ties(graph, "f")

    assert has_ties(graph, "f")
    assert ties == {1.0: ["a", "b"]}


def test_is_strictly_ordered_reports_unique_values() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, {"f": 1.0}),
            (1, {"f": 2.0}),
            (2, {"f": 3.0}),
        ]
    )

    assert is_strictly_ordered(graph, "f")


def test_perturb_ties_creates_default_output_scalar_without_mutating_input() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            ("b", {"f": 3.0}),
            ("a", {"f": 3.0}),
            ("x", {"f": 4.0}),
        ]
    )

    result = perturb_ties(graph, "f")

    assert result.output_scalar == "f_perturbed"
    assert result.ties_found
    assert result.perturbed_nodes == ["a", "b"]
    assert result.graph.nodes["x"]["f_perturbed"] == 4.0
    assert result.graph.nodes["a"]["f_perturbed"] < result.graph.nodes["b"]["f_perturbed"]
    assert "f_perturbed" not in graph.nodes["a"]


def test_perturb_ties_inplace_overwrites_input_scalar_when_requested() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, {"f": 2.0}),
            (1, {"f": 2.0}),
            (2, {"f": 3.0}),
        ]
    )

    result = perturb_ties(graph, "f", output_scalar="f", inplace=True, epsilon=1e-3)

    assert result.graph is graph
    assert abs(graph.nodes[0]["f"] - 2.0) < 1e-12
    assert abs(graph.nodes[1]["f"] - 2.001) < 1e-12
    assert abs(graph.nodes[2]["f"] - 3.0) < 1e-12
    assert is_strictly_ordered(graph, "f")


def test_perturb_ties_no_ties_returns_unchanged_values() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, {"f": 1.0}),
            (1, {"f": 2.0}),
            (2, {"f": 3.0}),
        ]
    )

    result = perturb_ties(graph, "f", output_scalar="fp")

    assert not result.ties_found
    assert result.epsilon == 0.0
    assert result.perturbed_nodes == []
    assert nx.get_node_attributes(result.graph, "fp") == {0: 1.0, 1: 2.0, 2: 3.0}


def test_perturb_ties_rejects_unsupported_method() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, {"f": 1.0}),
            (1, {"f": 1.0}),
        ]
    )

    with pytest.raises(ValueError, match="Unsupported perturbation method"):
        perturb_ties(graph, "f", method="random")


def test_perturb_ties_rejects_non_positive_epsilon() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, {"f": 1.0}),
            (1, {"f": 1.0}),
        ]
    )

    with pytest.raises(ValueError, match="epsilon must be positive"):
        perturb_ties(graph, "f", epsilon=0.0)
