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
