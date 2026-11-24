// Shared by every page: Tailwind theme, site data, header, footer and keyword search.
tailwind.config = { theme: { extend: {
  fontFamily: { sans: ['Inter', 'sans-serif'] },
  colors: { brand: { 50:'#eef6ff',100:'#d9eaff',500:'#1f6feb',600:'#1558c9',700:'#0f43a0',900:'#0a1f44' } }
}}};

// ---- Placeholder data: replace with real details ----
const CONTACT = {
  phone: '+91 00000 00000',
  email: 'info@ceratec.example',
  sales: 'sales@ceratec.example',
  address: ['Placeholder address, Industrial Estate', 'City – 000000, India'],
  whatsapp: 'https://wa.me/910000000000',
};
const PRODUCTS = [
  { name:'Solid Carbide End Mill – 4 Flute', cat:'End Mills', tags:'carbide milling steel square' },
  { name:'Ball Nose End Mill', cat:'End Mills', tags:'carbide die mould 3d profiling' },
  { name:'Corner Radius End Mill', cat:'End Mills', tags:'carbide radius roughing' },
  { name:'High-Feed End Mill', cat:'End Mills', tags:'carbide hfm roughing' },
  { name:'Solid Carbide Drill – 5xD', cat:'Drills', tags:'carbide drilling coolant through' },
  { name:'Step Drill', cat:'Drills', tags:'carbide custom drilling' },
  { name:'Spot / NC Drill', cat:'Drills', tags:'carbide centre spotting' },
  { name:'Turning Inserts', cat:'Inserts', tags:'ceramic cbn turning cnmg' },
  { name:'Milling Inserts', cat:'Inserts', tags:'carbide apkt face milling' },
  { name:'Thread Mill', cat:'Threading', tags:'carbide thread milling' },
  { name:'Machine Taps', cat:'Threading', tags:'hss tapping spiral' },
  { name:'Reamers', cat:'Special Tools', tags:'carbide finishing bore' },
  { name:'Custom Form Tools', cat:'Special Tools', tags:'custom profile drawing' },
];
// shortcut: file '#' is a placeholder, put real PDFs in /catalogues and set the path here.
const CATALOGUES = [
  { name:'General Catalogue 2026', size:'PDF · 24 MB', file:'#' },
  { name:'End Mills Catalogue', size:'PDF · 8 MB', file:'#' },
  { name:'Drills & Reamers', size:'PDF · 6 MB', file:'#' },
  { name:'Inserts & Holders', size:'PDF · 10 MB', file:'#' },
];
const SOCIALS = [
  { name:'Facebook', url:'https://facebook.com/', d:'M14 9h3V5h-3c-2.8 0-4 1.7-4 4v2H8v4h2v8h4v-8h3l1-4h-4V9.5c0-.3.2-.5.5-.5Z' },
  { name:'LinkedIn', url:'https://linkedin.com/', d:'M4 4h4v4H4zM4 10h4v10H4zM10 10h4v1.5c.6-1 1.8-1.8 3.5-1.8 2.7 0 3.5 1.8 3.5 4.5V20h-4v-5.3c0-1.2-.4-2-1.5-2s-1.5.8-1.5 2V20h-4z' },
  { name:'WhatsApp', url:CONTACT.whatsapp, d:'M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Zm4.6 12.6c-.2.6-1.2 1.1-1.7 1.1-.4 0-1 .1-3.1-.8-2.6-1.1-4.2-3.7-4.3-3.9-.1-.2-1-1.4-1-2.6s.6-1.8.9-2.1c.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.3 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.7 1.1 1.5 1.8 1 .9 1.8 1.1 2.1 1.3.3.1.4.1.6-.1l.8-1c.2-.2.4-.2.6-.1l1.8.9c.3.1.4.2.5.3.1.2.1.8-.1 1.3Z' },
  { name:'YouTube', url:'https://youtube.com/', d:'M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12 31 31 0 0 0 2 15.8a3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1c.4-1.2.4-3.8.4-3.8s0-2.6-.4-3.8ZM10 15V9l5.2 3Z' },
];
const NAV = [
  ['index.html','Home'], ['about.html','About Us'], ['products.html','Products'], ['catalogue.html','Catalogue'], ['contact.html','Contact'],
];

// ---- Helpers ----
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const matches = (p, q) => (p.name + ' ' + p.cat + ' ' + p.tags).toLowerCase().includes(q);
const ICON_SEARCH = '<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
const socialIcon = s => `<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="${s.d}"/></svg>`;

