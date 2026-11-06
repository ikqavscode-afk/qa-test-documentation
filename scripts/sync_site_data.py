#!/usr/bin/env python3
"""Копирует данные и медиа спринта 3 в docs/sprint3/, чтобы их раздавал GitHub Pages."""
import pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "docs" / "sprint3"
(SITE / "data").mkdir(parents=True, exist_ok=True)
(SITE / "media").mkdir(parents=True, exist_ok=True)
for f in (ROOT / "data").glob("sprint3-*.json"):
    shutil.copy(f, SITE / "data" / f.name)
bugs = ROOT / "spritn-3-CarSh" / "bug-reports"
for sub in ("screenshots", "media"):
    for f in (bugs / sub).glob("*"):
        shutil.copy(f, SITE / "media" / f.name)
print("sync ok")
