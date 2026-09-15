/* Wiseman Residential — real embedded map.
   Leaflet over OpenStreetMap tiles (Esri colour / grey / aerial styles as options). Loaded on demand so no page
   pays for it until a map is actually on screen. Falls back to WR.atlas (drawn SVG)
   if the CDN is unreachable, so the page is never broken by a network failure.

   WR.map({
     el:        '#portfolio-map',        // container selector
     points:    [{no,lat,lng,name,street,area,areaLabel,beds,rent,img,url}],
     areas:     {key:{name,count,lat,lng}},  // optional, for the zoomed-out view
     theme:     'light' | 'dark',        // page palette; dark pages default to aerial tiles
     tiles:     'osm' | 'topo' | 'streets' | 'imagery' | 'light' | 'dark',   // optional basemap
     onSelect:  fn(no)                   // optional
   })
*/
(function () {
  'use strict';
  var W = (window.WR = window.WR || {});

  var LEAFLET_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
  var LEAFLET_JS = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';

  var loading = null;
  function loadLeaflet() {
    if (window.L) return Promise.resolve(window.L);
    if (loading) return loading;
    loading = new Promise(function (res, rej) {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = LEAFLET_CSS;
      link.crossOrigin = '';
      document.head.appendChild(link);
      var s = document.createElement('script');
      s.src = LEAFLET_JS;
      s.crossOrigin = '';
      s.onload = function () { res(window.L); };
      s.onerror = function () { rej(new Error('leaflet failed to load')); };
      document.head.appendChild(s);
      setTimeout(function () { if (!window.L) rej(new Error('leaflet timed out')); }, 9000);
    });
    return loading;
  }

  /* Basemaps — all keyless. OpenStreetMap's own cartography is the default: it is
     the map people recognise, it has colour (parks, water, the coastline) and it
     serves native tiles to z19, so a building page can sit at z16 without blur.
     'topo' and 'streets' are Esri's colour styles; 'imagery' is aerial photography
     with Esri's transport and place-name overlays — the dark pages use it, since a
     bright street map punched into a dark band reads as a hole. Esri's Canvas greys
     stay under 'light' / 'dark' for a page that wants a quieter map (they were the
     default until the client asked for colour). A page picks with `tiles:` in the
     WR.map options, or sets WR.tiles / WR.tilesDark before boot.
     Production note: tile.openstreetmap.org is a community server with a usage
     policy (operations.osmfoundation.org/policies/tiles) — fine for a pitch, not
     for a launched site with 72 building pages. Swap in a keyed provider serving
     the same style (MapTiler, Stadia, Thunderforest); it is one URL here. */
  var ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/';
  var OSM_ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
  var ESRI_ATTR = 'Tiles &copy; <a href="https://www.esri.com/">Esri</a> &mdash; Esri, HERE, Garmin, ' + OSM_ATTR;
  var TILES = {
    osm:     { url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
               native: 19, max: 18, attr: OSM_ATTR, colour: true },
    topo:    { url: ESRI + 'World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
               native: 19, max: 18, attr: ESRI_ATTR, colour: true },
    streets: { url: ESRI + 'World_Street_Map/MapServer/tile/{z}/{y}/{x}',
               native: 19, max: 18, attr: ESRI_ATTR, colour: true },
    imagery: { url: ESRI + 'World_Imagery/MapServer/tile/{z}/{y}/{x}',
               refs: [ESRI + 'Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}',
                      ESRI + 'Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}'],
               native: 19, max: 18, attr: ESRI_ATTR, colour: true },
    light:   { url: ESRI + 'Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
               refs: [ESRI + 'Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}'],
               native: 16, max: 17, attr: ESRI_ATTR },
    dark:    { url: ESRI + 'Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
               refs: [ESRI + 'Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}'],
               native: 16, max: 17, attr: ESRI_ATTR }
  };
  W.tiles = W.tiles || 'osm';
  W.tilesDark = W.tilesDark || 'imagery';

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }

  W.map = function (opts) {
    var host = document.querySelector(opts.el);
    if (!host || !opts.points || !opts.points.length) return;
    host.classList.add('wr-map');
    host.setAttribute('role', 'region');
    host.setAttribute('aria-label', opts.label || ('Map of ' + opts.points.length + ' Wiseman buildings'));

    var note = document.createElement('p');
    note.className = 'wr-map-loading';
    note.textContent = 'Loading map…';
    host.appendChild(note);

    loadLeaflet().then(function (L) {
      note.remove();
      var pts = opts.points;
      var tilesKey = opts.tiles || (opts.theme === 'dark' ? W.tilesDark : W.tiles);
      var theme = TILES[tilesKey] || TILES.osm;
      host.dataset.tiles = tilesKey;
      host.dataset.colour = theme.colour ? '1' : '';

      var map = L.map(host, {
        scrollWheelZoom: false,          // never steal the page scroll
        zoomControl: false,
        attributionControl: true,
        /* Whole-number zoom put the portfolio fit on a cliff edge: 72 points
           need 525px of height at z12, and a band that leaves 516px after
           padding fell all the way to z11 — half of LA County drawn around a
           six-mile portfolio. A quarter-step snap lets the fit land where it
           belongs on any band height; the +/- buttons still step a whole zoom. */
        zoomSnap: 0.25,
        zoomDelta: 1,
        fadeAnimation: !W.reduce,
        zoomAnimation: !W.reduce,
        markerZoomAnimation: !W.reduce
      });
      L.control.zoom({ position: 'bottomright' }).addTo(map);
      /* Never upsample: cap the map at the basemap's ceiling, and on retina screens
         fetch z+1 tiles and paint them at half size so streets stay crisp. */
      var tileOpts = { maxZoom: theme.max, maxNativeZoom: theme.native, detectRetina: true, attribution: theme.attr };
      L.tileLayer(theme.url, tileOpts).addTo(map);
      /* reference overlays (labels, roads over imagery) ride in their own pane,
         above the basemap and below the pins */
      if (theme.refs) {
        map.createPane('wrLabels');
        map.getPane('wrLabels').style.zIndex = 350;
        map.getPane('wrLabels').style.pointerEvents = 'none';
        theme.refs.forEach(function (u) {
          L.tileLayer(u, { maxZoom: theme.max, maxNativeZoom: theme.native, detectRetina: true, pane: 'wrLabels' }).addTo(map);
        });
      }

      var bounds = L.latLngBounds(pts.map(function (p) { return [p.lat, p.lng]; }));
      /* Padding in proportion to the box, not a flat 48px. On a 320px-wide
         phone panel a fixed 48px each side spends 30% of the map on air and
         cost a whole zoom level — the portfolio opened showing Santa Clarita.
         Clamped so a large map still gets real margins. */
      function fitPad() {
        return [Math.max(16, Math.min(48, Math.round(host.clientWidth * 0.05))),
                Math.max(16, Math.min(48, Math.round(host.clientHeight * 0.06)))];
      }
      map.fitBounds(bounds, { padding: fitPad() });

      /* ---- individual building pins ----
         pins:'number' (default) — the register number, for the atlas and area pages.
         pins:'price'            — a Zillow-style starting-rent pill, for the search page.
         The rent comes from the matching result card when one is on the page, so a
         building whose rent must not be published (no data-rent) never gets a figure;
         p.pinLabel overrides everything (e.g. "New" for a lease-up). */
      var byNo = {}, markers = [];
      var PRICE = opts.pins === 'price';
      function pinLabel(p) {
        if (p.pinLabel) return p.pinLabel;
        var rent = (p.rentMin != null && p.rentMin !== '') ? +p.rentMin : null;
        if (rent == null) {
          var c = document.querySelector('[data-card][data-no="' + p.no + '"]');
          if (c && c.dataset.rent) rent = +c.dataset.rent;
        }
        if (rent && rent > 0) return rent >= 1000 ? '$' + (rent / 1000).toFixed(1).replace(/\.0$/, '') + 'K' : '$' + rent;
        return 'Ask';
      }
      /* A regular map pin, not a numbered disc — a number on a pin reads as "how many
         homes here". The register number stays in data-no for the row/pin highlight. */
      /* A plain dot, centred on the address. No tail, no number. */
      pts.forEach(function (p) {
        var icon = PRICE
          ? L.divIcon({
              className: 'wr-pin-wrap',
              html: '<span class="wr-pin price" data-no="' + esc(p.no) + '"><i>' + esc(pinLabel(p)) + '</i></span>',
              iconSize: [72, 28], iconAnchor: [36, 14], popupAnchor: [0, -16]
            })
          : L.divIcon({
              className: 'wr-pin-wrap',
              html: '<span class="wr-pin dot" data-no="' + esc(p.no) + '"></span>',
              iconSize: [18, 18], iconAnchor: [9, 9], popupAnchor: [0, -12]
            });
        var m = L.marker([p.lat, p.lng], { icon: icon, keyboard: true, title: p.name, riseOnHover: true });
        m.bindPopup(popupHTML(p), { className: 'wr-pop', minWidth: 232, maxWidth: 260, closeButton: true, autoPanPadding: [26, 26] });
        m.on('mouseover', function () { hi(p.no, true); });
        m.on('mouseout', function () { hi(p.no, false); });
        m.on('click', function () { if (opts.onSelect) opts.onSelect(p.no); });
        m._wrNo = p.no;
        m._wrRent = +p.rent || 0;
        byNo[p.no] = m;
        markers.push(m);
        m.addTo(map);
      });

      /* ---- area bubbles, shown instead of pins when zoomed out ---- */
      var bubbles = [], bubByArea = {}, areaOfNo = {};
      pts.forEach(function (p) { areaOfNo[p.no] = p.area; });
      if (false && opts.areas) {
        Object.keys(opts.areas).forEach(function (k, ai) {
          var a = opts.areas[k];
          if (!a.count) return;
          var mine = pts.filter(function (p) { return p.area === k; });
          if (!mine.length) return;
          var la = mine.reduce(function (s, p) { return s + p.lat; }, 0) / mine.length;
          var lo = mine.reduce(function (s, p) { return s + p.lng; }, 0) / mine.length;
          var b = L.marker([la, lo], {
            icon: L.divIcon({
              className: 'wr-bub-wrap',
              /* Seven true centroids inside one city sit close enough to
                 overlap at the opening zoom — West LA and Brentwood are 1.8km
                 apart, which is 29px at the zoom a 72-point fit lands on, and
                 the disc is 46px. The NAME is stepped down a row or two per
                 --bub-i; the DISC is separated by declutter() below, which
                 draws a leader back to the true centroid whenever it moves one,
                 so the map never claims a position it has not got. */
              html: '<span class="wr-bub" style="--bub-i:' + (ai % 3) + '"><i>' +
                    a.count + '</i><em>' + esc(a.name) + '</em></span>',
              iconSize: [0, 0], iconAnchor: [0, 0]
            }),
            /* the largest count draws on top: it is the one a reader is
               looking for, and it is the one worth reading */
            zIndexOffset: a.count,
            keyboard: false, interactive: true
          });
          b.on('click', function () { map.flyToBounds(L.latLngBounds(mine.map(function (p) { return [p.lat, p.lng]; })), { padding: [56, 56] }); });
          b._wrWeight = a.count;
          b._wrArea = k;
          b._wrCount = a.count;
          bubByArea[k] = b;
          bubbles.push(b);
        });
      }

      /* ---- declutter: separate overlapping area discs, and say so ----
         A pure relaxation on the projected pixel positions. The bigger count
         holds its ground and the smaller one yields, because the big disc is
         the one a reader is hunting for. Every displaced disc gets a 1px
         leader back to its real centroid, so the offset is disclosed rather
         than hidden. Layout, not choreography: it runs under reduced motion
         too — only the transition is gated, in map.css. */
      var BUB_SEP = 54;   /* 46px disc + 8px of air */
      function declutter() {
        if (bubbles.length < 2) return;
        var n = [], i, j;
        for (i = 0; i < bubbles.length; i++) {
          if (!map.hasLayer(bubbles[i])) return;   /* pins are showing */
          var p = map.latLngToLayerPoint(bubbles[i].getLatLng());
          n.push({ b: bubbles[i], x0: p.x, y0: p.y, x: p.x, y: p.y,
                   w: bubbles[i]._wrWeight || 1 });
        }
        for (var pass = 0; pass < 40; pass++) {
          var moved = false;
          for (i = 0; i < n.length; i++) {
            for (j = i + 1; j < n.length; j++) {
              var a = n[i], c = n[j];
              var dx = c.x - a.x, dy = c.y - a.y;
              var d = Math.sqrt(dx * dx + dy * dy);
              if (d >= BUB_SEP) continue;
              if (d < 0.01) { dx = (i - j) || 1; dy = 0.6; d = Math.sqrt(dx * dx + dy * dy); }
              var push = (BUB_SEP - d);
              var ux = dx / d, uy = dy / d;
              var sum = a.w + c.w;
              a.x -= ux * push * (c.w / sum); a.y -= uy * push * (c.w / sum);
              c.x += ux * push * (a.w / sum); c.y += uy * push * (a.w / sum);
              moved = true;
            }
          }
          if (!moved) break;
        }
        n.forEach(function (o) {
          var el = o.b.getElement();
          var span = el && el.querySelector('.wr-bub');
          if (!span) return;
          var ox = Math.round(o.x - o.x0), oy = Math.round(o.y - o.y0);
          var len = Math.sqrt(ox * ox + oy * oy);
          span.style.setProperty('--bub-ox', ox + 'px');
          span.style.setProperty('--bub-oy', oy + 'px');
          span.style.setProperty('--bub-lead', (len > 3 ? Math.round(len) : 0) + 'px');
          span.style.setProperty('--bub-ang', (len > 3 ? Math.round(Math.atan2(-oy, -ox) * 180 / Math.PI) : 0) + 'deg');
        });
      }

      var BREAK = opts.breakZoom || 13;
      function level() {
        var z = map.getZoom();
        host.dataset.far = z < 12 ? '1' : '';
        /* A filtered search should show the buildings themselves, not a count disc:
           once the result set is small the reader is comparing individual buildings,
           and an area bubble hides exactly what they asked for. */
        var filteredSmall = W._wrHidden && liveCount() <= 20;
        var showPins = z >= BREAK || !bubbles.length || filteredSmall;
        markers.forEach(function (m) {
          /* a filtered-out building stays off the map at every zoom */
          var allowed = !W._wrHidden || !W._wrHidden[m._wrNo];
          (showPins && allowed) ? m.addTo(map) : map.removeLayer(m);
        });
        bubbles.forEach(function (b) {
          (showPins || b._wrCount === 0) ? map.removeLayer(b) : b.addTo(map);
        });
        if (!showPins) declutter();
      }
      /* Price pills collide where the portfolio is dense — 27 buildings in West LA
         at the fit zoom is a heap of "$4.9K"s. Zillow's answer: keep the pills that
         fit, draw the rest as dots, and let zoom or hover bring the label back.
         Greedy by rent (a dearer building keeps its pill when two overlap); the lit
         one always keeps it; re-run on every zoom and pan. */
      function crowd() {
        if (opts.pins !== 'price') return;
        var kept = [], live = [];
        markers.forEach(function (m) {
          if (!map.hasLayer(m)) return;
          var el = m.getElement(); if (!el) return;
          var span = el.querySelector('.wr-pin'); if (!span) return;
          var pt = map.latLngToLayerPoint(m.getLatLng());
          live.push({ m: m, span: span, x: pt.x, y: pt.y, w: (span._wrW || span.offsetWidth || 60) + 6, h: 30,
                      rent: m._wrRent || 0, lit: span.classList.contains('lit') });
          if (!span._wrW && span.offsetWidth) span._wrW = span.offsetWidth;
        });
        live.sort(function (a, b) { return (b.lit - a.lit) || (b.rent - a.rent); });
        live.forEach(function (o) {
          var hit = kept.some(function (k) {
            return Math.abs(k.x - o.x) < (k.w + o.w) / 2 && Math.abs(k.y - o.y) < (k.h + o.h) / 2;
          });
          o.span.classList.toggle('crowd', hit);
          /* pills ride above the dots they shadow; hover still lifts any marker */
          o.m.setZIndexOffset(hit ? -400 : 400);
          if (!hit) kept.push(o);
        });
      }
      map.on('zoomend', level);
      map.on('resize', level);
      map.on('zoomend moveend', function () { setTimeout(crowd, 0); });
      level();
      setTimeout(crowd, 0);

      /* ---- two-way highlight with register rows ---- */
      function hi(no, on) {
        var row = document.querySelector('[data-row][data-no="' + no + '"]');
        if (row) row.classList.toggle('lit', on);
        var el = host.querySelector('.wr-pin[data-no="' + no + '"]');
        if (el) { el.classList.toggle('lit', on); return; }
        /* Zoomed out there is no pin for this number — the area disc is
           standing in for it — so light the disc instead. Without this the
           whole point of a map beside a register (point at a row, see where it
           is) is dead until the reader has zoomed in twice. */
        var b = bubByArea[areaOfNo[no]];
        var bel = b && b.getElement && b.getElement();
        var span = bel && bel.querySelector('.wr-bub');
        if (span) span.classList.toggle('lit', on);
      }
      W.mapFocus = function (no, opening) {
        var m = byNo[no];
        if (!m) return;
        hi(no, true);
        if (opening) { map.setView(m.getLatLng(), Math.max(map.getZoom(), BREAK + 1), { animate: !W.reduce }); m.openPopup(); }
      };
      W.mapBlur = function (no) { hi(no, false); };

      /* ---- filtered search: show only the buildings still in the result set ----
         Called by core/search.js on every filter change. The map re-fits to what is
         left, so a neighbourhood filter actually flies the map to that neighbourhood
         rather than leaving the reader to find it. */
      var visible = null;
      function liveCount() {
        if (!W._wrHidden) return pts.length;
        return pts.filter(function (p) { return !W._wrHidden[p.no]; }).length;
      }
      W.mapSetVisible = function (nos) {
        visible = (nos && nos.length < pts.length) ? nos.slice() : null;
        var set = visible ? visible.reduce(function (o, n) { o[n] = 1; return o; }, {}) : null;
        W._wrHidden = set ? pts.reduce(function (o, p) { if (!set[p.no]) o[p.no] = 1; return o; }, {}) : null;

        /* area discs recount against the filtered set, and disappear when empty */
        bubbles.forEach(function (b) {
          var mine = pts.filter(function (p) { return p.area === b._wrArea && (!set || set[p.no]); });
          var el = b.getElement && b.getElement();
          var n = el && el.querySelector('.wr-bub i');
          if (n) n.textContent = mine.length;
          if (el) el.style.display = mine.length ? '' : 'none';
          b._wrCount = mine.length;
        });

        var live = pts.filter(function (p) { return !set || set[p.no]; });
        if (live.length) {
          map.fitBounds(L.latLngBounds(live.map(function (p) { return [p.lat, p.lng]; })), {
            padding: fitPad(), maxZoom: 15, animate: !W.reduce
          });
        }
        level();
        setTimeout(crowd, 0);
      };

      [].forEach.call(document.querySelectorAll('[data-row][data-no]'), function (r) {
        var no = r.dataset.no;
        r.addEventListener('mouseenter', function () { hi(no, true); });
        r.addEventListener('mouseleave', function () { hi(no, false); });
        r.addEventListener('focusin', function () { hi(no, true); });
        r.addEventListener('focusout', function () { hi(no, false); });
      });

      /* scroll-wheel zoom only after a deliberate click, so the page still scrolls */
      map.on('click', function () { map.scrollWheelZoom.enable(); });
      map.on('mouseout', function () { map.scrollWheelZoom.disable(); });

      host.dataset.ready = '1';
      W.mapInstance = map;
      /* A search page hydrates its filters from the URL before the map exists, so the
         first apply() cannot reach it. Re-run it now that it can. */
      if (W.searchApply) W.searchApply(false);
      if (opts.onReady) opts.onReady(map, L);
    }).catch(function () {
      note.remove();
      host.classList.add('wr-map-fallback');
      if (W.atlas) W.atlas({ el: opts.el, points: opts.points });
    });

    function popupHTML(p) {
      var bits = [];
      if (p.beds) bits.push(esc(p.beds));
      if (p.rent) bits.push(esc(p.rent));
      return '' +
        (p.img ? '<a class="wr-pop-img" href="' + esc(p.url) + '"><img src="' + esc(p.img) + '" alt="" loading="lazy"></a>' : '') +
        '<div class="wr-pop-b">' +

        '<a class="wr-pop-nm" href="' + esc(p.url) + '">' + esc(p.name) + '</a>' +
        '<span class="wr-pop-st">' + esc(p.street || '') + (p.areaLabel ? ' · ' + esc(p.areaLabel) : '') + '</span>' +
        (bits.length ? '<span class="wr-pop-fx">' + bits.join(' · ') + '</span>' : '') +
        '</div>';
    }
  };
})();
