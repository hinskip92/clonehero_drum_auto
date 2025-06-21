
from pathlib import Path
from utils.logger import logger
from typing import List, Tuple

def write_chart(ticks_and_lanes: List[Tuple[int,int]], beat_times, output_dir: Path, song_name="Song"):
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
    chart_lines.append(f"  0 = B {int(120000)}")  # placeholder 120 BPM
    chart_lines.append("}")
    chart_lines.append("")
    chart_lines.append("[ExpertDrums]")
    chart_lines.append("{")
    for tick, lane in ticks_and_lanes:
        chart_lines.append(f"  {tick} = N {lane} 0")
    chart_lines.append("}")
    (output_dir / "notes.chart").write_text("\n".join(chart_lines))
    (output_dir / "song.ini").write_text("\n".join([
        f'name = "{song_name}"',
        "charter = "clonehero-drum-auto"",
        "audio = song.ogg",
        "delay = 0"
    ]))
    logger.info("Chart written to %s", output_dir / "notes.chart")
