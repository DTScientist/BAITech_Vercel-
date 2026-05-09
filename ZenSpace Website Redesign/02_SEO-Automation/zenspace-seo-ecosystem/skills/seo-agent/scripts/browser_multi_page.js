
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
