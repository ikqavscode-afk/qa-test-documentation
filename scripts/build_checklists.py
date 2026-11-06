#!/usr/bin/env python3
"""Собирает чек-листы проектов: data/checklists.json и checklist.md в папке каждого проекта.

Источник — файлы data/*.json. Запуск: python3 scripts/build_checklists.py
"""
import json
from collections import Counter, OrderedDict

from config import FOLDERS, ROOT, SITE

D = lambda n: json.loads((ROOT / "data" / n).read_text())

PROJECTS = [
    {
        "id": "sprint1", "folder": FOLDERS["1"], "sprint": "Спринт 1", "title": "Places — редактирование профиля",
        "essence": "Первое знакомство с циклом ручного тестирования: от чтения требований до регрессионных кейсов и баг-репортов, связанных с кейсами.",
        "object": "Веб-приложение Places: главная страница и окно редактирования профиля.",
        "focus": ["Функциональное тестирование", "Регрессионное тестирование", "Валидация полей формы", "Оформление баг-репортов"],
        "scope": ["Окно редактирования профиля: открытие, закрытие, поля, сохранение", "Валидация «Имя» (2–40 символов) и «Занятие» (2–200 символов)", "Активность кнопки «Сохранить»", "Баги, найденные кейсами (PlacesBug1–9), с приоритетами"],
        "out_of_scope": ["Автоматическое тестирование", "Карточки мест: добавление, лайк, удаление, просмотр", "Кроссбраузерная проверка"],
        "environment": "Windows 10, Y-браузер, веб-приложение Places",
        "data": "sprint1-checks.json", "status_key": "status", "demo": FOLDERS["1"] + "/",
    },
    {
        "id": "sprint2", "folder": FOLDERS["2"], "sprint": "Спринт 2", "title": "Маршруты — валидация и расчёт",
        "essence": "Тест-дизайн на практике: классы эквивалентности и границы, проверка валидации полей и формулы расчёта стоимости и времени поездки.",
        "object": "Форма построения маршрута «Маршрутов»: поля времени («Часы», «Минуты»), адреса («Откуда», «Куда»), расчёт для собственного автомобиля.",
        "focus": ["Тест-дизайн (классы эквивалентности, граничные значения)", "Позитивное и негативное тестирование полей", "Проверка расчёта по формуле t = S / V"],
        "scope": ["Валидация часов (0–23) и минут (0–59)", "Валидация адресов из фиксированного списка, обрезка пробелов", "Расчёт времени и стоимости по интервалам времени суток"],
        "out_of_scope": ["Другие виды транспорта", "Режимы «Оптимальный» и «Быстрый»", "Кроссбраузерность"],
        "environment": "Google Chrome 145, Windows 10",
        "data": "test-results.json", "status_key": "status", "group_key": "group", "demo": FOLDERS["2"] + "/",
    },
    {
        "id": "sprint3", "folder": FOLDERS["3"], "sprint": "Спринт 3", "title": "Каршеринг — форма бронирования",
        "essence": "Тестирование вёрстки и логики сложной формы: чек-листы по характеристикам элементов, кроссбраузерность, окна оплаты и добавления карты.",
        "object": "Форма бронирования каршеринга в «Маршрутах» (тариф «Повседневный») и иконки машин на карте.",
        "focus": ["Тестирование вёрстки", "Кроссбраузерная проверка", "Валидация полей карты", "Логика кнопки «Забронировать»", "Анализ серых зон требований"],
        "scope": ["Форма бронирования, блок тарифа, поля «Права» и «Способ оплаты»", "Окно «Машина забронирована», иконки машин на карте", "Окна «Способ оплаты» и «Добавление карты» (номер карты, код)"],
        "out_of_scope": ["Другие тарифы", "Расчёт расстояния и времени на кнопке", "Окна подтверждения отмены (проверки пропущены)"],
        "environment": "Firefox 148 / Windows 10 / 1920×1080; Y-браузер / macOS / 800×600",
        "data": "sprint3-checks.json", "status_key": "multi", "demo": FOLDERS["3"] + "/",
    },
    {
        "id": "sprint4", "folder": FOLDERS["4"], "sprint": "Итоговый проект (спринт 4)", "title": "Метро для Android — регрессия",
        "essence": "Мобильная регрессия после рефакторинга и решение о релизе: функциональные и регрессионные проверки, оценка рисков, Conditional Go.",
        "object": "Мобильное приложение «Метро» для Android v3.6 (рефакторинг с v2.13): карта схемы, маршрут, история, настройки.",
        "focus": ["Регрессионное тестирование", "Мобильные факторы: ориентация, жесты, сеть, прерывания", "Решение о релизе (Go/No-Go)", "Трассировка проверок и багов"],
        "scope": ["Построение маршрута, станции и их карточки", "История и временной интервал маршрута", "Смена ориентации экрана и жесты", "Сеть, установка и обновление, тёмная тема"],
        "out_of_scope": ["iOS", "Несколько версий Android и устройств", "Нагрузочное тестирование"],
        "environment": "Android 9.0, 1080×1920, эмулятор и смартфон; приложение v3.6",
        "data": "sprint4-checks.json", "status_key": "status", "demo": FOLDERS["4"] + "/",
    },
]
ICON = {"Passed": "✅", "Closed": "✅", "Failed": "❌", "Reopened": "🔁", "Blocked": "⛔", "Skipped": "⏭", "": "—"}
RANK = ["Failed", "Reopened", "Blocked", "Skipped", "Passed", "Closed", ""]


