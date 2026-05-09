#!/usr/bin/env python3
"""
SEO Agent — Browser Data Collector Generator
Generates a JavaScript snippet the user pastes into their browser console.
The script extracts all SEO-relevant data and outputs JSON to copy/paste back.
"""

import json
from pathlib import Path

JS_COLLECTOR = r"""
// ============================================
// SEO AGENT — Browser Data Collector v1.0
// Paste this into your browser console (F12)
// on each page you want to audit.
// ============================================

(function() {
    const data = {
        _collector: "seo-agent-v1",
        url: window.location.href,
        domain: window.location.hostname,
        path: window.location.pathname,
        timestamp: new Date().toISOString(),
        
        // TITLE
        title: document.title || null,
        title_length: (document.title || "").length,
        
        // META TAGS
        meta_description: (document.querySelector('meta[name="description"]') || {}).content || null,
        meta_robots: (document.querySelector('meta[name="robots"]') || {}).content || null,
        meta_viewport: (document.querySelector('meta[name="viewport"]') || {}).content || null,
        meta_charset: document.characterSet,
        
        // CANONICAL
        canonical: (document.querySelector('link[rel="canonical"]') || {}).href || null,
        
        // OPEN GRAPH
        og_tags: Object.fromEntries(
            [...document.querySelectorAll('meta[property^="og:"]')].map(m => [m.getAttribute('property'), m.content])
        ),
        
        // TWITTER CARD
        twitter_tags: Object.fromEntries(
            [...document.querySelectorAll('meta[name^="twitter:"]')].map(m => [m.name, m.content])
        ),
        
        // HEADINGS
        headings: {
            h1: [...document.querySelectorAll('h1')].map(h => h.innerText.trim()),
            h2: [...document.querySelectorAll('h2')].map(h => h.innerText.trim()),
            h3: [...document.querySelectorAll('h3')].map(h => h.innerText.trim()),
            h4: [...document.querySelectorAll('h4')].map(h => h.innerText.trim()),
            h5: [...document.querySelectorAll('h5')].map(h => h.innerText.trim()),
            h6: [...document.querySelectorAll('h6')].map(h => h.innerText.trim()),
        },
        
        // IMAGES
        images: [...document.querySelectorAll('img')].map(img => ({
            src: img.src,
            alt: img.alt,
            has_alt: Boolean(img.alt && img.alt.trim()),
            loading: img.loading || "auto",
            width: img.naturalWidth || img.width,
            height: img.naturalHeight || img.height,
            format: (img.src.split('.').pop() || "").split('?')[0].toLowerCase(),
        })),
        
        // LINKS
        internal_links: [...new Set(
            [...document.querySelectorAll('a[href]')]
                .map(a => a.href)
                .filter(h => h.includes(window.location.hostname))
        )],
        external_links: [...document.querySelectorAll('a[href]')]
            .filter(a => a.href.startsWith('http') && !a.href.includes(window.location.hostname))
            .map(a => ({ url: a.href, text: a.innerText.trim().substring(0, 100), rel: a.rel })),
        
        // SCHEMA MARKUP
        schema_markup: [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => {
            try { return JSON.parse(s.textContent); }
            catch(e) { return { error: "Invalid JSON-LD", raw: s.textContent.substring(0, 200) }; }
        }),
        
        // CONTENT STATS
        word_count: document.body.innerText.split(/\s+/).filter(w => w.length > 0).length,
        text_preview: document.body.innerText.substring(0, 500).replace(/\s+/g, ' ').trim(),
        
        // RESOURCES
        css_files: [...document.querySelectorAll('link[rel="stylesheet"]')].map(l => l.href),
        js_files: [...document.querySelectorAll('script[src]')].map(s => s.src),
        css_count: document.querySelectorAll('link[rel="stylesheet"]').length,
        js_count: document.querySelectorAll('script[src]').length,
        
        // HREFLANG
        hreflang: [...document.querySelectorAll('link[rel="alternate"][hreflang]')].map(l => ({
            lang: l.hreflang, href: l.href
        })),
        
        // PRELOAD / PREFETCH
        preloads: [...document.querySelectorAll('link[rel="preload"]')].map(l => l.href),
        prefetches: [...document.querySelectorAll('link[rel="prefetch"]')].map(l => l.href),
        
        // PERFORMANCE (what's available in browser)
        performance: (() => {
            try {
                const nav = performance.getEntriesByType('navigation')[0];
                const paint = performance.getEntriesByType('paint');
                return {
                    dom_load_ms: Math.round(nav?.domContentLoadedEventEnd || 0),
                    full_load_ms: Math.round(nav?.loadEventEnd || 0),
                    ttfb_ms: Math.round(nav?.responseStart - nav?.requestStart || 0),
                    transfer_size_kb: Math.round((nav?.transferSize || 0) / 1024),
                    first_paint_ms: Math.round(paint.find(p => p.name === 'first-paint')?.startTime || 0),
                    first_contentful_paint_ms: Math.round(paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0),
                };
            } catch(e) { return { error: e.message }; }
        })(),
        
        // SECURITY
        is_https: window.location.protocol === "https:",
        
        // FULL HTML (for deep analysis)
        html_length: document.documentElement.outerHTML.length,
    };
    
    // Count schema types
    data.schema_types = data.schema_markup.flatMap(s => {
        if (s['@type']) return [s['@type']];
        if (s['@graph']) return s['@graph'].filter(i => i['@type']).map(i => i['@type']);
        return [];
    });
    
    // Summary
    data.summary = {
        images_total: data.images.length,
        images_missing_alt: data.images.filter(i => !i.has_alt).length,
        internal_links_count: data.internal_links.length,
        external_links_count: data.external_links.length,
        schema_types_found: data.schema_types,
        h1_count: data.headings.h1.length,
        h2_count: data.headings.h2.length,
    };
    
    // Output
    const output = JSON.stringify(data, null, 2);
    
    // Try to copy to clipboard
    navigator.clipboard.writeText(output).then(() => {
        console.log('%c✅ SEO data copied to clipboard! Paste it back to Claude.', 'color: green; font-size: 14px; font-weight: bold;');
    }).catch(() => {
        console.log('%c⚠️ Could not auto-copy. Select and copy the JSON below:', 'color: orange; font-size: 14px;');
    });
    
    // Also log a summary
    console.log('%c📊 SEO Agent — Page Analysis Summary', 'color: #2563eb; font-size: 16px; font-weight: bold;');
    console.log(`URL: ${data.url}`);
    console.log(`Title: ${data.title} (${data.title_length} chars)`);
    console.log(`Meta Desc: ${data.meta_description ? data.meta_description.substring(0, 80) + '...' : 'MISSING ❌'}`);
    console.log(`H1: ${data.headings.h1.length === 1 ? '✅ ' + data.headings.h1[0] : data.headings.h1.length + ' found ⚠️'}`);
    console.log(`Word Count: ${data.word_count}`);
    console.log(`Schema Types: ${data.schema_types.length > 0 ? data.schema_types.join(', ') : 'NONE ❌'}`);
    console.log(`Images: ${data.summary.images_total} total, ${data.summary.images_missing_alt} missing alt`);
    console.log(`Links: ${data.summary.internal_links_count} internal, ${data.summary.external_links_count} external`);
    console.log(`Performance: FCP ${data.performance.first_contentful_paint_ms}ms, Full Load ${data.performance.full_load_ms}ms`);
    
    // Also create a downloadable file
    const blob = new Blob([output], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `seo-data-${data.domain}-${data.path.replace(/\//g, '_') || 'home'}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log('%c📁 JSON file downloaded! Upload it to Claude or paste the clipboard content.', 'color: green; font-size: 12px;');
    
    return data;
})();
"""

