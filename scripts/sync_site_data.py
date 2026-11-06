#!/usr/bin/env python3
"""Копирует данные и медиа спринтов в docs/, чтобы их раздавал GitHub Pages."""
import shutil

from config import FOLDERS, ROOT, SITE_TARGETS

for pattern, site, sprint in SITE_TARGETS:
    site = ROOT / site
    (site / "data").mkdir(parents=True, exist_ok=True)
    (site / "media").mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "data").glob(pattern):
        shutil.copy(f, site / "data" / f.name)
    bugs = ROOT / FOLDERS[sprint] / "bug-reports"
    for sub in ("screenshots", "media"):
        for f in (bugs / sub).glob("*"):
            shutil.copy(f, site / "media" / f.name)
(ROOT / "docs" / "data").mkdir(parents=True, exist_ok=True)
shutil.copy(ROOT / "data" / "checklists.json", ROOT / "docs" / "data" / "checklists.json")
print("sync ok")
