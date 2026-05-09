# ZenSpace SEO Audit — April 13, 2026
**Domain:** zenspaceevents.com | **Scope:** Full site (pre-publish gate check)
**Skill:** marketing:seo-audit | **Triggered by:** Final check before content publishing sprint

---

## Executive Summary

ZenSpace has a strong product story and unique first-party performance data — but only ~10 pages indexed, zero content hub, and the primary keyword target ("event pod rental") has no live page. Nook's competing event page has a weak title and no data transparency; ZenSpace's v2 page is significantly stronger. Three actions unlock immediate ranking opportunity: publish `/event-pod-rental`, fix homepage city schema error, and canonical the `/home` duplicate.

**Overall health: Needs work — but competitive gap is winnable in 60 days.**

---

## 🚨 Three Critical Fixes Before Anything Else

1. **Publish `/event-pod-rental` v2** — content done, schema ready, SERP wide open
2. **Fix homepage schema** — remove Chicago/Atlanta/Dallas, add Las Vegas/Orlando/SF Bay/New York
3. **Canonical `/home` → root** — two indexable homepages splits PageRank

---

## Keyword Opportunities (Top 18)

| Keyword | Vol | Difficulty | Opportunity | Status | Content |
|---|---|---|---|---|---|
| event pod rental | 300–600 | Medium | 🔴 High | Not ranked | `/event-pod-rental` ← READY |
| meeting pod rental trade show | 100–300 | Low–Med | 🔴 High | Not ranked | `/event-pod-rental` |
| trade show meeting pod | 200–400 | Medium | 🔴 High | Not ranked | Pillar page |
| soundproof meeting pod rental | 100–200 | Low | 🟡 High | Not ranked | `/event-pod-rental` |
| mobile meeting space trade show | 200–400 | Medium | 🔴 High | Not ranked | City pages |
| conference pod rental | 100–200 | Low | 🟡 High | Not ranked | `/event-pod-rental` |
| event pod Las Vegas | 50–150 | Low | 🔴 High | Not ranked | `/event-pods-las-vegas` |
| event pod Orlando | 50–100 | Low | 🔴 High | Not ranked | `/event-pods-orlando` |
| meeting pods booth alternative | 50–100 | Low | 🟡 High | Not ranked | Comparison page |
| what is an event pod | 100–200 | Low | 🟡 Med | Not ranked | Blog (written) |
| event pod vs trade show booth | 50–100 | Low | 🟢 Med | Not ranked | `/event-pod-rental` v2 |
| sponsor activation trade show | 100–200 | Medium | 🟡 Med | Not ranked | Blog |
| trade show booth technology 2026 | 100–200 | Medium | 🟡 Med | Not ranked | Blog |
| event pod San Francisco | 50–100 | Low | 🔴 High | Not ranked | `/event-pods-sf-bay-area` |
| event pod New York | 50–100 | Low | 🔴 High | Not ranked | `/event-pods-new-york` |
| ZenSpace event pods | Branded | Very Low | 🟢 High | Top 3 | Homepage |
| IMEX exhibitor meeting space | 50–100 | Low | 🟢 Med | Not ranked | Case study |
| trade show pod ADA compliant | 50–100 | Low | 🟢 Med | Not ranked | `/event-pod-rental` v2 |

---

## On-Page Issues

| Page | Issue | Severity | Fix |
|---|---|---|---|
| Homepage | Schema lists Chicago, Atlanta, Dallas | 🔴 Critical | Update areaServed in JSON-LD |
| `/home` | Duplicate of root homepage | 🔴 Critical | Add canonical → root |
| All pages | H1 JS-injected, not server-rendered | 🔴 Critical | Wix: ensure heading in page source |
| `/event-pod-rental` | Page does not exist | 🔴 Critical | Publish v2 today |
| Homepage | Meta description from JSON-LD only | 🟠 High | Add `<meta name="description">` in Wix |
| City pages | None exist | 🟠 High | Build 4 city pages (Apr 20–21) |
| Blog | No content hub | 🟠 High | Publish pillar Apr 18–19 |
| Internal links | Zero cross-page links observed | 🟠 High | Link all pages after publish |
| Homepage | Title 63 chars, not keyword-first | 🟡 Medium | → `Event Pod Rentals for Trade Shows \| ZenSpace` |
| All pages | Zero image alt text | 🟡 Medium | Add descriptive alts to all pod images |

---

## Content Gap vs Competitors