def worst(*s):
    s = [x for x in s if x]
    return min(s, key=RANK.index) if s else ""


def items_for(p):
    raw = D(p["data"])
    out = []
    for c in raw:
        if p["status_key"] == "multi":
            ff, ya = c.get("firefox_win", ""), c.get("ybr_mac", "")
            note = " · ".join(x for x in [f"Firefox: {ff}" if ff else "", f"Y-браузер: {ya}" if ya else ""] if x) if ff else ""
            status = worst(ff, ya)
        else:
            status, note = c["status"], c.get("note", "")
        section = c.get("group") or c.get("section") or "Проверки"
        if p["id"] == "sprint2":
            section = {"Часы": "Поле «Часы»", "Минуты": "Поле «Минуты»", "Откуда": "Поле «Откуда»", "Куда": "Поле «Куда»", "Расчёт": "Расчёт времени и стоимости"}[section]
        out.append({"id": c["id"], "section": section, "text": c["title"], "status": status, "bugs": c.get("bugs", []), "note": note})
    return out


def main():
    result = []
    for p in PROJECTS:
        items = items_for(p)
        secs = OrderedDict()
        for it in items:
            secs.setdefault(it["section"], []).append(it)
        total = Counter(i["status"] for i in items)
        result.append({**{k: v for k, v in p.items() if k not in ("data", "status_key", "group_key")}, "total": dict(total), "sections": [{"title": k, "items": v} for k, v in secs.items()]})
        # ---- markdown
        md = [f"# Чек-лист проекта: {p['title']}", "", f"> {p['sprint']}. {p['essence']}", "",
              f"🔗 Интерактивная версия: {SITE}checklists.html?p={p['id']}", "",
              "## Паспорт", "", "| | |", "|---|---|",
              f"| **Объект тестирования** | {p['object']} |",
              f"| **Направленность** | {'; '.join(p['focus'])} |",
              f"| **Окружение** | {p['environment']} |", "",
              "**Что проверялось:**", ""] + [f"- {x}" for x in p["scope"]] + ["", "**Не проверялось:**", ""] + [f"- {x}" for x in p["out_of_scope"]] + [
              "", "## Итоги", "", "| Статус | Кол-во |", "|---|---|"] + [f"| {ICON[k]} {k} | {v} |" for k, v in sorted(total.items(), key=lambda kv: RANK.index(kv[0]))] + [f"| **Всего** | **{len(items)}** |", "",
              "## Проверки по разделам", "", "| Раздел | Проверок | ✅ | ❌ | Прочее |", "|---|---|---|---|---|"]
        for k, v in secs.items():
            c = Counter(i["status"] for i in v)
            ok = c["Passed"] + c["Closed"]
            bad = c["Failed"] + c["Reopened"]
            md.append(f"| {k} | {len(v)} | {ok} | {bad} | {len(v) - ok - bad} |")
        issues = [i for i in items if i["status"] in ("Failed", "Reopened", "Blocked", "Skipped")]
        md += ["", f"## Проверки, требующие внимания ({len(issues)})", "", "| ID | Проверка | Статус | Баги |", "|---|---|---|---|"]
        for i in issues[:40]:
            t = i["text"].replace("|", "\\|")
            md.append(f"| {i['id']} | {t[:110]} | {ICON[i['status']]} {i['status']} | {', '.join(i['bugs']) or '—'} |")
        if len(issues) > 40:
            md.append(f"\n_Показано 40 из {len(issues)}. Полный список — в интерактивной версии._")
        md += ["", "## Как пользоваться", "", "1. Откройте интерактивную версию и выберите проект во вкладках.", "2. Отмечайте проверки галочками — прогресс сохраняется в браузере.", f"3. Подробные материалы проекта: [`{p['folder']}`](./)."]
        (ROOT / p["folder"] / "checklist.md").write_text("\n".join(md) + "\n")
    (ROOT / "data" / "checklists.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
    print("OK:", {r["id"]: sum(r["total"].values()) for r in result})


if __name__ == "__main__":
    main()
