"""Общие настройки скриптов: адреса, имена папок проектов и пути.

Любое переименование репозитория или папки проекта делается здесь один раз.
"""
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = os.environ.get("GITHUB_REPOSITORY", "ikqavscode-afk/qa-test-documentation")
SITE = "https://ikqavscode-afk.github.io/qa-test-documentation/"

# Папки проектов по номеру спринта
FOLDERS = {
    "1": "sprint-1-places",
    "2": "sprint-2-Routes",
    "3": "spritn-3-CarSh",
    "4": "spritn-4-Metro",
}

# Данные баг-репортов по номеру спринта (для создания Issues)
BUG_DATA = {"2": "data/bugs.json", "3": "data/sprint3-bugs.json", "4": "data/sprint4-bugs.json"}

# Куда копируются данные и медиа для сайта: (маска данных, папка сайта, номер спринта)
SITE_TARGETS = [
    ("sprint3-*.json", "docs/sprint3", "3"),
    ("sprint4-*.json", "docs/metro", "4"),
]


def raw_url(sprint: str, sub: str = "screenshots") -> str:
    """Адрес файла из папки bug-reports проекта на raw.githubusercontent.com."""
    return f"https://raw.githubusercontent.com/{REPO}/main/{FOLDERS[sprint]}/bug-reports/{sub}/"