function productCard(p) {
  return `<div class="group rounded-xl bg-white border border-slate-200 overflow-hidden hover:shadow-lg hover:-translate-y-0.5 transition">
    <div class="ph aspect-[4/3] grid place-items-center text-slate-400 text-sm">Product image</div>
    <div class="p-5">
      <div class="text-xs font-semibold text-brand-600 uppercase tracking-wide">${esc(p.cat)}</div>
      <div class="mt-1 font-bold text-brand-900">${esc(p.name)}</div>
      <a href="contact.html?product=${encodeURIComponent(p.name)}" class="mt-4 inline-flex text-sm font-semibold text-brand-600 group-hover:underline">Enquire →</a>
    </div>
  </div>`;
}
function catalogueCard(c) {
  return `<div class="rounded-xl border border-slate-200 bg-white p-5 flex flex-col">
    <div class="ph rounded-lg aspect-[3/4] grid place-items-center text-slate-400 text-sm">Cover</div>
    <div class="mt-4 font-bold text-brand-900">${esc(c.name)}</div>
    <div class="text-xs text-slate-500">${esc(c.size)}</div>
    <a href="${c.file}" download class="mt-4 h-10 inline-flex items-center justify-center rounded-md bg-brand-600 text-white text-sm font-semibold hover:bg-brand-700">⬇ Download</a>
  </div>`;
}

// ---- Header / footer / search ----
function headerHTML() {
  const page = location.pathname.split('/').pop() || 'index.html';
  const link = ([href, label], cls) => `<a href="${href}" class="${cls} ${href === page ? 'text-brand-600' : ''}"${href === page ? ' aria-current="page"' : ''}>${label}</a>`;
  return `
  <div class="bg-brand-900 text-slate-300 text-xs">
    <div class="max-w-7xl mx-auto px-4 h-9 flex items-center justify-between">
      <div class="flex gap-5"><span>📞 ${CONTACT.phone}</span><span class="hidden sm:inline">✉ ${CONTACT.email}</span></div>
      <div class="flex gap-2">${SOCIALS.map(s => `<a href="${s.url}" target="_blank" rel="noopener" aria-label="${s.name}" class="w-7 h-7 grid place-items-center rounded-md bg-white/10 hover:bg-brand-600 text-white transition">${socialIcon(s)}</a>`).join('')}</div>
    </div>
  </div>
  <header class="sticky top-0 z-40 bg-white/90 backdrop-blur border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-4">
      <a href="index.html" class="flex items-center gap-2 font-extrabold text-xl tracking-tight text-brand-900">
        <span class="w-9 h-9 rounded-lg bg-brand-600 text-white grid place-items-center">C</span>CERATEC
      </a>
      <nav class="hidden md:flex items-center gap-1 text-sm font-medium">${NAV.map(n => link(n, 'px-3 py-2 rounded-md hover:bg-slate-100')).join('')}</nav>
      <div class="flex items-center gap-2">
        <button onclick="openSearch()" class="flex items-center gap-2 h-9 px-3 rounded-md border border-slate-200 text-sm text-slate-500 hover:border-slate-300 md:w-56" aria-label="Search">
          ${ICON_SEARCH}<span class="hidden md:inline">Search products…</span><kbd class="hidden md:inline ml-auto text-[10px] border rounded px-1">Ctrl K</kbd>
        </button>
        <a href="contact.html" class="hidden sm:inline-flex h-9 items-center px-4 rounded-md bg-brand-600 text-white text-sm font-semibold hover:bg-brand-700">Get a Quote</a>
        <button class="md:hidden h-9 w-9 grid place-items-center rounded-md border" onclick="document.getElementById('mnav').classList.toggle('hidden')" aria-label="Menu">☰</button>
      </div>
    </div>
    <nav id="mnav" class="hidden md:hidden border-t px-4 py-2 text-sm font-medium flex flex-col">${NAV.map(n => link(n, 'py-2')).join('')}</nav>
  </header>
  <div id="search" class="hidden fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm p-4" onclick="if(event.target===this)closeSearch()">
    <div class="mx-auto mt-[10vh] max-w-xl rounded-xl bg-white shadow-2xl overflow-hidden">
      <div class="flex items-center gap-3 px-4 border-b text-slate-400">
        ${ICON_SEARCH}
        <input id="sq" oninput="renderSearch()" onkeydown="if(event.key==='Enter'){location.href='products.html?q='+encodeURIComponent(this.value)}" placeholder="Search products, categories, catalogues…" class="flex-1 h-14 outline-none text-base text-slate-800">
        <kbd class="text-[10px] border rounded px-1">ESC</kbd>
      </div>
      <ul id="sres" class="max-h-[50vh] overflow-auto p-2"></ul>
    </div>
  </div>`;
}

