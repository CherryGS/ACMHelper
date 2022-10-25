from pathlib import Path
import typer
from graphviz import Digraph, Graph

from .system import app as sys_app

app = typer.Typer()
app.add_typer(sys_app, name="sys")


@app.command("render")
def render_graph(
    file: Path = typer.Argument(...),
    directed: bool = typer.Option(False, "--directed", "-d", help="Directed graph."),
    ignore: bool = typer.Option(False, "--ignore", "-i", help="Ignore the first line."),
    clean: bool = typer.Option(False, "--clean", "-c", help="Clean the temp file."),
):
    """Render the graph from file by Graphviz."""
    graph = Digraph if directed else Graph
    dot = graph("Graph", "Rendered by Graphviz")
    n = 0
    with open(file, "r") as f:
        for i, j in enumerate(f):
            if ignore and i == 0:
                n = int(j.split()[0])
                continue
            lis = j.split()
            dot.edge(*lis)
    for i in range(1, n+1):
        dot.node(str(i))
    dot.render(file.stem, format="png", cleanup=clean)
