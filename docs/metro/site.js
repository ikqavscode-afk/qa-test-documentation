const $=(s,r=document)=>r.querySelector(s);
const load=n=>fetch('data/'+n).then(r=>r.json());
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const NAV=[['index.html','Обзор'],['bugs.html','Реестр багов'],['matrix.html','Трассировка'],['gray-zones.html','Серые зоны'],['release.html','Симулятор релиза'],['../checklists.html','Чек-листы проектов ↗'],['../index.html','Чек-лист ↗']];
function nav(){const cur=location.pathname.split('/').pop()||'index.html';$('#nav').innerHTML='<a href="https://github.com/ikqavscode-afk/qa-test-documentation">🏠 Репозиторий</a>'+NAV.map(([h,t])=>`<a href="${h}" class="${h===cur?'on':''}">${t}</a>`).join('')}
