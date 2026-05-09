# Handoff: ZenSpace Landing — v2 (Brilo-inspired)

## Overview

Marketing landing page for **ZenSpace Event Solutions** — a B2B company that rents smart soundproof meeting pods + booking software for trade shows, conferences, and corporate events. The page converts event organizers, exhibitors, and industry partners into "Get a Quote" leads.

This is **v2** — a reworked aesthetic direction inspired by the Brilo design system (Anton display, color-block tiles, warm editorial canvas) while preserving ZenSpace branding (navy/blue/green/mint palette, voice, content).

The user's current saved Tweaks state on `landing-d v2.html`:
- `display: "barlow"` (Barlow Condensed instead of Anton)
- `canvas: "cool"` (#fbfcff cool off-white instead of warm beige)
- `accent: "navy"` (default navy block tile)

Treat that combination as the **canonical visual direction** to ship — Barlow Condensed Bold uppercase display + cool canvas + navy accents.

## About the Design Files

`reference/landing-d v2.html` is a **design reference created in HTML** — a working prototype showing intended look, copy, and behavior. **Not production code to ship as-is.**

Recreate this design in ZenSpace's target stack. Per `reference/CLAUDE.md`, the project's preferred stack is **static HTML / CSS / vanilla JS** — no React, no build tools. The Tweaks panel uses React + Babel inline only because it's a design-time tool; **strip it from production**.

## Fidelity

**High-fidelity (hifi).** Final colors, type, spacing, copy, and interactions are locked. Recreate pixel-perfectly.

## File Map

```
design_handoff_zenspace_landing_v2/
├── README.md                           ← this file
└── reference/
    ├── landing-d v2.html               ← the canonical design
    ├── tweaks-panel.jsx                ← design-time only, strip from production
    ├── CLAUDE.md                       ← brand briefing (voice, persona, proof points, content rules)
    └── assets/
        ├── logo-horizontal-dark.png
        ├── logo-horizontal-white.png
        ├── logo-square-dark.png
        └── logo-square-white.png
```

## Page Structure

| # | Anchor | Section | Notes |
|---|---|---|---|
| 1 | — | Sticky nav | Logo · 5 anchor links · Sign In · green "Get a Quote" CTA |
| 2 | `#top` | Hero | Centered headline + 4 floating product cards (E-Glass swatch, 93%, 5A, 600+) on cool canvas |
| 3 | — | Ticker / marquee | Card-on-canvas with scrolling associations + event names |
| 4 | — | About + Stats | Off-white card with intro line + black 4-up stat block (250+, 93%, 600+, 5A) |
| 5 | `#pods` | Smart Meeting Pods | Color-block tile grid: hero E-Glass demo (navy span-2) + 6 feature tiles (mint, ink, sky, canvas, navy, canvas) |
| 6 | `#who` | Built For | Dark section, 3 alternating audience rows with big numbered Barlow numerals |
| 7 | `#process` | The Process | 5 numbered cards in 2 phases ("Before" / "During & after") with hover-slide arrows |
| 8 | — | CTA band | Full-width black rounded card with mint accent text + dual CTAs |
| 9 | `#results` | Results | Bento grid: navy hero tile (93% IMEX) + yellow + mint + black + sky tiles |
| 10 | `#contact` | Contact | 2-col: pitch + 6-item reasons list ↔ inquiry form |
| 11 | — | Footer | Black, 4-col with mint Barlow eyebrows |

## Design Tokens

### Colors (ZenSpace brand — locked)

| Var | Hex | Use |
|---|---|---|
| `--navy` | `#1c3f92` | Primary brand, block tile 1 |
| `--navy-dark` | `#0d1e45` | Body text |
| `--blue` | `#4099f2` | Accent, links, em text |
| `--green` | `#89c46e` | **Primary CTA only** |
| `--mint` | `#c8efb5` | Block tiles, eyebrows on dark |
| `--sky` | `#a0cdf9` | Block tiles |
| `--canvas` | `#fbfcff` | Page bg (cool variant — user's saved choice) |
| `--canvas-deep` | `#f0f3f9` | Section bg |
| `--canvas-card` | `#ffffff` | Inner cards |
| `#070607` | — | Ink — primary text |

**Color rules:** Green = primary CTAs only. Navy = headings & accents. Blue = `<em>` and link emphasis. Mint = eyebrows on dark, accent numerals.

### Typography

- **Display:** Barlow Condensed Bold 700, UPPERCASE, letter-spacing -0.01em (user's saved choice; was Anton in initial design)
- **Body:** Inter 400/500/600
- **Eyebrow chips:** Inter 500, 14px, 7×16px padding, full pill radius

Google Fonts URL:
```
https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap
```

### Heading scale (display = Barlow Condensed Bold uppercase)

| Use | Size | Line-height |
|---|---|---|
| `.display--xxl` (hero H1) | `clamp(60px, 8.4vw, 132px)` | 0.95 |
| `.display--xl` (section H2) | `clamp(44px, 5.4vw, 88px)` | 1.0 |
| `.display--lg` | `clamp(36px, 4vw, 60px)` | 1.05 |
| `.display--md` | `clamp(28px, 2.6vw, 40px)` | 1.1 |

### Shape & motion

| Token | Value |
|---|---|
| Pill radius | 240px |
| Card radius | 24px |
| Tile radius | 28px |
| Transition | 0.28s `cubic-bezier(0.4, 0, 0.2, 1)` |
| Shadow sm / md / lg | see `:root` block in HTML |

### Buttons

- `.btn--green` (primary CTA) — green bg, navy text, pill radius
- `.btn--dark` — black bg, white text
- `.btn--ghost` — transparent, 1px border
- `.btn--white` — white on dark backgrounds

All: 14px 26px padding, 600/15px Inter, hover lifts -2px with tinted shadow.

## Section Specs (key bits)

### Hero
- Centered Barlow Bold uppercase H1 ("ON-DEMAND WORKSPACE. ANYTIME. ANYPLACE.") with `<em>` line in `--navy`
- 4 absolutely-positioned floating cards (one per corner-ish), each rotated ±5–7°, with idle 6s float animation
- Top-left card auto-cycles its E-Glass swatch (clear ↔ opaque) every 3.5s

### Color-block tiles (`#pods`)
- 2-column grid, 24px gap
- First tile spans both columns (`tile--feat`) — split into copy + interactive E-Glass demo
- Tile palette rotation: navy → mint → ink → sky → canvas → navy → canvas
- Hover: translateY(-4px) + soft shadow
- Each tile has a 48px icon block + Barlow uppercase title + body copy
- Inline SVG icons (24×24, stroke 1.8) — replace with the existing icon system if one exists

### Audiences (`#who`)
- Dark `#070607` section
- 3 rows with grid `140px 1.4fr 1fr`, white border-bottom
- 120px Barlow Bold uppercase row number at 18% opacity (ghost numerals)
- Each row: mint chip + Barlow uppercase title (with mint `<em>`) + sky italic pull-quote + descriptor + outline tag pills

### Process timeline
- Replaces v1's vertical-line timeline with **stacked numbered cards**
- Each card: 64px Barlow Bold number + title + description + 48px circular arrow
- Hover: card slides right 6px, arrow translates 4px
- Two phase headers ("Before the event", "During & after the event") above their groups

### Results bento
- 12-column grid, 20px gap, 5 tiles
- Hero (`span 7`, navy bg, 140px Barlow stat)
- Two (`span 5`, yellow `#f1ef89` bg, 96px stat)
- Three/Four/Five (`span 4` each — mint / ink / sky)

### Contact form
- 2-col `1fr 1.1fr`
- Left: chip + left-aligned H2 + lede + reasons list (right-arrow prefix that slides on hover)
- Right: white form card with first/last/email/company (2-col) + event name + event date/reason (2-col) + textarea + green pill submit + pulsing-dot SLA line

## Interactions & Behavior

| Interaction | Implementation |
|---|---|
| Smooth-scroll | `html { scroll-behavior: smooth }` |
| Sticky blur nav | `position: sticky` + `backdrop-filter: blur(20px)` over `rgba(247,246,243,0.86)` |
| Pulsing chip dot | `@keyframes pulse` 2s |
| Hero entrance | sequential fade-up: chips (0) → title (.1s) → sub (.22s) → CTA (.32s) |
| Floating cards idle | `@keyframes floatIdle` 6s, staggered -1.5s / -3s / -4.5s |
| Hero E-Glass auto-cycle | `setInterval` every 3.5s toggles `.clear` ↔ `.opaque` |
| E-Glass main demo | `setEG('clear'\|'opaque')` toggles glass class + button active state, 0.9s ease transition |
| Ticker scroll | `@keyframes scroll` 36s linear infinite, content duplicated for seamless loop |
| Tile hover lift | `translateY(-4px)` + shadow |
| Process row hover | card slides right 6px, arrow circle slides 4px and turns navy |
| Reasons list | hover left-pads 8px, arrow slides 4px |
| Reveal-on-scroll | IntersectionObserver toggles `.in` on `.reveal` and `.stagger` |
| Form submit | Currently a no-op `alert()` — wire to ZenSpace's lead pipeline |

All animations gated on `@media (prefers-reduced-motion: no-preference)`.

## Voice & Copy Rules (from `CLAUDE.md`)

- Pods are **pods** / **meeting pods** — never "booths"
- **Smart E-Glass** always proper-case
- Always include **UL-certified**
- Use real numbers (93%, 600+, 5 Amp)
- No emoji, no exclamation marks, no hype words

Required signature phrases:
- "On-Demand Workspace. Anytime. Anyplace." (the hero H1)
- "Refined by experience"
- "Only requirement: a 5 Amp power outlet per pod"
- "Zero burden on your team"

## State / Backend Needs

- **Form submit** → POST to lead pipeline; trigger SLA email to `hello@zenspaceevents.com`; show success state
- **Reasons list ↔ form select** wiring (clicking a reason should pre-select the matching `<option>`) — not yet wired, easy enhancement
- **Stats / ticker / case-study tiles** → CMS-source if updates are frequent

## Open Questions

1. Software section — standalone or stay nested under Pods?
2. Final form fields — confirm field set + which are required
3. Footer link taxonomy — confirm columns
4. Privacy / Terms / Accessibility URLs
5. Analytics stack + conversion events
6. Imagery — keep all-CSS, or commission product photography?

## Assets

In `reference/assets/`:
- `logo-horizontal-dark.png` — nav logo (36px high in v2)
- `logo-horizontal-white.png` — alternate, footer uses dark + CSS invert filter
- `logo-square-dark.png` / `logo-square-white.png` — favicons / social cards

No photography is used. All graphics are CSS/SVG — the E-Glass demo, hero radial glows, inline 1.8-stroke SVG icons.

## Tweaks Panel — Strip from Production

`reference/tweaks-panel.jsx` and the `<script type="text/babel">` block at the bottom of the HTML are **design-time only** — they let the design reviewer toggle display font, canvas, and accent tile color live. Remove them in production.

The user's saved choice as of handoff: **Barlow display + cool canvas + navy accent**. Bake those values into the production CSS as the single locked variant.
