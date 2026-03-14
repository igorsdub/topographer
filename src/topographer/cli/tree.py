"""Grouped CLI commands for join/split/contour tree computation."""

import ast
from pathlib import Path

import networkx as nx
import typer

from topographer.algorithms.contour_tree import compute_contour_tree
from topographer.algorithms.join_tree import compute_join_tree
from topographer.algorithms.split_tree import compute_split_tree
from topographer.io.load import load_graph
from topographer.io.save import save_graph
from topographer.plotting import draw_tree, planar_layout, save_figure
from topographer.plotting.layout import assign_planar_layout

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


@app.command("layout")
def layout(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
    root: str | None = typer.Option(
        None,
        "--root",
        help="Optional root node identifier. Literal parsing is attempted.",
    ),
    x_mode: str = typer.Option(
        "leaf_span",
        "--x-mode",
        help="Horizontal coordinate strategy.",
    ),
    x_attr: str = typer.Option("layout_x", "--x-attr", help="Node x-attribute name."),
    y_attr: str = typer.Option("layout_y", "--y-attr", help="Node y-attribute name."),
    pos_attr: str = typer.Option("pos", "--pos-attr", help="Node tuple position attribute."),
):
    """Compute planar layout attributes for a tree graph and save the graph."""
    try:
        graph = load_graph(input_file)
        parsed_root = _parse_root_node(root, graph)
        assign_planar_layout(
            graph,
            scalar=scalar,
            root=parsed_root,
            x_mode=x_mode,
            x_attr=x_attr,
            y_attr=y_attr,
            pos_attr=pos_attr,
        )
        save_graph(graph, output_file)
    except (TypeError, ValueError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc

    typer.echo(f"Computed tree layout: {input_file} -> {output_file}")


@app.command("plot")
def plot(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Scalar attribute name."),
    root: str | None = typer.Option(
        None,
        "--root",
        help="Optional root node identifier. Literal parsing is attempted.",
    ),
    x_mode: str = typer.Option(
        "leaf_span",
        "--x-mode",
        help="Horizontal coordinate strategy.",
    ),
    with_labels: bool = typer.Option(False, "--with-labels", help="Show node labels."),
    show_regular: bool = typer.Option(
        False,
        "--show-regular",
        help="Display regular (non-critical) nodes.",
    ),
    output_format: str | None = typer.Option(
        None,
        "--format",
        help="Output image format: png, pdf, svg, html. Default is inferred from output path.",
    ),
):
    """Render a planar tree plot and export it to an image/HTML file."""
    try:
        graph = load_graph(input_file)
        parsed_root = _parse_root_node(root, graph)
        pos = planar_layout(graph, scalar=scalar, root=parsed_root, x_mode=x_mode)
        fig, _ = draw_tree(
            graph,
            pos=pos,
            with_labels=with_labels,
            show_regular=show_regular,
            scalar_attr=scalar,
        )
        save_figure(fig, output_file, format=output_format)
    except (RuntimeError, TypeError, ValueError) as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc
    finally:
        try:
            import matplotlib.pyplot as plt

            plt.close("all")
        except Exception:
            pass

    typer.echo(f"Saved tree plot: {input_file} -> {output_file}")


def _parse_root_node(root: str | None, graph: nx.Graph):
    if root is None:
        return None

    if root in graph:
        return root

    try:
        parsed = ast.literal_eval(root)
    except (SyntaxError, ValueError):
        parsed = root

    if parsed in graph:
        return parsed

    raise ValueError(f"Root {root!r} is not in tree")
