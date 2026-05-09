# Handoff: ZenSpace Event Solutions — Marketing Landing Page

## Overview

This package contains the design and copy for the ZenSpace Event Solutions marketing landing page. ZenSpace is a B2B company that rents smart soundproof meeting pods (and complementary booking software) for trade shows, conferences, and corporate events.

The page's job: convert event organizers, exhibitors, and industry partners into "Get a Quote" leads by communicating product capability, full-service operating model, and credibility (events delivered, utilization, named clients).

The primary deliverable is **`reference/landing-c.html`** — the high-fidelity HTML/CSS/vanilla-JS prototype to recreate in production.

---

## About the Design Files

The files in `reference/` are **design references created in HTML** — a working prototype that captures the intended look, copy, layout, and interaction behavior. They are **not production code to ship as-is**.

Your task is to **recreate this design in ZenSpace's target codebase / framework** using its established patterns, component library, and CMS conventions. The HTML is canonical for visual decisions: colors, type, spacing, copy, layout. Treat it as the single source of truth for "what it should look like" — but rebuild it with whatever stack the project actually uses.

If no production environment exists yet, the project's stated stack preference (per `reference/CLAUDE.md`) is **static HTML / CSS / vanilla JS** — no React, no build tools. In that case, lift the markup more directly, but still:
- Split inline `<style>` into a real `.css` file
- Split inline `<script>` into separate `.js` files
- Replace hardcoded copy with whatever CMS / data source ZenSpace uses

---

## Fidelity

**High-fidelity (hifi).**

Final colors, typography, spacing, copy, and interactions are all locked. Recreate pixel-perfectly:
- Exact hex values from the design tokens table below
- Exact font families, weights, sizes, letter-spacing, line-heights
- Exact padding/margin/gap values
- All hover, focus, and reveal animations

The only thing **not** locked: the inner image content of `<image-slot>`-style placeholders (none used here — all imagery is illustrative SVG / CSS) and any final copy edits the content team may want.

---

## File Map

```
design_handoff_zenspace_landing/
├── README.md                           ← this file
└── reference/
    ├── landing-c.html                  ← the canonical design (single-file prototype)
    ├── CLAUDE.md                       ← brand briefing: voice, messaging, tokens, content rules
    └── assets/
        ├── logo-horizontal-dark.png    ← primary nav logo (on light bg)
        ├── logo-horizontal-white.png   ← logo on dark bg (footer)
        ├── logo-square-dark.png
        └── logo-square-white.png
```

`reference/CLAUDE.md` is critical reading. It is the brand briefing — voice, persona definitions, proof-point numbers, "do/don't" copy rules. Anything that changes content (microcopy, form fields, footer links) should reconcile against it.

---

## Page Structure

The landing page is a single long-scroll page with anchor-linked sections. Top to bottom:

| # | Anchor | Section | Purpose |
|---|---|---|---|
| 1 | — | **Sticky Nav** | Logo, 5 anchor links, primary CTA |
| 2 | `#top` | **Hero** | Headline, subhead, dual CTA, "Outside / Inside / The Door" split band |
| 3 | — | **Ticker / Marquee** | Scrolling associations + event names (trust signal) |
| 4 | — | **Stats Bar** | 4 stat cards: 250+ events, 93% utilization, 600+ users, 5A requirement |
| 5 | `#pods` | **Smart Meeting Pods** | Section header + asymmetric "feat hero + E-Glass live demo" + 6-card feature grid |
| 6 | `#who` | **Built For** (dark section) | 3 alternating audience rows: Event Runners / Floor Participants / Industry Partners |
| 7 | `#process` | **The Process** | Section header + vertical timeline with 2 phase labels and 5 numbered steps |
| 8 | — | **CTA Band** (dark) | "Refined by experience" mid-page conversion push |
| 9 | `#results` | **Real Events. Real Results.** | Bento grid of 5–6 case-study tiles (IMEX hero + Hospitality Show / VenueConnect / Expo! Expo! / ILHA Inspire) |
| 10 | `#contact` | **Contact / Quote** | Two-column: pitch + reasons-list ↔ inquiry form |
| 11 | — | **Footer** (dark) | Logo, descriptor, 3 link columns, bottom legal bar |

