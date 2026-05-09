# ZenSpace Phase 2 — On-Page SEO Action Plan
**Date:** April 12, 2026 | **Audit baseline:** April 5, 2026 | **33 pages audited**

---

## 📊 Site-Wide Audit Summary

| Grade | Pages | Count |
|-------|-------|-------|
| 🟢 GOOD (7.0–8.0) | Homepage, all pod pages, most service pages | 21 |
| 🟡 NEEDS WORK (5.0–6.8) | Case studies, blog posts, legal pages, FAQ | 12 |
| 🔴 CRITICAL | None — no page scored below 5 | 0 |

**Site-wide average score: 6.7 / 10**

### The 3 Universal Issues
These appear on nearly every page and are the root cause of the low scores:

1. **Schema missing on 27 of 33 pages** — Phase 1 addressed product + FAQ schemas. Service pages still need it.
2. **Missing H2 structure on case study pages** — 6 pages with 7,800+ words each and ZERO H2 subheadings. Google can't understand the content hierarchy.
3. **Image alt text** — 447 of 704 images missing (Fix 22, ongoing). Worst offender: /4-seater (77/97 missing).

---

## 🔴 PRIORITY 1 — Case Study Content Restructure (Highest SEO Impact)

**Why this matters most:** All 6 case study pages have 7,800+ words with NO H2 subheadings. That's like writing 6 essays with no paragraph breaks. Google can't parse topical signals. This is killing relevance scores for competitive event industry keywords.

These pages score 5/10 despite having rich word count because the content is structurally invisible to search engines.

**Note:** Meta descriptions were fixed in Phase 1 via the CMS SEO Description field.

### Fix for each case study page
In **Wix Editor → Pages → Case Study (Item) template**:

