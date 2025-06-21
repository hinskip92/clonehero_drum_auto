
import typer
from pathlib import Path
from .pipeline import generate_chart
app = typer.Typer()

@app.command()
def chart(
    audio: str = typer.Argument(..., help="Input .mp3 or .wav"),
    outdir: str = typer.Option("output_chart", help="Output directory")
):
    """Generate Clone Hero drum chart from audio."""
    generate_chart(audio, outdir)

if __name__ == "__main__":
    app()
