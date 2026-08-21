# Motor Tides Demo — Talk Track (v2, matches current hub flow)
**Audience:** Wiseman Residential (property owner) · **Also in the room:** Donghao, Honglu
**Length:** ~15 minutes + Q&A · **Hub flow:** hero → why a concierge → widget styles → own your website → the concepts · **Presenter:** Zhen

**Tabs to have open, in order:**
1. Hub — https://motor-tides-concepts.vercel.app/ *(the presentation spine — most of the demo lives here)*
2. Their live site — https://motortides.wisemanresidential.com/
3. Current site + concierge demo — https://motor-tides-current.vercel.app/
4. Concepts, in hub order — https://motor-tides-concept-a.vercel.app · -c · -b · -e *(Estate Green opens from the hub card)*

**Before the meeting:** reload tab 3 fresh (so the teaser fires on cue), sound on, click that page once so the chime is unlocked. Backup for bad wifi: `python3 -m http.server 8734 --directory "<repo>/redesign"`.

**Naming note:** the product is "the AI leasing concierge." She introduces herself as *Maya* inside the demo chat — that's fine to acknowledge in the moment ("she's calling herself Maya for this demo"), but don't pitch "Maya" as the product name.

---

## 1 · Cold open on the hub (1 min) — tab 1

Open the hub and **say nothing for ~10 seconds** — let the animated conversation on the right play: renter asks a price → instant answer → tour booked → *"Tuesday · 11:48 PM — office closed, lead captured."*

> "That conversation is the whole pitch. A renter asked a question at 11:48 on a Tuesday night, got the real price, and booked a Saturday tour — while the office was closed. Today we'll show you two things: that concierge running on your current website, and — since it's part of the package — a free redesign of the site itself. Everything you'll see is live, not slides."