Add these H2 sections to the template (they'll apply to all case study pages):

```
H2: About [Event Name]
H2: The Challenge: Why [Event Name] Needed Private Meeting Spaces
H2: ZenSpace Solution: Pod Configuration & Setup
H2: Results & Attendee Experience
H2: Key Takeaways for Event Planners
H2: Ready to Bring ZenSpace to Your Event?
```

**Estimated time:** 20 min in Wix Editor (edits to template apply to all 5 dynamic pages)

**Impact:** All 5 case study pages go from 5/10 → estimated 7.5/10

---

## 🟠 PRIORITY 2 — Service Page Schema Sprint (30 min)

Phase 1 added Product schema to pod pages. Now add schema to service pages using the same method: **Wix Editor → page → gear icon → SEO → Advanced → Structured Data Markup → Edit**.

### /event-organizers (Score: 8 → 8.5+)
Strong page (4,217 words, 7 H2s, good meta desc). Only missing schema.

```json
{"@context":"https://schema.org","@type":"Service","name":"ZenSpace Event Pod Rental for Event Organizers","description":"Premium IoT-enabled meeting pods for conference and trade show organizers. ZenSpace handles delivery, setup, branding, and post-event reporting so organizers focus on their event.","provider":{"@type":"Organization","name":"ZenSpace Event Solutions","url":"https://www.zenspaceevents.com"},"serviceType":"Event Equipment Rental","areaServed":{"@type":"Country","name":"United States"},"url":"https://www.zenspaceevents.com/event-organizers"}
```

### /venues (Score: 8 → 8.5+)
Strong page (3,872 words, 4 H2s).

```json
{"@context":"https://schema.org","@type":"Service","name":"ZenSpace Event Pods for Venues and Convention Centers","description":"IoT-enabled meeting pods that transform convention center lobbies and exhibit halls into private meeting zones. ZenSpace partners with venues to offer branded, bookable pods for conferences and trade shows.","provider":{"@type":"Organization","name":"ZenSpace Event Solutions","url":"https://www.zenspaceevents.com"},"serviceType":"Venue Partnership Program","areaServed":{"@type":"Country","name":"United States"},"url":"https://www.zenspaceevents.com/venues"}
```

### /exhibitors (Score: 8 → 8.5+)

```json
{"@context":"https://schema.org","@type":"Service","name":"Trade Show Exhibitor Meeting Pods","description":"Private meeting pods for trade show exhibitors. Replace expensive hospitality suites with ZenSpace pods — private, branded, tech-enabled meeting spaces starting at $900/day.","provider":{"@type":"Organization","name":"ZenSpace Event Solutions","url":"https://www.zenspaceevents.com"},"serviceType":"Trade Show Equipment Rental","areaServed":{"@type":"Country","name":"United States"},"url":"https://www.zenspaceevents.com/exhibitors"}
```

### /corporate (Score: 7.2 → 7.8+)
Also fix title: trim from 61 chars to ≤60. Ensure "corporate meeting pod" is in title front half.

```json
{"@context":"https://schema.org","@type":"Service","name":"Corporate Event Meeting Pod Rental","description":"ZenSpace smart meeting pods for corporate events, conferences, and off-site meetings. Private, branded pods with smart E-glass, wireless screen sharing, and AI-powered booking software.","provider":{"@type":"Organization","name":"ZenSpace Event Solutions","url":"https://www.zenspaceevents.com"},"serviceType":"Corporate Event Equipment","areaServed":{"@type":"Country","name":"United States"},"url":"https://www.zenspaceevents.com/corporate"}
```

### /booking-software (Score: 7.2 → 7.8+)

```json
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"ZenSpace Event Pod Booking Software","description":"Cloud-based platform for managing event pod reservations without additional on-site staff. Includes branded booking website, real-time dashboards, AI monitoring alerts, and post-event lead generation reports.","applicationCategory":"BusinessApplication","operatingSystem":"Web-based","provider":{"@type":"Organization","name":"ZenSpace Event Solutions"},"url":"https://www.zenspaceevents.com/booking-software"}
```

### /contacts (Score: 7.5 → 8.0+)

```json
{"@context":"https://schema.org","@type":"ContactPage","name":"Contact ZenSpace Event Solutions","description":"Get a quote for event pod rental. ZenSpace serves Las Vegas, Chicago, Orlando, New York, San Francisco, Atlanta, Baltimore, and Dallas. Response within 24 hours.","url":"https://www.zenspaceevents.com/contacts","mainEntity":{"@type":"Organization","name":"ZenSpace Event Solutions","email":"info@zenspace.io","url":"https://www.zenspaceevents.com","contactPoint":{"@type":"ContactPoint","contactType":"sales","email":"info@zenspace.io","areaServed":"US","availableLanguage":"English"}}}
```

### /blog (Score: 8 → 8.5+)

```json
{"@context":"https://schema.org","@type":"Blog","name":"ZenSpace Event Technology Blog","description":"Insights on event pods, trade show technology, and smart event management from ZenSpace Event Solutions.","url":"https://www.zenspaceevents.com/blog","publisher":{"@type":"Organization","name":"ZenSpace Event Solutions","url":"https://www.zenspaceevents.com"}}
```

### /attendees, /sponsors, /partnerships, /our-process, /other-products, /design-hub
All these score 7-8 with single issue: no schema. Apply **Service** or **WebPage** schema to each:

```json
{"@context":"https://schema.org","@type":"WebPage","name":"[Page name]","description":"[Existing meta description]","url":"https://www.zenspaceevents.com/[slug]","isPartOf":{"@type":"WebSite","name":"ZenSpace Event Solutions","url":"https://www.zenspaceevents.com"}}
```

---

## 🟡 PRIORITY 3 — Content Depth on Thin Product Pages (1–2 hrs writing)

Four pod pages are thin (~2,200 words each). Competitors like Nook have 3,500+ words on product pages. The fix is adding a structured content section to each page.

**Pages affected:**
- /1-seater (2,276 words → target 3,000+)
- /6-seater (2,288 words → target 3,000+)
- /aura-gather (2,289 words → target 3,000+)
- /digital-kiosk (2,297 words → target 3,000+)

**Section to add to each (in Wix Editor → add rich text section):**

```
H2: Frequently Asked Questions — [Pod Type]
Q: How does [pod type] fit into my event floor plan?
Q: What's included in the rental price?
Q: How quickly can I get a quote?
Q: Can I customize the branding on the [pod type]?

H2: Ideal Events for the [Pod Type]
[3-4 sentence paragraph with keyword-rich use cases]

H2: Compare [Pod Type] to Other ZenSpace Models
[brief comparison paragraph + internal links to other pod pages]
```

This approach adds 700-900 words of genuine value per page AND adds FAQ structure that AI systems love to cite.

---

## 🟡 PRIORITY 4 — Title Tag Optimization

Two pages have truncating title tags (over 60 characters):

| Page | Current | Issue | Fix |
|------|---------|-------|-----|
| /corporate | ~61 chars | Google truncates | Trim to ≤60ch |
| /post/smart-e-glass | ~65 chars | Truncates | Trim to ≤60ch |

**Steps:** Wix Editor → page → gear icon → SEO Basics → "What's the page called?" field → edit → Save

**Suggested titles:**
- /corporate: `Corporate Meeting Pods for Events | ZenSpace` (45 chars) ✅
- /post/smart-e-glass: `Smart E-Glass Event Pods Explained | ZenSpace` (46 chars) ✅

---

## 🟢 PRIORITY 5 — Internal Linking Improvements

The site has low internal link density across service pages. Add cross-links using these natural anchors:

**High-value links to add:**
- From /event-organizers → /faq (anchor: "event pod rental FAQ")
- From /exhibitors → /case-studies (anchor: "see how we've served exhibitors")
- From /corporate → /booking-software (anchor: "our event booking software")
- From /blog posts → relevant pod product pages
- From all case study pages → /case-studies index

**In Wix:** Click any text → highlight phrase → link icon → internal page → select page

---

## 📊 Expected Score Improvements After All Fixes

| Page Group | Before | After | Key Change |
|-----------|--------|-------|-----------|
| Case study pages (6) | 5.0 | 7.5 | H2 structure added |
| Blog posts (4) | 5.0–5.5 | 6.5 | Meta descs done in Phase 1 |
| Strong service pages (8) | 8.0 | 8.5 | Schema added |
| Product pages (6) | 7.0–7.5 | 8.0 | Content expanded + schema |
| **Site average** | **6.7** | **7.8** | |

---

## 🏙️ PHASE 2 TRACK 2 — City/Local SEO Pages

See: `zenspace-city-seo-strategy.md`

---

## Verification Checklist

After completing fixes:
1. Run `verify-seo-fixes.ps1` (with 3000ms delay) from Downloads folder
2. Test rich results: https://search.google.com/test/rich-results?url=https://www.zenspaceevents.com/[page]
3. Re-score 5 priority pages in Notion On-Page Audit database
4. Set baseline SERP rankings for city page target keywords
