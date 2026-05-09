#!/usr/bin/env python3
"""
SEO Agent — Task Queue
Every SEO fix as a structured task with code, Wix instructions, and plain-language explanation.
"""

TASKS = [
    # ──────────────── PRIORITY 1: CRITICAL (Day 1) ────────────────
    {
        "id": "org_schema",
        "name": "Organization Schema (All Pages)",
        "priority": 1,
        "category": "Schema Markup",
        "time_estimate": "5 min",
        "plain_explanation": (
            "This tells Google and AI systems who ZenSpace is — your name, "
            "what you do, and where to find you online. Think of it as your "
            "digital business card. Nook has this on every page. You don't. "
            "This is the #1 gap between you and them."
        ),
        "wix_steps": [
            "1. Go to Wix Dashboard",
            "2. Click 'Settings' in the left sidebar",
            "3. Click 'Custom Code'",
            "4. Click '+ Add Custom Code'",
            "5. Paste the code below",
            "6. Name it: 'Organization Schema'",
            "7. Set 'Add Code to Pages': All Pages",
            "8. Set 'Place Code in': Head",
            "9. Click Apply",
        ],
        "code": '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ZenSpace Event Solutions",
  "alternateName": "ZenSpace Events",
  "url": "https://www.zenspaceevents.com",
  "logo": "https://www.zenspaceevents.com/logo.png",
  "description": "ZenSpace Event Solutions provides premium IoT-enabled meeting pod rentals for trade shows, conferences, and corporate events. Since 2017, we have delivered 250+ events with smart, soundproof, mobile pods featuring booking software, digital branding, and lead capture technology.",
  "foundingDate": "2017",
  "email": "info@zenspace.io",
  "areaServed": {"@type": "Country", "name": "United States"},
  "serviceType": ["Event Pod Rental", "Meeting Pod Rental", "Booking Software", "Digital Branding Solutions"],
  "knowsAbout": ["event pods", "meeting pods", "trade show technology", "conference pods", "IoT event solutions"],
  "sameAs": [
    "https://www.linkedin.com/company/zenspace-event-solutions",
    "https://www.instagram.com/zenspaceevents"
  ]
}
</script>''',
        "verify_url": "https://search.google.com/test/rich-results?url=https://www.zenspaceevents.com",
        "auto_executable": False,
    },

    {
        "id": "local_biz_schema",
        "name": "LocalBusiness Schema (All Pages)",
        "priority": 1,
        "category": "Schema Markup",
        "time_estimate": "5 min",
        "plain_explanation": (
            "This tells Google you serve real locations. It powers 'near me' searches "
            "and Google Maps results. When someone searches 'event pod rental Las Vegas', "
            "this is what makes you show up."
        ),
        "wix_steps": [
            "1. Go to Wix Dashboard → Settings → Custom Code",
            "2. Click '+ Add Custom Code'",
            "3. Paste the code below",
            "4. Name it: 'LocalBusiness Schema'",
            "5. Set 'Add Code to Pages': All Pages",
            "6. Set 'Place Code in': Head",
            "7. Click Apply",
        ],
        "code": '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "ZenSpace Event Solutions",
  "url": "https://www.zenspaceevents.com",
  "description": "Premium IoT-enabled meeting pod rentals for trade shows, conferences, and corporate events. Full-service delivery including setup, branding, and on-site support.",
  "email": "info@zenspace.io",
  "priceRange": "$$-$$$",
  "areaServed": [
    {"@type": "City", "name": "Las Vegas"},
    {"@type": "City", "name": "Chicago"},
    {"@type": "City", "name": "Orlando"},
    {"@type": "City", "name": "New York"},
    {"@type": "City", "name": "San Francisco"},
    {"@type": "City", "name": "Atlanta"},
    {"@type": "City", "name": "Baltimore"},
    {"@type": "City", "name": "Dallas"}
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Event Pod Rentals",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "1-Seater Event Pod Rental"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "4-Seater Event Pod Rental"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "6-Seater Event Pod Rental"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "ADA Event Pod Rental"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Aura Gather Pod Rental"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "ZenSpace Booking Software"}}
    ]
  }
}
</script>''',
        "auto_executable": False,
    },

    {
        "id": "robots_ai_bots",
        "name": "Allow AI Bots in robots.txt",
        "priority": 1,
        "category": "AIEO/GEO",
        "time_estimate": "2 min",
        "plain_explanation": (
            "This tells ChatGPT, Claude, and Perplexity they're allowed to read your site. "
            "If they can't read it, they can't recommend you. Neither you nor Nook have this — "
            "whoever does it first gets cited first."
        ),
        "wix_steps": [
            "1. Go to Wix Dashboard",
            "2. Click 'Marketing & SEO' in the left sidebar",
            "3. Click 'SEO Tools'",
            "4. Click 'robots.txt Editor'",
            "5. ADD these lines at the end (don't delete existing content)",
            "6. Click Save",
        ],
        "code": '''User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /''',
        "auto_executable": False,
    },

    # ──────────────── PRIORITY 1: FAQ SCHEMA (Day 2) ────────────────
    {
        "id": "faq_schema",
        "name": "FAQPage Schema (/faq page)",
        "priority": 1,
        "category": "Schema Markup",
        "time_estimate": "5 min",
        "plain_explanation": (
            "This tells Google your FAQ page has questions and answers. Google shows them "
            "as expandable dropdowns right in search results — taking up huge space. "
            "AI systems LOVE this format for citing sources. Neither you nor Nook have this. "
            "First mover wins."
        ),
        "wix_steps": [
            "1. Open Wix Editor",
            "2. Navigate to the FAQ page",
            "3. Click the gear icon (Page Settings)",
            "4. Go to 'SEO (Google)' tab",
            "5. Scroll to 'Advanced SEO'",
            "6. Find 'Structured Data Markup' and click Edit",
            "7. Paste the JSON below (WITHOUT the script tags)",
            "8. Save and Publish",
        ],
        "code": '''{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does it cost to rent an event pod?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ZenSpace Event Pod rental pricing starts at approximately $900 per pod per event day, with a one-time relocation fee of around $500 per pod. Pricing varies based on the number of pods, event duration, and customization. Contact us for a custom quote."
      }
    },
    {
      "@type": "Question",
      "name": "What types of event pods does ZenSpace offer?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ZenSpace offers six pod models: 1-Seater privacy pod, 4-Seater meeting pod, 6-Seater conference pod, Element ADA pod for wheelchair accessibility, Aura Gather pod for collaborative settings, and Digital Kiosks for wayfinding and sponsor branding."
      }
    },
    {
      "@type": "Question",
      "name": "How long does pod setup take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "ZenSpace event pods can be set up in under 30 minutes per pod. Our full-service team handles delivery, placement, branding installation, and technical setup. We also manage teardown after your event."
      }
    },
    {
      "@type": "Question",
      "name": "What features are included in ZenSpace pods?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Every pod includes certified acoustic privacy (over -29dB), 32-inch TV monitor with USB-C and HDMI, Wi-Fi, premium smart LED lighting (CRI 92), ventilation, charging stations, and mobility casters. Advanced models add smart E-glass, wireless screen sharing, digital signage, and AI monitoring."
      }
    },
    {
      "@type": "Question",
      "name": "Do you deliver nationwide?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. ZenSpace delivers event pods across the United States. We have deployed pods at 250+ events since 2017 in Las Vegas, Chicago, Orlando, New York, Atlanta, Baltimore, Dallas, Los Angeles, Boston, and San Francisco."
      }
    },
    {
      "@type": "Question",
      "name": "Can pods be customized with our branding?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. ZenSpace offers custom graphics on pod windows, walls, doors, and tables. Digital branding is available through built-in screens. Graphics are installed at our warehouse before shipping. Pricing starts at $200 per panel."
      }
    },
    {
      "@type": "Question",
      "name": "Are the pods ADA-compliant?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. The Element ADA pod is designed for wheelchair accessibility with wider entry and accessible interior. All ZenSpace pods are UL-certified for electrical safety."
      }
    },
    {
      "@type": "Question",
      "name": "What is ZenSpace Booking Software?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A cloud-based platform managing pod reservations without extra staff. Includes branded booking website per event, real-time dashboards, AI monitoring alerts, and post-event utilization reports with lead generation data."
      }
    }
  ]
}''',
        "verify_url": "https://search.google.com/test/rich-results?url=https://www.zenspaceevents.com/faq",
        "auto_executable": False,
    },

    # ──────────────── META DESCRIPTIONS (Day 2) ────────────────
    {
        "id": "meta_case_studies",
        "name": "Add Meta Description: /case-studies",
        "priority": 2,
        "category": "Meta Tags",
        "time_estimate": "2 min",
        "plain_explanation": (
            "This page has no meta description — Google is writing its own snippet for you, "
            "probably badly. This tells Google exactly what to show when someone finds this page."
        ),
        "wix_steps": [
            "1. Open Wix Editor → click Case Studies page",
            "2. Click gear icon (Page Settings)",
            "3. Go to 'SEO (Google)' tab",
            "4. In 'What's this page about?' paste the text below",
            "5. Save",
        ],
        "code": "See how ZenSpace event pods transformed trade shows and conferences. Real results from IMEX, Expo! Expo!, IAVM VenueConnect, and more. 250+ events delivered.",
        "auto_executable": False,
    },
    {
        "id": "meta_imex",
        "name": "Add Meta Description: /case-studies/imex",
        "priority": 2,
        "category": "Meta Tags",
        "time_estimate": "2 min",
        "plain_explanation": "Case study page missing its meta description. This tells Google what to show in search results.",
        "wix_steps": ["Same as above — Page Settings → SEO → 'What's this page about?'"],
        "code": "How ZenSpace deployed smart meeting pods at IMEX, one of the world's largest meetings industry trade shows. See the setup, results, and attendee experience.",
        "auto_executable": False,
    },
    {
        "id": "meta_expo",
        "name": "Add Meta Description: /case-studies/expo-expo",
        "priority": 2,
        "category": "Meta Tags",
        "time_estimate": "2 min",
        "plain_explanation": "Case study page missing its meta description.",
        "wix_steps": ["Page Settings → SEO → 'What's this page about?'"],
        "code": "ZenSpace event pods at Expo! Expo! — IAEE's annual exhibition. Discover how smart pods created private meeting spaces for event professionals.",
        "auto_executable": False,
    },
    {
        "id": "meta_iavm",
        "name": "Add Meta Description: /case-studies/iavm",
        "priority": 2, "category": "Meta Tags", "time_estimate": "2 min",
        "plain_explanation": "Case study page missing its meta description.",
        "wix_steps": ["Page Settings → SEO → 'What's this page about?'"],
        "code": "ZenSpace meeting pods at IAVM VenueConnect. See how IoT-enabled pods provided quiet, bookable workspaces for venue management professionals.",
        "auto_executable": False,
    },
    {
        "id": "meta_inspire",
        "name": "Add Meta Description: /case-studies/inspire",
        "priority": 2, "category": "Meta Tags", "time_estimate": "2 min",
        "plain_explanation": "Case study page missing its meta description.",
        "wix_steps": ["Page Settings → SEO → 'What's this page about?'"],
        "code": "ZenSpace event pods at ILHA INSPIRE. Learn how smart meeting pods enhanced the attendee experience with private, tech-enabled spaces.",
        "auto_executable": False,
    },
    {
        "id": "meta_ths",
        "name": "Add Meta Description: /case-studies/ths",
        "priority": 2, "category": "Meta Tags", "time_estimate": "2 min",
        "plain_explanation": "Case study page missing its meta description.",
        "wix_steps": ["Page Settings → SEO → 'What's this page about?'"],
        "code": "ZenSpace event pods at The Hospitality Show. See how our smart meeting pods delivered private meeting spaces for hospitality industry leaders.",
        "auto_executable": False,
    },
    {
        "id": "meta_blog1",
        "name": "Add Meta Description: Smart E-Glass blog post",
        "priority": 2, "category": "Meta Tags", "time_estimate": "2 min",
        "plain_explanation": "Blog post missing its meta description.",
        "wix_steps": ["Blog Editor → click post → SEO Settings (left panel) → Description"],
        "code": "Meet ZenSpace Smart E-Glass — switch from transparent to opaque at the touch of a button. The latest in event pod technology for trade shows and conferences.",
        "auto_executable": False,
    },
    {
        "id": "meta_blog2",
        "name": "Add Meta Description: Corporate Events blog post",
        "priority": 2, "category": "Meta Tags", "time_estimate": "2 min",
        "plain_explanation": "Blog post missing its meta description.",
        "wix_steps": ["Blog Editor → click post → SEO Settings → Description"],
        "code": "How ZenSpace Booking Software streamlines pod management at corporate events. Self-service booking, real-time dashboards, and utilization reports — no extra staff needed.",
        "auto_executable": False,
    },
    {
        "id": "meta_blog3",
        "name": "Add Meta Description: Non-Profit Events blog post",
        "priority": 2, "category": "Meta Tags", "time_estimate": "2 min",
        "plain_explanation": "Blog post missing its meta description.",
        "wix_steps": ["Blog Editor → click post → SEO Settings → Description"],
        "code": "ZenSpace Booking Software for non-profit and charity events. Manage meeting pods with self-service booking, branded pages, and post-event analytics.",
        "auto_executable": False,
    },

    # ──────────────── HEADING FIX (Day 2) ────────────────
    {
        "id": "fix_homepage_h1",
        "name": "Fix Homepage: 3 H1 tags → 1 H1 tag",
        "priority": 1,
        "category": "Headings",
        "time_estimate": "5 min",
        "plain_explanation": (
            "Your homepage has 3 H1 headings — there should be exactly 1. "
            "Multiple H1s confuse Google about what the page is about. "
            "Keep the main headline as H1, change the others to H2."
        ),
        "wix_steps": [
            "1. Open Wix Editor → go to Homepage",
            "2. Find ALL text styled as 'Heading 1'",
            "3. Keep only the main headline ('Smart Event Pod Rentals...') as Heading 1",
            "4. Change all other Heading 1 elements to Heading 2",
            "5. Save and Publish",
        ],
        "code": "Keep: 'Smart Event Pod Rentals for Trade Shows, Conferences & Events' as H1\nChange all other H1s to H2 using the text style dropdown in Wix Editor.",
        "auto_executable": False,
    },

    # ──────────────── PRODUCT SCHEMAS (Day 3) ────────────────
    {
        "id": "schema_1seater",
        "name": "Product Schema: 1-Seater Pod",
        "priority": 2, "category": "Schema Markup", "time_estimate": "3 min",
        "plain_explanation": "Adds product details to Google for the 1-Seater pod page — specs, features, and availability.",
        "wix_steps": ["Wix Editor → /1-seater page → Page Settings → SEO → Advanced SEO → Structured Data Markup → Edit → Paste JSON"],
        "code": '''{"@context":"https://schema.org","@type":"Product","name":"ZenSpace 1-Seater Event Pod","description":"Compact single-person privacy pod for trade shows. Features -29dB acoustic privacy, 32-inch TV, smart LED lighting, ventilation, charging, and mobility casters.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Capacity","value":"1 person"},{"@type":"PropertyValue","name":"Acoustic Privacy","value":"Over -29dB"},{"@type":"PropertyValue","name":"Setup Time","value":"Under 30 minutes"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/1-seater"}}''',
        "auto_executable": False,
    },
    {
        "id": "schema_4seater",
        "name": "Product Schema: 4-Seater Pod",
        "priority": 2, "category": "Schema Markup", "time_estimate": "3 min",
        "plain_explanation": "Adds product details to Google for the 4-Seater pod page.",
        "wix_steps": ["Wix Editor → /4-seater page → Page Settings → SEO → Advanced SEO → Structured Data → Paste JSON"],
        "code": '''{"@context":"https://schema.org","@type":"Product","name":"ZenSpace 4-Seater Event Pod","description":"Lightweight 4-person meeting pod for events. Interior: 81.8in W x 54.24in D x 66in H. Floor: 35.5 sqft. Features -29dB acoustic privacy, 32-inch TV, smart E-glass, wireless screen sharing.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Capacity","value":"4 persons"},{"@type":"PropertyValue","name":"Interior","value":"81.8in W x 54.24in D x 66in H"},{"@type":"PropertyValue","name":"Floor Space","value":"35.5 sq ft"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/4-seater"}}''',
        "auto_executable": False,
    },
    {
        "id": "schema_6seater",
        "name": "Product Schema: 6-Seater Pod",
        "priority": 2, "category": "Schema Markup", "time_estimate": "3 min",
        "plain_explanation": "Adds product details for the 6-Seater conference pod.",
        "wix_steps": ["Wix Editor → /6-seater → Page Settings → SEO → Advanced → Structured Data → Paste JSON"],
        "code": '''{"@context":"https://schema.org","@type":"Product","name":"ZenSpace 6-Seater Event Pod","description":"Spacious 6-person conference pod for trade shows. -29dB acoustic privacy, 32-inch TV, smart E-glass, wireless screen sharing, digital signage, AI alerts.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Capacity","value":"6 persons"},{"@type":"PropertyValue","name":"Acoustic Privacy","value":"Over -29dB"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/6-seater"}}''',
        "auto_executable": False,
    },
    {
        "id": "schema_ada",
        "name": "Product Schema: ADA Pod",
        "priority": 2, "category": "Schema Markup", "time_estimate": "3 min",
        "plain_explanation": "Adds product details for the ADA-compliant accessible pod.",
        "wix_steps": ["Wix Editor → /ada-pod → Page Settings → SEO → Advanced → Structured Data → Paste JSON"],
        "code": '''{"@context":"https://schema.org","@type":"Product","name":"ZenSpace Element ADA Event Pod","description":"ADA-compliant wheelchair-accessible meeting pod for events. Wider doorways, accessible interior, -29dB acoustic privacy, UL-certified, all smart features included.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","additionalProperty":[{"@type":"PropertyValue","name":"Accessibility","value":"ADA-compliant, wheelchair accessible"},{"@type":"PropertyValue","name":"Certification","value":"UL-certified"}],"offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/ada-pod"}}''',
        "auto_executable": False,
    },
    {
        "id": "schema_aura",
        "name": "Product Schema: Aura Gather Pod",
        "priority": 2, "category": "Schema Markup", "time_estimate": "3 min",
        "plain_explanation": "Adds product details for the Aura Gather collaborative pod.",
        "wix_steps": ["Wix Editor → /aura-gather → Page Settings → SEO → Advanced → Structured Data → Paste JSON"],
        "code": '''{"@context":"https://schema.org","@type":"Product","name":"ZenSpace Aura Gather Pod","description":"Multi-person gathering pod for collaborative meetings at trade shows. Acoustic privacy, smart E-glass, wireless screen sharing, digital signage, AI monitoring.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Equipment Rental","offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/aura-gather"}}''',
        "auto_executable": False,
    },
    {
        "id": "schema_kiosk",
        "name": "Product Schema: Digital Kiosk",
        "priority": 2, "category": "Schema Markup", "time_estimate": "3 min",
        "plain_explanation": "Adds product details for the Digital Kiosk.",
        "wix_steps": ["Wix Editor → /digital-kiosk → Page Settings → SEO → Advanced → Structured Data → Paste JSON"],
        "code": '''{"@context":"https://schema.org","@type":"Product","name":"ZenSpace Digital Kiosk","description":"Interactive digital kiosk for event wayfinding, sponsor branding, and attendee engagement. Digital signage, real-time alerts, sponsor integration.","brand":{"@type":"Brand","name":"ZenSpace Event Solutions"},"category":"Event Technology","offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":"https://www.zenspaceevents.com/digital-kiosk"}}''',
        "auto_executable": False,
    },
]


def get_tasks_by_priority(priority=None):
    if priority:
        return [t for t in TASKS if t["priority"] == priority]
    return TASKS


def get_task_by_id(task_id):
    for t in TASKS:
        if t["id"] == task_id:
            return t
    return None


def get_progress_summary():
    total = len(TASKS)
    return {
        "total": total,
        "critical": len([t for t in TASKS if t["priority"] == 1]),
        "high": len([t for t in TASKS if t["priority"] == 2]),
        "medium": len([t for t in TASKS if t["priority"] == 3]),
    }