// Footer: 21st.dev "Footer Section" (Spectrum UI), ported to static Tailwind
function footerHTML() {
  return `
  <footer class="relative border-t border-white/10 bg-[#05070d] text-slate-100">
    <div class="max-w-7xl mx-auto px-4 py-12 md:px-6 lg:px-8">
      <div class="grid gap-12 md:grid-cols-2 lg:grid-cols-4">
        <div class="relative">
          <div class="mb-4 flex items-center gap-2 font-extrabold text-lg"><span class="w-8 h-8 rounded-lg bg-brand-600 grid place-items-center">C</span>CERATEC</div>
          <h2 class="mb-4 text-3xl font-bold tracking-tight">Stay Connected</h2>
          <p class="mb-6 text-slate-400">Join our newsletter for new tools, catalogues and offers.</p>
          <form class="relative" onsubmit="event.preventDefault(); this.reset()">
            <input type="email" required placeholder="Enter your email" aria-label="Email" class="w-full h-10 rounded-md border border-white/15 bg-white/5 px-3 pr-12 text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-500">
            <button type="submit" class="absolute right-1 top-1 h-8 w-8 grid place-items-center rounded-full bg-brand-500 text-white transition-transform hover:scale-105">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg><span class="sr-only">Subscribe</span>
            </button>
          </form>
          <div class="absolute -right-4 top-0 h-24 w-24 rounded-full bg-brand-500/10 blur-2xl"></div>
        </div>
        <div>
          <h3 class="mb-4 text-lg font-semibold">Quick Links</h3>
          <nav class="space-y-2 text-sm text-slate-300">${NAV.map(([h, l]) => `<a href="${h}" class="block transition-colors hover:text-brand-100">${l}</a>`).join('')}</nav>
        </div>
        <div>
          <h3 class="mb-4 text-lg font-semibold">Contact Us</h3>
          <address class="space-y-2 text-sm not-italic text-slate-300">
            ${CONTACT.address.map(a => `<p>${a}</p>`).join('')}<p>Phone: ${CONTACT.phone}</p><p>Email: ${CONTACT.email}</p>
          </address>
        </div>
        <div>
          <h3 class="mb-4 text-lg font-semibold">Follow Us</h3>
          <div class="mb-6 flex gap-4">${SOCIALS.map(s => `<a href="${s.url}" target="_blank" rel="noopener" class="group relative h-10 w-10 grid place-items-center rounded-full border border-white/15 hover:bg-white/10 transition">${socialIcon(s)}<span class="sr-only">${s.name}</span><span class="tip rounded-md bg-white px-3 py-1.5 text-xs text-slate-900">Follow us on ${s.name}</span></a>`).join('')}</div>
        </div>
      </div>
      <div class="mt-12 flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-8 text-center md:flex-row">
        <p class="text-sm text-slate-400">© 2026 Ceratec. All rights reserved.</p>
        <nav class="flex gap-4 text-sm text-slate-300"><a href="#" class="hover:text-brand-100">Privacy Policy</a><a href="#" class="hover:text-brand-100">Terms of Service</a><a href="#" class="hover:text-brand-100">Cookie Settings</a></nav>
      </div>
    </div>
  </footer>`;
}

function renderSearch() {
  const q = document.getElementById('sq').value.trim().toLowerCase();
  const res = document.getElementById('sres');
  if (!q) { res.innerHTML = '<li class="px-3 py-6 text-center text-sm text-slate-400">Type a keyword, e.g. "carbide", "drill", "insert"</li>'; return; }
  const hits = PRODUCTS.filter(p => matches(p, q)).map(p => ({ t:p.name, s:p.cat, href:'products.html?q=' + encodeURIComponent(p.name) }))
    .concat(CATALOGUES.filter(c => c.name.toLowerCase().includes(q)).map(c => ({ t:c.name, s:'Catalogue', href:'catalogue.html' })));
  res.innerHTML = hits.length
    ? hits.map(h => `<li><a href="${h.href}" class="flex justify-between px-3 py-2.5 rounded-md hover:bg-slate-100"><span class="font-medium">${esc(h.t)}</span><span class="text-xs text-slate-400">${h.s}</span></a></li>`).join('')
    : '<li class="px-3 py-6 text-center text-sm text-slate-400">No results</li>';
}
function openSearch() { document.getElementById('search').classList.remove('hidden'); const i = document.getElementById('sq'); i.value = ''; renderSearch(); i.focus(); }
function closeSearch() { document.getElementById('search').classList.add('hidden'); }

document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
  if (e.key === 'Escape') closeSearch();
});
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('site-header').outerHTML = headerHTML();
  document.getElementById('site-footer').outerHTML = footerHTML();
});
