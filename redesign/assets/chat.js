/* Motor Tides — Leasing Concierge chat widget
   Self-contained. Themed via CSS custom properties on :root:
   --mtc-accent, --mtc-accent-ink, --mtc-surface, --mtc-ink, --mtc-muted,
   --mtc-bubble-bot, --mtc-bubble-user, --mtc-bubble-user-ink, --mtc-radius, --mtc-font

   Launcher variants (window.MTC_VARIANT or ?chat= URL param):
     "minimal" (default) — round chat-bubble button
     "logo"              — the Wiseman three-bars mark; bars rise like the tide
     "agent"             — a human leasing-agent photo with an online dot
     "robot"             — a calm concierge robot with blinking eyes
     "lighthouse"        — "Beacon", a smiling lighthouse with a sweeping gold light
     "buddy"             — "Chatty", a chat-bubble character whose eyes follow the cursor
     "pill"              — a labeled pill: chat icon + "Chat with us"
*/
(function () {
  'use strict';

  var THEME = {
    accent: 'var(--mtc-accent, #0E6B72)',
    accentInk: 'var(--mtc-accent-ink, #ffffff)',
    surface: 'var(--mtc-surface, #ffffff)',
    ink: 'var(--mtc-ink, #17272b)',
    muted: 'var(--mtc-muted, #6b7c80)',
    bubbleBot: 'var(--mtc-bubble-bot, #eef3f3)',
    bubbleUser: 'var(--mtc-bubble-user, #0E6B72)',
    bubbleUserInk: 'var(--mtc-bubble-user-ink, #ffffff)',
    radius: 'var(--mtc-radius, 20px)',
    font: 'var(--mtc-font, inherit)'
  };

  // ---------- variant resolution (allowlisted) ----------
  var variant = '';
  try { variant = new URLSearchParams(location.search).get('chat') || ''; } catch (e) {}
  variant = variant || window.MTC_VARIANT || 'minimal';
  if (variant === 'bubble') variant = 'minimal';
  if (variant === 'pet' || variant === 'mascot' || variant === 'wave') variant = 'logo';
  if (variant === 'beacon') variant = 'lighthouse';
  if (variant === 'eyes' || variant === 'face' || variant === 'chatty') variant = 'buddy';
  if (variant === 'human' || variant === 'maya' || variant === 'photo') variant = 'agent';
  if (variant === 'label' || variant === 'text') variant = 'pill';
  if (!/^(minimal|robot|lighthouse|buddy|logo|agent|pill)$/.test(variant)) variant = 'minimal';

  var REDUCED = false;
  try { REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  var FINE_POINTER = false;
  try { FINE_POINTER = matchMedia('(pointer: fine)').matches; } catch (e) {}

  var APPLY_URL = 'https://motortides-wisemanresidential.securecafe.com/onlineleasing/motor-tabor-by-wiseman/guestlogin.aspx';
  var TEL = 'tel:+12132869912';
  var TEL_LABEL = '(213) 286-9912';

  var STYLE = [
    '.mtc-root{--_a:' + THEME.accent + ';--_ai:' + THEME.accentInk + ';--_s:' + THEME.surface + ';--_i:' + THEME.ink + ';--_m:' + THEME.muted + ';--_bb:' + THEME.bubbleBot + ';--_bu:' + THEME.bubbleUser + ';--_bui:' + THEME.bubbleUserInk + ';--_r:' + THEME.radius + ';font-family:' + THEME.font + ';position:fixed;z-index:9999;bottom:0;right:0;pointer-events:none;font-size:15px;line-height:1.45;-webkit-font-smoothing:antialiased}',
    '.mtc-root *{box-sizing:border-box;margin:0;padding:0}',

    /* ---------- launcher: shared ---------- */
    '.mtc-launch{pointer-events:auto;position:fixed;right:22px;bottom:calc(22px + env(safe-area-inset-bottom,0px));border:0;cursor:pointer;background:none;padding:0;display:flex;align-items:flex-end;justify-content:flex-end;min-width:48px;min-height:48px}',
    '.mtc-badge{position:absolute;min-width:20px;height:20px;border-radius:10px;background:#e2554a;color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;padding:0 5px;border:2px solid var(--_s);opacity:0;transform:scale(.5);transition:.25s;pointer-events:none;z-index:3}',
    '.mtc-badge.show{opacity:1;transform:scale(1)}',

    /* minimal variant */
    '.mtc-v-minimal .mtc-launch,.mtc-v-logo .mtc-launch{width:60px;height:60px;border-radius:50%;background:var(--_a);color:var(--_ai);align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(7,45,48,.35),0 2px 8px rgba(7,45,48,.28);transition:transform .25s cubic-bezier(.34,1.56,.64,1)}',
    '@media (hover:hover) and (pointer:fine){.mtc-v-minimal .mtc-launch:hover,.mtc-v-logo .mtc-launch:hover{transform:scale(1.07)}}',
    '.mtc-v-minimal .mtc-launch>svg,.mtc-v-logo .mtc-launch>svg{width:26px;height:26px;transition:opacity .18s,transform .25s}',
    '.mtc-v-minimal .mtc-launch .mtc-ico-x,.mtc-v-logo .mtc-launch .mtc-ico-x{position:absolute;opacity:0;transform:rotate(-45deg) scale(.6)}',
    '.mtc-v-minimal.open .mtc-launch .mtc-ico-chat,.mtc-v-logo.open .mtc-launch .mtc-ico-chat{opacity:0;transform:rotate(30deg) scale(.6)}',
    '.mtc-v-minimal.open .mtc-launch .mtc-ico-x,.mtc-v-logo.open .mtc-launch .mtc-ico-x{opacity:1;transform:rotate(0) scale(1)}',
    '.mtc-v-minimal .mtc-badge,.mtc-v-logo .mtc-badge,.mtc-v-agent .mtc-badge{top:-2px;right:-2px}',

    /* pill variant: icon + label, morphs to a round close button when open */
    '.mtc-v-pill .mtc-launch{height:56px;max-width:300px;border-radius:999px;background:var(--_a);color:var(--_ai);align-items:center;justify-content:center;gap:10px;padding:0 22px 0 18px;box-shadow:0 10px 30px rgba(7,45,48,.35),0 2px 8px rgba(7,45,48,.28);transition:transform .25s cubic-bezier(.34,1.56,.64,1),padding .3s cubic-bezier(.22,1,.36,1),gap .3s cubic-bezier(.22,1,.36,1),max-width .3s cubic-bezier(.22,1,.36,1)}',
    '@media (hover:hover) and (pointer:fine){.mtc-v-pill .mtc-launch:hover{transform:scale(1.05)}}',
    '.mtc-pill-ico{position:relative;width:22px;height:22px;flex:none;display:block}',
    '.mtc-pill-ico svg{position:absolute;inset:0;width:22px;height:22px;transition:opacity .18s,transform .25s}',
    '.mtc-pill-ico .mtc-ico-x{opacity:0;transform:rotate(-45deg) scale(.6)}',
    '.mtc-v-pill.open .mtc-pill-ico .mtc-ico-chat{opacity:0;transform:rotate(30deg) scale(.6)}',
    '.mtc-v-pill.open .mtc-pill-ico .mtc-ico-x{opacity:1;transform:rotate(0) scale(1)}',
    '.mtc-pill-label{font-size:15px;font-weight:700;letter-spacing:.01em;white-space:nowrap;max-width:140px;overflow:hidden;transition:max-width .3s cubic-bezier(.22,1,.36,1),opacity .2s}',
    '.mtc-v-pill.open .mtc-launch{max-width:56px;width:56px;padding:0;gap:0}',
    '.mtc-v-pill.open .mtc-pill-label{max-width:0;opacity:0}',
    '.mtc-v-pill .mtc-badge{top:-5px;right:-3px}',
    '.mtc-v-pill.mtc-enter .mtc-launch{animation:mtcPillIn .6s cubic-bezier(.22,1,.36,1) both}',
    '@keyframes mtcPillIn{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}',
    '.mtc-v-pill.mtc-pulse .mtc-launch{animation:mtcPillNudge .9s ease-in-out 2}',
    '@keyframes mtcPillNudge{0%,100%{transform:translateY(0)}40%{transform:translateY(-5px)}}',

    /* character variants: transparent button holding artwork + swap-in close disc */
    '.mtc-v-robot .mtc-launch,.mtc-v-buddy .mtc-launch{width:76px;height:84px}',
    '.mtp-l,.mtp-r{transition:transform .18s ease-out;will-change:transform}',

    /* lighthouse: disc drawn inside the SVG so the light beams overflow the circle */
    '.mtc-v-lighthouse .mtc-launch{width:84px;height:84px}',
    '.mtc-v-lighthouse .mtc-art{filter:drop-shadow(0 8px 16px rgba(7,45,48,.28))}',
    '.mtc-v-lighthouse .mtc-x-alt{right:8px;bottom:8px}',
    '.mtc-v-lighthouse .mtc-badge{top:6px;right:4px}',
    '.mtl-bl{transform-box:fill-box;transform-origin:100% 50%;animation:mtlBeam 3.6s ease-in-out infinite}',
    '.mtl-br{transform-box:fill-box;transform-origin:0% 50%;animation:mtlBeam 3.6s ease-in-out -1.8s infinite}',
    '@keyframes mtlBeam{0%,100%{opacity:.16;transform:scaleX(.88)}50%{opacity:.6;transform:scaleX(1)}}',
    '.mtc-art{position:absolute;inset:0;pointer-events:none;color:var(--_a);transition:opacity .28s,transform .32s cubic-bezier(.22,1,.36,1)}',
    '.mtc-art svg{width:100%;height:100%;display:block;pointer-events:none}',
    '.mtc-art *{pointer-events:none}',
    '.mtc-root.open .mtc-art{opacity:0;transform:translateY(12px) scale(.55)}',
    '.mtc-x-alt{position:absolute;right:0;bottom:0;width:48px;height:48px;border-radius:50%;background:var(--_a);color:var(--_ai);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(7,45,48,.35);opacity:0;transform:scale(.4) rotate(-45deg);transition:.28s cubic-bezier(.22,1,.36,1);pointer-events:none}',
    '.mtc-x-alt svg{width:19px;height:19px}',
    '.mtc-root.open .mtc-x-alt{opacity:1;transform:scale(1) rotate(0)}',
    '.mtc-v-robot .mtc-badge,.mtc-v-buddy .mtc-badge{top:2px;right:0}',

    /* entrance: drop in, one landing compression, settle */
    '.mtc-enter .mtc-art{animation:mtcDrop .7s cubic-bezier(.22,1,.36,1) both}',
    '@keyframes mtcDrop{0%{opacity:0;transform:translateY(-26px)}55%{opacity:1;transform:translateY(2px)}75%{transform:translateY(0) scale(1.04,.95)}100%{transform:none}}',

    /* idle bob: gentle, killed after first open, paused on hidden tab */
    '.mtc-idle .mtx-all{animation:mtcBob 4.6s ease-in-out infinite}',
    '@keyframes mtcBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2.5px)}}',
    '.mtc-root.tab-hidden .mtc-art *{animation-play-state:paused!important}',
    '.mtc-root.was-opened .mtx-all{animation:none}',
    '.mtc-root.was-opened .mtl-bl,.mtc-root.was-opened .mtl-br{animation:none;opacity:.3}',

    /* face bits: blink, glance (JS-scheduled) */
    '.mtx-eyes{transform-box:fill-box;transform-origin:50% 50%;transition:transform .12s ease}',
    '.mtc-blink .mtx-eyes{transform:scaleY(.08)}',
    '.mtx-pupils{transform:translateX(0);transition:transform .5s cubic-bezier(.22,1,.36,1)}',
    '.mtc-glance-l .mtx-pupils{transform:translateX(-2.4px)}',
    '.mtc-glance-r .mtx-pupils{transform:translateX(2.4px)}',

    /* mascot squish: body around lower center, face counter-transformed, shadow widens */
    '.mtx-body{transform-box:fill-box;transform-origin:50% 85%;transition:transform .22s cubic-bezier(.34,1.56,.64,1)}',
    '.mtx-face{transform-box:fill-box;transform-origin:50% 60%;transition:transform .22s cubic-bezier(.34,1.56,.64,1)}',
    '.mtx-shadow{transform-box:fill-box;transform-origin:50% 50%;transition:transform .22s ease}',
    '@media (hover:hover) and (pointer:fine){',
    '.mtc-launch:hover .mtx-body{transform:translateY(2px) scale(1.07,.94)}',
    '.mtc-launch:hover .mtx-face{transform:scale(.96,1.035)}',
    '.mtc-launch:hover .mtx-shadow{transform:scaleX(1.14)}',
    '}',
    '.mtc-launch:active .mtx-body{transform:translateY(2px) scale(1.07,.94)}',

    /* logo variant: the three bars rise like the tide on entrance, ripple on pulse */
    '.mtc-v-logo .mtc-launch>svg.mtc-logo-mark{width:30px;height:30px}',
    '.mtb{transform-box:fill-box}',
    '.mtc-enter .mtb{animation:mtbRise .6s cubic-bezier(.22,1,.36,1) both}',
    '.mtc-enter .mtb-2{animation-delay:.09s}',
    '.mtc-enter .mtb-3{animation-delay:.18s}',
    '@keyframes mtbRise{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}',
    '.mtc-pulse .mtb-1{animation:mtbTide 1.1s ease-in-out 1}',
    '.mtc-pulse .mtb-2{animation:mtbTide 1.1s ease-in-out .12s 1}',
    '.mtc-pulse .mtb-3{animation:mtbTide 1.1s ease-in-out .24s 1}',
    '@keyframes mtbTide{0%,100%{transform:translateY(0)}35%{transform:translateY(-4px)}}',

    /* agent variant: human photo in a ring with an online dot */
    '.mtc-v-agent .mtc-launch{width:62px;height:62px}',
    '.mtc-v-agent .mtc-art{border-radius:50%;overflow:hidden;border:2.5px solid var(--_s);box-shadow:0 10px 30px rgba(7,45,48,.35),0 2px 8px rgba(7,45,48,.25);background:var(--_bb)}',
    '.mtc-v-agent .mtc-art img{width:100%;height:100%;object-fit:cover;display:block}',
    '.mtc-agent-dot{position:absolute;right:1px;bottom:1px;width:13px;height:13px;border-radius:50%;background:#3ddc84;border:2.5px solid var(--_s);z-index:2;pointer-events:none;transition:opacity .25s}',
    '.mtc-root.open .mtc-agent-dot{opacity:0}',
    '.mtc-v-agent .mtc-x-alt{right:7px;bottom:7px}',
    '.mtc-pulse .mtc-agent-dot{animation:mtcPing 1.5s ease-out 2}',
    '@keyframes mtcPing{0%{box-shadow:0 0 0 0 rgba(61,220,132,.55)}100%{box-shadow:0 0 0 9px rgba(61,220,132,0)}}',

    /* robot antenna: soft pulse, JS-scheduled (never a fast flash) */
    '.mtx-tip{transform-box:fill-box;transform-origin:50% 50%}',
    '.mtc-pulse .mtx-tip{animation:mtcPulse 1.8s ease-in-out 1}',
    '@keyframes mtcPulse{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.3)}}',

    /* ---------- teaser: stacked ABOVE the launcher, right-aligned ---------- */
    '.mtc-teaser{pointer-events:none;visibility:hidden;position:fixed;right:22px;bottom:calc(94px + env(safe-area-inset-bottom,0px));width:min(280px,calc(100vw - 32px));background:var(--_s);color:var(--_i);border-radius:16px;box-shadow:0 12px 40px rgba(10,40,44,.22);padding:13px 16px;font-size:13.5px;opacity:0;transform:translateY(8px);transition:.35s cubic-bezier(.22,1,.36,1);cursor:pointer;border:1px solid color-mix(in srgb, var(--mtc-ink, #16323a) 9%, transparent)}',
    '.mtc-v-robot .mtc-teaser,.mtc-v-buddy .mtc-teaser{bottom:calc(118px + env(safe-area-inset-bottom,0px))}',
    '.mtc-v-lighthouse .mtc-teaser{bottom:calc(122px + env(safe-area-inset-bottom,0px))}',
    '.mtc-teaser.show{opacity:1;transform:translateY(0);visibility:visible;pointer-events:auto}',
    '.mtc-teaser b{display:block;margin-bottom:2px}',
    '.mtc-teaser .mtc-teaser-x{position:absolute;top:-8px;left:-8px;width:22px;height:22px;border-radius:50%;background:var(--_i);color:var(--_s);border:0;font-size:11px;cursor:pointer;line-height:1}',

    /* ---------- panel ---------- */
    '.mtc-panel{pointer-events:auto;position:fixed;right:22px;bottom:calc(96px + env(safe-area-inset-bottom,0px));width:378px;max-width:calc(100vw - 32px);height:min(600px,calc(100dvh - 130px));background:var(--_s);color:var(--_i);border-radius:var(--_r);box-shadow:0 24px 80px rgba(8,40,44,.35),0 4px 16px rgba(8,40,44,.18);display:flex;flex-direction:column;overflow:hidden;opacity:0;transform:translateY(16px) scale(.98);visibility:hidden;transition:.32s cubic-bezier(.22,1,.36,1)}',
    '.mtc-v-robot .mtc-panel,.mtc-v-buddy .mtc-panel{bottom:calc(112px + env(safe-area-inset-bottom,0px))}',
    '.mtc-root.open .mtc-panel{opacity:1;transform:none;visibility:visible}',
    '.mtc-head{background:var(--_a);color:var(--_ai);padding:16px 18px;display:flex;align-items:center;gap:12px;flex:none}',
    '.mtc-ava{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.16);display:flex;align-items:center;justify-content:center;flex:none;position:relative;overflow:hidden}',
    '.mtc-ava svg{width:20px;height:20px}',
    '.mtc-ava.mtc-ava-art svg{width:30px;height:30px;margin-top:6px}',
    '.mtc-head-t b{display:block;font-size:15px;letter-spacing:.01em}',
    '.mtc-head-t span{font-size:12px;opacity:.82;display:flex;align-items:center;gap:5px}',
    '.mtc-head-t span::before{content:"";width:7px;height:7px;border-radius:50%;background:#3ddc84}',
    '.mtc-close{margin-left:auto;background:none;border:0;color:var(--_ai);opacity:.75;cursor:pointer;font-size:20px;padding:4px;line-height:1}',
    '.mtc-close:hover{opacity:1}',
    '.mtc-body{flex:1;overflow-y:auto;padding:18px 16px 8px;display:flex;flex-direction:column;gap:4px;scroll-behavior:smooth;background:linear-gradient(color-mix(in srgb,var(--_s) 96%,var(--_a) 4%),var(--_s))}',
    '.mtc-day{align-self:center;font-size:11px;color:var(--_m);letter-spacing:.08em;text-transform:uppercase;margin:2px 0 10px}',
    '.mtc-row{display:flex;gap:9px;margin:3px 0;align-items:flex-end;animation:mtcIn .3s cubic-bezier(.22,1,.36,1)}',
    '@keyframes mtcIn{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}',
    '.mtc-row.user{flex-direction:row-reverse}',
    '.mtc-row .mtc-mava{width:26px;height:26px;border-radius:50%;background:var(--_a);color:var(--_ai);display:flex;align-items:center;justify-content:center;flex:none;margin-bottom:16px;overflow:hidden}',
    '.mtc-row .mtc-mava svg{width:13px;height:13px}',
    '.mtc-row .mtc-mava.mtc-ava-art svg{width:20px;height:20px;margin-top:4px}',
    '.mtc-msg{max-width:76%}',
    '.mtc-bub{padding:10px 14px;border-radius:16px 16px 16px 5px;background:var(--_bb);color:var(--_i);font-size:14px;white-space:pre-line;overflow-wrap:break-word}',
    '.mtc-row.user .mtc-bub{background:var(--_bu);color:var(--_bui);border-radius:16px 16px 5px 16px}',
    '.mtc-time{font-size:10.5px;color:var(--_m);margin:3px 6px 0;display:block}',
    '.mtc-row.user .mtc-time{text-align:right}',
    '.mtc-typing{display:inline-flex;gap:4px;padding:13px 15px;border-radius:16px 16px 16px 5px;background:var(--_bb)}',
    '.mtc-typing i{width:7px;height:7px;border-radius:50%;background:var(--_m);animation:mtcB 1.1s infinite}',
    '.mtc-typing i:nth-child(2){animation-delay:.15s}.mtc-typing i:nth-child(3){animation-delay:.3s}',
    '@keyframes mtcB{0%,60%,100%{transform:none;opacity:.45}30%{transform:translateY(-5px);opacity:1}}',
    '.mtc-chips{display:flex;flex-wrap:wrap;gap:7px;margin:8px 0 10px;padding-left:35px;animation:mtcIn .3s .05s both}',
    '.mtc-chip{border:1.5px solid color-mix(in srgb,var(--_a) 55%,transparent);background:transparent;color:var(--_a);border-radius:999px;padding:7px 14px;font-size:13px;font-weight:600;cursor:pointer;transition:.16s;font-family:inherit}',
    '.mtc-chip:hover{background:var(--_a);color:var(--_ai)}',
    '.mtc-card{background:var(--_bb);border-radius:14px;padding:12px 14px;margin-top:6px;font-size:13.5px}',
    '.mtc-card b{font-size:14px}',
    '.mtc-card .mtc-price{float:right;font-weight:700;color:var(--_a)}',
    '.mtc-card small{color:var(--_m)}',
    '.mtc-linkbtn{display:inline-block;margin:8px 6px 2px 0;background:var(--_a);color:var(--_ai)!important;text-decoration:none;font-weight:700;font-size:13px;padding:9px 16px;border-radius:999px;transition:.16s}',
    '.mtc-linkbtn:hover{filter:brightness(1.12)}',
    '.mtc-linkbtn.ghost{background:transparent;color:var(--_a)!important;border:1.5px solid color-mix(in srgb,var(--_a) 55%,transparent)}',
    '.mtc-foot{flex:none;display:flex;gap:8px;padding:12px 14px;border-top:1px solid color-mix(in srgb, var(--mtc-ink, #16323a) 10%, transparent);background:var(--_s)}',
    '.mtc-in{flex:1;border:1.5px solid color-mix(in srgb, var(--mtc-ink, #16323a) 18%, transparent);background:transparent;color:var(--_i);border-radius:999px;padding:10px 16px;font-size:14px;font-family:inherit;outline:none;transition:border-color .16s}',
    '.mtc-in:focus{border-color:var(--_a)}',
    '.mtc-in::placeholder{color:var(--_m)}',
    '.mtc-send{width:42px;height:42px;border-radius:50%;border:0;background:var(--_a);color:var(--_ai);cursor:pointer;display:flex;align-items:center;justify-content:center;flex:none;transition:.16s}',
    '.mtc-send:hover{filter:brightness(1.12)}',
    '.mtc-send svg{width:17px;height:17px}',
    '.mtc-pow{flex:none;text-align:center;font-size:10px;color:var(--_m);padding:0 0 8px;background:var(--_s)}',
    '.mtc-by{display:block;margin-top:3px;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;opacity:.9}',
    '.mtc-by b{font-weight:700;color:var(--_a)}',
    '@media (max-width:560px){.mtc-panel{right:0;left:0;bottom:0!important;width:100%;max-width:100%;height:min(88dvh,640px);border-radius:var(--_r) var(--_r) 0 0}.mtc-launch{right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px))}.mtc-root.open .mtc-launch{opacity:0;pointer-events:none;transition:opacity .2s;animation:none}.mtc-teaser{right:16px;bottom:calc(86px + env(safe-area-inset-bottom,0px))}.mtc-v-robot .mtc-launch,.mtc-v-buddy .mtc-launch{width:64px;height:70px}.mtc-v-robot .mtc-teaser,.mtc-v-buddy .mtc-teaser{right:16px;bottom:calc(96px + env(safe-area-inset-bottom,0px))}.mtc-v-lighthouse .mtc-launch{width:72px;height:72px}.mtc-v-lighthouse .mtc-teaser{right:16px;bottom:calc(100px + env(safe-area-inset-bottom,0px))}}',
    '@media (prefers-reduced-motion: reduce){.mtc-root *{animation:none!important;transition-duration:.01ms!important}.mtc-panel{transition:none!important}}'
  ].join('\n');

  var BARS = '<svg viewBox="0 0 100 100" fill="currentColor" aria-hidden="true"><polygon points="14,18 34,18 34,74 14,80"/><polygon points="40,18 60,18 60,71 40,77"/><polygon points="66,18 86,18 86,68 66,74"/></svg>';
  var ICO_CHAT = '<svg class="mtc-ico-chat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';
  var ICO_X = '<svg class="mtc-ico-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  var ICO_X_PLAIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  var ICO_SEND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/></svg>';

  /* "Tidey" — teal wave-blob mascot. Layers back-to-front:
     shadow / body(+crest) / highlight / face(eyes,pupils,cheeks,mouth) / front fin arm */
  /* Logo mark — the Wiseman three bars with per-bar animation classes */
  var LOGO_MARK = '<svg class="mtc-ico-chat mtc-logo-mark" viewBox="0 0 100 100" fill="currentColor" aria-hidden="true">' +
    '<polygon class="mtb mtb-1" points="14,18 34,18 34,74 14,80"/>' +
    '<polygon class="mtb mtb-2" points="40,18 60,18 60,71 40,77"/>' +
    '<polygon class="mtb mtb-3" points="66,18 86,18 86,68 66,74"/></svg>';

  /* Agent — a human leasing-agent portrait (demo photo; swap for the real team) */
  var AGENT_PHOTO = 'https://randomuser.me/api/portraits/women/65.jpg';
  var ART_AGENT = '<img src="' + AGENT_PHOTO + '" alt="">';
  var AVA_AGENT = '<img src="' + AGENT_PHOTO + '" alt="" style="width:100%;height:100%;object-fit:cover">';

  /* "Chatty" — a living chat bubble with big googly eyes that follow the
     cursor (fine pointers only; falls back to random glances on touch). */
  var ART_BUDDY =
    '<svg viewBox="0 0 96 96" aria-hidden="true" focusable="false">' +
      '<ellipse class="mtx-shadow" cx="48" cy="91" rx="24" ry="4" fill="rgba(10,30,33,.28)"/>' +
      '<g class="mtx-all"><g class="mtx-body">' +
        '<path fill="currentColor" d="M30 14 h36 a20 20 0 0 1 20 20 v18 a20 20 0 0 1 -20 20 h-8 l6 14 -18 -14 h-16 a20 20 0 0 1 -20 -20 v-18 a20 20 0 0 1 20 -20 Z"/>' +
        '<ellipse cx="27" cy="26" rx="9" ry="5.5" fill="rgba(255,255,255,.18)" transform="rotate(-18 27 26)"/>' +
        '<g class="mtx-face">' +
          '<g class="mtx-eyes">' +
            '<ellipse cx="34" cy="42" rx="9.5" ry="10.5" fill="#fff"/>' +
            '<ellipse cx="62" cy="42" rx="9.5" ry="10.5" fill="#fff"/>' +
            '<g class="mtx-pupils">' +
              '<g class="mtp-l"><circle cx="34" cy="44" r="4.4" fill="#132A2D"/><circle cx="35.6" cy="42.2" r="1.4" fill="#fff"/></g>' +
              '<g class="mtp-r"><circle cx="62" cy="44" r="4.4" fill="#132A2D"/><circle cx="63.6" cy="42.2" r="1.4" fill="#fff"/></g>' +
            '</g>' +
          '</g>' +
          '<circle cx="24" cy="55" r="3.2" fill="rgba(255,255,255,.28)"/>' +
          '<circle cx="72" cy="55" r="3.2" fill="rgba(255,255,255,.28)"/>' +
          '<path d="M40 57 Q48 64 56 57" stroke="rgba(255,255,255,.95)" stroke-width="3" stroke-linecap="round" fill="none"/>' +
        '</g>' +
      '</g></g>' +
    '</svg>';

  /* "Beacon" — smiling lighthouse in a disc. Beams sweep alternately inside
     the launcher disc; gold lantern dome doubles as the pulse light (mtx-tip). */
  var ART_LIGHTHOUSE =
    '<svg viewBox="0 0 96 96" aria-hidden="true" focusable="false">' +
      '<g class="mtx-all">' +
        '<g class="mtl-disc">' +
          '<circle cx="48" cy="50" r="42" fill="#F6F0E2"/>' +
          '<circle cx="48" cy="50" r="41" fill="none" stroke="currentColor" stroke-width="2"/>' +
        '</g>' +
        '<g class="mtl-beams">' +
          '<polygon class="mtl-bl" points="43,15.5 4,5.5 4,30 43,22.5" fill="#E9C874"/>' +
          '<polygon class="mtl-br" points="53,15.5 92,5.5 92,30 53,22.5" fill="#E9C874"/>' +
        '</g>' +
        '<g class="mtx-body">' +
          '<circle cx="48" cy="7" r="1.7" fill="currentColor"/>' +
          '<line x1="48" y1="8.7" x2="48" y2="10.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' +
          '<path class="mtx-tip" d="M41.5 15.5 A6.5 6.5 0 0 1 54.5 15.5 Z" fill="#E9C874"/>' +
          '<rect x="42.5" y="15.5" width="11" height="5.5" fill="currentColor"/>' +
          '<rect x="45.6" y="16.6" width="4.8" height="3.4" rx="0.8" fill="#E9C874"/>' +
          '<rect x="39.5" y="21" width="17" height="3" rx="1.5" fill="currentColor"/>' +
          '<path fill="#FDFAF2" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" d="M42.5 24 L53.5 24 L58.8 76 L37.2 76 Z"/>' +
          '<polygon points="42.2,28 53.8,28 54.2,33 41.8,33" fill="currentColor"/>' +
          '<g class="mtx-face">' +
            '<g class="mtx-eyes"><g class="mtx-pupils">' +
              '<circle cx="44.6" cy="43" r="2.5" fill="#132A2D"/>' +
              '<circle cx="51.4" cy="43" r="2.5" fill="#132A2D"/>' +
              '<circle cx="45.4" cy="42.2" r="0.8" fill="#fff"/>' +
              '<circle cx="52.2" cy="42.2" r="0.8" fill="#fff"/>' +
            '</g></g>' +
            '<circle cx="41.6" cy="48" r="1.7" fill="rgba(255,130,120,.45)"/>' +
            '<circle cx="54.4" cy="48" r="1.7" fill="rgba(255,130,120,.45)"/>' +
            '<path d="M45.2 48.6 Q48 51 50.8 48.6" stroke="#132A2D" stroke-width="2" stroke-linecap="round" fill="none"/>' +
          '</g>' +
          '<polygon points="39.4,57 56.6,57 57.3,64 38.7,64" fill="currentColor"/>' +
          '<rect x="33.5" y="76" width="29" height="9" rx="4.5" fill="currentColor"/>' +
        '</g>' +
      '</g>' +
    '</svg>';

  /* Concierge robot — calm, architectural. Rounded head, face plate with the
     Wiseman three-bars etched above two blinking eyes; single soft antenna light. */
  var ART_ROBOT =
    '<svg viewBox="0 0 96 104" aria-hidden="true" focusable="false">' +
      '<ellipse class="mtx-shadow" cx="48" cy="98" rx="26" ry="4.5" fill="rgba(10,30,33,.28)"/>' +
      '<g class="mtx-all"><g class="mtx-body">' +
        '<line x1="48" y1="22" x2="48" y2="13" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>' +
        '<circle class="mtx-tip" cx="48" cy="10" r="4" fill="#FFD97A" opacity=".55"/>' +
        '<rect x="10" y="42" width="7" height="18" rx="3.5" fill="currentColor" opacity=".75"/>' +
        '<rect x="79" y="42" width="7" height="18" rx="3.5" fill="currentColor" opacity=".75"/>' +
        '<rect x="16" y="22" width="64" height="58" rx="18" fill="currentColor"/>' +
        '<rect x="23" y="30" width="50" height="42" rx="12" fill="rgba(255,255,255,.92)"/>' +
        '<g fill="currentColor" opacity=".8" transform="translate(41.5,34) scale(.13)">' +
          '<polygon points="14,18 34,18 34,74 14,80"/><polygon points="40,18 60,18 60,71 40,77"/><polygon points="66,18 86,18 86,68 66,74"/>' +
        '</g>' +
        '<g class="mtx-face">' +
          '<g class="mtx-eyes">' +
            '<g class="mtx-pupils">' +
              '<rect x="33" y="49" width="8" height="13" rx="4" fill="#132A2D"/>' +
              '<rect x="55" y="49" width="8" height="13" rx="4" fill="#132A2D"/>' +
            '</g>' +
          '</g>' +
          '<path d="M43 67 Q48 70.5 53 67" stroke="#132A2D" stroke-width="2.2" stroke-linecap="round" fill="none"/>' +
        '</g>' +
        '<rect x="34" y="80" width="28" height="9" rx="4.5" fill="currentColor" opacity=".85"/>' +
      '</g></g>' +
    '</svg>';

  var MINI_ROBOT = ART_ROBOT.replace('class="mtx-shadow"', 'class="mtx-shadow" opacity="0"');
  var MINI_LIGHTHOUSE = ART_LIGHTHOUSE.replace('class="mtl-beams"', 'class="mtl-beams" opacity="0"');
  var MINI_BUDDY = ART_BUDDY.replace('class="mtx-shadow"', 'class="mtx-shadow" opacity="0"');

  var AVA = variant === 'robot' ? MINI_ROBOT : variant === 'lighthouse' ? MINI_LIGHTHOUSE : variant === 'buddy' ? MINI_BUDDY : variant === 'agent' ? AVA_AGENT : BARS;
  var AVA_CLS = (variant === 'minimal' || variant === 'logo' || variant === 'agent' || variant === 'pill') ? '' : ' mtc-ava-art';

  var PLANS = [
    { n: 'Harbor', b: '2 bd · 2 ba', s: '722–754 sq ft', p: '$3,770', a: 4 },
    { n: 'Reef', b: '2 bd · 2 ba', s: '768 sq ft', p: '$3,845', a: 2 },
    { n: 'Pacific', b: '2 bd · 2 ba', s: '757 sq ft', p: '$3,895', a: 1 },
    { n: 'Lighthouse', b: '2 bd · 2 ba', s: '742–766 sq ft', p: '$3,950', a: 4 },
    { n: 'Seacliff', b: '2 bd · 2 ba', s: '895 sq ft', p: '$3,975', a: 2 },
    { n: 'Channel', b: '2 bd · 2 ba', s: '799 sq ft', p: '$4,095', a: 1 },
    { n: 'Coral', b: '3 bd · 2 ba', s: '876 sq ft', p: '$4,495', a: 5 }
  ];

  // ---------- widget scaffold ----------
  var launcherInner =
    variant === 'minimal' ? ICO_CHAT + ICO_X + '<span class="mtc-badge">1</span>'
    : variant === 'pill' ? '<span class="mtc-pill-ico">' + ICO_CHAT + ICO_X + '</span><span class="mtc-pill-label">Chat with us</span><span class="mtc-badge">1</span>'
    : variant === 'logo' ? LOGO_MARK + ICO_X + '<span class="mtc-badge">1</span>'
    : variant === 'agent'
      ? '<span class="mtc-art">' + ART_AGENT + '</span><span class="mtc-agent-dot"></span>' +
        '<span class="mtc-x-alt">' + ICO_X_PLAIN + '</span><span class="mtc-badge">1</span>'
      : '<span class="mtc-art">' + (variant === 'lighthouse' ? ART_LIGHTHOUSE : variant === 'buddy' ? ART_BUDDY : ART_ROBOT) + '</span>' +
        '<span class="mtc-x-alt">' + ICO_X_PLAIN + '</span>' +
        '<span class="mtc-badge">1</span>';

  var root = document.createElement('div');
  root.className = 'mtc-root mtc-v-' + variant + (REDUCED ? '' : ' mtc-enter mtc-idle');
  root.innerHTML =
    '<style>' + STYLE + '</style>' +
    '<div class="mtc-teaser" role="button" tabindex="0" aria-label="Open chat">' +
      '<button class="mtc-teaser-x" aria-label="Dismiss">&#10005;</button>' +
      '<b>Maya &middot; Motor Tides</b>Hi there! &#128075; Looking for pricing or a tour? I can help right now.' +
    '</div>' +
    '<div class="mtc-panel" id="mtc-panel" role="dialog" aria-label="Motor Tides leasing chat">' +
      '<div class="mtc-head">' +
        '<div class="mtc-ava' + AVA_CLS + '">' + AVA + '</div>' +
        '<div class="mtc-head-t"><b>Maya &middot; Leasing Concierge</b><span>Online &middot; replies instantly</span></div>' +
        '<button class="mtc-close" aria-label="Close chat">&#10005;</button>' +
      '</div>' +
      '<div class="mtc-body" aria-live="polite"></div>' +
      '<div class="mtc-foot">' +
        '<input class="mtc-in" type="text" placeholder="Ask about pricing, tours, pets&hellip;" aria-label="Type a message">' +
        '<button class="mtc-send" aria-label="Send">' + ICO_SEND + '</button>' +
      '</div>' +
      '<div class="mtc-pow">Motor Tides by Wiseman &middot; 3557 Motor Ave &middot; ' + TEL_LABEL +
        '<span class="mtc-by">Powered by <b>UnitPulse</b></span></div>' +
    '</div>' +
    '<button class="mtc-launch" aria-label="Chat with the leasing team" aria-expanded="false" aria-controls="mtc-panel">' + launcherInner + '</button>';

  function init() {
    document.body.appendChild(root);

    var body = root.querySelector('.mtc-body');
    var launch = root.querySelector('.mtc-launch');
    var teaser = root.querySelector('.mtc-teaser');
    var badge = root.querySelector('.mtc-badge');
    var input = root.querySelector('.mtc-in');
    var send = root.querySelector('.mtc-send');
    var closeB = root.querySelector('.mtc-close');
    var opened = false, greeted = false, busy = false;

    // ---------- character life (blink / glance / wave / antenna) ----------
    var timers = [];
    function later(fn, ms) { var t = setTimeout(fn, ms); timers.push(t); return t; }
    function stopLife() { timers.forEach(clearTimeout); timers = []; }
    function rand(a, b) { return a + Math.random() * (b - a); }

    if (variant !== 'minimal' && !REDUCED) {
      var flash = function (cls, dur) {
        root.classList.add(cls);
        later(function () { root.classList.remove(cls); }, dur);
      };
      var blinkLoop = function () {
        later(function () {
          if (opened) return;
          if (!document.hidden) {
            flash('mtc-blink', 150);
            if (Math.random() < 0.22) later(function () { flash('mtc-blink', 150); }, 260);
          }
          blinkLoop();
        }, rand(4000, 8000));
      };
      var glanceLoop = function () {
        later(function () {
          if (opened) return;
          if (!document.hidden) {
            flash(Math.random() < 0.5 ? 'mtc-glance-l' : 'mtc-glance-r', 1400);
          }
          glanceLoop();
        }, rand(9000, 16000));
      };
      // sequence: drop-in → settle → one expression, then calm idle
      later(function () {
        if (/^(logo|agent|robot|lighthouse|pill)$/.test(variant)) flash('mtc-pulse', 2400);
        if (variant === 'buddy') { flash('mtc-blink', 150); later(function () { flash('mtc-blink', 150); }, 280); }
      }, 850);
      // blink/glance apply only to the character variants with faces
      if (/^(robot|lighthouse|buddy)$/.test(variant)) later(blinkLoop, 2600);
      // buddy's eyes follow the cursor on fine pointers — random glances would fight it
      if (/^(robot|lighthouse)$/.test(variant) || (variant === 'buddy' && !FINE_POINTER)) later(glanceLoop, 5000);
      document.addEventListener('visibilitychange', function () {
        root.classList.toggle('tab-hidden', document.hidden);
      });
    }

    // "Chatty" eye tracking: pupils follow the cursor (rAF-throttled, fine pointers only)
    if (variant === 'buddy' && !REDUCED && FINE_POINTER) {
      var eyeRaf = 0, eyeX = 0, eyeY = 0;
      // scope to the launcher artwork — the panel avatar contains a mini
      // buddy with the same classes and sits earlier in the DOM
      var EYES = [['.mtc-art .mtp-l', 34, 44], ['.mtc-art .mtp-r', 62, 44]];
      var trackEyes = function () {
        eyeRaf = 0;
        var art = root.querySelector('.mtc-art');
        if (!art) return;
        var rect = art.getBoundingClientRect();
        if (!rect.width) return;
        var scale = rect.width / 96;
        EYES.forEach(function (e) {
          var el = root.querySelector(e[0]);
          if (!el) return;
          var cx = rect.left + e[1] * scale, cy = rect.top + e[2] * scale;
          var dx = eyeX - cx, dy = eyeY - cy;
          var d = Math.hypot(dx, dy) || 1;
          var reach = Math.min(1, d / 140) * 3.4; // svg units; full deflection past ~140px
          el.style.transform = 'translate(' + (dx / d * reach).toFixed(2) + 'px,' + (dy / d * reach).toFixed(2) + 'px)';
        });
      };
      document.addEventListener('mousemove', function (ev) {
        eyeX = ev.clientX; eyeY = ev.clientY;
        // cancel+reschedule so a swallowed frame (hidden tab) can never deadlock the tracker
        if (eyeRaf) cancelAnimationFrame(eyeRaf);
        eyeRaf = requestAnimationFrame(trackEyes);
      }, { passive: true });
      document.addEventListener('mouseleave', function () {
        EYES.forEach(function (e) { var el = root.querySelector(e[0]); if (el) el.style.transform = ''; });
      });
    }

    var day = document.createElement('div');
    day.className = 'mtc-day';
    day.textContent = new Date().toLocaleDateString([], { weekday: 'long', month: 'short', day: 'numeric' });
    body.appendChild(day);

    function now() { return new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }); }
    function scroll() { body.scrollTop = body.scrollHeight; }

    var MAVA = '<div class="mtc-mava' + AVA_CLS + '">' + AVA + '</div>';

    function addMsg(who, html, plain) {
      var row = document.createElement('div');
      row.className = 'mtc-row ' + who;
      row.innerHTML = (who === 'bot' ? MAVA : '') +
        '<div class="mtc-msg"><div class="mtc-bub"></div><span class="mtc-time">' + now() + '</span></div>';
      var bub = row.querySelector('.mtc-bub');
      if (plain) { bub.textContent = html; } else { bub.innerHTML = html; }
      body.appendChild(row); scroll();
      return row;
    }

    var typingEl = null;
    function showTyping() {
      hideTyping();
      typingEl = document.createElement('div');
      typingEl.className = 'mtc-row bot';
      typingEl.innerHTML = MAVA + '<div class="mtc-typing"><i></i><i></i><i></i></div>';
      body.appendChild(typingEl); scroll();
    }
    function hideTyping() { if (typingEl) { typingEl.remove(); typingEl = null; } }

    function bot(html, delay, plain) {
      busy = true;
      return new Promise(function (res) {
        setTimeout(function () { showTyping(); }, 260);
        setTimeout(function () {
          hideTyping(); addMsg('bot', html, plain); busy = false; res();
          if (!root.classList.contains('open')) { badge.classList.add('show'); }
        }, delay || 1050);
      });
    }

    var chipsEl = null;
    function chips(list) {
      clearChips();
      chipsEl = document.createElement('div');
      chipsEl.className = 'mtc-chips';
      list.forEach(function (c) {
        var b = document.createElement('button');
        b.className = 'mtc-chip'; b.type = 'button'; b.textContent = c.t;
        b.addEventListener('click', function () { clearChips(); addMsg('user', c.t, true); c.f(); });
        chipsEl.appendChild(b);
      });
      body.appendChild(chipsEl); scroll();
    }
    function clearChips() { if (chipsEl) { chipsEl.remove(); chipsEl = null; } }

    var MAIN_CHIPS = [
      { t: '💰 Pricing & availability', f: flowPricing },
      { t: '📅 Schedule a tour', f: flowTour },
      { t: '🐾 Pet policy', f: flowPets },
      { t: '✨ Amenities', f: flowAmenities },
      { t: '📍 Neighborhood', f: flowHood }
    ];
    function mainChips(extraDelay) {
      setTimeout(function () { chips(MAIN_CHIPS); }, extraDelay || 0);
    }

    // ---------- flows ----------
    function flowPricing() {
      bot('Great question — here’s what’s available right now at Motor Tides ⤵️', 900).then(function () {
        var cards = PLANS.map(function (p) {
          return '<div class="mtc-card"><span class="mtc-price">' + p.p + '+</span><b>' + p.n + '</b><br><small>' + p.b + ' &middot; ' + p.s + ' &middot; ' + p.a + ' available</small></div>';
        }).join('');
        return bot('<div>' + cards + '</div>', 1400);
      }).then(function () {
        return bot('Move-in specials are running on select homes right now &#127881; Want to lock one in?', 1100);
      }).then(function () {
        chips([
          { t: 'Apply online', f: flowApply },
          { t: 'Schedule a tour', f: flowTour },
          { t: 'What about utilities?', f: flowUtilities }
        ]);
      });
    }

    function flowTour() {
      bot('I’d love to show you around! We do in-person and virtual tours, 7 days a week. What works best?', 1000).then(function () {
        var days = [];
        var names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        for (var i = 0; i < 4; i++) {
          var d = new Date(); d.setDate(d.getDate() + i);
          var label = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : names[d.getDay()] + ' ' + (d.getMonth() + 1) + '/' + d.getDate();
          days.push({ t: label, f: pickTime(label) });
        }
        chips(days);
      });
    }
    function pickTime(dayLabel) {
      return function () {
        bot('Perfect — here’s what’s open ' + dayLabel.toLowerCase() + ':', 850).then(function () {
          chips(['11:00 AM', '1:30 PM', '3:00 PM', '5:15 PM'].map(function (t) {
            return { t: t, f: confirmTour(dayLabel, t) };
          }));
        });
      };
    }
    function confirmTour(dayLabel, time) {
      return function () {
        bot('You’re on the books ✨ <b>' + dayLabel + ' at ' + time + '</b> — tour of Motor Tides, 3557 Motor Ave.\n\nOur leasing team will call you shortly to confirm. Prefer to talk now?', 1250).then(function () {
          return bot('<a class="mtc-linkbtn" href="' + TEL + '">&#128222; Call ' + TEL_LABEL + '</a><a class="mtc-linkbtn ghost" href="' + APPLY_URL + '" target="_blank" rel="noopener">Start application</a>', 900);
        }).then(function () { mainChips(400); });
      };
    }

    function flowPets() {
      bot('Motor Tides is proudly pet-friendly &#128054;&#128049; Cats and dogs are both welcome — your best friend gets a rooftop with a view too.', 1100).then(function () {
        return bot('Breed and weight details are confirmed with the leasing team during application. Anything else?', 1000);
      }).then(function () { mainChips(); });
    }

    function flowAmenities() {
      bot('Here’s what life at Motor Tides comes with:\n\n&#127750; Rooftop deck with sweeping city views\n&#127947;️ Fitness center\n&#128054; Pet-friendly living\n&#9728;️ Private balconies & patios (most homes)\n&#128682; Controlled access + elevator\n&#128690; Steps from Ballona Creek Trail & the E Line', 1500).then(function () {
        return bot('Every residence has open layouts, quartz kitchens, stainless appliances, and huge windows. Want to see it in person?', 1150);
      }).then(function () {
        chips([{ t: 'Yes — schedule a tour', f: flowTour }, { t: 'Pricing first', f: flowPricing }]);
      });
    }

    function flowHood() {
      bot('You’re in one of LA’s most walkable pockets — the Motor Ave corridor on the Culver City border.', 1000).then(function () {
        return bot('&#9749; Mornings: Super Domestic Coffee, Destroyer, Love Yoga\n&#127863; Evenings: Hatchet Hall, Simonette, The Culver Hotel, Dear John’s\n&#127916; Nearby: Sony Pictures, Amazon MGM, Apple TV+ campus\n&#128649; Expo/Culver E Line a few minutes away', 1500);
      }).then(function () {
        return bot('Honestly, the rooftop sunset over the Westside might be the best amenity of all &#127751;', 950);
      }).then(function () { mainChips(); });
    }

    function flowApply() {
      bot('Amazing! Applications are online and take about 10 minutes. I’ll send you straight to our secure leasing portal:', 1000).then(function () {
        return bot('<a class="mtc-linkbtn" href="' + APPLY_URL + '" target="_blank" rel="noopener">Apply now &#8599;</a><a class="mtc-linkbtn ghost" href="' + TEL + '">Questions? ' + TEL_LABEL + '</a>', 850);
      }).then(function () { mainChips(400); });
    }

    function flowUtilities() {
      bot('Good to know upfront: utilities (trash, gas, electric, and water) are set up by the resident — so you control your own usage.', 1150).then(function () { mainChips(); });
    }

    function flowHours() {
      bot('The leasing office at 3557 Motor Ave is open:\n\nMon–Fri &middot; 9:30 AM – 6:30 PM\nSat–Sun &middot; 11 AM – 4 PM\n\nWalk-ins welcome, appointments preferred!', 1200).then(function () { mainChips(); });
    }

    function flowLocation() {
      bot('We’re at <b>3557 Motor Avenue, Los Angeles, CA 90034</b> — right where Palms meets Culver City.', 1000).then(function () {
        return bot('<a class="mtc-linkbtn" href="https://maps.google.com/?q=3557%20Motor%20Avenue%20Los%20Angeles,%20CA%2090034" target="_blank" rel="noopener">&#128205; Open in Maps</a>', 800);
      }).then(function () { mainChips(400); });
    }

    function flowParking() {
      bot('On-site garage parking is available — options and monthly rates are confirmed with the leasing team based on your home. Want me to set up a quick call?', 1200).then(function () {
        chips([{ t: '📞 Yes, call me', f: function () {
          bot('<a class="mtc-linkbtn" href="' + TEL + '">&#128222; Call ' + TEL_LABEL + '</a> or stop by — we’re open 7 days a week.', 900).then(function () { mainChips(400); });
        } }, { t: 'Schedule a tour instead', f: flowTour }]);
      });
    }

    function fallback() {
      bot('Great question! For anything detailed, our (human &#128522;) leasing team has the answer — they’re at ' + TEL_LABEL + ', open 7 days a week. Meanwhile, I can help with:', 1150).then(function () { mainChips(); });
    }

    // ---------- keyword router ----------
    function route(text) {
      var t = text.toLowerCase();
      if (/\b(price|pricing|cost|rent|how much|rate|special|deal|month)/.test(t)) return flowPricing;
      if (/\b(tour|visit|see|viewing|appointment|schedule|book|stop by|come in)/.test(t)) return flowTour;
      if (/\b(pet|dog|cat|puppy|kitten|animal)/.test(t)) return flowPets;
      if (/\b(park|garage|car|ev\b)/.test(t)) return flowParking;
      if (/\b(gym|fitness|amenit|roof|deck|pool|workout|feature)/.test(t)) return flowAmenities;
      if (/\b(neighborhood|area|restaurant|coffee|around|nearby|walk|metro|transit|studio)/.test(t)) return flowHood;
      if (/\b(apply|application|lease|leasing|sign|qualify|approve)/.test(t)) return flowApply;
      if (/\b(utilit|water|electric|gas|trash|internet|wifi)/.test(t)) return flowUtilities;
      if (/\b(hour|open|close|when|office)/.test(t)) return flowHours;
      if (/\b(where|address|location|directions|map)/.test(t)) return flowLocation;
      if (/\b(hi|hello|hey|hola|morning|afternoon)\b/.test(t)) return function () {
        bot('Hey! &#128075; Welcome to Motor Tides. What can I help with today?', 850).then(function () { mainChips(); });
      };
      if (/\b(thank|thanks|great|awesome|cool|perfect)/.test(t)) return function () {
        bot('Anytime! That’s what I’m here for &#127754; Anything else?', 850).then(function () { mainChips(); });
      };
      return fallback;
    }

    function userSend() {
      var text = input.value.trim();
      if (!text || busy) return;
      input.value = '';
      clearChips();
      addMsg('user', text, true);
      route(text)();
    }

    // ---------- open/close ----------
    function openPanel() {
      root.classList.add('open');
      root.classList.add('was-opened');
      root.classList.remove('mtc-idle');
      stopLife();
      teaser.classList.remove('show');
      badge.classList.remove('show');
      launch.setAttribute('aria-expanded', 'true');
      opened = true;
      if (!greeted) {
        greeted = true;
        bot('Welcome to <b>Motor Tides by Wiseman</b> &#127754; I’m Maya from the leasing team.', 900).then(function () {
          return bot('Brand-new 2 & 3 bedroom homes are open now on Motor Ave — from <b>$3,770/mo</b> with move-in specials. What would you like to explore?', 1250);
        }).then(function () { mainChips(); });
      }
      if (FINE_POINTER) setTimeout(function () { input.focus(); }, 350);
    }
    function closePanel() {
      root.classList.remove('open');
      launch.setAttribute('aria-expanded', 'false');
      launch.focus();
    }

    launch.addEventListener('click', function () { root.classList.contains('open') ? closePanel() : openPanel(); });
    closeB.addEventListener('click', closePanel);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && root.classList.contains('open')) closePanel(); });
    send.addEventListener('click', userSend);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') userSend(); });

    teaser.addEventListener('click', function (e) {
      if (e.target.classList.contains('mtc-teaser-x')) { teaser.classList.remove('show'); return; }
      openPanel();
    });
    teaser.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') openPanel(); });

    // ---------- soft teaser chime ----------
    // Browsers block audio until a user gesture (click/tap/keydown), so the
    // context is armed on first gesture; the chime stays silent otherwise.
    var audioCtx = null, chimePending = false;
    function armAudio() {
      try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      } catch (e) { return; }
      // Some browsers create the context suspended even inside a gesture —
      // resume() is async, so only stand down once it's actually running.
      var p = audioCtx.state === 'suspended' ? audioCtx.resume() : Promise.resolve();
      Promise.resolve(p).then(function () {
        if (!audioCtx || audioCtx.state !== 'running') return; // keep listening for the next gesture
        document.removeEventListener('pointerdown', armAudio);
        document.removeEventListener('keydown', armAudio);
        // teaser appeared while audio was locked — play now, while it's still on screen
        if (chimePending && !opened && teaser.classList.contains('show')) {
          chimePending = false;
          setTimeout(chime, 60);
        }
      }).catch(function () {});
    }
    document.addEventListener('pointerdown', armAudio, { passive: true });
    document.addEventListener('keydown', armAudio);
    function chime() {
      if (!audioCtx || audioCtx.state !== 'running') { chimePending = true; return; }
      try {
        var t = audioCtx.currentTime;
        [[740, 0], [988, 0.11]].forEach(function (n) {
          var o = audioCtx.createOscillator(), g = audioCtx.createGain();
          o.type = 'sine'; o.frequency.value = n[0];
          g.gain.setValueAtTime(0.0001, t + n[1]);
          g.gain.exponentialRampToValueAtTime(0.09, t + n[1] + 0.02);
          g.gain.exponentialRampToValueAtTime(0.0001, t + n[1] + 0.3);
          o.connect(g); g.connect(audioCtx.destination);
          o.start(t + n[1]); o.stop(t + n[1] + 0.32);
        });
      } catch (e) {}
    }

    // teaser + badge after a short delay, if user hasn't opened yet
    setTimeout(function () {
      if (!opened) {
        teaser.classList.add('show');
        badge.classList.add('show');
        chime();
        if (/^(logo|agent|robot|lighthouse|pill)$/.test(variant) && !REDUCED) {
          root.classList.add('mtc-pulse');
          later(function () { root.classList.remove('mtc-pulse'); }, 2400);
        }
        if (variant === 'buddy' && !REDUCED) {
          root.classList.add('mtc-blink');
          later(function () { root.classList.remove('mtc-blink'); }, 150);
          later(function () { root.classList.add('mtc-blink'); later(function () { root.classList.remove('mtc-blink'); }, 150); }, 300);
        }
      }
    }, 5200);
    setTimeout(function () { if (!opened) teaser.classList.remove('show'); }, 26000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
