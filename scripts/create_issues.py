#!/usr/bin/env python3
"""Создаёт GitHub Issues из data/bugs.json и (опционально) метки из .github/labels.yml.

Повторный запуск безопасен: уже созданные Issues пропускаются.
Запускается кнопкой в GitHub Actions (workflow "Setup issues") или локально через GitHub CLI.

  python3 scripts/create_issues.py            # сухой прогон: только печатает, что будет создано
  python3 scripts/create_issues.py --apply    # создать метки и Issues в репозитории
  python3 scripts/create_issues.py --apply --sprint 3   # только спринт 3 (2, 3, 4 или all)
"""
import json, subprocess, sys, re

from config import BUG_DATA as DATA, REPO, ROOT, raw_url

RAW = {sp: raw_url(sp) for sp in DATA}
PRIO = {"critical": "high", "major": "medium", "minor": "low"}
AREA = {"Часы": "hours", "Минуты": "minutes", "Откуда": "address-from", "Куда": "address-to", "Расчёт": "calculation"}
SEV_RU = {"critical": "Critical (критический)", "major": "Major (стандартный)", "minor": "Minor (желательный)"}
apply = "--apply" in sys.argv
SPRINTS = ["2", "3", "4"] if "--sprint" not in sys.argv else [sys.argv[sys.argv.index("--sprint") + 1]]
if SPRINTS == ["all"]:
    SPRINTS = ["2", "3", "4"]


def run(cmd):
    if apply:
        subprocess.run(cmd, check=True)
    else:
        print("DRY-RUN:", " ".join(cmd[:6]), "...")


def body(b, sp):
    steps = "\n".join(b["steps"])
    shot = f"\n\n### Скриншот\n![{b['id']}]({RAW[sp]}{b['screenshot']})" if b.get("screenshot") else ""
    if b.get("video_gif"):
        shot += f"\n\n### Видео (GIF)\n![{b['id']} GIF]({raw_url(sp, 'media')}{b['video_gif']})"
    return f"""**ID:** `{b['id']}` · {('**Тест-кейс:** `' + b['test_case'] + '` · ') if b.get('test_case') else ''}**Серьёзность:** {SEV_RU[b['severity']]}

### Предусловия
{b['preconditions']}

### Шаги воспроизведения
{steps}

### Ожидаемый результат
{b['expected']}

### Фактический результат
{b['actual']}

### Окружение
{b['environment']}{shot}
"""


def main():
    labels = [l for l in re.findall(r'name: "([^"]+)", color: "(\w+)", description: "([^"]*)"', (ROOT / ".github/labels.yml").read_text())]
    for n, c, d in labels:
        run(["gh", "label", "create", n, "--color", c, "--description", d, "--force", "--repo", REPO])
    existing = set()
    if apply:
        out = subprocess.run(["gh", "issue", "list", "--repo", REPO, "--state", "all", "--limit", "500", "--json", "title"],
                             check=True, capture_output=True, text=True).stdout
        existing = {i["title"] for i in json.loads(out)}
    for sp in SPRINTS:
        for b in json.loads((ROOT / DATA[sp]).read_text()):
            title = f"[С{sp}][{b['id']}] {b['title']}" if sp in ("3", "4") else f"[{b['id']}] {b['title']}"
            if title in existing:
                print("уже есть, пропуск:", b["id"])
                continue
            area = AREA.get(b["area"], b["area"])
            lab = ["bug", f"sprint-{sp}", f"severity: {b['severity']}", f"priority: {PRIO[b['severity']]}", f"area: {area}", "status: open"]
            cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body(b, sp)]
            for l in lab:
                cmd += ["--label", l]
            run(cmd)
    print("Готово." if apply else "Это был сухой прогон. Добавьте --apply, чтобы создать Issues.")


if __name__ == "__main__":
    main()
