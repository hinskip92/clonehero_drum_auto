
"""Utilities for preparing datasets from existing charts."""
from pathlib import Path
import pretty_midi, re, numpy as np
from utils.logger import logger

def parse_chart(chart_path: Path):
    """Very naive .chart drum note parser."""
    notes = []
    in_drums = False
    tick_regex = re.compile(r"(\d+) = N (\d+) 0")
    for line in chart_path.read_text().splitlines():
        if line.strip() == "[ExpertDrums]":
            in_drums = True
            continue
        if in_drums and line.strip() == "}":
            break
        if in_drums:
            m = tick_regex.search(line)
            if m:
                tick, lane = map(int, m.groups())
                notes.append((tick, lane))
    return notes

def chart_to_midi(chart_path: Path, resolution=192):
    notes = parse_chart(chart_path)
    pm = pretty_midi.PrettyMIDI()
    drum = pretty_midi.Instrument(program=0, is_drum=True)
    for tick, lane in notes:
        pitch = [43, 38, 42, 51, 36][lane]  # simple mapping
        start = tick / resolution / 2.0  # placeholder timing
        drum.notes.append(pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=start+0.1))
    pm.instruments.append(drum)
    return pm