# Also generate a multi-page crawler version
JS_MULTI_PAGE = r"""
// ============================================
// SEO AGENT — Multi-Page Collector
// Collects data from ALL internal links on current page.
// Run on the HOMEPAGE to capture the whole site.
// ============================================

(async function() {
    const domain = window.location.hostname;
    const baseUrl = window.location.origin;
    
    // Get all internal links
    const links = [...new Set(
        [...document.querySelectorAll('a[href]')]
            .map(a => a.href)
            .filter(h => h.includes(domain) && !h.includes('#') && !h.match(/\.(pdf|jpg|png|gif|svg|css|js|zip)$/i))
    )];
    
    console.log(`%c🕷️ SEO Agent Multi-Page Crawler`, 'color: #2563eb; font-size: 16px; font-weight: bold;');
    console.log(`Found ${links.length} internal pages to analyze.`);
    console.log(`This will take about ${Math.ceil(links.length * 1.5)} seconds...`);
    
    const allPages = {};
    let count = 0;
    
    for (const link of links.slice(0, 50)) { // Max 50 pages
        count++;
        console.log(`[${count}/${Math.min(links.length, 50)}] Fetching: ${link}`);
        
        try {
            const resp = await fetch(link);
            const html = await resp.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            allPages[link] = {
                url: link,
                status: resp.status,
                title: doc.title || null,
                meta_description: (doc.querySelector('meta[name="description"]') || {}).content || null,
                canonical: (doc.querySelector('link[rel="canonical"]') || {}).href || null,
                h1: [...doc.querySelectorAll('h1')].map(h => h.innerText.trim()),
                h2: [...doc.querySelectorAll('h2')].map(h => h.innerText.trim()),
                word_count: doc.body ? doc.body.innerText.split(/\s+/).filter(w => w.length > 0).length : 0,
                images_total: doc.querySelectorAll('img').length,
                images_no_alt: [...doc.querySelectorAll('img')].filter(i => !i.alt || !i.alt.trim()).length,
                internal_links: [...new Set([...doc.querySelectorAll('a[href]')].map(a => a.href).filter(h => h.includes(domain)))].length,
                schema_types: [...doc.querySelectorAll('script[type="application/ld+json"]')].flatMap(s => {
                    try { const d = JSON.parse(s.textContent); return d['@type'] ? [d['@type']] : d['@graph'] ? d['@graph'].map(i => i['@type']) : []; }
                    catch(e) { return []; }
                }),
                schema_markup: [...doc.querySelectorAll('script[type="application/ld+json"]')].map(s => {
                    try { return JSON.parse(s.textContent); }
                    catch(e) { return { error: "Invalid JSON" }; }
                }),
                og_tags: Object.fromEntries([...doc.querySelectorAll('meta[property^="og:"]')].map(m => [m.getAttribute('property'), m.content])),
            };
            
            await new Promise(r => setTimeout(r, 500)); // Be polite
        } catch(e) {
            allPages[link] = { url: link, error: e.message };
        }
    }
    
    const output = JSON.stringify({
        _collector: "seo-agent-multi-v1",
        domain: domain,
        base_url: baseUrl,
        timestamp: new Date().toISOString(),
        pages_crawled: Object.keys(allPages).length,
        pages: allPages,
    }, null, 2);
    
    // Download
    const blob = new Blob([output], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `seo-full-crawl-${domain}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log(`%c✅ Done! ${Object.keys(allPages).length} pages analyzed. JSON file downloaded.`, 'color: green; font-size: 14px; font-weight: bold;');
    console.log('Upload the downloaded JSON file to Claude for full analysis.');
    
    return allPages;
})();
"""


