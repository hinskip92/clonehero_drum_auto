
from pathlib import Path
from utils.logger import logger
from .audio_preprocessing import separate_drums, detect_beats_tempo, convert_to_ogg
from .transcription import transcribe_drums
from .mapping import map_midi
from .chart_generation import write_chart

def generate_chart(audio_path: str, output_dir: str):
    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    drum_stem = separate_drums(audio_path)
    beat_times = detect_beats_tempo(audio_path)
    pm = transcribe_drums(drum_stem)
    ticks_and_lanes = map_midi(pm, beat_times)
    convert_to_ogg(audio_path, output_dir / "song.ogg")
    write_chart(ticks_and_lanes, beat_times, output_dir, song_name=audio_path.stem)
    logger.info("Done.")
