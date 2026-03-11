import typer

from .gun import app as gun_app
from .version import app as version_app

app = typer.Typer()

app.add_typer(version_app)
app.add_typer(gun_app, name="gun")


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """
