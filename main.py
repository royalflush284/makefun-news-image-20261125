"""Runner for the Final 1 NI25 entry, THE CAPITAL STANDARD.

The finished front page lives beside this file as entry.png.  This
runner is deliberately plain: it uses only the standard library,
touches no network, and copies that picture byte for byte into the
/output folder so the grader receives exactly the image that was
built and checked in this repository.

If entry.png is missing it is first rebuilt by running compose.py,
which paints the page from scratch with the standard library alone.
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def ensure_picture():
    if os.path.exists(SOURCE):
        return
    painter = os.path.join(HERE, "compose.py")
    subprocess.run([sys.executable, painter], check=True)


def main():
    ensure_picture()
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    print("copied entry.png to", DEST, os.path.getsize(DEST), "bytes")


if __name__ == "__main__":
    main()
