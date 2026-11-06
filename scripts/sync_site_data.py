#!/usr/bin/env python3
"""Копирует данные и медиа спринтов в docs/, чтобы их раздавал GitHub Pages."""
import pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGETS = [
    ("sprint3-*.json", "docs/sprint3", "spritn-3-CarSh"),
    ("sprint4-*.json", "docs/metro", "spritn-4-Metro"),
]
for pattern, site, project in TARGETS:
    site = ROOT / site
    (site / "data").mkdir(parents=True, exist_ok=True)
    (site / "media").mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "data").glob(pattern):
        shutil.copy(f, site / "data" / f.name)
    bugs = ROOT / project / "bug-reports"
    for sub in ("screenshots", "media"):
        for f in (bugs / sub).glob("*"):
            shutil.copy(f, site / "media" / f.name)
(ROOT / "docs" / "data").mkdir(parents=True, exist_ok=True)
shutil.copy(ROOT / "data" / "checklists.json", ROOT / "docs" / "data" / "checklists.json")
print("sync ok")
