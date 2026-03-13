"""Composite CLI commands that orchestrate multi-step workflows."""

from pathlib import Path

import typer

from ._validation import load_and_validate_graph_or_exit

app = typer.Typer()


@app.command()
def pipeline(input_file: Path, output_file: Path):
    """Validate input graph and run the end-to-end topographic pipeline."""
    load_and_validate_graph_or_exit(input_file)

    typer.echo(f"Running pipeline: {input_file} -> {output_file}")