*(Point at the two hero buttons: "Try the concierge" and "View website concepts" — that's the agenda.)*

## 2 · The problem, in their own experience (1–2 min) — tab 2, their live site

> "Quick look at your site as a renter sees it at 9pm. Beautiful photos. But what can they *do*? Pricing is two clicks behind this menu, and the only action is calling an office that closed at 6:30. Most of them don't call back tomorrow — they go back to Zillow and tour someone else's building. Every one of those visits cost marketing dollars."

*(One scroll, open the hamburger once, move on. Don't dwell.)*

## 3 · The concierge, live on THEIR site (4–5 min) — tab 3 ⭐ the heart of the demo

> "This is your current homepage — same layout, same content, rebuilt exactly. One difference, bottom right."

**Wait for the teaser** (~5s after load, soft chime): *"Hi there! 👋 Looking for pricing or a tour?"*

> "Notice it's a face, not a robot icon — for leasing, a human face is the highest-trust signal. In production that's a photo of your actual leasing team."

**The 5-step click path (practice this):**
1. **Open the chat** → greeting with typing indicators. *"She greets like a person — for the demo she's introducing herself as Maya."*
2. **💰 Pricing & availability** → all 7 plans, real prices. *"Your actual plans and prices. In production this pulls live from your Yardi RentCafe feed — when a unit leases, the answer updates itself. It never quotes a stale price."*
3. **Schedule a tour** → day → time → confirmation. *"Thirty seconds, no phone tag. The booking reaches your team — and lands as a guest card in Voyager, so the lead is tracked from the first message."*
4. **Type:** `can I bring my dog?` → pet answer. *"Free-typed questions too — pets, parking, utilities, hours."*
5. **Point at the Apply link** in a response. *"When they're ready, she hands them into your existing SecureCafe application. We're not replacing your leasing stack — we're putting a 24/7 front door on it."*

**Key line:** > "Everything you just saw runs on the site you already have. No redesign required. This could be live this month."

## 4 · Back to the hub: why now, the styles, and the offer (3–4 min) — tab 1, scroll down

**Scroll to "Why a concierge, and why now"** — four cards, read them as beats, not slides:
> "Four reasons this matters: after-hours leads get caught instead of lost · tours get booked inside the chat · every answer comes from one source of truth · and it syncs with the Yardi stack you already run — availability in, guest cards and tours back out. Nothing new for your team to manage."

**Scroll to "Concierge widget styles"** — seven launcher cards:
> "And the concierge is a system, not a gimmick. Seven launcher personalities: the minimal bubble, your own three-bars logo rising like a tide, a labeled 'Chat with us' pill — the clearest call to action — the human face you just saw, and three characters if you ever want more personality. Any style works on any design; it's a brand decision we make together."

*(If the owner leans conservative, point at the pill: "this one is the classic — nobody ever wonders what it does.")*

**Scroll to "And when you're ready: own your website":**
> "One honest observation about the website itself. Yardi RentCafe got you online fast — that was the right call. The trade-off is control: the code isn't yours, the template resists your brand, and there's little room to optimize for Google — or for the AI assistants renters now ask, 'find me an apartment near Sony Pictures.' Template sites are nearly invisible to those.
>
> So here's our offer, and it's simple: give us the website, and **the redesign is free — it's already built.** Four directions, fully working. And we keep supporting search and AI-visibility after launch to grow organic leads."

*(Point at the four chips: you own the code · fully on-brand · SEO-ready · visible to AI search.)*

## 5 · The five concepts (5–6 min, ~60 sec each) — hub "The concepts," open each

For each: open, scroll hero → floor plans → the illustrated neighborhood map → virtual tours. Point at the chat corner; don't re-demo it.

**01 · Coastal Editorial** *(quiet luxury)*
> "The boutique-hotel feel — cream, deep sea-teal, serif type, calm pacing. Positions Motor Tides as an address, not a listing. Right renter: choosing on feel between you and the nicest building in Culver City. Note the floor plans read like a menu, and your neighborhood is drawn as an illustrated map."

**02 · Architectural Dark** *(bold, cinematic)*
> "The building as the hero — dark, confident, oversized type: 'Good living, seven stories above Motor Ave.' Photographs beautifully in social ads; makes a lease-up feel like an event. Right renter: the studios crowd."

**03 · Estate Green** *(classic, warm — opens from the hub card)*
> "The most traditional — deep green, gold, classic structure. Familiar and trustworthy, closest to established property brands. It even has its own lighthouse concierge character."

**04 · Modern Platform** *(crisp, product-like)*
> "The proptech feel — like booking travel. Rotating hero, annotated photos, availability cards, an interactive map where every restaurant opens in Google Maps, 3D tours. Right renter: the one comparing five buildings in five tabs."

**05 · Resort Immersive** *(full-screen luxury, multi-page — save it for last)*
> "And the newest one, modeled on the top luxury lease-ups. Scroll slowly: photography pins in place, the page glides over it, and the chapter titles sweep from white to ink as the sections cross — pure boutique-hotel energy. It's a real multi-page site: Residences with the floor-plan menu and 3D tours, Experience for the rooftop and amenities, Location with the illustrated map. Use the arrow at the bottom to step section by section. Right renter: the one who books the hotel because of the website."

**Wrap:** land on the hub's concepts grid one last time — five cards side by side.
> "Any of these five, tailored with you — and the concierge lives in every one of them."

## 6 · Close & next steps (1 min)

> "Three takeaways. One: the concierge can go live on your current site quickly — that's the fastest win. Two: the redesign is free and essentially done — pick a direction and we tailor it. Three: everything stays connected to Yardi, so your team's workflow doesn't change.
>
> Our proposed next step: a two-week pilot on the live site, and we measure after-hours leads captured. Donghao / Honglu can walk through integration and timeline."

**Handoffs:** Donghao — Yardi/RentCafe integration (availability feed, guest cards, tour sync). Honglu — pilot logistics, analytics/reporting, SEO-GEO plan. *(Swap to whoever owns what.)*

---

## Likely questions & answers

- **"What does it answer from — can it go off script?"** Only your listing data and an approved knowledge base (policies, hours, specials). Outside that, it hands off to your team with the visitor's contact — it never invents pricing.
- **"What happens to the lead?"** Each conversation can create a guest card in Yardi with the transcript; tour bookings sync to your calendar.
- **"Can it use our branding / a real person's photo?"** Yes — launcher style, colors, greeting name, and photo are configurable; you saw six styles.
- **"Fair Housing compliance?"** Responses are templated from your approved content — the concierge avoids steering and answers policy questions verbatim from your policies.
- **"How much?"** *(Your pricing talk track — the demo intentionally leaves it open.)*
- **"Do we lose anything leaving RentCafe's website?"** No — applications, resident login, and leasing stay on Yardi. Only the marketing site moves to code you own.

## Demo hygiene
- The hub's hero conversation animates on load and loops — arrive on the tab a few seconds early so it's mid-play when screens share.
- The chime plays only after a click on the page (browser rule) — click once after loading tab 3.
- Teaser fires ~5s after load; reload the tab between dry runs for a clean transcript.
- The tour "booking" is a demo flow — say "in production this syncs to your calendar," don't claim it just booked.
- The face is a stock stand-in — if asked: "in production, your leasing team's photo."
- Product name is "the AI leasing concierge" — "Maya" is just her demo greeting name.
