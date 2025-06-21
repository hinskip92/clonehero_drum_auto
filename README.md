
# CloneHero Drum Auto

Generate Clone Hero drum charts from audio.

### Highlights

- Automatic audio conversion to `song.ogg` using FFmpeg
- Graceful Demucs fallback if no GPU or CLI is available
- Beat‑accurate SyncTrack and stubbed Star Power phrases
- 16th‑note quantisation with velocity accents

## Install

```bash
python -m pip install -r requirements.txt
```

## CLI Usage

```bash
python -m clonehero_drum_auto.cli chart my_song.mp3 --outdir MySongChart
```

## GUI Usage

```bash
python -m clonehero_drum_auto.gui
```

A Gradio browser window opens where you can upload a song and download the generated `.chart` and `song.ini`.
