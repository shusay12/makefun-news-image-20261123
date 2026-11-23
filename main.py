#!/usr/bin/env python3
"""news-image-20261123 entrypoint: put the pre-drawn front page where the grader looks.

The picture was drawn at build time by build_image.py and ships beside this
file as entry.png. This program only checks that the picture still fits the
gate and copies it, byte for byte, into the grader's output directory.
Standard library only; no network; the same input always yields the same
output bytes. Outside the grader, MAKEFUN_OUTPUT_DIR overrides /output.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(HERE, "entry.png")
LIMIT_BYTES = 1024 * 1024
LIMIT_SIDE = 1024


def read_dimensions(path):
    """Return (width, height) from a PNG file's IHDR chunk."""
    with open(path, "rb") as handle:
        prefix = handle.read(33)
    if len(prefix) < 33 or prefix[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: " + path)
    if prefix[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk: " + path)
    return struct.unpack(">II", prefix[16:24])


def digest(path):
    """SHA-256 hex digest of a file's bytes."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1 << 16)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def run():
    if not os.path.isfile(PICTURE):
        print("entry.png is missing next to main.py", file=sys.stderr)
        return 1
    nbytes = os.path.getsize(PICTURE)
    if nbytes > LIMIT_BYTES:
        print(f"entry.png is {nbytes} bytes, over the 1 MiB gate", file=sys.stderr)
        return 1
    width, height = read_dimensions(PICTURE)
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        print(f"entry.png is {width}x{height}, over the 1024px gate", file=sys.stderr)
        return 1
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(PICTURE, target)
    if digest(PICTURE) != digest(target):
        print("copied entry.png differs from the source", file=sys.stderr)
        return 1
    print(f"wrote {target} ({nbytes} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
