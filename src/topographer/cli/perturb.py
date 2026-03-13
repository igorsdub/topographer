"""CLI command for deterministic scalar tie perturbation."""

from pathlib import Path

import typer

from topographer.io.load import load_graph
from topographer.io.save import save_graph
from topographer.transforms.perturb import perturb_ties

app = typer.Typer()


@app.callback(invoke_without_command=True)
def perturb(
    input_file: Path,
    output_file: Path,
    scalar: str = typer.Option("scalar", "--scalar", help="Input scalar attribute name."),
    output_scalar: str | None = typer.Option(
        None,
        "--output-scalar",
        help="Output scalar attribute name (defaults to '<scalar>_perturbed').",
    ),
    epsilon: float | None = typer.Option(
        None,
        "--epsilon",
        help="Perturbation step size. If omitted, chosen automatically.",
    ),
    method: str = typer.Option(
        "lexicographic",
        "--method",
        help="Tie-breaking strategy (currently only 'lexicographic').",
    ),
    inplace: bool = typer.Option(
        False,
        "--inplace",
        help="Write perturbed values into the input scalar attribute.",
    ),
) -> None:
    """Break tied scalar values and save the resulting graph."""

    graph = load_graph(input_file)

    try:
        result = perturb_ties(
            graph,
            scalar,
            output_scalar=output_scalar,
            inplace=inplace,
            epsilon=epsilon,
            method=method,
        )
    except KeyError as exc:
        missing_attr = exc.args[0]
        typer.echo(f"Missing scalar attribute: {missing_attr}")
        raise typer.Exit(code=1) from exc
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1) from exc

    save_graph(result.graph, output_file)

    typer.echo(
        "Perturbed scalar ties "
        f"({result.input_scalar} -> {result.output_scalar}, ties_found={result.ties_found}, "
        f"perturbed_nodes={len(result.perturbed_nodes)}): {input_file} -> {output_file}"
    )
