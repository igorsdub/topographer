"""CLI commands for contour-tree computation."""

from pathlib import Path

import typer

from topographer.algorithms.contour_tree import compute_contour_tree
from topographer.io.save import save_graph

from ._validation import load_and_validate_graph_or_exit

app = typer.Typer()


@app.command()
def compute(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
):
    """Compute a contour tree from the input graph and save the result."""
    graph = load_and_validate_graph_or_exit(input_file, scalar_attr=scalar)
    result = compute_contour_tree(graph, scalar=scalar)
    save_graph(result.tree, output_file)

    typer.echo(f"Computed contour tree: {input_file} -> {output_file}")
