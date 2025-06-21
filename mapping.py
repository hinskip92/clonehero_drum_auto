
from utils.logger import logger
import numpy as np

LANE_MAP = {
    "kick": 4,   # Orange
    "snare": 1,  # Red
    "closed hi-hat": 2,  # Yellow
    "open hi-hat": 2,
    "ride": 3,   # Blue
    "crash": 0,  # Green
    "tom low floor": 0,
    "tom mid": 3,
    "tom high": 2,
}

def quantize(times, beat_times, resolution=192):
    """Quantize absolute second times to ticks.

    Returns integer tick positions.
    """
    tick_positions = []
    for t in times:
        idx = np.argmin(np.abs(beat_times - t))
        beat = idx
        quarter = beat * resolution
        tick_positions.append(int(quarter))
    return tick_positions

def map_midi(pm, beat_times):
    """Map PrettyMIDI drum track into lanes.

    Returns list of tuples (tick, lane)
    """
    events = []
    for inst in pm.instruments:
        if not inst.is_drum: 
            continue
        for note in inst.notes:
            lane = LANE_MAP.get(pretty_midi.note_number_to_drum_name(note.pitch).lower(), 1)
            events.append((note.start, lane))
    events.sort(key=lambda x: x[0])
    times, lanes = zip(*events) if events else ([], [])
    ticks = quantize(np.array(times), np.array(beat_times))
    logger.info("Mapped %d events to lanes.", len(ticks))
    return list(zip(ticks, lanes))
