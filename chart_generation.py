
from pathlib import Path
from utils.logger import logger
from typing import List, Tuple

def write_chart(ticks_and_lanes: List[Tuple[int,int,int]], beat_times, output_dir: Path, song_name="Song"):
    """Generate .chart and song.ini files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    resolution = 192
    chart_lines = []
    chart_lines.append("[Song]")
    chart_lines.append("{")
    chart_lines.append(f'  Name = "{song_name}"')
    chart_lines.append(f"  Resolution = {resolution}")
    chart_lines.append("  Player2 = drum")
    chart_lines.append("}")
    chart_lines.append("")
    chart_lines.append("[SyncTrack]")
    chart_lines.append("{")
    chart_lines.append("  0 = TS 4")
    beat_ticks = []
    for i, bt in enumerate(beat_times):
        tick = i * resolution
        beat_ticks.append(tick)
        if i + 1 < len(beat_times):
            interval = beat_times[i + 1] - bt
        elif i > 0:
            interval = beat_times[i] - beat_times[i - 1]
        else:
            interval = 0.5
        bpm = 60.0 / interval
        chart_lines.append(f"  {tick} = B {int(bpm * 1000)}")
    chart_lines.append("}")
    chart_lines.append("")
    chart_lines.append("[Events]")
    chart_lines.append("{")
    sp_len = 8 * resolution
    for i in range(25, len(beat_ticks), 25):
        start = beat_ticks[i]
        end = start + sp_len
        chart_lines.append(f'  {start} = E "star_power"')
        chart_lines.append(f'  {end} = E "star_power_end"')
    chart_lines.append("}")
    chart_lines.append("")
    chart_lines.append("[ExpertDrums]")
    chart_lines.append("{")
    for tick, lane, vel in ticks_and_lanes:
        chart_lines.append(f"  {tick} = N {lane} 0")
        if vel >= 96:
            chart_lines.append(f"  {tick} = A {lane}")
    chart_lines.append("}")
    (output_dir / "notes.chart").write_text("\n".join(chart_lines))
    (output_dir / "song.ini").write_text("\n".join([
        f'name = "{song_name}"',
        'charter = "clonehero-drum-auto"',
        "audio = song.ogg",
        "delay = 0"
    ]))
    logger.info("Chart written to %s", output_dir / "notes.chart")

