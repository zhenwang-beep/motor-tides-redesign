# Build conventions — Wiseman Residential corporate site

Every item here cost a debugging session on the Motor Tides project. Read before writing a page.

## Layout

1. **`overflow-x: clip` on `html` and `body` — never `hidden`.** `overflow:hidden` on an ancestor
   creates a scroll container and silently kills `position: sticky`. Every pinned stage depends on it.
2. **Longhand padding on anything carrying `.wrap`.** The reset is `*{margin:0;padding:0}` and the
   gutter comes from `.wrap{padding-left:var(--pad);padding-right:var(--pad)}`. Writing
   `padding: 80px 0` on a `.wrap` element zeroes the gutter and the text runs to the viewport edge.
   Full-bleed sections use shorthand padding **plus a nested `<div class="wrap">`**.
3. **Every `100vh` needs an `svh` twin.** `--vh100:100vh` at `:root`, then
   `@supports (height:100svh){:root{--vh100:100svh}}`. Mobile URL-bar show/hide changes `vh` and
   makes pinned stages jump.
4. **Flex buttons: `flex:1 1 auto; min-width:max-content`** — never a pixel `min-width`. A pixel
   floor clips long labels between ~312px and ~430px of container width.
5. **Masked line reveals must clear descenders.** An `overflow:hidden` line mask cuts ~0.098em off
   descenders. Extend the mask `padding-bottom:.14em` and cancel with `margin-bottom:-.14em`.
6. **Non-positioned text paints below any positioned `z-index >= 0` sibling.** Give hero copy an
   explicit `position:relative; z-index:N` when it sits over a positioned decoration.

## Colour and contrast

7. **Two-token accent pairs.** A decorative accent (`--sand`) and a text-safe accent (`--sand-ink`).
   Never set body copy in the decorative token. Body copy stays on the AA-safe neutral.
8. **Display type over photography: stroke, not offset shadow.** `-webkit-text-stroke` with
   `paint-order: stroke fill`, thinned under 640px, with a `text-shadow` fallback in
   `@supports not (-webkit-text-stroke: 1px currentColor)`. An offset shadow ghosts at a clip edge.
9. **Never interpolate ink through a low-contrast midpoint.** If a palette is scroll-lerped, snap
   the ink at the seam; lerping dark-on-light toward light-on-dark passes through grey-on-grey.

## Motion

10. **No scroll hijacking.** Native scroll only. `scroll-behavior: smooth` for anchors, gated on
    `prefers-reduced-motion`. Signature mechanics read scroll position; they do not drive it.
11. **One rAF loop per page.** `WR.onScroll(fn)` batches every subscriber into a single
    rAF-gated dispatch. Do not add a second `requestAnimationFrame` loop.
12. **Transform and opacity only.** Nothing animates `height`, `top`, `width` or `margin`.
13. **One brand easing curve.** `--ease: cubic-bezier(.22,.61,.36,1)`. Every transition uses it.
    A single shared curve is the highest-leverage anti-slop move available.
14. **Reduced motion collapses choreography but keeps composition.** Each mechanic reads
    `WR.reduce` once and branches to a static end state — it does not simply stop mid-animation.
15. **Scale forward, never backward.** A bloom that contracts undoes the reveal it just paid for.

## Content

16. **Never invent prices, unit counts, founding dates, names, awards or ratings.** Anything the
    client has not confirmed renders as a visible `[CLIENT]` chip, not as plausible fiction.
    See `FACT-CHECK.md` for the specific claims that are unverified.
17. **Fair housing.** Copy describes the apartment, never the household. No "perfect for young
    professionals", "ideal for families", "great for roommates". No voucher-exclusion language of
    any kind. Neighbourhood copy stays on verifiable non-demographic facts.
18. **Equal Housing Opportunity mark in every footer**, as a real element with
    `alt="Equal Housing Opportunity"`, no smaller than the Wiseman mark.
19. **The live leasing system is the authority** on availability and pricing. Every number on this
    site is a point-in-time snapshot; every property links out to its RentCafe page.

## Accessibility floor — every page

20. Skip link; visible `:focus-visible` outline; hamburger under 760px with `inert` on the
    background and focus return; keyboard parity for every hover behaviour (the specimen plate
    swaps on `focus-within` as well as `:hover`); the list is always complete and usable with the
    map disabled; `content-visibility:auto` on long row groups.
21. `<script>document.documentElement.classList.add('js')</script>` inline in `<head>`, and all
    reveal rules written `.js .rv{...}` so content is visible if the script fails.

## Assets

22. Cache-bust with `?v=N` on `style.css`, `app.js`, `core.js`. Bump on every change.
23. Photography is hotlinked from the RentCafe CDN (`resource.rentcafe.com`, open, no auth) with
    Cloudinary-style transforms in the path: `q_auto,f_auto,w_1400`. Percent-encode `(` and `)`
    in any Vercel rewrite destination — the router reads them as regex groups.
