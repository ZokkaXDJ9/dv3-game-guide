const dragons=[
{name:'Fire',element:'Fire',rarity:'Element note',description:'A bright starting point for a balanced collection.',tag:'Heat & courage'},
{name:'Water',element:'Water',rarity:'Element note',description:'A cool counterpoint when planning coverage.',tag:'Flow & focus'},
{name:'Earth',element:'Earth',rarity:'Element note',description:'A grounded note for your first team-building pass.',tag:'Root & resolve'},
{name:'Wind',element:'Wind',rarity:'Element note',description:'Keep an eye out for speed and team synergy.',tag:'Quick & curious'},
{name:'Light',element:'Light',rarity:'Element note',description:'A luminous collection path worth tracking.',tag:'Radiance & hope'},
{name:'Dark',element:'Dark',rarity:'Element note',description:'Check unlock conditions before planning around it.',tag:'Mystery & might'},
{name:'Special',element:'Special',rarity:'Collection note',description:'Event and limited availability can change over time.',tag:'Watch notices'},
{name:'Your next find',element:'Any',rarity:'Field note',description:'Add a dragon you discover and note where it came from.',tag:'Your discovery'}
];
const glyphs={Fire:'♨',Water:'≈',Earth:'◈',Wind:'〰',Light:'✧',Dark:'☾',Special:'✦',Any:'+'};
const grid=document.querySelector('#dragon-grid'),search=document.querySelector('#dragon-search');let activeElement='all';
function render(){const term=search.value.trim().toLowerCase();const visible=dragons.filter(d=>(activeElement==='all'||d.element===activeElement)&&(d.name+' '+d.element+' '+d.rarity+' '+d.description+' '+d.tag).toLowerCase().includes(term));grid.innerHTML=visible.length?visible.map(d=>`<article class="dragon-card element-${d.element}"><div class="dragon-card-top"><span class="dragon-glyph">${glyphs[d.element]}</span><span class="dragon-badge">${d.rarity}</span></div><h3>${d.name}</h3><p>${d.description}</p><span class="dragon-meta">${d.tag}</span></article>`).join(''):'<div class="empty-state">No notes match that search. Try a different word or element.</div>'}
document.querySelector('#element-filters').addEventListener('click',e=>{const b=e.target.closest('button[data-element]');if(!b)return;activeElement=b.dataset.element;document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));render()});search.addEventListener('input',render);render();
document.querySelector('.menu-toggle').addEventListener('click',e=>{const nav=document.querySelector('#nav-links');const open=nav.classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',String(open))});document.querySelectorAll('.nav-links a').forEach(a=>a.addEventListener('click',()=>{document.querySelector('#nav-links').classList.remove('open');document.querySelector('.menu-toggle').setAttribute('aria-expanded','false')}));document.querySelector('#year').textContent=new Date().getFullYear();