| Missing Content | Competitor Coverage | Priority | Status |
|---|---|---|---|
| `/event-pod-rental` | Nook: weak page, bad title | 🔴 High | ✅ Ready to publish |
| 4 city pages | Nobody has them | 🔴 High | Write Apr 20–21 |
| "What Is an Event Pod?" | None | 🟠 High | ✅ Written, publish Apr 19 |
| "ZenSpace vs Nook" | None | 🟠 High | Apr 23 |
| "Best Event Pods 2026" | None | 🟠 High | Apr 23 |
| IMEX case study | None | 🟡 Med | May |
| Sponsor revenue blog | None | 🟡 Med | Apr 28 |
| ROI calculator | None | 🟡 Med | June |

---

## Technical SEO Checklist

| Check | Status | Action |
|---|---|---|
| HTTPS | ✅ Pass | None |
| Mobile responsive | ✅ Pass | None |
| XML sitemap submitted | ⚠️ Warning | Verify in Google Search Console |
| robots.txt | ⚠️ Warning | Confirm no accidental Disallow |
| Canonical tags | 🔴 Fail | Fix /home duplicate |
| Server-rendered H1 | 🔴 Fail | Wix fix required |
| Meta description tags | 🔴 Fail | Add via Wix SEO Basics |
| Structured data | ⚠️ Warning | Fix city error; publish event-pod-rental schema |
| LCP (Core Web Vitals) | ⚠️ Warning | Compress hero images to WebP |
| CLS | ✅ Likely Pass | Monitor after publishing |
| Internal links | 🔴 Fail | None observed between pages |
| Image alt text | 🔴 Fail | Add to all images |
| Breadcrumb schema | ⚠️ Missing | Add BreadcrumbList to all pages |
| GSC verification | ⚠️ Unknown | Confirm |

---

## Competitor Snapshot

| Dimension | ZenSpace | Nook | Skyline |
|---|---|---|---|
| Pages indexed | ~10 | ~50+ | ~200+ |
| "event pod rental" optimized page | ❌ (publishing today) | ⚠️ Weak | ⚠️ Moderate |
| City pages | ❌ | ❌ | ❌ |
| Pricing transparency | ✅ v2 | ❌ | ❌ |
| FAQ schema | ✅ v2 | ❌ | ❌ |
| ROI/performance data | ✅ v2 | ❌ | ❌ |
| Domain authority | 🔴 Low | 🟡 Moderate | 🟢 High |
| Technical SEO | 🔴 Issues | ⚠️ Moderate | ✅ Strong |
| Blog / content hub | ❌ | ⚠️ Minimal | ✅ Active |

**Key insight:** Nook's `/event` page title is "Booths and Pods For Office & Home" — they are NOT competing for "event pod rental" in title tags. ZenSpace's v2 page is better structured, more data-rich, and has schema. Once published, it should outrank Nook within 30–60 days.

---

## Quick Wins — Do This Week

- [ ] **Publish `/event-pod-rental` v2** (Wix + schema paste) — 30 min — Impact: 🔴 High
- [ ] **Fix homepage schema cities** (Chicago → Las Vegas, etc.) — 15 min — Impact: 🔴 High
- [ ] **Canonical `/home` → root** (Wix Advanced SEO) — 10 min — Impact: 🔴 High
- [ ] **Update homepage title tag** (keyword-first, 58 chars) — 5 min — Impact: 🟠 High
- [ ] **Add homepage meta description** (`<meta>` tag, not just JSON-LD) — 5 min — Impact: 🟠 High
- [ ] **Submit sitemap in Google Search Console** — 10 min — Impact: 🟠 High
- [ ] **Add image alt text** to all pod photos — 30 min — Impact: 🟡 Medium

## Strategic Investments — April–May

- [ ] Publish 4 city pages (Apr 20–21) — Impact: 🔴 High
- [ ] Publish blog pillar: "What Is an Event Pod?" (Apr 19) — Impact: 🟠 High
- [ ] Publish "ZenSpace vs Nook" + "Best Event Pods 2026" (Apr 23) — Impact: 🟠 High
- [ ] Build internal linking web after all pages live — Impact: 🟠 High
- [ ] Investigate and fix JS-rendered H1 on homepage — Impact: 🔴 High
- [ ] Add BreadcrumbList schema to all pages — Impact: 🟡 Medium
- [ ] Publish IMEX America case study (May) — Impact: 🟡 Medium
- [ ] "Sponsor Revenue from Event Pods" blog (Apr 28) — Impact: 🟡 Medium
