
from utils.logger import logger
import numpy as np
import pretty_midi

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
    """Quantize absolute second times to ticks on a 16th note grid."""
    times = np.asarray(times)
    beat_times = np.asarray(beat_times)
    if len(beat_times) < 2:
        interval = 0.5  # fallback to 120 BPM
    else:
        interval = float(np.median(np.diff(beat_times)))
    subdiv = resolution // 4  # 16th note ticks
    ticks = []
    for t in times:
        idx = np.searchsorted(beat_times, t) - 1
        if idx < 0:
            idx = 0
        beat_start = beat_times[idx]
        offset = t - beat_start
        tick = idx * resolution
        if interval > 0:
            quant = round(offset / (interval / 4))
            tick += quant * subdiv
        ticks.append(int(tick))
    return ticks

def map_midi(pm, beat_times):
    """Map PrettyMIDI drum track into lanes with velocity."""
    events = []
    for inst in pm.instruments:
        if not inst.is_drum:
            continue
        for note in inst.notes:
            lane = LANE_MAP.get(pretty_midi.note_number_to_drum_name(note.pitch).lower(), 1)
            events.append((note.start, lane, note.velocity))
    events.sort(key=lambda x: x[0])
    if events:
        times, lanes, vels = zip(*events)
    else:
        times, lanes, vels = [], [], []
    ticks = quantize(np.array(times), np.array(beat_times))
    logger.info("Mapped %d events to lanes.", len(ticks))
    return list(zip(ticks, lanes, vels))
