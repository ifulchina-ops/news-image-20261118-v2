#!/usr/bin/env python3
"""Entrypoint for the news-image-20261118 V2 entry.

Copies the front-page image this repository holds to the output
directory make.fun grades. No network, no drawing at grade time:
the image was generated during the build session by build_art.py
and is shipped in this repo as entry.png.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    if not os.path.isfile(SRC):
        print("error: %s is missing; run build_art.py first" % SRC,
              file=sys.stderr)
        return 1
    # MAKEFUN_OUTPUT_DIR names a directory; tolerate a full file path too.
    if out_dir.endswith(".png"):
        dest = out_dir
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
    else:
        os.makedirs(out_dir, exist_ok=True)
        dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    print("wrote %s (%d bytes, identical to entry.png)"
          % (dest, os.path.getsize(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
