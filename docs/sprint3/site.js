const $=(s,r=document)=>r.querySelector(s);
const load=n=>fetch('data/'+n).then(r=>r.json());
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const NAV=[['index.html','Обзор'],['bugs.html','Реестр багов'],['matrix.html','Матрица браузеров'],['gray-zones.html','Серые зоны'],['trainer.html','Тренажёр «Найди баг»'],['../checklists.html','Чек-листы проектов ↗'],['../index.html','Чек-лист ↗']];
function goBack(fb){if(history.length>1&&document.referrer&&new URL(document.referrer).origin===location.origin)history.back();else location.href=fb}
function nav(){const cur=location.pathname.split('/').pop()||'index.html';const home=(location.pathname.split('/').pop()||'index.html')==='index.html';
  $('#nav').innerHTML='<button class="back" onclick="goBack(\''+(home?'../checklists.html':'index.html')+'\')">← Назад</button>'+NAV.map(([h,t])=>`<a href="${h}" class="${h===cur?'on':''}">${t}</a>`).join('')}
