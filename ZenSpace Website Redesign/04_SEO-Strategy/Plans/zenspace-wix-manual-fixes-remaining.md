# ZenSpace Wix Manual Fixes — Remaining 17 Fixes
**Date:** April 12, 2026 | **Est. Time:** ~45 min | **Impact:** Schema 27% → 100%

---

## ✅ Already Done (No Action Needed)

| Fix | What Was Done | How |
|-----|--------------|-----|
| Fix 1 | AI bots added to robots.txt (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) | Wix API |
| Fix 16 | Smart E-Glass blog meta description set | Blog API |
| Fix 17 | Corporate Events blog meta description set | Blog API |
| Fix 18 | Non-Profit Events blog meta description set | Blog API |
| Fix 21 | Homepage schema CONFIRMED WORKING — both Organization + LocalBusiness live | Verified live |

---

## 🔴 PRIORITY 1 — Do First (15 min, highest impact)

### Fix 2: Fix Homepage H1 — Change "250+" and "15+" from H1 to H2 (5 min)
**Why:** Multiple H1s dilute keyword signal. Google expects exactly 1 H1 per page.

1. Open **Wix Editor** → click the **Homepage**
2. Find the text **"250+"** → click it → change style from **Heading 1** → **Heading 2**
3. Find the text **"15+"** → click it → change style from **Heading 1** → **Heading 2**
4. Verify only **"Smart Event Pod Rentals for Trade Shows, Conferences & Events"** remains as H1
5. Click **Publish**

---

### Fix 3: FAQPage Schema on /faq (5 min)
**Why:** Triggers FAQ rich results (huge SERP real estate) + AI systems love this format for citations.

1. Wix Editor → click **FAQ page** in left page list
2. Click **gear icon** (Page Settings) → **SEO (Google)** → **Advanced SEO**
3. Click **Structured Data Markup** → **Edit**
4. Paste this JSON (replace any existing content):

```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to rent an event pod?","acceptedAnswer":{"@type":"Answer","text":"ZenSpace Event Pod rental pricing starts at approximately $900 per pod per event day, with a one-time relocation fee of around $500 per pod. Pricing varies based on the number of pods, event duration, and customization requirements."}},{"@type":"Question","name":"What types of event pods does ZenSpace offer?","acceptedAnswer":{"@type":"Answer","text":"ZenSpace offers six pod models: 1-Seater privacy pod, 4-Seater meeting pod, 6-Seater conference pod, Element ADA accessible pod, Aura Gather collaborative pod, and Digital Kiosks for wayfinding and branding."}},{"@type":"Question","name":"How long does pod setup take?","acceptedAnswer":{"@type":"Answer","text":"Under 30 minutes per pod. ZenSpace handles delivery, placement, power connection, branding verification, and full system testing."}},{"@type":"Question","name":"What smart features are included?","acceptedAnswer":{"@type":"Answer","text":"Every pod includes -29dB acoustic privacy, 32-inch TV with USB-C and HDMI, Wi-Fi, smart LED lighting with CRI 92, ventilation, and charging stations. Advanced models add smart E-glass, wireless screen sharing via Airtame, digital signage, and AI-powered monitoring alerts."}},{"@type":"Question","name":"Do you deliver nationwide?","acceptedAnswer":{"@type":"Answer","text":"Yes. ZenSpace has delivered 250+ events across the United States including Las Vegas, Chicago, Orlando, New York, San Francisco, Atlanta, Baltimore, and Dallas."}},{"@type":"Question","name":"Can pods be customized with branding?","acceptedAnswer":{"@type":"Answer","text":"Yes. Custom graphics on windows, walls, doors, and center tables. Digital branding through built-in 32-inch screens. Branded booking pages. Graphics professionally installed before shipping. Starts at $200 per panel."}},{"@type":"Question","name":"Are pods ADA-compliant?","acceptedAnswer":{"@type":"Answer","text":"Yes. The Element ADA pod features wider doorways, accessible interior layout, and all standard smart features. All ZenSpace pods are UL-certified for electrical safety."}},{"@type":"Question","name":"What is ZenSpace Booking Software?","acceptedAnswer":{"@type":"Answer","text":"A cloud-based platform that manages pod reservations without additional on-site staff. Includes a branded booking website, real-time utilization dashboards, AI monitoring alerts, and comprehensive post-event reports with lead generation data."}}]}
```

