
from pathlib import Path
import pretty_midi
from utils.logger import logger

try:
    from omnizart.music.app import MusicTranscription
except ImportError:
    MusicTranscription = None  # placeholder

def transcribe_drums(audio_path: str, model: str = "drum") -> pretty_midi.PrettyMIDI:
    """Transcribe drums using Omnizart.

    Returns PrettyMIDI object containing a drum track.
    """
    if MusicTranscription is None:
        raise ImportError("Omnizart not installed. Please install with `pip install omnizart`.")
    logger.info("Transcribing drums with Omnizart...")
    mt = MusicTranscription()
    pm = mt.transcribe(audio_path, model=model)
    logger.info("Transcribed %d notes", sum(len(i.notes) for i in pm.instruments))
    return pm
