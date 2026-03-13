"""CLI commands for join-tree computation."""

from pathlib import Path

import typer

from ._validation import load_and_validate_graph_or_exit

app = typer.Typer()


@app.command()
def compute(input_file: Path, output_file: Path):
    """Compute a join tree from the input scalar graph and write it to disk."""
    load_and_validate_graph_or_exit(input_file)

    typer.echo(f"Computing join tree: {input_file} -> {output_file}")
