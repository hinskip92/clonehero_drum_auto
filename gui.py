
import gradio as gr
import tempfile, pathlib
from .pipeline import generate_chart

def run(audio_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = pathlib.Path(tmpdir)
        generate_chart(audio_file, tmpdir)
        chart_path = tmpdir / "notes.chart"
        ini_path = tmpdir / "song.ini"
        return chart_path.read_text(), ini_path.read_text()

demo = gr.Interface(
    fn=run,
    inputs=gr.Audio(type="filepath", label="Upload song (.mp3/.wav)"),
    outputs=[gr.Code(label=".chart file"), gr.Code(label="song.ini")],
    title="Clone Hero Drum Chart Generator"
)

if __name__ == "__main__":
    demo.launch()
