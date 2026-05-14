#!/usr/bin/env python3
"""Crawl TLDR landing pages: take screenshots, extract page structure, capture accessibility snapshots."""
from playwright.sync_api import sync_playwright
import json, time, os

urls = [
    'https://tldr.tech',
    'https://tldr.tech/signup',
    'https://advertise.tldr.tech',
    'https://tldr.tech/ai',
    'https://tldr.tech/webdev',
    'https://tldr.tech/crypto',
]

output_dir = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    results = []

    for url in urls:
        slug = url.split('/')[-1] or 'homepage'
        try:
            # Desktop viewport
            page = browser.new_page(viewport={'width': 1440, 'height': 900})
            page.goto(url, wait_until='networkidle', timeout=30000)
            time.sleep(2)

            page.screenshot(path=os.path.join(output_dir, f'screenshot_{slug}.png'), full_page=True)

            # Mobile viewport screenshot
            mobile_page = browser.new_page(viewport={'width': 375, 'height': 812})
            mobile_page.goto(url, wait_until='networkidle', timeout=30000)
            time.sleep(1)
            mobile_page.screenshot(path=os.path.join(output_dir, f'screenshot_{slug}_mobile.png'), full_page=True)

            title = page.title()
            h1 = page.query_selector('h1')
            h1_text = h1.inner_text() if h1 else ''

            h2_els = page.query_selector_all('h2')
            h2_texts = [el.inner_text() for el in h2_els[:5]]

            ctas = page.query_selector_all('button, a[class*="cta"], a[class*="btn"], a[class*="button"], input[type="submit"], [role="button"]')
            cta_texts = []
            for cta in ctas[:15]:
                txt = cta.inner_text().strip()
                if txt:
                    cta_texts.append(txt)

            forms = page.query_selector_all('form')
            form_details = []
            for form in forms[:5]:
                inputs = form.query_selector_all('input, select, textarea')
                input_types = []
                for inp in inputs:
                    inp_type = inp.get_attribute('type') or 'text'
                    inp_name = inp.get_attribute('name') or inp.get_attribute('placeholder') or ''
                    input_types.append(f"{inp_type}({inp_name})")
                form_details.append(input_types)

            meta = page.query_selector('meta[name="description"]')
            meta_text = meta.get_attribute('content') if meta else ''

            links = page.query_selector_all('a[href]')
            nav_links = []
            for link in links[:30]:
                href = link.get_attribute('href') or ''
                text = link.inner_text().strip()
                if text and len(text) < 60:
                    nav_links.append({"text": text, "href": href})

            # Accessibility snapshot
            try:
                a11y_snapshot = page.accessibility.snapshot()
            except Exception:
                a11y_snapshot = None

            # Page load performance
            perf = page.evaluate("""() => {
                const t = performance.timing;
                return {
                    domContentLoaded: t.domContentLoadedEventEnd - t.navigationStart,
                    loadComplete: t.loadEventEnd - t.navigationStart,
                    firstByte: t.responseStart - t.navigationStart
                };
            }""")

            results.append({
                'url': url,
                'slug': slug,
                'title': title,
                'h1': h1_text,
                'h2s': h2_texts,
                'meta_description': meta_text,
                'cta_count': len(ctas),
                'cta_texts': cta_texts,
                'form_count': len(forms),
                'form_details': form_details,
                'nav_links_sample': nav_links[:10],
                'performance': perf,
                'a11y_snapshot_available': a11y_snapshot is not None,
            })

            mobile_page.close()
            page.close()
            print(f"  OK: {url}")

        except Exception as e:
            results.append({'url': url, 'slug': slug, 'error': str(e)})
            print(f"  FAIL: {url} — {e}")

    browser.close()

    with open(os.path.join(output_dir, 'crawl_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