def generate_collector_scripts():
    """Generate the browser collector scripts."""
    output_dir = Path(__file__).parent.parent / "scripts"
    
    (output_dir / "browser_single_page.js").write_text(JS_COLLECTOR)
    (output_dir / "browser_multi_page.js").write_text(JS_MULTI_PAGE)
    
    print("\n" + "=" * 65)
    print("  SEO AGENT — Browser Data Collectors Generated")
    print("=" * 65)
    print()
    print("  Two scripts created:")
    print()
    print("  1. browser_single_page.js")
    print("     → Paste into browser console (F12) on any page")
    print("     → Extracts all SEO data + performance metrics")
    print("     → Auto-copies to clipboard + downloads JSON")
    print()
    print("  2. browser_multi_page.js")
    print("     → Paste into browser console on the HOMEPAGE")
    print("     → Crawls all internal links (up to 50 pages)")
    print("     → Downloads a full-site JSON crawl file")
    print()
    print("  USAGE:")
    print("  1. Open zenspaceevents.com in Chrome")
    print("  2. Press F12 → Console tab")
    print("  3. Paste the multi-page script → hit Enter")
    print("  4. Wait for it to finish (~30-60 seconds)")
    print("  5. Upload the downloaded JSON file to this chat")
    print()
    print("  Then repeat for nookeventpods.us")
    print("=" * 65)


if __name__ == "__main__":
    generate_collector_scripts()
