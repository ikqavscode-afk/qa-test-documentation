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

# ---- спринт 3
b3 = json.loads((ROOT / "data/sprint3-bugs.json").read_text())
c3 = json.loads((ROOT / "data/sprint3-checks.json").read_text())
res3 = Counter(c[br] for c in c3 for br in ("firefox_win", "ybr_mac") if c[br])
sv3 = Counter(b["severity"] for b in b3)
tot3 = sum(res3.values())
block3 = f"""<!-- STATS3:START (генерируется scripts/update_stats.py — не редактировать вручную) -->
{badge('checks', len(c3), 'blue')} {badge('results', tot3, 'blue')} {badge('passed', res3['Passed'], 'brightgreen')} {badge('failed', res3['Failed'], 'red')} {badge('blocked', res3['Blocked'], 'orange')} {badge('bugs', len(b3), 'orange')} {badge('critical', sv3['critical'], 'red')} {badge('release', 'No--Go', 'red')}

```mermaid
pie showData title Спринт 3: дефекты по серьёзности
    "Critical" : {sv3['critical']}
    "Major" : {sv3['major']}
    "Minor" : {sv3['minor']}
```
<!-- STATS3:END -->"""

# ---- спринт 4 (Метро)
b4 = json.loads((ROOT / "data/sprint4-bugs.json").read_text())
c4 = json.loads((ROOT / "data/sprint4-checks.json").read_text())
st4 = Counter(c["status"] for c in c4)
sv4 = Counter(b["severity"] for b in b4)
block4 = f"""<!-- STATS4:START (генерируется scripts/update_stats.py — не редактировать вручную) -->
{badge('checks', len(c4), 'blue')} {badge('passed', st4['Passed'], 'brightgreen')} {badge('failed', st4['Failed'], 'red')} {badge('blocked', st4['Blocked'], 'orange')} {badge('skipped', st4['Skipped'], 'lightgrey')} {badge('bugs', len(b4), 'orange')} {badge('critical', sv4['critical'], 'red')} {badge('release', 'Conditional%20Go', 'yellow')}

```mermaid
pie showData title Метро: результаты проверок
    "Passed" : {st4['Passed']}
    "Failed" : {st4['Failed']}
    "Blocked" : {st4['Blocked']}
    "Skipped" : {st4['Skipped']}
```
<!-- STATS4:END -->"""

p = ROOT / "README.md"
txt = p.read_text()
new = re.sub(r"<!-- STATS:START.*?<!-- STATS:END -->", lambda m: block, txt, flags=re.S)
new = re.sub(r"<!-- STATS3:START.*?<!-- STATS3:END -->", lambda m: block3, new, flags=re.S)
new = re.sub(r"<!-- STATS4:START.*?<!-- STATS4:END -->", lambda m: block4, new, flags=re.S)
p.write_text(new)
print("README обновлён:", dict(st), dict(sv))
