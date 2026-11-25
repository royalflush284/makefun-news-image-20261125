#!/usr/bin/env python3
"""THE CAPITAL STANDARD — entrypoint. Stdlib only, copy-only, no network.
Copies the embedded entry.png beside this file to /output/entry.png."""
import shutil
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path("/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / "entry.png"
    except OSError:
        dest = Path.cwd() / "output" / "entry.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)


if __name__ == "__main__":
    main()
