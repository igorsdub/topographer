"""Grouped CLI commands for join/split/contour tree computation."""

from pathlib import Path

import typer

from topographer.algorithms.contour_tree import compute_contour_tree
from topographer.algorithms.join_tree import compute_join_tree
from topographer.algorithms.split_tree import compute_split_tree
from topographer.io.save import save_graph

from ._validation import load_and_validate_graph_or_exit

app = typer.Typer()


@app.command("join")
def join(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
):
    """Compute a join tree from input graph and save it."""
    graph = load_and_validate_graph_or_exit(input_file, scalar_attr=scalar)
    result = compute_join_tree(graph, scalar=scalar)
    save_graph(result.tree, output_file)
    typer.echo(f"Computed join tree: {input_file} -> {output_file}")


@app.command("split")
def split(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
):
    """Compute a split tree from input graph and save it."""
    graph = load_and_validate_graph_or_exit(input_file, scalar_attr=scalar)
    result = compute_split_tree(graph, scalar=scalar)
    save_graph(result.tree, output_file)
    typer.echo(f"Computed split tree: {input_file} -> {output_file}")


@app.command("contour")
def contour(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
):
    """Compute a contour tree from input graph and save it."""
    graph = load_and_validate_graph_or_exit(input_file, scalar_attr=scalar)
    result = compute_contour_tree(graph, scalar=scalar)
    save_graph(result.tree, output_file)
    typer.echo(f"Computed contour tree: {input_file} -> {output_file}")