5. Click **Save** → **Publish**

---

## 🟠 PRIORITY 2 — Product Schemas (15 min)
**For each page below:** Wix Editor → click page → gear icon → SEO (Google) → Advanced SEO → Structured Data Markup → Edit → Paste JSON → Save

### Fix 4: /1-seater

```json
{"@context":"https://schema.org","@type":"Product","name":"ZenSpace 1-Seater Event Pod","description":"Compact single-person privacy pod for trade shows and conferences. Features -29dB acoustic privacy, 32-inch TV monitor with USB-C and HDMI, smart LED lighting with CRI 92, ventilation, charging stations, and mobility casters for easy repositioning.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Capacity","value":"1 person"},{"@type":"PropertyValue","name":"Acoustic Privacy","value":"Over -29dB"},{"@type":"PropertyValue","name":"Display","value":"32-inch TV with USB-C and HDMI"},{"@type":"PropertyValue","name":"Setup Time","value":"Under 30 minutes"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/1-seater"}}
```

### Fix 5: /4-seater

```json
{"@context":"https://schema.org","@type":"Product","name":"ZenSpace 4-Seater Event Pod","description":"Lightweight 4-person meeting pod for events. Interior: 81.8in W x 54.24in D x 66in H, 35.5 sq ft. Features -29dB acoustic privacy, smart E-glass, wireless screen sharing, 32-inch TV, built-in bench seating and work surface.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Capacity","value":"4 persons"},{"@type":"PropertyValue","name":"Interior Dimensions","value":"81.8in W x 54.24in D x 66in H"},{"@type":"PropertyValue","name":"Floor Space","value":"35.5 sq ft"},{"@type":"PropertyValue","name":"Work Surface","value":"219.7in W x 39.4in D"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/4-seater"}}
```

### Fix 6: /6-seater

```json
{"@context":"https://schema.org","@type":"Product","name":"ZenSpace 6-Seater Event Pod","description":"Spacious 6-person conference pod for presentations and group meetings. Features -29dB acoustic privacy, smart E-glass, wireless screen sharing via Airtame, 32-inch TV, digital signage, and AI-powered monitoring alerts.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Capacity","value":"6 persons"},{"@type":"PropertyValue","name":"Acoustic Privacy","value":"Over -29dB"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/6-seater"}}
```

### Fix 7: /ada-pod

```json
{"@context":"https://schema.org","@type":"Product","name":"ZenSpace Element ADA Event Pod","description":"ADA-compliant wheelchair-accessible meeting pod for events. Features wider doorways, accessible interior layout, -29dB acoustic privacy, all standard smart features, and UL electrical safety certification.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Accessibility","value":"ADA-compliant"},{"@type":"PropertyValue","name":"Certification","value":"UL-certified"},{"@type":"PropertyValue","name":"Acoustic Privacy","value":"Over -29dB"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/ada-pod"}}
```

### Fix 8: /aura-gather

```json
{"@context":"https://schema.org","@type":"Product","name":"ZenSpace Aura Gather Pod","description":"Multi-person collaborative meeting pod for sponsor activations, VIP networking, and team huddles. Semi-open design with acoustic treatment, smart E-glass, wireless screen sharing, and digital signage.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/aura-gather"}}
```

### Fix 9: /digital-kiosk

```json
{"@context":"https://schema.org","@type":"Product","name":"ZenSpace Digital Kiosk","description":"Interactive digital kiosk for event wayfinding, sponsor branding, and attendee engagement. Displays event agendas, venue maps, real-time alerts, and rotating sponsor content.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Technology","offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/digital-kiosk"}}
```

