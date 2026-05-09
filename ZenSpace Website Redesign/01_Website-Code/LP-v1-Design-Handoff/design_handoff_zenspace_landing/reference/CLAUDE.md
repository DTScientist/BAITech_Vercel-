# ZenSpace Event Solutions — Project Briefing

This file gives full context on ZenSpace: who they are, what they sell, who they sell to, how they work. Read this before making any copy, design, or feature decisions.

---

## Company Overview

**Name:** ZenSpace Event Solutions
**Tagline:** "On-Demand Workspace. Anytime. Anyplace."
**Founded:** 2017 (8+ years in operation)
**Contact:** hello@zenspaceevents.com
**Response SLA:** Within 2 business hours

ZenSpace is a B2B company that rents smart soundproof meeting pods and provides complementary booking software for trade shows, conferences, and corporate events. They are a full-service operator — they handle everything from delivery and assembly to live event support and post-event removal. The core value proposition is that event organizers and exhibitors get private, productive meeting spaces on the show floor with zero operational burden on their own team.

---

## Products

### 1. Smart Meeting Pods — Core Product

The ZenSpace **4-Seater Pod** is a fully enclosed, soundproof, UL-certified meeting pod designed for trade show floors and conference venues. Mobile, deployable as a single unit or fleet of 30+.

**Only client requirement:** One 5 Amp power outlet per pod.

**15+ Smart Features:**
- **Smart E-Glass** — electrochromic glass goes transparent → opaque in 1 second
- **AI Remote Monitoring** — alerts for occupancy, open doors, loitering, lost items
- **Connectivity** — dedicated WiFi, Airtame screen sharing, USB-C hub
- **Soundproof Acoustic Walls** — industry-grade panels and floor system
- **Booking Software Integration** — QR self-serve, 10" displays, dashboards, lead reports
- **Branding Surfaces** — full exterior wraps + dynamic digital screens (updateable mid-event)

### 2. Booking Software — Add-on

Standalone or paired with pods. QR self-serve, 10" on-site displays, hourly slots (free or paid → sponsor monetization), real-time dashboard, post-event utilization + lead reports.

---

## Target Audiences

| Persona | One-liner | Pain |
|---|---|---|
| **Event Runners** | "You control the event itself." Trade show + corporate organizers, planners. | Private meeting space at scale without adding headcount. |
| **Floor Participants** | "You compete for attention on the floor." Exhibitors, sponsors, partners. | Standing out; converting traffic into qualified meetings. |
| **Industry Partners** | "You spec & procure for clients." GSCs, exhibit designers, agencies, venues. | Reliable turnkey pod they can confidently spec. |

---

## Proof Points

- **8+ years** in operation (since 2017)
- **250+ events** delivered
- **15+ smart features** per pod
- **30+ pods** max deployment

### Real Event Results

| Event | Result |
|---|---|
| **IMEX** | 600+ registered users · 93% peak utilization |
| **The Hospitality Show** | 120+ meetings booked in 1.5 days |
| **IAVM VenueConnect** | 200+ users · 92% utilization · 6 pods |
| **Expo! Expo!** | 110+ meetings booked |
| **ILHA Inspire** | 55+ meetings booked (1.5-day boutique event) |

### Trust Markers
**Associations:** IAEE · IMEX Group · MPI · SISO · IAVM · Questex
**Delivered at:** IMEX · Hospitality Show · ILHA Inspire · IAVM VenueConnect · Expo! Expo! · InfoComm · CES · MPI WEC · PCMA Convening Leaders

---

## Service Model — Full-Service Process

**Before:** (1) Event Alignment & Onboarding (2) Design & Booking Setup Approval (3) Logistics & On-Site Installation
**During & After:** (4) Live Support + Real-Time Dashboard (5) Removal + Full Utilization Report

Client provides power. ZenSpace handles everything else.

---

## Voice & Messaging

**Tone:** Confident, calm, precise, professional-not-stuffy. Real numbers always beat vague claims (93%, 600+, 5 Amp).

**Key phrases:**
- "On-Demand Workspace. Anytime. Anyplace."
- "Refined by experience"
- "Full-service" / "We handle everything"
- "Only requirement: a 5 Amp power outlet per pod"
- "Zero burden on your team"
- "Real conversations, not just brochures"
- **Smart E-Glass** (always proper-name capitalized)
- **UL-certified** (always include for credibility)

