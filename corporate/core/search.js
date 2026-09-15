/* Wiseman Residential — ILS search behaviour.
   The 72 result cards are static HTML (crawlable, instant); this module filters,
   sorts, and keeps the URL in step. Conventions borrowed from the marketplaces
   renters already use: dropdown filter popovers, a More-filters modal, active
   chips, a live count, a sort select, and a synced map.

   Markup contract — see availability.html in any direction:
     [data-search]                  the root
     [data-fpop] > [data-fbtn] + [data-fmenu]      one dropdown
     input[name=area|beds|baths|amen|feature]      checkboxes anywhere inside
     select[name=pmin|pmax|sqmin|sort]
     [data-card] with data-no/-area/-bedsmin/-bedsmax/-bathsmin/-bathsmax/
                 -rent/-sqft/-tags/-name/-street
     [data-count] [data-chips] [data-empty] [data-clearall]
     dialog[data-fmodal]  with [data-fmodal-open] / [data-fmodal-close] / [data-fmodal-apply]
*/
(function () {
  'use strict';
  var W = (window.WR = window.WR || {});

  var LABELS = {
    area: {}, beds: { '0': 'Studio', '1': '1 bed', '2': '2 beds', '3': '3 beds', '4': '4 beds', '5': '5 beds' },
    baths: { '1': '1+ bath', '2': '2+ baths', '3': '3+ baths', '4': '4+ baths' },
    amen: {}, feature: {}
  };

  function money(n) { return '$' + Number(n).toLocaleString('en-US'); }

  W.searchPage = function (opts) {
    opts = opts || {};
    var root = document.querySelector(opts.root || '[data-search]');
    if (!root) return;

    var cards = [].slice.call(root.querySelectorAll('[data-card]'));
    var countEls = [].slice.call(root.querySelectorAll('[data-count]'));
    var chipsEl = root.querySelector('[data-chips]');
    var emptyEl = root.querySelector('[data-empty]');
    var listEl = root.querySelector('[data-cards]');
    var sortEl = root.querySelector('[name="sort"]');
    var qEl = root.querySelector('[name="q"]');
    var modal = root.querySelector('dialog[data-fmodal]');

    /* collect every control, wherever it lives (bar or modal) */
    function boxes(name) { return [].slice.call(root.querySelectorAll('input[name="' + name + '"]')); }
    function sel(name) { return root.querySelector('select[name="' + name + '"]'); }
    var MULTI = ['area', 'beds', 'baths', 'amen', 'feature'];

    /* label lookup straight off the control, so the chips read like the UI */
    MULTI.forEach(function (n) {
      boxes(n).forEach(function (b) {
        var host = b.closest('label');
        if (!host) return;
        /* the label carries a live result count in .cnt — that is chrome, not the name */
        var t = [].slice.call(host.childNodes).map(function (node) {
          if (node.nodeType === 3) return node.nodeValue;
          return (node.classList && node.classList.contains('cnt')) ? '' : (node.textContent || '');
        }).join('');
        t = t.replace(/\s+/g, ' ').trim();
        if (t && !LABELS[n][b.value]) LABELS[n][b.value] = t;
      });
    });

    /* ─────────────────────────── state ─────────────────────────── */
    function read() {
      var s = { q: qEl ? qEl.value.trim() : '' };
      MULTI.forEach(function (n) {
        s[n] = boxes(n).filter(function (b) { return b.checked; }).map(function (b) { return b.value; });
      });
      ['pmin', 'pmax', 'sqmin'].forEach(function (n) { var e = sel(n); s[n] = e && e.value ? +e.value : null; });
      s.sort = sortEl ? sortEl.value : 'no';
      return s;
    }

    function write(s) {
      MULTI.forEach(function (n) {
        boxes(n).forEach(function (b) { b.checked = (s[n] || []).indexOf(b.value) > -1; });
      });
      ['pmin', 'pmax', 'sqmin'].forEach(function (n) { var e = sel(n); if (e) e.value = s[n] == null ? '' : String(s[n]); });
      if (sortEl && s.sort) sortEl.value = s.sort;
      if (qEl) qEl.value = s.q || '';
    }

    function fromURL() {
      var p = new URLSearchParams(location.search), s = { q: p.get('q') || '' };
      MULTI.forEach(function (n) { s[n] = p.getAll(n); });
      ['pmin', 'pmax', 'sqmin'].forEach(function (n) { s[n] = p.get(n) ? +p.get(n) : null; });
      s.sort = p.get('sort') || 'no';
      return s;
    }

    function toURL(s) {
      var p = new URLSearchParams();
      if (s.q) p.set('q', s.q);
      MULTI.forEach(function (n) { (s[n] || []).forEach(function (v) { p.append(n, v); }); });
      ['pmin', 'pmax', 'sqmin'].forEach(function (n) { if (s[n] != null) p.set(n, s[n]); });
      if (s.sort && s.sort !== 'no') p.set('sort', s.sort);
      var q = p.toString();
      try { history.replaceState(null, '', location.pathname + (q ? '?' + q : '')); } catch (e) {}
    }

    /* ─────────────────────────── matching ─────────────────────────── */
    /* `+"" === 0`, so an empty data-attribute would answer "studio, zero beds" and put a
       building that publishes no bedroom figure into the Studio facet. Read numbers through
       this instead of coercing with +. */
    function num(v) { return (v === undefined || v === null || v === '') ? NaN : +v; }

    function matches(c, s) {
      var d = c.dataset;
      if (s.area.length && s.area.indexOf(d.area) < 0) return false;
      if (s.beds.length) {
        var lo = num(d.bedsmin), hi = num(d.bedsmax);
        if (isNaN(lo)) return false;
        var ok = s.beds.some(function (v) {
          var n = +v;
          return n === 5 ? hi >= 5 : (lo <= n && n <= hi);
        });
        if (!ok) return false;
      }
      if (s.baths.length) {
        var bh = num(d.bathsmax);
        if (isNaN(bh) || bh < Math.min.apply(null, s.baths.map(Number))) return false;
      }
      if (s.pmin != null || s.pmax != null) {
        var r = isNaN(num(d.rent)) ? null : num(d.rent);
        if (r == null) return false;                 /* "call for details" drops out of a price filter */
        if (s.pmin != null && r < s.pmin) return false;
        if (s.pmax != null && r > s.pmax) return false;
      }
      if (s.sqmin != null) {
        var sq = isNaN(num(d.sqft)) ? null : num(d.sqft);
        if (sq == null || sq < s.sqmin) return false;
      }
      var tags = '|' + (d.tags || '') + '|';
      if (s.amen.length && !s.amen.every(function (a) { return tags.indexOf('|' + a + '|') > -1; })) return false;
      if (s.feature.length && !s.feature.every(function (a) { return tags.indexOf('|' + a + '|') > -1; })) return false;
      if (s.q) {
        var hay = ((d.name || '') + ' ' + (d.street || '') + ' ' + (d.arealabel || '') + ' ' + (d.no || '')).toLowerCase();
        if (hay.indexOf(s.q.toLowerCase()) < 0) return false;
      }
      return true;
    }

    var SORTS = {
      no: function (a, b) { return a.dataset.no.localeCompare(b.dataset.no); },
      priceup: function (a, b) { return (+a.dataset.rent || Infinity) - (+b.dataset.rent || Infinity); },
      pricedown: function (a, b) { return (+b.dataset.rent || -1) - (+a.dataset.rent || -1); },
      beds: function (a, b) { return (+b.dataset.bedsmax || 0) - (+a.dataset.bedsmax || 0) || a.dataset.no.localeCompare(b.dataset.no); },
      sqft: function (a, b) { return (+b.dataset.sqft || 0) - (+a.dataset.sqft || 0); },
      name: function (a, b) { return (a.dataset.name || '').localeCompare(b.dataset.name || ''); },
      area: function (a, b) { return (a.dataset.arealabel || '').localeCompare(b.dataset.arealabel || '') || a.dataset.no.localeCompare(b.dataset.no); }
    };

    /* ─────────────────────────── apply ─────────────────────────── */
    var shownNos = [];
    function apply(push) {
      var s = read(), n = 0;
      shownNos = [];
      cards.forEach(function (c) {
        var ok = matches(c, s);
        c.hidden = !ok;
        if (ok) { n++; shownNos.push(c.dataset.no); }
      });

      if (listEl && SORTS[s.sort]) {
        cards.slice().sort(SORTS[s.sort]).forEach(function (c) { listEl.appendChild(c); });
      }

      countEls.forEach(function (e) { e.textContent = n; });
      if (emptyEl) emptyEl.hidden = n > 0;
      if (listEl) listEl.hidden = n === 0;
      paintChips(s);
      paintButtons(s);
      liveCounts(s);
      if (push !== false) toURL(s);
      if (W.mapSetVisible) W.mapSetVisible(shownNos);
      root.dispatchEvent(new CustomEvent('wr:filtered', { detail: { count: n, nos: shownNos, state: s } }));
    }

    /* option counts update against everything EXCEPT that option's own group,
       the way a marketplace does it, so a facet never shows a zero it caused */
    function liveCounts(s) {
      MULTI.forEach(function (n) {
        var without = Object.assign({}, s); without[n] = [];
        var pool = cards.filter(function (c) { return matches(c, without); });
        boxes(n).forEach(function (b) {
          var k = Object.assign({}, without); k[n] = [b.value];
          var c = pool.filter(function (card) { return matches(card, k); }).length;
          var host = b.closest('label') || b.parentElement;
          var slot = host && host.querySelector('.cnt');
          if (slot) slot.textContent = c;
          if (host) host.classList.toggle('off', c === 0 && !b.checked);
        });
      });
    }

    function paintButtons(s) {
      [].forEach.call(root.querySelectorAll('[data-fbtn]'), function (btn) {
        var group = btn.dataset.fbtn;
        var active = 0, label = btn.dataset.label || btn.textContent.trim();
        if (MULTI.indexOf(group) > -1) active = (s[group] || []).length;
        else if (group === 'price') active = (s.pmin != null || s.pmax != null) ? 1 : 0;
        else if (group === 'more') active = (s.amen || []).length + (s.feature || []).length + (s.sqmin != null ? 1 : 0);
        btn.classList.toggle('on', active > 0);
        var t = btn.querySelector('[data-fbtn-label]');
        if (t) {
          if (group === 'price' && active) {
            t.textContent = (s.pmin ? money(s.pmin) : 'Any') + '–' + (s.pmax ? money(s.pmax) : 'Any');
          } else {
            t.textContent = active ? label + ' · ' + active : label;
          }
        }
      });
    }

    function paintChips(s) {
      if (!chipsEl) return;
      var out = [];
      MULTI.forEach(function (n) {
        (s[n] || []).forEach(function (v) {
          out.push({ k: n, v: v, t: LABELS[n][v] || v });
        });
      });
      if (s.pmin != null || s.pmax != null) {
        out.push({ k: 'price', v: '', t: (s.pmin ? money(s.pmin) : 'Any') + ' – ' + (s.pmax ? money(s.pmax) : 'Any') });
      }
      if (s.sqmin != null) out.push({ k: 'sqmin', v: '', t: s.sqmin.toLocaleString('en-US') + '+ sq ft' });
      if (s.q) out.push({ k: 'q', v: '', t: '“' + s.q + '”' });

      chipsEl.innerHTML = out.map(function (c) {
        return '<span class="chip-f">' + esc(c.t) +
          '<button type="button" data-drop="' + c.k + '" data-drop-v="' + esc(c.v) + '" aria-label="Remove filter ' + esc(c.t) + '">' +
          '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1 1l8 8M9 1l-8 8"/></svg></button></span>';
      }).join('');
      /* there are two: one beside the chips and one in the modal footer. The modal's
         sits in a space-between row, so hiding it threw the Apply button across the
         dialog — it greys out in place instead. */
      [].forEach.call(root.querySelectorAll('[data-clearall]'), function (b) {
        if (b.closest('.fmodal-f')) { b.disabled = out.length === 0; b.hidden = false; }
        else { b.hidden = out.length === 0; }
      });
    }

    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }

    /* ─────────────────────────── wiring ─────────────────────────── */
    root.addEventListener('change', function (e) {
      if (e.target.matches('input[type="checkbox"], select')) apply();
    });
    if (qEl) {
      var t = null;
      qEl.addEventListener('input', function () { clearTimeout(t); t = setTimeout(apply, 180); });
      var form = qEl.closest('form');
      if (form) form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    }

    root.addEventListener('click', function (e) {
      var drop = e.target.closest('[data-drop]');
      if (drop) {
        var k = drop.dataset.drop, v = drop.dataset.dropV;
        if (MULTI.indexOf(k) > -1) {
          boxes(k).forEach(function (b) { if (b.value === v) b.checked = false; });
        } else if (k === 'price') { ['pmin', 'pmax'].forEach(function (n) { var s = sel(n); if (s) s.value = ''; }); }
        else if (k === 'sqmin') { var sq = sel('sqmin'); if (sq) sq.value = ''; }
        else if (k === 'q' && qEl) { qEl.value = ''; }
        apply();
        return;
      }
      if (e.target.closest('[data-clearall]')) {
        e.preventDefault();
        MULTI.forEach(function (n) { boxes(n).forEach(function (b) { b.checked = false; }); });
        ['pmin', 'pmax', 'sqmin'].forEach(function (n) { var s = sel(n); if (s) s.value = ''; });
        if (qEl) qEl.value = '';
        apply();
        return;
      }
      var clearGroup = e.target.closest('[data-clear]');
      if (clearGroup) {
        e.preventDefault();
        var g = clearGroup.dataset.clear;
        if (MULTI.indexOf(g) > -1) boxes(g).forEach(function (b) { b.checked = false; });
        if (g === 'price') ['pmin', 'pmax'].forEach(function (n) { var s = sel(n); if (s) s.value = ''; });
        apply();
      }
    });

    /* dropdown popovers — position:fixed and placed from the button's rect, so the
       scrolling filter rail can never clip them and they float over the map/list */
    var openPop = null, popRaf = 0;
    function placePop() {
      if (!openPop) return;
      var b = openPop.btn.getBoundingClientRect(), m = openPop.menu;
      var w = m.offsetWidth, left = b.left;
      if (left + w > window.innerWidth - 12) left = Math.max(12, b.right - w);
      m.style.top = Math.round(b.bottom + 7) + 'px';
      m.style.left = Math.round(left) + 'px';
      m.style.right = 'auto';
      /* A skinned bar may carry backdrop-filter / transform / contain, any of which turns
         it into the containing block for a fixed child — the menu would then land at
         (bar-relative) coordinates far from the button. Measure and correct the delta, so
         the placement is right no matter what an ancestor does. */
      var got = m.getBoundingClientRect();
      var dy = got.top - (b.bottom + 7), dx = got.left - left;
      if (Math.abs(dy) > 1 || Math.abs(dx) > 1) {
        m.style.top = Math.round(b.bottom + 7 - dy) + 'px';
        m.style.left = Math.round(left - dx) + 'px';
      }
      /* the button scrolled out of the rail — a menu hanging off nothing is worse than none */
      var track = openPop.btn.closest('[data-rail-track]');
      if (track) {
        var t = track.getBoundingClientRect();
        if (b.right < t.left || b.left > t.right) closePop();
      }
    }
    function queuePop() { if (!popRaf) popRaf = requestAnimationFrame(function () { popRaf = 0; placePop(); }); }
    function closePop() {
      if (!openPop) return;
      openPop.btn.setAttribute('aria-expanded', 'false');
      openPop.menu.hidden = true;
      openPop = null;
    }
    addEventListener('scroll', queuePop, { passive: true, capture: true });
    addEventListener('resize', queuePop);
    [].forEach.call(root.querySelectorAll('[data-fpop]'), function (pop) {
      var btn = pop.querySelector('[data-fbtn]'), menu = pop.querySelector('[data-fmenu]');
      if (!btn || !menu) return;
      menu.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var was = openPop && openPop.btn === btn;
        closePop();
        if (was) return;
        btn.setAttribute('aria-expanded', 'true');
        menu.hidden = false;
        openPop = { btn: btn, menu: menu };
        placePop();
        var first = menu.querySelector('input, select, button');
        if (first) first.focus({ preventScroll: true });
      });
      menu.addEventListener('click', function (e) { e.stopPropagation(); });
      menu.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.stopPropagation(); closePop(); btn.focus(); }
      });
    });
    document.addEventListener('click', closePop);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePop(); });

    /* more-filters modal.

       A <dialog> closes in the frame .close() is called: it leaves the top layer
       and [open] goes, so a CSS close animation never gets a frame to run in.
       Every path out of this dialog therefore goes through dismiss(), which
       stamps [data-closing] (core/search.css animates on that), waits for the
       animation to finish and only then closes for real. Two guards: the
       animationend listener is paired with a timeout, so a dropped event or a
       browser that does not fire one can never strand the dialog open; and the
       native Escape close is intercepted with preventDefault + dismiss, so the
       key still closes the dialog and now closes it the same way as the others. */
    if (modal) {
      var closing = false;

      function dismiss() {
        if (!modal.open) return;
        if (closing) return;
        if (!modal.close) { modal.removeAttribute('open'); return; }
        closing = true;
        modal.setAttribute('data-closing', '');
        var done = false;
        function finish() {
          if (done) return;
          done = true; closing = false;
          modal.removeAttribute('data-closing');
          if (modal.open) modal.close();
        }
        modal.addEventListener('animationend', function h(e) {
          if (e.target !== modal) return;
          modal.removeEventListener('animationend', h);
          finish();
        });
        setTimeout(finish, 600);
      }

      var opener = root.querySelector('[data-fmodal-open]');
      if (opener) opener.addEventListener('click', function () {
        closePop();
        modal.removeAttribute('data-closing');
        closing = false;
        if (modal.showModal) modal.showModal(); else modal.setAttribute('open', '');
      });
      [].forEach.call(modal.querySelectorAll('[data-fmodal-close]'), function (b) {
        b.addEventListener('click', dismiss);
      });
      var applyBtn = modal.querySelector('[data-fmodal-apply]');
      if (applyBtn) applyBtn.addEventListener('click', function () {
        apply();
        dismiss();
      });
      modal.addEventListener('click', function (e) { if (e.target === modal) dismiss(); });
      modal.addEventListener('cancel', function (e) { e.preventDefault(); dismiss(); });
    }

    /* list / map toggle on narrow screens */
    var split = root.querySelector('[data-split]');
    [].forEach.call(root.querySelectorAll('[data-view]'), function (b) {
      b.addEventListener('click', function () {
        var m = b.dataset.view === 'map';
        if (split) split.classList.toggle('show-map', m);
        [].forEach.call(root.querySelectorAll('[data-view]'), function (o) {
          o.setAttribute('aria-pressed', String(o.dataset.view === b.dataset.view));
        });
        if (m && W.mapInstance) setTimeout(function () { W.mapInstance.invalidateSize(); }, 60);
      });
    });

    /* card ⇄ pin highlight */
    cards.forEach(function (c) {
      var no = c.dataset.no;
      c.addEventListener('mouseenter', function () { if (W.mapFocus) W.mapFocus(no); });
      c.addEventListener('mouseleave', function () { if (W.mapBlur) W.mapBlur(no); });
      c.addEventListener('focusin', function () { if (W.mapFocus) W.mapFocus(no); });
      c.addEventListener('focusout', function () { if (W.mapBlur) W.mapBlur(no); });
    });

    write(fromURL());
    apply(false);
    toURL(read());
    W.searchApply = apply;
  };
})();