---

## 🟠 PRIORITY 3 — Meta Descriptions for Static Pages (10 min)
**Steps:** Wix Editor → click page → gear icon → SEO (Google) → paste in "What's this page about?" field → Save

### Fix 10: /case-studies
```
See how ZenSpace event pods transformed trade shows and conferences. Real results from IMEX, Expo! Expo!, IAVM VenueConnect, and more. 250+ events delivered.
```

### Fix 11: /case-studies/imex
```
How ZenSpace deployed smart meeting pods at IMEX, one of the worlds largest meetings industry trade shows. See the setup, results, and attendee experience.
```

### Fix 12: /case-studies/expo-expo
```
ZenSpace event pods at Expo! Expo! — IAEE annual exhibition. Discover how smart pods created private meeting spaces for event professionals.
```

### Fix 13: /case-studies/iavm
```
ZenSpace meeting pods at IAVM VenueConnect. IoT-enabled pods provided quiet, bookable workspaces for venue management professionals.
```

### Fix 14: /case-studies/inspire
```
ZenSpace event pods at ILHA INSPIRE. Smart meeting pods enhanced the attendee experience with private, tech-enabled spaces.
```

### Fix 15: /case-studies/ths
```
ZenSpace event pods at The Hospitality Show. Smart meeting pods delivered private meeting spaces for hospitality industry leaders.
```

---

## 🟡 PRIORITY 4 — Heading Fixes on Legal Pages (5 min)

### Fix 19: Add H1 to /privacy-policy
Wix Editor → Privacy Policy page → Add text "**Privacy Policy**" at the very top of the page content → set style to **Heading 1** → Publish

### Fix 20: Add H1 to /terms-conditions
Wix Editor → Terms & Conditions page → Add text "**Terms & Conditions**" at the very top → set style to **Heading 1** → Publish

---

## 🟡 PRIORITY 5 — Image Alt Text (ongoing, 2+ hrs)

### Fix 22: Image alt text — 447 of 704 images missing
Wix Editor → click image → Settings icon → fill "What's in the image?" field

**Formula:** `[What the image shows] — [ZenSpace brand context]`

**Examples:**
- `ZenSpace 4-seater meeting pod at trade show with custom branding`
- `Attendees using ZenSpace pod for private meeting at IMEX conference`
- `ZenSpace event pod interior showing 32-inch TV and bench seating`

**Batch order (most impact first):**
1. Homepage hero images — 5 images, ~10 min
2. Pod product pages (/1-seater through /digital-kiosk) — ~42 images, ~30 min
3. Case study event photos — ~300 images, ~1-2 hrs
4. Remaining service pages — ~100 images, ~30 min

---

## After All Fixes — Verify

1. **Publish** the Wix site
2. Re-run `verify-seo-fixes.ps1` (edit to change `Start-Sleep -Milliseconds 800` → `Start-Sleep -Milliseconds 3000`)
3. Test rich results:
   - [Homepage](https://search.google.com/test/rich-results?url=https://www.zenspaceevents.com)
   - [FAQ page](https://search.google.com/test/rich-results?url=https://www.zenspaceevents.com/faq)
   - [4-Seater](https://search.google.com/test/rich-results?url=https://www.zenspaceevents.com/4-seater)

---

## Summary Scoreboard

| Category | Fixes | Est. Time |
|----------|-------|-----------|
| ✅ Done via API | 5 (1, 16, 17, 18, 21) | 0 min |
| 🔴 Priority 1 (do first) | 2 (2, 3) | 10 min |
| 🟠 Priority 2 | 6 (4-9) | 15 min |
| 🟠 Priority 3 | 6 (10-15) | 10 min |
| 🟡 Priority 4 | 2 (19-20) | 5 min |
| 🟡 Priority 5 | 1 (22) | 2+ hrs |
| **Total remaining** | **17 fixes** | **~45 min** |
