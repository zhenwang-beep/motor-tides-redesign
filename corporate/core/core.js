/* Wiseman Residential — shared spine. No dependencies. No scroll hijacking.
   One rAF-gated scroll dispatcher; everything else subscribes to it.
   See ../CONVENTIONS.md before adding to this file. */
(function () {
  'use strict';

  var W = (window.WR = window.WR || {});
  W.reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------ scroll */
  var subs = [], ticking = false, lastY = -1;
  function flush() {
    ticking = false;
    var y = window.pageYOffset, h = window.innerHeight;
    for (var i = 0; i < subs.length; i++) { try { subs[i](y, h); } catch (e) {} }
    lastY = y;
  }
  function tick() { if (!ticking) { ticking = true; requestAnimationFrame(flush); } }
  W.onScroll = function (fn) { subs.push(fn); tick(); return fn; };
  addEventListener('scroll', tick, { passive: true });
  addEventListener('resize', tick);
  W.pump = tick;

  /* progress of an element through the viewport, 0 before it enters, 1 after it leaves */
  W.through = function (el) {
    var r = el.getBoundingClientRect(), h = window.innerHeight;
    return Math.min(1, Math.max(0, (h - r.top) / (h + r.height)));
  };
  /* progress of a pinned stage: 0 when the section top hits the viewport top, 1 at the bottom */
  W.pinned = function (el) {
    var r = el.getBoundingClientRect(), span = el.offsetHeight - window.innerHeight;
    if (span <= 0) return 0;
    return Math.min(1, Math.max(0, -r.top / span));
  };
  W.clamp01 = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  W.smooth = function (t) { t = W.clamp01(t); return t * t * (3 - 2 * t); };
  W.lerp = function (a, b, t) { return a + (b - a) * t; };

  /* ------------------------------------------------------------------ reveals */
  W.reveals = function (root) {
    root = root || document;
    var text = root.querySelectorAll('.rv'), imgs = root.querySelectorAll('.rvi');
    if (W.reduce) {
      [].forEach.call(text, function (e) { e.classList.add('in'); });
      [].forEach.call(imgs, function (e) { e.classList.add('in'); });
      return;
    }
    var ot = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ot.unobserve(e.target); } });
    }, { threshold: 0.14, rootMargin: '0px 0px -6% 0px' });
    /* images fire on the first pixel so nothing paints into an empty frame */
    var oi = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); oi.unobserve(e.target); } });
    }, { threshold: 0.001 });
    [].forEach.call(text, function (e) { ot.observe(e); });
    [].forEach.call(imgs, function (e) { oi.observe(e); });
  };

  /* ------------------------------------------------------------------ header */
  W.header = function (opts) {
    opts = opts || {};
    var hd = document.querySelector('.hd');
    if (!hd) return;
    var heroEnd = opts.heroEnd || 110, prev = 0, HYST = 6;
    W.onScroll(function (y) {
      if (y < heroEnd) { hd.classList.remove('up', 'frost'); prev = y; return; }
      if (Math.abs(y - prev) > HYST) {
        var down = y > prev;
        hd.classList.toggle('up', down && !hd.matches(':focus-within'));
        hd.classList.toggle('frost', !down);
        prev = y;
      }
    });
    hd.addEventListener('focusin', function () { hd.classList.remove('up'); });
    /* light/dark inversion over dark sections */
    var dark = document.querySelectorAll('[data-hd="dark"]');
    if (dark.length) {
      /* A page can have several dark sections. Toggle on whether ANY of them is
         under the header band — not on whichever entry the observer happened to
         report last, which on a page with two dark sections left the header in
         ink over a dark hero. */
      var lit = [];
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var i = lit.indexOf(e.target);
          if (e.isIntersecting) { if (i < 0) lit.push(e.target); }
          else if (i >= 0) { lit.splice(i, 1); }
        });
        hd.classList.toggle('inv', lit.length > 0);
      }, { rootMargin: '0px 0px -88% 0px' });
      [].forEach.call(dark, function (e) { io.observe(e); });
    }
  };

  /* ------------------------------------------------------------------ menu */
  W.menu = function () {
    var btn = document.querySelector('.mbtn'), nav = document.querySelector('.mnav');
    if (!btn || !nav) return;
    var main = document.getElementById('main'), hd = document.querySelector('.hd'), last = null;
    var links = nav.querySelectorAll('a');
    function stagger(on) {
      [].forEach.call(links, function (a, i) { a.style.transitionDelay = on ? (0.07 + i * 0.045) + 's' : '0s'; });
    }
    function open() {
      last = document.activeElement;
      nav.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
      nav.setAttribute('aria-modal', 'true');
      if (main) main.inert = true;
      document.body.style.overflow = 'hidden';
      stagger(true);
      var f = nav.querySelector('a'); if (f) setTimeout(function () { f.focus(); }, 120);
    }
    function close() {
      nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false');
      nav.removeAttribute('aria-modal');
      if (main) main.inert = false;
      document.body.style.overflow = '';
      stagger(false);
      if (last && last.focus) last.focus();
    }
    btn.addEventListener('click', function () { nav.classList.contains('open') ? close() : open(); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) close(); });
    if (hd) hd.style.zIndex = 960; /* button stays clickable above the overlay */
  };

  /* ------------------------------------------------------------------ page transition */
  W.transition = function () {
    var pt = document.querySelector('.pt');
    if (!pt || W.reduce) return;
    requestAnimationFrame(function () { pt.classList.add('reveal'); });
    addEventListener('pageshow', function (e) { if (e.persisted) { pt.classList.remove('cover'); pt.classList.add('reveal'); } });
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      var href = a.getAttribute('href') || '';
      if (!href || href[0] === '#' || a.target === '_blank' || /^(https?|tel|mailto):/i.test(href)) return;
      if (a.origin && a.origin !== location.origin) return;
      e.preventDefault();
      pt.classList.remove('reveal'); pt.classList.add('cover');
      setTimeout(function () { location.href = a.href; }, 620);
    });
  };

  /* ------------------------------------------------------------------ data */
  var dataPromise = null;
  W.load = function (url) {
    if (!dataPromise) {
      dataPromise = fetch(url || (document.documentElement.dataset.data || '../data/wiseman.json'))
        .then(function (r) { return r.json(); });
    }
    return dataPromise;
  };
  W.money = function (n) { return n == null ? null : '$' + Math.round(n).toLocaleString('en-US'); };
  W.priceLabel = function (p) {
    if (p.priceMin == null) return 'Call for details';
    if (p.priceMax && p.priceMax > p.priceMin) return W.money(p.priceMin) + '–' + W.money(p.priceMax);
    return 'From ' + W.money(p.priceMin);
  };
  W.bedLabel = function (p) { return (p.beds || '').replace(/\s*Beds?$/i, '') || '—'; };
  W.sqftLabel = function (p) { return (p.sqft || '—').replace(/\s*Sq\. Ft\.$/i, ''); };

  /* ------------------------------------------------------------------ register */
  /* Sort a complete list; never hide rows. `rows` are elements carrying data-* keys. */
  W.register = function (opts) {
    opts = opts || {};
    var list = document.querySelector(opts.list || '[data-register]');
    if (!list) return;
    var groups = [].slice.call(list.querySelectorAll('[data-group]'));
    var allRows = [].slice.call(list.querySelectorAll('[data-row]'));
    var controls = document.querySelectorAll('[data-sort]');
    var plate = document.querySelector('[data-plate]');

    function sortBy(key) {
      var flat = allRows.slice();
      var cmp = {
        no: function (a, b) { return a.dataset.no.localeCompare(b.dataset.no); },
        street: function (a, b) { return a.dataset.street.localeCompare(b.dataset.street) || a.dataset.no.localeCompare(b.dataset.no); },
        name: function (a, b) { return a.dataset.name.localeCompare(b.dataset.name); },
        beds: function (a, b) { return (+b.dataset.bedsmax || 0) - (+a.dataset.bedsmax || 0) || a.dataset.no.localeCompare(b.dataset.no); },
        rent: function (a, b) { return (+a.dataset.rent || 1e9) - (+b.dataset.rent || 1e9); }
      }[key] || null;

      if (key === 'area') { /* restore the authored grouping */
        groups.forEach(function (g) { g.hidden = false; });
        groups.forEach(function (g) {
          var body = g.querySelector('[data-rows]');
          allRows.forEach(function (r) { if (r.dataset.area === g.dataset.group) body.appendChild(r); });
        });
        list.dataset.mode = 'grouped';
      } else if (cmp) {
        flat.sort(cmp);
        groups.forEach(function (g, i) { g.hidden = i > 0; });
        var head = groups[0];
        if (head) {
          var lbl = head.querySelector('[data-grouplabel]');
          if (lbl) lbl.textContent = opts.flatLabel || ('All ' + allRows.length + ' buildings');
          var body = head.querySelector('[data-rows]');
          flat.forEach(function (r) { body.appendChild(r); });
        }
        list.dataset.mode = 'flat';
      }
      [].forEach.call(controls, function (c) { c.setAttribute('aria-pressed', String(c.dataset.sort === key)); });
      try { var u = new URL(location.href); u.searchParams.set('sort', key); history.replaceState(null, '', u); } catch (e) {}
    }

    [].forEach.call(controls, function (c) {
      c.addEventListener('click', function () { sortBy(c.dataset.sort); });
    });

    /* specimen plate: hover OR keyboard focus, never hover-only */
    if (plate) {
      var pimg = plate.querySelector('img'), pno = plate.querySelector('[data-plateno]'),
          pnm = plate.querySelector('[data-platename]'), pst = plate.querySelector('[data-platestreet]');
      var pending = null;
      function show(r) {
        if (!r || plate.dataset.cur === r.dataset.no) return;
        plate.dataset.cur = r.dataset.no;
        var src = r.dataset.img;
        if (pending) pending.onload = null;
        var next = new Image();
        pending = next;
        next.onload = function () {
          if (pending !== next) return;
          pimg.src = src; pimg.alt = r.dataset.name;
          plate.classList.remove('swap'); void plate.offsetWidth; plate.classList.add('swap');
        };
        next.src = src;
        if (pno) pno.textContent = r.dataset.no;
        if (pnm) pnm.textContent = r.dataset.name;
        if (pst) pst.textContent = r.dataset.street + ' · ' + r.dataset.arealabel;
      }
      allRows.forEach(function (r) {
        r.addEventListener('mouseenter', function () { show(r); });
        r.addEventListener('focusin', function () { show(r); });
      });
    }

    var initial = new URLSearchParams(location.search).get('sort');
    if (initial) sortBy(initial); else sortBy('area');
    W.sortRegister = sortBy;
  };

  /* ------------------------------------------------------------------ atlas */
  /* A drawn SVG of the real extent from lat/lng. Numbers as pins, not dots. */
  W.atlas = function (opts) {
    var host = document.querySelector(opts.el);
    if (!host) return;
    var pts = opts.points || [];
    if (!pts.length) return;
    var W_ = 1000, H_ = 700, PAD = 46;
    var lats = pts.map(function (p) { return p.lat; }), lngs = pts.map(function (p) { return p.lng; });
    var la0 = Math.min.apply(null, lats), la1 = Math.max.apply(null, lats);
    var lo0 = Math.min.apply(null, lngs), lo1 = Math.max.apply(null, lngs);
    /* keep aspect honest: 1 deg lng is cos(lat) as long as 1 deg lat */
    var k = Math.cos((la0 + la1) / 2 * Math.PI / 180);
    var spanX = (lo1 - lo0) * k, spanY = (la1 - la0);
    var s = Math.min((W_ - PAD * 2) / (spanX || 1), (H_ - PAD * 2) / (spanY || 1));
    var ox = (W_ - spanX * s) / 2, oy = (H_ - spanY * s) / 2;
    function X(p) { return ox + (p.lng - lo0) * k * s; }
    function Y(p) { return H_ - (oy + (p.lat - la0) * s); }

    var svg = ['<svg viewBox="0 0 ' + W_ + ' ' + H_ + '" role="img" aria-label="Map of ' + pts.length + ' Wiseman buildings across Los Angeles" class="atlas-svg">'];
    svg.push('<g class="atlas-grid" aria-hidden="true">');
    for (var gx = 0; gx <= 10; gx++) svg.push('<line x1="' + (gx * W_ / 10) + '" y1="0" x2="' + (gx * W_ / 10) + '" y2="' + H_ + '"/>');
    for (var gy = 0; gy <= 7; gy++) svg.push('<line x1="0" y1="' + (gy * H_ / 7) + '" x2="' + W_ + '" y2="' + (gy * H_ / 7) + '"/>');
    svg.push('</g>');
    pts.forEach(function (p) {
      var x = X(p).toFixed(1), y = Y(p).toFixed(1);
      svg.push('<g class="pin" data-no="' + p.no + '" transform="translate(' + x + ',' + y + ')">' +
        '<circle r="13" class="pin-hit"/>' +
        '<text class="pin-no" text-anchor="middle" dy="3.6">' + p.no + '</text>' +
        '</g>');
    });
    svg.push('</svg>');
    host.innerHTML = svg.join('');

    var pins = host.querySelectorAll('.pin');
    [].forEach.call(pins, function (g) {
      var no = g.dataset.no;
      g.addEventListener('mouseenter', function () { link(no, true); });
      g.addEventListener('mouseleave', function () { link(no, false); });
      g.addEventListener('click', function () {
        var row = document.querySelector('[data-row][data-no="' + no + '"] a');
        if (row) location.href = row.href;
      });
    });
    function link(no, on) {
      var row = document.querySelector('[data-row][data-no="' + no + '"]');
      if (row) row.classList.toggle('lit', on);
      var g = host.querySelector('.pin[data-no="' + no + '"]');
      if (g) g.classList.toggle('lit', on);
    }
    W.atlasLink = link;
  };

  /* ------------------------------------------------------------------ favourites */
  var FAV = 'wr-saved';
  function readFav() { try { return JSON.parse(localStorage.getItem(FAV) || '[]'); } catch (e) { return []; } }
  function writeFav(a) { try { localStorage.setItem(FAV, JSON.stringify(a)); } catch (e) {} }
  W.saved = readFav;
  W.favourites = function () {
    function paint() {
      var s = readFav();
      [].forEach.call(document.querySelectorAll('[data-fav]'), function (b) {
        var on = s.indexOf(b.dataset.fav) > -1;
        b.setAttribute('aria-pressed', String(on));
        var l = b.querySelector('[data-favlabel]');
        if (l) l.textContent = on ? 'Saved' : 'Save';
      });
      [].forEach.call(document.querySelectorAll('[data-favcount]'), function (e) {
        e.textContent = s.length; e.closest('[data-favwrap]') && (e.closest('[data-favwrap]').hidden = !s.length);
      });
    }
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-fav]');
      if (!b) return;
      e.preventDefault();
      var s = readFav(), i = s.indexOf(b.dataset.fav);
      if (i > -1) s.splice(i, 1); else s.push(b.dataset.fav);
      writeFav(s); paint();
    });
    paint();
    addEventListener('storage', paint);
  };

  /* ------------------------------------------------------------------ typeahead */
  W.typeahead = function (opts) {
    var input = document.querySelector(opts.input);
    var out = document.querySelector(opts.out);
    if (!input || !out) return;
    var items = opts.items || [];
    var idx = -1, open = false;
    function close() { out.innerHTML = ''; out.hidden = true; open = false; idx = -1; input.setAttribute('aria-expanded', 'false'); }
    function run() {
      var q = input.value.trim().toLowerCase();
      if (q.length < 2) return close();
      var hits = items.filter(function (it) { return it.hay.indexOf(q) > -1; }).slice(0, 8);
      if (!hits.length) {
        out.innerHTML = '<li class="ta-empty">No building or street matches that.</li>';
        out.hidden = false; open = true; input.setAttribute('aria-expanded', 'true'); return;
      }
      out.innerHTML = hits.map(function (h, i) {
        return '<li role="option" id="ta' + i + '"><a href="' + h.url + '"><span class="ta-no tnum">' + h.no +
          '</span><span class="ta-nm">' + h.name + '</span><span class="ta-sub">' + h.sub + '</span></a></li>';
      }).join('');
      out.hidden = false; open = true; idx = -1; input.setAttribute('aria-expanded', 'true');
    }
    input.addEventListener('input', run);
    input.addEventListener('keydown', function (e) {
      if (!open) return;
      var li = out.querySelectorAll('li a');
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        idx = (idx + (e.key === 'ArrowDown' ? 1 : -1) + li.length) % li.length;
        li[idx].focus();
      } else if (e.key === 'Escape') { close(); input.focus(); }
      else if (e.key === 'Enter' && li.length) { e.preventDefault(); (li[idx] || li[0]).click(); }
    });
    document.addEventListener('click', function (e) { if (!e.target.closest(opts.input) && !e.target.closest(opts.out)) close(); });
  };

  /* ------------------------------------------------------------------ availability filters */
  W.filters = function (opts) {
    var form = document.querySelector(opts.form), rows = [].slice.call(document.querySelectorAll(opts.rows));
    if (!form || !rows.length) return;
    var count = document.querySelector(opts.count), empty = document.querySelector(opts.empty);

    function state() {
      var fd = new FormData(form), s = {};
      fd.forEach(function (v, k) { if (v) (s[k] = s[k] || []).push(v); });
      return s;
    }
    function apply(push) {
      var s = state(), shown = 0;
      rows.forEach(function (r) {
        var ok = true;
        if (s.area && s.area.indexOf(r.dataset.area) < 0) ok = false;
        if (ok && s.beds) {
          ok = s.beds.some(function (b) {
            var n = +b;
            return (+r.dataset.bedsmin || 0) <= n && n <= (+r.dataset.bedsmax || 0);
          });
        }
        if (ok && s.max && s.max[0]) { var m = +s.max[0]; if (!r.dataset.rent || +r.dataset.rent > m) ok = false; }
        if (ok && s.amen) { ok = s.amen.every(function (a) { return (r.dataset.amen || '').indexOf('|' + a + '|') > -1; }); }
        r.hidden = !ok; if (ok) shown++;
      });
      if (count) count.textContent = shown;
      if (empty) empty.hidden = shown > 0;
      if (push !== false) {
        try {
          var u = new URL(location.href); u.search = '';
          Object.keys(s).forEach(function (k) { s[k].forEach(function (v) { u.searchParams.append(k, v); }); });
          history.replaceState(null, '', u);
        } catch (e) {}
      }
    }
    form.addEventListener('change', function () { apply(); });
    form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    var reset = form.querySelector('[data-reset]');
    if (reset) reset.addEventListener('click', function (e) { e.preventDefault(); form.reset(); apply(); });

    /* hydrate from the URL so results are shareable and the back button works */
    var q = new URLSearchParams(location.search), any = false;
    q.forEach(function (v, k) {
      [].forEach.call(form.elements, function (el) {
        if (el.name !== k) return;
        if (el.type === 'checkbox' || el.type === 'radio') { if (el.value === v) { el.checked = true; any = true; } }
        else { el.value = v; any = true; }
      });
    });
    apply(any);
  };

  /* ------------------------------------------------------------------ boot */
  W.boot = function (opts) {
    opts = opts || {};
    W.reveals();
    W.header(opts.header);
    W.menu();
    W.favourites();
    if (opts.transition !== false) W.transition();
    tick();
  };
})();
