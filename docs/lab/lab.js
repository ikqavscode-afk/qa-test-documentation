const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const NAV = [
  ['index.html', 'Тренажёры'],
  ['ep.html', 'КЭ и граничные значения'],
  ['decision.html', 'Таблица принятия решений'],
  ['findbug.html', 'Найди баг и оформи отчёт'],
  ['../checklists.html', 'Чек-листы проектов ↗'],
  ['../index.html', 'Чек-лист тестировщика ↗']
];
function nav() {
  const cur = location.pathname.split('/').pop() || 'index.html';
  $('#nav').innerHTML = '<a href="https://github.com/ikqavscode-afk/qa-test-documentation">🏠 Репозиторий</a>' +
    NAV.map(([h, t]) => `<a href="${h}" class="${h === cur ? 'on' : ''}">${t}</a>`).join('');
}
function store(key, def) {
  let v; try { v = JSON.parse(localStorage.getItem(key)); } catch (e) { v = null; }
  return { get: () => v ?? def, set: x => { v = x; try { localStorage.setItem(key, JSON.stringify(x)); } catch (e) { } } };
}
function copy(text, btn) {
  navigator.clipboard.writeText(text).then(() => { const t = btn.textContent; btn.textContent = 'Скопировано ✓'; setTimeout(() => btn.textContent = t, 1400); });
}
