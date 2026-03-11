import typer

app = typer.Typer()

@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")