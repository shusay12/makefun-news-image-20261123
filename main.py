#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261123.

Copies the pre-drawn front page (entry.png, built by build_image.py)
to the grader's output directory, byte for byte. Standard library only,
no network, fully deterministic: two runs write identical bytes.

The grader runs this with a read-only repository and a writable
/output; outside the grader, MAKEFUN_OUTPUT_DIR overrides the target.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def png_size(path):
    """Read width/height from a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError("entry.png is not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print("error: entry.png missing next to main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the 1 MiB gate",
              file=sys.stderr)
        return 1
    width, height = png_size(SRC)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"error: entry.png is {width}x{height}, over the 1024px gate",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if sha256(SRC) != sha256(dst):
        print("error: copied file differs from source", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
