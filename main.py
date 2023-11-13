import typer
from rich import print as rprint

from transcribe import make_transcription

app = typer.Typer()


@app.command("transcribe")
def transcribe(path: str = "", model_name: str = None, output: str = ""):
    make_transcription(path, model_name, output)


@app.command("summarize")
def summarize():
    rprint("[#00e0d7]Welcome to Summarize AI![/#00e0d7]")
    rprint("[red]This feature is not implemented yet. Please check back later.")


if __name__ == "__main__":
    app()
