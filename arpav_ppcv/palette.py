import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def parse_palette(palette: str, palettes_dir: Path) -> Optional[list[str]]:
    palette_name = palette.split("/")[-1].lower()
    if is_inverted := "-inv" in palette_name:
        name = palette_name.replace("-inv", "")
    else:
        name = palette_name
    colors = []
    for file_path in [f for f in palettes_dir.iterdir() if f.is_file()]:
        if file_path.stem.lower() == name:
            try:
                colors = [
                    line.strip()
                    for line in file_path.read_text().splitlines()
                    if line.startswith("#")
                ]
            except OSError:
                logger.warning(f"Error reading file {file_path}")
            break
    else:
        logger.warning(f"Could not find a palette named {name!r} at {palettes_dir!r}")
    if is_inverted:
        colors.reverse()
    return colors if len(colors) > 0 else None


def apply_palette(
    colors: list[str], minimum: float, maximum: float
) -> list[tuple[float, str]]:
    minmax_range = maximum - minimum
    step_increment = minmax_range / (len(colors) - 1)
    result = []
    for i, current_color in enumerate(colors):
        current_value = minimum + i * step_increment
        result.append((current_value, current_color))
    return result
