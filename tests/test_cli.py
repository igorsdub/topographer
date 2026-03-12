import pickle

import networkx as nx
from typer.testing import CliRunner

from topograph.cli.main import app
from topograph.io.load import load_graph

runner = CliRunner()


def _sample_graph() -> nx.Graph:
    graph = nx.Graph(name="sample")
    graph.add_node("a", value=1)
    graph.add_node("b", value=2)
    graph.add_edge("a", "b", weight=1.5)
    return graph


def _write_pickle_graph(path, graph: nx.Graph) -> None:
    with path.open("wb") as handle:
        pickle.dump(graph, handle)


def test_convert_command_converts_graph(tmp_path):
    source_path = tmp_path / "source.pkl"
    target_path = tmp_path / "converted.gexf"
    _write_pickle_graph(source_path, _sample_graph())

    result = runner.invoke(app, ["convert", str(source_path), str(target_path)])

    assert result.exit_code == 0
    assert target_path.exists()
    assert "Converted graph" in result.stdout

    loaded = load_graph(target_path)
    assert loaded.number_of_nodes() == 2
    assert loaded.number_of_edges() == 1


def _write_graph(path, graph: nx.Graph) -> None:
    with path.open("wb") as handle:
        pickle.dump(graph, handle)


def test_split_tree_compute_rejects_missing_scalar(tmp_path):
    source_path = tmp_path / "invalid.pkl"
    output_path = tmp_path / "split_tree.pkl"

    graph = nx.Graph()
    graph.add_edge("a", "b")
    graph.nodes["a"]["scalar"] = 1.0

    _write_graph(source_path, graph)

    result = runner.invoke(
        app,
        ["split-tree", "compute", str(source_path), str(output_path)],
    )

    assert result.exit_code == 1
    assert "missing scalar attribute" in result.stdout


def test_run_pipeline_validates_graph_before_execution(tmp_path):
    source_path = tmp_path / "valid.pkl"
    output_path = tmp_path / "output.pkl"

    graph = nx.Graph()
    graph.add_edge("a", "b")
    graph.nodes["a"]["scalar"] = 1.0
    graph.nodes["b"]["scalar"] = 2.0

    _write_graph(source_path, graph)

    result = runner.invoke(
        app,
        ["run", "pipeline", str(source_path), str(output_path)],
    )

    assert result.exit_code == 0
    assert "Running pipeline" in result.stdout
