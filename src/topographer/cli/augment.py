"""Grouped CLI commands for tree augmentation workflows."""

from pathlib import Path

import typer

from topographer.algorithms.augmentation import (
    augment_contour_tree,
    augment_join_tree,
    augment_split_tree,
)
from topographer.algorithms.contour_tree import compute_contour_tree
from topographer.algorithms.merge_tree import compute_join_tree, compute_split_tree
from topographer.io.save import save_graph

from ._validation import load_and_validate_graph_or_exit

app = typer.Typer()


@app.command("join")
def join(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
):
    """Compute and save an augmented join tree with intermediate arc vertices."""
    graph = load_and_validate_graph_or_exit(input_file, scalar_attr=scalar)
    base = compute_join_tree(graph, scalar=scalar)
    result = augment_join_tree(base)
    save_graph(result.tree, output_file)
    typer.echo(f"Computed augmented join tree: {input_file} -> {output_file}")


@app.command("split")
def split(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
):
    """Compute and save an augmented split tree with intermediate arc vertices."""
    graph = load_and_validate_graph_or_exit(input_file, scalar_attr=scalar)
    base = compute_split_tree(graph, scalar=scalar)
    result = augment_split_tree(base)
    save_graph(result.tree, output_file)
    typer.echo(f"Computed augmented split tree: {input_file} -> {output_file}")


@app.command("contour")
def contour(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
):
    """Compute and save an augmented contour tree with intermediate arc vertices."""
    graph = load_and_validate_graph_or_exit(input_file, scalar_attr=scalar)
    base = compute_contour_tree(graph, scalar=scalar)
    result = augment_contour_tree(base)
    save_graph(result.tree, output_file)
    typer.echo(f"Computed augmented contour tree: {input_file} -> {output_file}")
