# Каршеринг — форма бронирования (Спринт 3)

Демо-версия тестовой документации по форме бронирования каршеринга в приложении «Маршруты».

🔗 **Интерактивные материалы:** [реестр багов](https://ikqavscode-afk.github.io/qa-test-documentation/sprint3/bugs.html) · [матрица браузеров](https://ikqavscode-afk.github.io/qa-test-documentation/sprint3/matrix.html) · [серые зоны](https://ikqavscode-afk.github.io/qa-test-documentation/sprint3/gray-zones.html) · [тренажёр «Найди баг»](https://ikqavscode-afk.github.io/qa-test-documentation/sprint3/trainer.html)

## Объём тестирования
- **Верстка:** форма бронирования, блок тарифа, поля «Права» и «Способ оплаты», панель «Требования к заказу», кнопка, окно «Машина забронирована», иконки машин на карте.
- **Логика:** окна «Способ оплаты» и «Добавление карты», логика кнопки «Забронировать».
- Тариф «Повседневный», ручное тестирование.
- Не проверялись: расчёт расстояния и времени на кнопке, другие тарифы.

**Окружения:** Firefox 148 / Windows 10 / 1920×1080 · Y-браузер / macOS Ventura / 800×600.

## Итоги (пересчитаны из таблиц результатов)
| Показатель | Значение |
|---|---|
| Проверок | 163 |
| Результатов (с учётом двух браузеров) | 265 |
| ✅ Passed / ❌ Failed / ⏭ Skipped / ⛔ Blocked | 174 / 65 / 22 / 4 |
| Баги | 43: 16 critical, 20 major, 7 minor |
| Вывод | **No-Go** — см. [отчёт о готовности](reports/release-readiness.md) |

## Содержание
| Раздел | Что внутри |
|---|---|
| [test-analysis](test-analysis/) | декомпозиция, классы эквивалентности и границы, **серые зоны** |
| [test-cases](test-cases/) | фрагмент чек-листа верстки и тест-кейсы кнопки |
| [bug-reports](bug-reports/bug-reports.md) | 10 подробных баг-репортов со скриншотами и GIF (все 43 — в [реестре](https://ikqavscode-afk.github.io/qa-test-documentation/sprint3/bugs.html)) |
| [reports](reports/) | отчёт о готовности к релизу, матрица браузеров |
| [regression](regression/retest-checklist.md) | краткий чек-лист ретеста после исправлений |
