#!/usr/bin/env python3
"""Ship the finished front page as the competition entry.

draw_front.py renders the page once into entry.png next to this file.
This entry point only places that finished picture where the grader
looks: $MAKEFUN_OUTPUT_DIR, falling back to /output. No network, no
re-rendering, so every run writes identical bytes.
"""

import os
import shutil
from pathlib import Path

SOURCE_NAME = "entry.png"


def output_directory() -> Path:
    """Where the grader expects the entry picture."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    directory = Path(chosen)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def ship() -> Path:
    """Copy the rendered front page into the output directory."""
    source = Path(__file__).resolve().parent / SOURCE_NAME
    destination = output_directory() / SOURCE_NAME
    shutil.copyfile(source, destination)
    return destination


if __name__ == "__main__":
    placed = ship()
    print(f"wrote {placed} ({placed.stat().st_size} bytes)")
