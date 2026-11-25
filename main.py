#!/usr/bin/env python3
"""Entry point: copy the finished front page to the grader's output.

The picture is drawn ahead of time by draw_front.py and shipped here
as entry.png, so this program needs no network and always writes the
same bytes. The grader sets MAKEFUN_OUTPUT_DIR; otherwise /output.
"""

import os
import shutil
from pathlib import Path


def main() -> Path:
    here = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(here / "entry.png", target)
    return target


if __name__ == "__main__":
    written = main()
    print(f"wrote {written} ({written.stat().st_size} bytes)")