**Avoid:**
- Calling pods "booths" — they are **pods**, **meeting pods**, or **private meeting spaces**
- Generic event-vendor language
- Hype words, exclamation marks, emoji

### Contact reasons (form options)
- I have an upcoming event I could use pods for
- I want to explore this as a sponsorship asset
- I'd like to discuss pricing or a custom proposal
- I have a unique activation idea to discuss
- I'm a GSC / exhibit designer exploring options
- Just exploring — keep me in the loop

---

## Design System

### Colors
| Token | Hex | Usage |
|---|---|---|
| `--navy` | `#1c3f92` | Primary brand, buttons, borders |
| `--navy-dark` | `#0d1e45` | Darkest bg, body text |
| `--navy-mid` | `#183477` | Mid-tone navy bg |
| `--navy-deep` | `#133153` | Deep accent navy |
| `--blue` | `#4099f2` | Accent, labels, links |
| `--sky` | `#a0cdf9` | Light blue accent |
| `--sky-mid` | `#79b8f6` | Mid sky blue |
| `--green` | `#89c46e` | **Primary CTA**, success, highlights |
| `--green-mid` | `#a1d08b` | Hover state for green |
| `--mint` | `#c8efb5` | Very light green accent |
| `--white` | `#fbfcff` | Off-white page bg |
| `--off` | `#f4f8ff` | Light section bg |
| `--gray` | `#e6e6e6` | Borders, dividers |
| `--gray-mid` | `#c8cdd8` | Placeholder, muted |
| `--gray-dk` | `#5a6070` | Body copy, secondary text |

**Rule:** Green = CTA only. Navy dark = primary text. Blue = labels/accents only.

### Type
- **Body:** Poppins 300–700, line-height 1.68–1.72
- **H1:** Poppins Bold 700, letter-spacing -1.5px, `clamp(40px, 4.5vw, 62px)`
- **H2:** Poppins Bold 700, letter-spacing -0.8px, `clamp(28px, 3.5vw, 44px)`
- **Eyebrows:** Barlow Condensed, UPPERCASE, 11px, letter-spacing 3px, color `--blue`
- **Nav:** Poppins 500, 14px

### Tokens
- `--r: 14px` (radius), `--t: 0.28s`, `--ease: cubic-bezier(.4,0,.2,1)`
- `--sh-sm: 0 2px 12px rgba(13,30,69,.07)`
- `--sh-md: 0 8px 32px rgba(13,30,69,.11)`
- `--sh-lg: 0 20px 60px rgba(13,30,69,.16)`

### Layout
- `.wrap` max 1200px, padding 0 6%
- `.sec` 96px 0 · `.sec--sm` 64px 0
- Breakpoints: 1024 / 768 / 480

### Buttons
- `.btn-green` (primary CTA): green bg, navy text
- `.btn-navy` (secondary): navy bg, white text
- `.btn-outline` (on dark): transparent, white border
- `.btn-ghost` (tertiary): transparent, gray border
- All: padding 13px 26px, radius 10px, hover lifts -2px

---

## Tech Stack

Static HTML/CSS/vanilla JS. **No** React, Vue, TS, build tools, or npm. Inline `<script>` tags only. Google Fonts via CDN. Inline SVG for graphics.

---

## Page Structure (landing-perfect.html)

| Anchor | Section |
|---|---|
| `#top` | Hero — full-viewport, navy dark, pod illustration |
| — | Marquee bar (trust keywords) |
| — | Trust / Associations (IAEE, IMEX, MPI, SISO, IAVM, Questex + events tabs) |
| `#offer` | What We Offer — Pods (dark card) + Software (light card) |
| `#who` | Built For — three persona cards |
| `#process` | Our Process — 5-step timeline (Before / During & After) |
| — | Why ZenSpace — four stat cards |
| `#features` | Smart Pod Features — E-Glass demo + 6 features |
| `#results` | Real Events. Real Results. — six case study cards |
| — | Branding as Value (navy bg) |
| `#contact` | Contact form + reasons sidebar |
| — | Footer |

Nav: Pods · Software · Process · Results · Contact + green "Get a Quote" CTA.
