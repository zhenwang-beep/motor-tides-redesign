/* Motor Midway — neighbourhood map.
 *
 * MapLibre GL over a Positron basemap retoned for this property
 * (assets/maps/midway-positron.json). Tiles, glyphs and sprites all come from
 * OpenFreeMap's public endpoints, so the map needs no key and no account.
 *
 * Coordinates are cached in the markup by the generator — there is no
 * client-side geocoding, so the pins cannot drift or rate-limit.
 *
 * If the library or the tiles fail to load, the list beside the map is the
 * real content and stays usable on its own; the canvas just says so rather
 * than sitting there blank.
 */
(function () {
  'use strict';

  var canvas = document.getElementById('map-canvas');
  if (!canvas) return;

  var items = [].slice.call(document.querySelectorAll('[data-place]'));
  var home = {
    lat: parseFloat(canvas.dataset.lat),
    lon: parseFloat(canvas.dataset.lon),
    label: canvas.dataset.label || ''
  };
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pins = new Map();
  var map = null;

  function fail(msg) {
    canvas.classList.add('map-failed');
    var p = document.createElement('p');
    p.className = 'map-fallback';
    p.textContent = msg;
    canvas.appendChild(p);
  }

  function pinEl(label, isHome) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'map-pin' + (isHome ? ' is-home' : '');
    b.setAttribute('aria-pressed', 'false');
    b.setAttribute('aria-label', label);
    b.innerHTML = isHome
      ? '<span class="map-home-mark" aria-hidden="true"></span>'
        + '<span class="map-home-label">' + label + '</span>'
      : '<span aria-hidden="true">' + (isHome ? '' : label) + '</span>';
    return b;
  }

  function select(item) {
    items.forEach(function (other) {
      var on = other === item;
      other.setAttribute('aria-current', on ? 'true' : 'false');
      var pin = pins.get(other);
      if (pin) pin.el.setAttribute('aria-pressed', String(on));
    });
    var pin = pins.get(item);
    if (pin && map) {
      map.easeTo({
        center: [pin.lon, pin.lat],
        zoom: Math.max(map.getZoom(), 14.4),
        duration: reduced ? 0 : 650
      });
    }
  }

  items.forEach(function (item) {
    item.addEventListener('click', function (e) {
      // the row is a button; let any real link inside it behave normally
      if (e.target.closest('a')) return;
      select(item);
    });
  });

  var resetBtn = document.getElementById('map-reset');
  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      items.forEach(function (i) { i.setAttribute('aria-current', 'false'); });
      pins.forEach(function (p) { p.el.setAttribute('aria-pressed', 'false'); });
      if (map) map.easeTo({ center: [home.lon, home.lat], zoom: 14.1,
                            duration: reduced ? 0 : 650 });
    });
  }

  function build() {
    if (!window.maplibregl) { fail('The map could not load. The places are listed beside it.'); return; }
    try {
      map = new maplibregl.Map({
        container: canvas,
        style: canvas.dataset.style,
        center: [home.lon, home.lat],
        zoom: 14.1,
        attributionControl: false,
        cooperativeGestures: true    // a page-scroll over the map scrolls the page
      });
    } catch (err) {
      fail('The map could not load. The places are listed beside it.');
      return;
    }

    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-left');
    // The style file already declares its own attribution, so adding a
    // customAttribution printed the same credits twice end to end.
    map.addControl(new maplibregl.AttributionControl({ compact: false }), 'bottom-right');

    map.on('error', function (e) {
      // a single missing tile is not worth a failure message
      if (e && e.error && /style|Failed to fetch/i.test(String(e.error.message || ''))) {
        fail('The map could not load. The places are listed beside it.');
      }
    });

    map.on('load', function () {
      canvas.classList.add('map-ready');

      var h = pinEl(home.label, true);
      new maplibregl.Marker({ element: h, anchor: 'bottom' })
        .setLngLat([home.lon, home.lat]).addTo(map);
      h.addEventListener('click', function () {
        map.easeTo({ center: [home.lon, home.lat], zoom: 15.4, duration: reduced ? 0 : 650 });
      });

      items.forEach(function (item) {
        var lat = parseFloat(item.dataset.lat), lon = parseFloat(item.dataset.lon);
        var el = pinEl(item.dataset.num, false);
        el.title = item.dataset.place;
        el.setAttribute('aria-label', item.dataset.place);
        new maplibregl.Marker({ element: el, anchor: 'center' })
          .setLngLat([lon, lat]).addTo(map);
        el.addEventListener('click', function () { select(item); item.focus(); });
        pins.set(item, { el: el, lat: lat, lon: lon });
      });

      // frame the building and everything pinned around it
      var b = new maplibregl.LngLatBounds([home.lon, home.lat], [home.lon, home.lat]);
      pins.forEach(function (p) { b.extend([p.lon, p.lat]); });
      map.fitBounds(b, { padding: { top: 70, bottom: 60, left: 70, right: 70 },
                         duration: 0, maxZoom: 15 });
    });
  }

  // MapLibre is loaded with `defer`, so it may or may not be ready yet.
  if (window.maplibregl) build();
  else {
    var s = document.getElementById('maplibre-js');
    if (!s) { fail('The map could not load. The places are listed beside it.'); return; }
    s.addEventListener('load', build);
    s.addEventListener('error', function () {
      fail('The map could not load. The places are listed beside it.');
    });
  }
})();
