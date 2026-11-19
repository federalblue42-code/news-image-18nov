#!/usr/bin/env python3
"""news-image-20261118 entrypoint.

Copies the committed front page — one image summing up Wednesday
18 November 2026's world news — to /output/entry.png.
Deterministic: no network, no clock, byte-identical on every run.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.environ.get("OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))