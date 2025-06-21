
from pathlib import Path
import subprocess
import tempfile
import shutil
import librosa
import numpy as np
from madmom.features import beats
from utils.logger import logger

def separate_drums(audio_path: str, model: str = "htdemucs") -> Path:
    """Run Demucs to obtain a isolated drum stem.

    Returns path to drum stem wav file. If Demucs is unavailable, returns the
    original audio path.
    """
    logger.info("Separating drums with Demucs (%s)...", model)
    audio_path = Path(audio_path)
    out_dir = Path(tempfile.mkdtemp(prefix="demucs_"))
    cmd = ["demucs", "-o", str(out_dir), "-n", model, str(audio_path)]
    try:
        subprocess.run(cmd, check=True)
        stem_path = next(out_dir.rglob("drums.wav"))
        logger.info("Drum stem created at %s", stem_path)
        return stem_path
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        logger.warning("Demucs unavailable (%s). Using mix as drum stem.", e)
        return audio_path

def convert_to_ogg(src: Path, dst: Path) -> Path:
    """Convert any audio file to OGG Vorbis using ffmpeg."""
    src = Path(src)
    dst = Path(dst)
    if src.suffix.lower() == ".ogg":
        shutil.copy(src, dst)
        return dst
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg not found. Please install to convert audio.")
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-c:a",
        "libvorbis",
        "-qscale:a",
        "5",
        str(dst),
    ]
    subprocess.run(cmd, check=True)
    return dst

def detect_beats_tempo(audio_path: str):
    """Detect beat positions and tempo using madmom (fallback to librosa)."""
    logger.info("Running beat tracking...")
    proc = beats.RNNBeatProcessor()(str(audio_path))
    act = np.asarray(proc)
    dproc = beats.DBNBeatTrackingProcessor(fps=100)
    beats_ = dproc(act)
    if len(beats_) < 4:  # fallback
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        tempo, beats_ = librosa.beat.beat_track(y=y, sr=sr, units='time')
    logger.info("Detected %d beats", len(beats_))
    return beats_