Nav order: **Pods · Software · Process · Results · Contact** + green **"Get a Quote"** CTA.
(Note: the current prototype's nav links `#software` to a software section that lives within `#pods` — confirm with stakeholders whether Software gets its own section or remains a sub-block.)

---

## Design Tokens

These are also in `reference/CLAUDE.md`. Lift them into your design-token system / CSS variables exactly.

### Colors

| CSS var | Hex | Role |
|---|---|---|
| `--navy` | `#1c3f92` | Primary brand, primary buttons, borders |
| `--navy-dark` | `#0d1e45` | Darkest bg, primary body text |
| `--navy-mid` | `#183477` | Mid-tone navy bg |
| `--navy-deep` | `#133153` | Deep accent navy |
| `--blue` | `#4099f2` | Accent, eyebrow labels, links |
| `--sky` | `#a0cdf9` | Light blue accent |
| `--sky-mid` | `#79b8f6` | Mid sky blue |
| `--green` | `#89c46e` | **Primary CTA only**, success indicators, highlights |
| `--green-mid` | `#a1d08b` | Hover state on green |
| `--mint` | `#c8efb5` | Very light green accent (eyebrows on dark bg, gradient stops) |
| `--white` | `#fbfcff` | Off-white page bg |
| `--off` | `#f4f8ff` | Light section bg |
| `--gray` | `#e6e6e6` | Borders, dividers |
| `--gray-mid` | `#c8cdd8` | Placeholder, muted icons |
| `--gray-dk` | `#5a6070` | Body copy on light bg, secondary text |

**Color rules (enforce):**
- Green is for primary CTAs only. Never use it for body text, decoration, or non-CTA accents.
- Navy-dark is the default body text color on light backgrounds.
- Blue is for eyebrow labels, links, and small accents — never large text or backgrounds.

### Typography

- **Body:** Poppins, weights 300/400/500/600/700, line-height 1.65–1.7
- **Display headings:** Barlow Condensed Bold 700 (most large headings on the page use this — note this is a deliberate evolution from the v1 system that used Poppins for H1/H2)
- **Eyebrow labels:** Barlow Condensed 600, UPPERCASE, 11px, letter-spacing 0.24em, color `--blue` (or `--mint` on dark bg)
- **Nav links:** Poppins 500, 14px

Google Fonts CDN URL used in the prototype:
```
https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;500;600;700&display=swap
```

### Heading scale (display = Barlow Condensed Bold)

| Use | Size | Letter-spacing | Line-height |
|---|---|---|---|
| Hero H1 | `clamp(56px, 8vw, 128px)` | -0.02em | 1.0 |
| Section H2 | `clamp(40px, 5vw, 72px)` | -0.015em | 0.98 |
| Audience row title | `clamp(32px, 3.6vw, 52px)` | -0.01em | 1.0 |
| Process step title | 28px | -0.005em | 1.1 |
| Feature card title | 24px | -0.005em | 1.1 |

### Spacing & layout

- `.wrap` max-width 1240px, side padding 6%
- Section padding (`.sec`): 130px top/bottom (collapses to 80px under 1024px)
- Section header bottom margin: 80px

### Shape & motion

| Token | Value |
|---|---|
| Border radius (cards) | 20px |
| Border radius (buttons) | 10px |
| Border radius (form fields) | 8px |
| Transition duration `--t` | 0.28s |
| Transition easing `--ease` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Card shadow (sm) | `0 2px 12px rgba(13,30,69,0.07)` |
| Card shadow (md) | `0 8px 32px rgba(13,30,69,0.11)` |
| Card shadow (lg) | `0 20px 60px rgba(13,30,69,0.16)` |

### Buttons

| Class | Background | Text color | Border | Use |
|---|---|---|---|---|
| `.btn-green` | `--green` | `--navy-dark` | none | **Primary CTA** (Get a Quote) |
| `.btn-navy` | `--navy-dark` | `#fff` | none | Secondary |
| `.btn-outline` | transparent | `#fff` | `1px solid rgba(255,255,255,0.4)` | On dark bg |
| `.btn-ghost` | transparent | `--navy-dark` | `1px solid --gray` | Tertiary |

All buttons: padding `14px 28px`, border-radius `10px`, weight 600, size 14px. Hover: `translateY(-2px)` plus tinted shadow.

The green primary button has a built-in shine sweep on hover (a `::before` pseudo-element with a translucent linear gradient that animates across the button).

### Breakpoints

- `1024px` — nav collapses, sections stack to 1 column, padding shrinks to 80px
- `600px` — form rows stack, footer stacks, back link hidden, form padding shrinks

---

## Section-by-Section Specs

### 1. Sticky Nav

- Position: sticky top:0, z-index 100
- Background: `rgba(251,252,255,0.92)` with `backdrop-filter: blur(18px)`
- Border-bottom: 1px `--gray`
- Inner: 73px tall, flex space-between
- Logo: `assets/logo-horizontal-dark.png`, height 38px
- Links (Pods, Software, Process, Results, Contact): Poppins 500 / 14px / `--gray-dk`
- Link hover: text → `--navy-dark`, **and** an animated underline (a 2px gradient `--blue → --green` line that scales in from the left)
- Right-side CTA: `.btn-green` "Get a Quote"

### 2. Hero

- Min-height 780px, full-width, navy-dark bg
- **Two stacked decorative layers** behind content:
  1. `::before` — two radial gradients (bottom-center blue glow + top-center navy glow), animated drift via `@keyframes heroBgDrift` (14s, alternates ±2% Y)
  2. `::after` — diagonal stripe pattern at 12% opacity (`repeating-linear-gradient(45deg, transparent 0 24px, rgba(255,255,255,0.06) 24px 25px)`)
- **Hero content** (centered, max-width 980px):
  - Pulsing chip: green dot + "250+ events delivered since 2017" (Barlow Condensed, 12px, mint text on `rgba(255,255,255,0.08)` rounded pill)
  - H1: "On-demand workspace.<br>**Anytime. Anyplace.**" — second line wrapped in `<em>` and styled with a `linear-gradient(135deg, --blue 0%, --mint 100%)` text fill
  - Sub: "Smart, soundproof, **UL-certified** meeting pods for trade shows, conferences, and corporate events. Refined by experience — and one 5 Amp outlet is the only thing we'll ever ask of you."
  - CTA pair: green "Get a Quote" + outline "Explore Pods"
- **Hero split band** (the section's signature element): a 3-column grid — Outside / The Door / Inside — with the door label set vertical (`writing-mode: vertical-rl; transform: rotate(180deg)`). All three use Barlow Condensed Bold uppercase. The right "Inside" column uses `--mint` text + a subtle `rgba(255,255,255,0.03)` bg tint.
- **Hero entrance animation**: chip → H1 → sub → CTAs → split band fade up sequentially (delays 0 / 0.12s / 0.24s / 0.34s / 0.5s)

### 3. Ticker

- Single row of 10 names (IAEE, IMEX Group, MPI, SISO, IAVM, Questex, Hospitality Show, VenueConnect, Expo! Expo!, ILHA Inspire) duplicated for seamless scroll
- Each name: Barlow Condensed 600 / 20px / `--navy-deep` / letter-spacing 0.04em
- Separator: a small blue dot between items (`::after { content: '●'; color: --blue }`)
- Animation: `transform: translateX(0) → translateX(-50%)` over 30s linear infinite
- Edge fade masks (`::before` / `::after`) on container with 120px white→transparent gradients

### 4. Stats Bar

- 4 columns, separated by 1px `--gray` vertical dividers
- Big number: Barlow Condensed Bold, `clamp(56px, 7vw, 96px)`, with text-fill linear-gradient `--navy-dark → --blue`
- Superscript suffixes: `+`, `%`, `+`, `A` — half size, `--blue`, weight 600
- Labels: Barlow Condensed 500 / 13px / 0.18em / `--gray-dk`
- Values: 250+ events delivered, 93% IMEX peak utilization, 600+ IMEX users registered, 5A only client requirement

### 5. Smart Meeting Pods (`#pods`)

- Section bg: `linear-gradient(180deg, --white 0%, --off 100%)`
- Eyebrow: "Smart Meeting Pods · 01"
- H2: "15+ smart features.<br>One **5 Amp** outlet." (em styled blue)
- Lede: see HTML

**Asymmetric feature row** (1.4fr / 1fr grid, 24px gap):
- Left "feat hero" card (min-height 420px): navy gradient bg, mint "— Feature 01" eyebrow, big Barlow title "Smart E-Glass. Privacy in 1 second.", supporting paragraph. A radial glow sits in the top-right corner via `::after`.
- Right "demo" card (white): a **live interactive E-Glass demo**:
  - 170×200px rectangle (the "glass") with a 2px navy border and a subtle inner border via `::before`
  - Default state: light blue gradient + "Transparent" label
  - Toggle to "Frosted": dark navy gradient + mint "Frosted (private)" label, with a 0.8s `--ease` transition
  - Below the glass: a pill-shaped segmented toggle with "Transparent" / "Frosted" buttons (active state: navy-dark fill, white text, soft shadow)
  - Idle animation: a slow blue glow pulse via `glassPulse` 4s

**6-card feature grid** (3 columns, 24px gap):
1. AI Remote Monitoring
2. Built-in Connectivity
3. Soundproof Acoustics
4. Self-serve QR Booking
5. Brand Surfaces
6. Lead Data, Captured

Each card: white bg, 1px `--gray` border, 20px radius, 36px×28px padding, Barlow eyebrow ("— Feature 0X"), Barlow Bold title (with intentional `<br>` line break in titles for visual rhythm), Poppins description. Hover: border → navy, lift 4px, shadow.

### 6. Built For (`#who`) — dark section

- Section bg: `--navy-dark`, white text
- Eyebrow on dark: `--mint`
- 3 audience rows, **alternating layout**:
  - Odd rows (1, 3): grid `120px 1fr 1fr` — number ↔ title block ↔ description block, left-aligned
  - Even row (2): grid `1fr 1fr 120px` — description ↔ title block ↔ number, all right-aligned via `:nth-child(even)` overrides
- Number: Barlow Bold 80px, `rgba(255,255,255,0.15)` (ghost-style)
- Eyebrow label per row: mint, 0.24em
- Title: Barlow Bold up to 52px, with `<em>` words colored `--blue`
- Pull quote (`.aud__q`): Barlow italic, `--sky`, 18px
- Description: Poppins 15px, `rgba(255,255,255,0.7)`
- Tags: small Barlow rounded outline pills (border `rgba(255,255,255,0.2)`, padding `6px 12px`)
- Row separator: 1px `rgba(255,255,255,0.1)` bottom border

Three audiences (per `CLAUDE.md`):
1. **Event Runners** — "You control the event itself." Tags: Organizers, Planners.
2. **Floor Participants** — "You compete for attention on the floor." Tags: Exhibitors, Sponsors, Partners.
3. **Industry Partners** — "You spec & procure for clients." Tags: GSCs, Designers, Venues.

### 7. The Process (`#process`)

- White section, 130px padding
- Eyebrow: "The process · 03"
- H2: "Five steps.<br>**Zero burden** on your team."
- A vertical timeline (max-width 920px):
  - A single 2px gradient line (`--blue → --green`) runs vertically at left:60px, top:24px → bottom:24px
  - Two **phase labels** ("— Before the event", "— During & after the event") with a 14px blue dot on the line
  - Five **steps**, each: grid `120px 1fr` with a Barlow 48px right-aligned step number (01–05), a 14px white-fill / navy-bordered dot on the line, and a step title + description
  - Step dot scales to 1.25× and turns green when scrolled into view (`.proc__i.in .proc__sq::after`)

Steps (per `CLAUDE.md`):
- **Before:** 01 Alignment & onboarding · 02 Design & booking setup · 03 Logistics & install
- **During & after:** 04 Live support + real-time dashboard · 05 Removal + full utilization report

### 8. CTA Band

- Full-bleed dark band: `linear-gradient(135deg, --navy-dark 0%, --navy 50%, --navy-deep 100%)` + radial green glow
- 100px vertical padding
- Big H heading + sub + dual CTAs (green primary + outline secondary)

### 9. Results (`#results`) — bento grid

- 12-column grid, 20px gap
- 5 tiles, sized:
  - Tile 1: `span 7` (hero, navy gradient, white text, min-height 340px, big 120px stat)
  - Tile 2: `span 5`
  - Tiles 3–5: `span 4` each (filling the second row)
- White tiles: 1px `--gray` border, 20px radius, 40px×36px padding, big stat 64px with `--navy → --blue` gradient text fill, Barlow eyebrow label, title 24px, supporting copy 13px

Stats (from `CLAUDE.md`):
- IMEX: 600+ registered users · 93% peak utilization (this is the hero tile)
- Hospitality Show: 120+ meetings booked in 1.5 days
- IAVM VenueConnect: 200+ users · 92% utilization · 6 pods
- Expo! Expo!: 110+ meetings booked
- ILHA Inspire: 55+ meetings booked (1.5-day boutique event)

### 10. Contact / Quote (`#contact`)

- 2-column grid `1fr 1.1fr`, 64px gap
- **Left column:** eyebrow + "Let's plan your next event." H2 + supporting copy + reasons list. Reasons list = `<ul>` with top + bottom 1px `--gray` dividers per item, Barlow 600 / 15px / navy-dark, blue right-arrow `→` prefix that slides 4px right on hover
  - Reasons (use these exactly — from `CLAUDE.md`):
    1. I have an upcoming event I could use pods for
    2. I want to explore this as a sponsorship asset
    3. I'd like to discuss pricing or a custom proposal
    4. I have a unique activation idea to discuss
    5. I'm a GSC / exhibit designer exploring options
    6. Just exploring — keep me in the loop
- **Right column:** white form card, 48px padding, 20px radius, soft shadow:
  - Fields: First name + Last name (2-col), Work email + Company (2-col), Event name, Event date, Reason for inquiry (select), Anything else (textarea), green submit button
  - Field styling: Poppins 14px input, `--off` bg, 1px `--gray` border, 8px radius. Focus: navy border + white bg + 3px blue glow shadow.
  - SLA pin under the button: pulsing green dot + "Reply within 2 business hours"

### 11. Footer

- Bg: `--navy-dark`
- 4-col grid `1.6fr 1fr 1fr 1fr`:
  - Brand col: white logo (height 42px, achieved via `filter: brightness(0) invert(1)`), short descriptor, social links
  - Three link columns with mint Barlow eyebrow headings ("Product", "Company", "Resources" or similar — confirm taxonomy with content team)
- Bottom bar: 1px `rgba(255,255,255,0.1)` top border, Barlow 12px / 0.16em / `rgba(255,255,255,0.4)` (left: copyright, right: legal links)

---

## Interactions & Behavior

| Interaction | Where | Implementation |
|---|---|---|
| Smooth-scroll anchor jumps | All nav + CTA links | `html { scroll-behavior: smooth }` |
| Sticky nav with blur | Top nav | `position: sticky` + `backdrop-filter: blur(18px)` |
| Pulsing chip dot | Hero chip + form SLA | `@keyframes pulse` 2s |
| Hero entrance fade-up | Chip / H1 / sub / CTA / split | Sequential `animation-delay` 0–0.5s |
| Hero bg drift | Hero `::before` | `@keyframes heroBgDrift` 14s alternate |
| Marquee scroll | Trust ticker | `@keyframes scroll` 30s linear infinite, content duplicated |
| Nav link gradient underline | Nav links hover | `::after` 2px gradient bar, scaleX 0→1 |
| Button shine sweep | `.btn-green:hover` | `::before` translucent gradient sliding L→R |
| E-Glass live toggle | Pods section demo | Inline JS `setEG('clear'|'opaque')` toggles `.opaque` class on glass + active state on segmented buttons |
| E-Glass idle pulse | Pods section demo | `@keyframes glassPulse` 4s glow when not opaque |
| Card lift on hover | Feature cards, results tiles | `translateY(-4px)` + soft shadow |
| Reasons-list arrow slide | Contact reasons | `:hover { padding-left: 8px }` + arrow `translateX(4px)` |
| Reveal-on-scroll | Sections marked `.reveal` / `.reveal-l` / `.reveal-r` / `.reveal-scale` / `.stagger` | IntersectionObserver toggles `.in` (see `<script>` at bottom of `landing-c.html`) |
| Process dot grow | Each `.proc__i` step | When `.in` class added, dot scales 1.25× and turns green |
| Form submit | Contact form | **Currently a no-op in the prototype.** Wire to ZenSpace's lead pipeline (HubSpot / custom backend) and route confirmation to `hello@zenspaceevents.com` |

All animations respect `@media (prefers-reduced-motion: no-preference)` — the entire animation block is gated on this. Make sure any reimplementation preserves that gate.

---

## Voice & Copy Rules (from `CLAUDE.md`)

When tweaking copy, enforce these:
- Pods are **pods** / **meeting pods** / **private meeting spaces** — never "booths"
- Always use **Smart E-Glass** as a proper noun (capitalized)
- Always include **UL-certified** when describing pods
- Real numbers > vague claims (use 93%, 600+, 5 Amp wherever possible)
- Avoid hype words, exclamation marks, emoji
- Tone: confident, calm, precise — professional but not stuffy

Required signature phrases that should remain visible somewhere on the page:
- "On-Demand Workspace. Anytime. Anyplace." (the tagline — currently the hero H1)
- "Refined by experience"
- "Only requirement: a 5 Amp power outlet per pod"
- "Zero burden on your team"

---

## Assets

All in `reference/assets/`:
- `logo-horizontal-dark.png` — used in nav (38px high)
- `logo-horizontal-white.png` — also exists; the prototype uses the dark logo + a CSS `filter: brightness(0) invert(1)` in the footer instead, but the white logo is available if you'd prefer to swap it in
- `logo-square-dark.png` / `logo-square-white.png` — for favicons, social cards, app icons

No photography or product shots are used in the prototype — imagery is pure CSS/SVG (the gradient glass demo, the hero gradient field, the radial glows on dark cards). If the production design wants product photography, that's a content-team conversation; the current design intentionally avoids it.

Fonts are loaded from Google Fonts CDN. Self-host them in production if PageSpeed / privacy is a concern.

---

## State & Data Needs

Most of the page is static. The interactive bits that need wiring:

| Element | Backend dependency |
|---|---|
| Contact form | POST to ZenSpace's lead pipeline; trigger 2-business-hour SLA email to `hello@zenspaceevents.com`; show inline success state |
| Reasons list (left of form) | Clicking a reason should pre-select the matching `<select>` option in the form (currently not wired in the prototype — straightforward enhancement) |
| Stat numbers (250+, 93%, 600+) | Currently hardcoded. If ZenSpace wants these to update without a redeploy, expose them via CMS / a small JSON config |
| Event names in ticker | Hardcoded list of 10. Same — CMS-source if updates are frequent |
| Case-study tiles | Hardcoded. CMS-source if more events should be added |

---

## Suggested Build Order

1. Tokens + base layer (CSS variables, body type, `.wrap`, `.btn` classes)
2. Nav + footer (chrome — easiest to validate against the design)
3. Hero (most complex single section — get this right first)
4. Stats bar + ticker (small, build muscle memory)
5. Pods section + E-Glass interactive demo
6. Built For + Process (dark + light section pair)
7. Results bento grid
8. Contact form (wire to backend)
9. Reveal-on-scroll IntersectionObserver pass
10. Responsive QA at 1024 / 768 / 600 / 360

---

## Open Questions for ZenSpace

These were not resolved in the prototype — flag with the client before launch:
1. **Software section**: should `#software` be a dedicated standalone section, or stay nested under `#pods`?
2. **Final form fields**: are first/last name, work email, company, event name, event date, reason, message the right field set? Should event date be required?
3. **Footer link taxonomy**: which links go in each of the three columns? Confirm.
4. **Privacy / Terms / Accessibility links**: confirm exact URLs for the bottom legal bar.
5. **Analytics**: which stack (GA4? Plausible? HubSpot tracking?) and which conversion events should fire on form submit / CTA clicks?
6. **Imagery**: stay all-CSS, or commission product photography for the Pods and Results sections?
