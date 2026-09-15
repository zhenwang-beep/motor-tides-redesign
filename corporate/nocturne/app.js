/* ============================================================================
   WISEMAN RESIDENTIAL — DIRECTION "NOCTURNE"
   One file for every page. Everything is guarded by element presence, so a page
   with no hero / reel / plate / map simply skips that block. Depends on
   core/core.js, and on core/map.js + core/rail.js wherever a page carries them.
   No second requestAnimationFrame loop: every scroll-bound mechanic subscribes
   to the single WR.onScroll dispatcher and branches on WR.reduce.
   ========================================================================== */
(function () {
  'use strict';
  var W = window.WR;
  if (!W) return;
  var doc = document, root = doc.documentElement;
  var BASE = root.dataset.base || '';

  /* Every map on Nocturne runs on the dark Esri imagery. The shared editorial
     generator hard-codes the contact office map to theme:'light'; wrap WR.map
     (before any DOMContentLoaded boot runs) so that one map is dark too, without
     editing the shared generator. */
  if (W.map && !W._noctMap) {
    var _wrMap = W.map;
    W.map = function (o) {
      if (o && o.el === '#office-map') { o = Object.assign({}, o, { theme: 'dark' }); }
      return _wrMap.call(W, o);
    };
    W._noctMap = true;
  }
  function $(s, c) { return (c || doc).querySelector(s); }
  function $$(s, c) { return [].slice.call((c || doc).querySelectorAll(s)); }

  /* the shared spine: reveals, header, menu, favourites, curtain */
  W.boot({ header: { heroEnd: 90 }, transition: true });
  if (W.rails) W.rails();

  /* ---- an index.json loader shared by the map, typeahead and inquire ---- */
  var idxPromise = null;
  function loadIndex() {
    if (!idxPromise) {
      idxPromise = fetch(root.dataset.index || '../data/index.json')
        .then(function (r) { return r.json(); }).catch(function () { return null; });
    }
    return idxPromise;
  }

  /* ------------------------------------------------------------------ 1. HERO
     One orchestrated arrival after the display face is in, and the header turns
     from transparent-over-photo to solid once the hero has scrolled past. */
  (function hero() {
    var go = function () { requestAnimationFrame(function () { root.classList.add('ld'); }); };
    if (doc.fonts && doc.fonts.ready) { doc.fonts.ready.then(go); setTimeout(go, 900); } else { go(); }

    var hd = $('.hd');
    if (!hd || !hd.classList.contains('over')) return;
    var band = $('.hero') || $('.ed-hero');
    W.onScroll(function () {
      var y = window.pageYOffset;
      var past = band ? (band.getBoundingClientRect().bottom <= hd.offsetHeight + 2)
                      : (y > 90);
      /* The Nocturne header never retracts (.hd.up is a no-op), so it must stay
         legible over anything that scrolls beneath it. Transparent only at the
         very top of the hero; frosted while the hero scrolls past (so the display
         line and the search bar read through a blur, not a clash); solid once the
         hero is gone. This overrides core.js's scroll-direction frosting, which
         assumed a header that retracts on the way down. */
      hd.classList.toggle('solid', past);
      hd.classList.toggle('frost', !past && y > 6);
      hd.classList.toggle('over', y <= 6);
    });
  })();

  /* ------------------------------------------------------------------ 2. THE REEL
     Desktop (>=900, fine pointer, no reduced motion): a pinned 300vh runway with
     a sticky stage; vertical scroll maps to translateX, the frame at the gate is
     lit and its ticks travel with it. Elsewhere it stays the native scroll rail
     the markup ships (SPEC risk 5): a broken pin never leaves a blank band,
     because pinning is opt-in from JS. Arrows/arrow-keys step one frame in both. */
  (function reel() {
    var reel = $('[data-reel]');
    if (!reel) return;
    var stage = $('.reel-stage', reel), track = $('[data-reel-track]', reel);
    if (!stage || !track) return;
    var frames = $$('.frame', track);
    if (!frames.length) return;
    var gates = $$('.gate', reel), fill = $('.reel-fill');
    var prev = $('.rbtn.prev'), next = $('.rbtn.next');
    var GAP = 22, pinned = false;

    var coarse = matchMedia('(pointer: coarse)').matches;
    var mqWide = matchMedia('(min-width: 900px)');
    /* the pinned runway is opt-in per reel (data-reel-pin) — used on buildings.html,
       where there is no page-length budget; the home reel stays a scroll rail so the
       page keeps under its length target and matches the concept board. */
    function wantPin() { return reel.hasAttribute('data-reel-pin') && mqWide.matches && !W.reduce && !coarse; }

    function frameW() { return frames[0].getBoundingClientRect().width + GAP; }
    function centerX() { var r = stage.getBoundingClientRect(); return r.left + r.width / 2; }

    /* light the frame nearest the gate line; move the ticks to it; fill the rule */
    function litUpdate(progress) {
      var gx = centerX(), best = null, bd = 1e9;
      frames.forEach(function (f) {
        var b = f.getBoundingClientRect(), c = b.left + b.width / 2, d = Math.abs(c - gx);
        if (d < bd) { bd = d; best = f; }
      });
      frames.forEach(function (f) { f.classList.toggle('lit', f === best); });
      if (best && gates.length) {
        var rr = reel.getBoundingClientRect(), bb = best.getBoundingClientRect();
        var x = (bb.left + bb.width / 2 - rr.left) + 'px';
        gates.forEach(function (g) { g.style.left = x; });
      }
      if (fill) {
        var p = progress;
        if (p == null) {
          var max = track.scrollWidth - stage.clientWidth;
          p = max > 0 ? stage.scrollLeft / max : 0;
        }
        fill.style.width = (18 + 82 * W.clamp01(p)) + '%';
      }
    }

    /* --- pinned runway --- */
    function span() { return Math.max(0, track.scrollWidth - stage.clientWidth); }
    function pinScroll() {
      if (!pinned) return;
      var s = span();
      if (s <= 0) { unpin(); return; }
      var p = W.pinned(reel);
      track.style.transform = 'translateX(' + (-(p * s).toFixed(2)) + 'px)';
      litUpdate(p);
    }
    function pin() {
      if (pinned) return;
      reel.classList.add('is-pinned');
      pinned = true;
      // let layout settle, then verify there is travel to map
      requestAnimationFrame(function () {
        if (span() <= 0) { unpin(); return; }
        pinScroll();
      });
    }
    function unpin() {
      if (!pinned) return;
      reel.classList.remove('is-pinned');
      track.style.transform = '';
      pinned = false;
      litUpdate();
    }
    function sync() { if (wantPin()) pin(); else unpin(); }

    W.onScroll(function () { if (pinned) pinScroll(); });
    stage.addEventListener('scroll', function () { if (!pinned) litUpdate(); }, { passive: true });
    addEventListener('resize', function () { sync(); if (pinned) pinScroll(); else litUpdate(); });
    if (mqWide.addEventListener) mqWide.addEventListener('change', sync);

    /* arrows / keys — step one frame */
    function step(dir) {
      if (pinned) {
        var s = span(); if (s <= 0) return;
        var pageTravel = reel.offsetHeight - window.innerHeight;
        var dy = (frameW() / s) * pageTravel;
        window.scrollBy({ top: dir * dy, behavior: W.reduce ? 'auto' : 'smooth' });
      } else {
        stage.scrollBy({ left: dir * frameW(), behavior: W.reduce ? 'auto' : 'smooth' });
      }
    }
    if (next) next.addEventListener('click', function () { step(1); });
    if (prev) prev.addEventListener('click', function () { step(-1); });
    track.setAttribute('tabindex', '0');
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    });

    sync();
    litUpdate();
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { sync(); litUpdate(); });
  })();

  /* ------------------------------------------------------------------ 3. BUILDINGS.HTML VIEWS
     ?view=reel | index | atlas. Panes are anchors + hidden toggles; the map wakes
     when its pane is shown. */
  (function views() {
    var btns = $$('[data-viewbtn]');
    if (!btns.length) return;
    var panes = $$('[data-viewpane]');
    function inList(v, n) { return (v || '').split(/\s+/).indexOf(n) >= 0; }
    function show(name, push) {
      btns.forEach(function (b) { b.setAttribute('aria-selected', String(b.dataset.viewbtn === name)); });
      panes.forEach(function (p) { p.hidden = !inList(p.dataset.viewpane, name); });
      if (push !== false) { try { var u = new URL(location.href); u.searchParams.set('view', name); history.replaceState(null, '', u); } catch (e) {} }
      if (W.wakeMaps) W.wakeMaps();
      W.pump();
    }
    btns.forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); show(b.dataset.viewbtn); }); });
    var q = new URLSearchParams(location.search).get('view');
    show(btns.some(function (b) { return b.dataset.viewbtn === q; }) ? q : btns[0].dataset.viewbtn, false);
  })();

  /* ------------------------------------------------------------------ 4. THE SPECIMEN PLATE
     buildings.html ?view=index. WR.register does sorting + hover/focus wiring;
     this shows a building from the first paint and follows the scroll while the
     pointer is off the rows. */
  (function specimen() {
    var list = $('[data-register]'), plate = $('[data-plate]');
    if (!list) return;
    if ($('[data-sort]') || plate) {
      W.register({ list: '[data-register]', flatLabel: 'All ' + $$('[data-row]', list).length + ' buildings' });
    }
    if (!plate) return;
    var img = $('img', plate), nm = $('[data-platename]', plate), st = $('[data-platestreet]', plate);
    function paint(r) {
      if (!r || plate.dataset.cur === r.dataset.no) return;
      plate.dataset.cur = r.dataset.no;
      var src = r.dataset.img;
      var pre = new Image();
      pre.onload = function () {
        img.src = src; img.alt = r.dataset.name;
        plate.classList.remove('swap'); void plate.offsetWidth; plate.classList.add('swap');
      };
      pre.onerror = function () { if (nm) nm.textContent = r.dataset.name; };
      pre.src = src;
      if (nm) nm.textContent = r.dataset.name;
      if (st) st.textContent = r.dataset.street + ' · ' + r.dataset.arealabel;
    }
    function first() { return list.querySelector('[data-group]:not([hidden]) [data-row]'); }
    paint(first());
    $$('[data-sort]').forEach(function (b) { b.addEventListener('click', function () { setTimeout(function () { paint(first()); }, 0); }); });

    var want = null, timer = 0;
    W.onScroll(function () {
      if (!plate.getClientRects().length) return;
      if (list.matches(':hover') || list.contains(doc.activeElement)) return;
      var pr = plate.getBoundingClientRect(), y = pr.top + 40, lr = list.getBoundingClientRect();
      if (y < lr.top || y > lr.bottom || y > innerHeight - 1) return;
      var el = doc.elementFromPoint(Math.min(lr.left + 24, innerWidth - 1), y);
      var row = el && el.closest ? el.closest('[data-row]') : null;
      if (!row || row === want) return;
      want = row; clearTimeout(timer);
      timer = setTimeout(function () { paint(want); }, 160);
    });
  })();

  /* ------------------------------------------------------------------ 5. FLOOR-PLAN TABS
     Building page: bedroom tabs, BUILT from the rendered rows so the shared
     generator needs no change. With JS off every row shows (no tabs). */
  (function planTabs() {
    var host = $('[data-ptabs]'), table = $('[data-ptable]');
    if (!host || !table) return;
    var rows = $$('[data-prow]', table);
    if (rows.length < 2) return;
    var order = [], seen = {};
    rows.forEach(function (r) { var k = r.dataset.beds || 'x'; if (!seen[k]) { seen[k] = 1; order.push(k); } });
    if (order.length < 2) return;
    function label(k) {
      if (k === '0') return 'Studios';
      if (k === 'x') return 'Other';
      return k + (k === '1' ? ' bedroom' : ' bedrooms');
    }
    function mk(key, txt) { var b = doc.createElement('button'); b.type = 'button'; b.dataset.beds = key; b.textContent = txt; host.appendChild(b); }
    mk('all', 'All'); order.forEach(function (k) { mk(k, label(k)); });
    var btns = $$('button', host);
    function show(key) {
      btns.forEach(function (b) { b.setAttribute('aria-selected', String(b.dataset.beds === key)); });
      rows.forEach(function (r) { r.hidden = key !== 'all' && (r.dataset.beds || 'x') !== key; });
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.beds); }); });
    show('all');
  })();

  /* ------------------------------------------------------------------ 6. THE MAPS
     A container declares itself with data-map='{...}'. Nocturne runs every map
     theme:'dark' (Esri imagery) unless the container asks otherwise. */
  (function maps() {
    var hosts = $$('[data-map]');
    if (!hosts.length || !W.map) return;
    var pending = [];
    function cfgOf(el) { try { return JSON.parse(el.getAttribute('data-map') || '{}'); } catch (e) { return {}; } }
    function bedLabel(p) {
      if (p.bmin == null && p.bmax == null) return '';
      var lo = p.bmin == null ? p.bmax : p.bmin, hi = p.bmax == null ? p.bmin : p.bmax;
      if (lo === 0 && hi === 0) return 'Studio';
      if (lo === hi) return lo + ' bed';
      return (lo === 0 ? 'Studio' : lo) + '–' + hi + ' bed';
    }
    function build(el, cfg, ix) {
      var areas = (ix && ix.areas) || {}, byNo = {};
      if (ix && ix.p) ix.p.forEach(function (p) { byNo[p.no] = p; });
      var wanted;
      if (cfg.one) wanted = [cfg.one];
      else if (cfg.points && cfg.points.length) wanted = cfg.points;
      else if (cfg.area) wanted = (ix && ix.p ? ix.p : []).filter(function (p) { return p.a === cfg.area; });
      else wanted = (ix && ix.p) ? ix.p : [];
      var pts = wanted.map(function (w) {
        var p = byNo[w.no] || {}, area = areas[p.a] || {}, img = w.img || p.img || '';
        return {
          no: w.no, lat: w.lat != null ? w.lat : p.lat, lng: w.lng != null ? w.lng : p.lng,
          name: w.name || p.n || ('Building ' + w.no), street: w.street || p.s || '',
          area: p.a || cfg.area || '', areaLabel: w.areaLabel || area.name || '',
          beds: w.beds || bedLabel(p),
          rent: p.pmin == null ? '' : 'From $' + Math.round(p.pmin).toLocaleString('en-US'),
          img: img.replace('w_600,h_400', 'w_420,h_280').replace('w_700,h_500', 'w_420,h_300'),
          url: w.url || (p.u ? BASE + 'buildings/' + p.u + '.html' : '#')
        };
      }).filter(function (p) { return p.lat != null && p.lng != null; });
      if (!pts.length) return;
      var opts = { el: '#' + el.id, points: pts, theme: cfg.theme || 'dark', pins: cfg.pins || 'dot', label: cfg.label || null };
      var CEIL = cfg.maxZoom || 15;
      opts.onReady = function (m) {
        if (cfg.zoom) m.setView([pts[0].lat, pts[0].lng], cfg.zoom, { animate: false });
        else if (m.getZoom() > CEIL) m.setZoom(CEIL, { animate: false });
        setTimeout(function () { m.invalidateSize(); }, 40);
      };
      W.map(opts);
    }
    function visible(el) { return !!(el.offsetParent || el.getClientRects().length); }
    function start(el) {
      if (el.dataset.mapped) return;
      if (!visible(el)) { if (pending.indexOf(el) < 0) pending.push(el); return; }
      el.dataset.mapped = '1';
      var cfg = cfgOf(el);
      loadIndex().then(function (ix) { build(el, cfg, ix); });
    }
    hosts.forEach(start);
    W.wakeMaps = function () {
      pending.slice().forEach(function (el) { if (visible(el)) { pending.splice(pending.indexOf(el), 1); start(el); } });
      if (W.mapInstance) setTimeout(function () { W.mapInstance.invalidateSize(); }, 60);
    };
  })();

  /* ------------------------------------------------------------------ 7. TYPEAHEAD */
  (function search() {
    var input = $('[data-typeahead]'); if (!input) return;
    loadIndex().then(function (ix) {
      if (!ix || !ix.p) return;
      var areas = ix.areas || {};
      var items = ix.p.map(function (p) {
        var area = (areas[p.a] && (areas[p.a].name || areas[p.a])) || p.a;
        return { hay: (p.n + ' ' + p.s + ' ' + area).toLowerCase(), no: '', name: p.n,
                 sub: p.s + ' · ' + area, url: BASE + 'buildings/' + p.u + '.html' };
      });
      W.typeahead({ input: '[data-typeahead]', out: '[data-typeahead-out]', items: items });
    });
  })();

  /* ------------------------------------------------------------------ 8. INQUIRE (?building) */
  (function inquire() {
    var form = $('form.ed-form'); if (!form) return;
    var slug = new URLSearchParams(location.search).get('building');
    if (!slug || !/^[a-z0-9-]+$/.test(slug)) return;
    var field = form.querySelector('[name="building"]'), topic = form.querySelector('[name="topic"]');
    loadIndex().then(function (ix) {
      var p = null;
      if (ix && ix.p) ix.p.forEach(function (q) { if (q.u === slug) p = q; });
      if (!p) return;
      if (field && !field.value) field.value = p.n + ' — ' + p.s;
      if (topic) topic.selectedIndex = 0;
      var line = doc.createElement('p');
      line.className = 'ed-about'; line.id = 'inquire';
      line.appendChild(doc.createTextNode('About '));
      var b = doc.createElement('b'); b.textContent = p.n; line.appendChild(b);
      line.appendChild(doc.createTextNode(' · '));
      var a = doc.createElement('a'); a.href = BASE + 'buildings/' + p.u + '.html'; a.textContent = p.s; line.appendChild(a);
      form.parentNode.insertBefore(line, form);
      try { line.scrollIntoView({ block: 'start', behavior: 'instant' }); } catch (e) { line.scrollIntoView(true); }
      W.pump();
    });
  })();

  /* ------------------------------------------------------------------ 9. MENU HOUSEKEEPING */
  (function menuInert() {
    var btn = $('.mbtn'), targets = $$('[data-menu-inert]');
    if (!btn || !targets.length || !window.MutationObserver) return;
    new MutationObserver(function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      targets.forEach(function (el) { el.inert = open; });
    }).observe(btn, { attributes: true, attributeFilter: ['aria-expanded'] });
  })();

  /* ------------------------------------------------------------------ 10. THE BOTTOM BAR
     Building page ≤1059px: the three CTAs ride at the foot; the bar slides away
     while the footer is on screen so it never covers the Equal Housing mark. */
  (function bottomBar() {
    var bar = $('[data-mbar]'), foot = $('footer.ft');
    if (!bar || !foot || !window.IntersectionObserver) return;
    new IntersectionObserver(function (es) {
      bar.classList.toggle('off', es[es.length - 1].isIntersecting);
    }).observe(foot);
  })();

  /* ------------------------------------------------------------------ 11. AREA SWAP
     Home page: the seven-areas frame swaps to the hovered/focused area's hero
     building. Keyboard parity via focus. With JS off the frame is the first area. */
  (function areaSwap() {
    var fig = $('[data-areafig]'); if (!fig) return;
    var img = $('img', fig); if (!img) return;
    var first = img.getAttribute('src');
    var rows = $$('.arow[data-areaimg]');
    if (!rows.length) return;
    var cur = first;
    function swap(src) {
      if (!src || src === cur) return;
      cur = src;
      var pre = new Image();
      pre.onload = function () { img.src = src; };
      pre.src = src;
    }
    rows.forEach(function (a) {
      a.addEventListener('mouseenter', function () { swap(a.dataset.areaimg); });
      a.addEventListener('focusin', function () { swap(a.dataset.areaimg); });
    });
    var list = rows[0].closest('.areas-list');
    if (list) list.addEventListener('mouseleave', function () { swap(first); });
  })();

  addEventListener('hashchange', function () { W.pump(); });
})();
