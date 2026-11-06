#!/usr/bin/env python3
"""Пересчитывает статистику из data/*.json и обновляет блок между маркерами STATS в README.md."""
import json, pathlib, re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
tests = json.loads((ROOT / "data/test-results.json").read_text())
bugs = json.loads((ROOT / "data/bugs.json").read_text())
st = Counter(t["status"] for t in tests)
sv = Counter(b["severity"] for b in bugs)
total = len(tests)
rate = round(100 * st["Passed"] / total)


def badge(label, msg, color):
    return f"![{label}](https://img.shields.io/badge/{label.replace(' ', '%20')}-{msg}-{color})"


areas = ["Часы", "Минуты", "Откуда", "Куда", "Расчёт"]
rows = []
for a in areas:
    ts = [t for t in tests if t["group"] == a]
    c = Counter(t["status"] for t in ts)
    nb = sum(1 for b in bugs if b["area"] == a)
    rows.append(f"| {a} | {len(ts)} | {c['Passed']} | {c['Failed']} | {c['Skipped']} | {nb} |")

block = f"""<!-- STATS:START (генерируется scripts/update_stats.py — не редактировать вручную) -->
{badge('test cases', total, 'blue')} {badge('passed', st['Passed'], 'brightgreen')} {badge('failed', st['Failed'], 'red')} {badge('skipped', st['Skipped'], 'lightgrey')} {badge('pass rate', str(rate) + '%25', 'yellowgreen')} {badge('bugs found', len(bugs), 'orange')}

| Область | Кейсов | ✅ | ❌ | ⏭ | Багов |
|---|---|---|---|---|---|
{chr(10).join(rows)}

```mermaid
pie showData title Результаты тест-кейсов
    "Passed" : {st['Passed']}
    "Failed" : {st['Failed']}
    "Skipped" : {st['Skipped']}
```

```mermaid
pie showData title Дефекты по серьёзности
    "Critical" : {sv['critical']}
    "Major" : {sv['major']}
    "Minor" : {sv['minor']}
```
<!-- STATS:END -->"""

p = ROOT / "README.md"
txt = p.read_text()
new = re.sub(r"<!-- STATS:START.*?<!-- STATS:END -->", lambda m: block, txt, flags=re.S)
p.write_text(new)
print("README обновлён:", dict(st), dict(sv))
