#!/usr/bin/env python3
"""Создаёт GitHub Issues из data/bugs.json и (опционально) метки из .github/labels.yml.

Повторный запуск безопасен: уже созданные Issues пропускаются.
Запускается кнопкой в GitHub Actions (workflow "Setup issues") или локально через GitHub CLI.

  python3 scripts/create_issues.py            # сухой прогон: только печатает, что будет создано
  python3 scripts/create_issues.py --apply    # создать метки и Issues в репозитории
"""
import json, os, subprocess, sys, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = os.environ.get("GITHUB_REPOSITORY", "ikqavscode-afk/qa-test-documentation")
RAW = f"https://raw.githubusercontent.com/{REPO}/main/sprint-2-YaM/bug-reports/screenshots/"
PRIO = {"critical": "high", "major": "medium", "minor": "low"}
AREA = {"Часы": "hours", "Минуты": "minutes", "Откуда": "address-from", "Куда": "address-to", "Расчёт": "calculation"}
SEV_RU = {"critical": "Critical (критический)", "major": "Major (стандартный)", "minor": "Minor (желательный)"}
apply = "--apply" in sys.argv


def run(cmd):
    if apply:
        subprocess.run(cmd, check=True)
    else:
        print("DRY-RUN:", " ".join(cmd[:6]), "...")


def body(b):
    steps = "\n".join(b["steps"])
    shot = f"\n\n### Скриншот\n![{b['id']}]({RAW}{b['screenshot']})" if b.get("screenshot") else ""
    return f"""**ID:** `{b['id']}` · **Тест-кейс:** `{b['test_case']}` · **Серьёзность:** {SEV_RU[b['severity']]}

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
    for b in json.loads((ROOT / "data/bugs.json").read_text()):
        if f"[{b['id']}] {b['title']}" in existing:
            print("уже есть, пропуск:", b["id"])
            continue
        lab = ["bug", f"severity: {b['severity']}", f"priority: {PRIO[b['severity']]}", f"area: {AREA[b['area']]}", "status: open"]
        cmd = ["gh", "issue", "create", "--repo", REPO, "--title", f"[{b['id']}] {b['title']}", "--body", body(b)]
        for l in lab:
            cmd += ["--label", l]
        run(cmd)
    print("Готово." if apply else "Это был сухой прогон. Добавьте --apply, чтобы создать Issues.")


if __name__ == "__main__":
    main()
