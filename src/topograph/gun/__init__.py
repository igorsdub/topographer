import typer

from .load import app as load_app
from .shoot import app as shoot_app

app = typer.Typer()

app.add_typer(load_app)
app.add_typer(shoot_app)