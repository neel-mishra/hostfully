import urllib.request
import urllib.error
import urllib.parse
import ssl
import urllib.parse
import sys
from html.parser import HTMLParser
import json
import csv
import os
import concurrent.futures
import time
import argparse
import datetime
import typing

# Default globals (will be overridden by args in main)
PREFIX = ""
OUTPUT_DIR = ""
SITEMAP_URL = ""
LIMIT = 160  # max urls to audit

class SEOHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1_tags = []
        self.meta_desc = ""
        self.text_content = []
        
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("name", "").lower() == "description":
                self.meta_desc = attrs_dict.get("content", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self._in_title:
            self.title = data
        elif self._in_h1:
            self.h1_tags.append(data)
        
        # very rough text extraction
        self.text_content.append(data)

def _get_urls_via_gsc():
    """Try to get URL list from Google Search Console (same credentials as .env). Returns list or None."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        gsc_script = os.path.join(workspace_root, "automations", "lib", "gsc_api.py")
        if not os.path.isfile(gsc_script):
            return None
        import subprocess
        result = subprocess.run(
            [sys.executable, gsc_script, "sitemap-urls"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=workspace_root,
            env={**os.environ},
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        urls = data.get("urls") or []
        return urls if isinstance(urls, list) else None
    except Exception:
        return None


def get_sitemap_urls():
    print("Phase 1: URL Inventory Building")
    urls = []
    # Prefer Google Search Console when GSC_SITE_URL and GOOGLE_APPLICATION_CREDENTIALS are set
    gsc_urls = _get_urls_via_gsc()
    if gsc_urls:
        urls = gsc_urls
        print(f"Found {len(urls)} URLs via Google Search Console.")
    if not urls:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = urllib.request.Request(SITEMAP_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response:
                sitemap_xml = response.read().decode('utf-8')

                # Very basic extraction instead of full XML parsing
                parts = sitemap_xml.split("<loc>")
                for part in parts[1:]:
                    end_idx = part.find("</loc>")
                    if end_idx != -1:
                        urls.append(part[:end_idx].strip())
        except Exception as e:
            print(f"Failed to fetch sitemap: {e}")
            base_url = urllib.parse.urljoin(SITEMAP_URL, '/')
            urls.append(base_url)  # fallback
        print(f"Found {len(urls)} URLs from sitemap.")

    unique_urls = list(dict.fromkeys(urls))[:LIMIT]  # pyre-ignore
    return unique_urls

def save_inventory(urls):
    print("Phase 2: Inventory Storage")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, f"{PREFIX}_url_inventory.json")
    csv_path = os.path.join(OUTPUT_DIR, f"{PREFIX}_url_inventory.csv")
    
    with open(json_path, 'w') as f:
        json.dump([{"url": u, "source": "sitemap"} for u in urls], f, indent=2)
        
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Source"])
        for u in urls:
            writer.writerow([u, "sitemap"])
    print(f"Saved inventory to {json_path} and {csv_path}")

def fetch_and_analyze(url: str) -> typing.Dict[str, typing.Any]:
    result: typing.Dict[str, typing.Any] = {
        "url": url,
        "status_code": 0,
        "title": "",
        "title_length": 0,
        "h1_count": 0,
        "h1_text": "",
        "meta_desc": "",
        "word_count": 0,
        "issues": []
    }
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 SEO-Audit'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            result["status_code"] = response.getcode()
            html = response.read().decode('utf-8', errors='ignore')
            
            parser = SEOHTMLParser()
            parser.feed(html)
            
            result["title"] = parser.title
            result["title_length"] = len(parser.title)
            result["h1_count"] = len(parser.h1_tags)
            result["h1_text"] = " | ".join(parser.h1_tags)
            result["meta_desc"] = parser.meta_desc
            result["word_count"] = len(" ".join(parser.text_content).split())
            
            # Analyze Phase logic
            if result["title_length"] == 0:
                result["issues"].append("Missing Title")
            elif result["title_length"] > 60:
                result["issues"].append("Title too long")
                
            if result["h1_count"] == 0:
                result["issues"].append("Missing H1")
            elif result["h1_count"] > 1:
                result["issues"].append("Multiple H1s")
                
            if not result["meta_desc"]:
                result["issues"].append("Missing Meta Description")
                
            if result["word_count"] < 300:
                result["issues"].append("Thin Content (<300 words)")
                
    except urllib.error.HTTPError as e:
        result["status_code"] = e.code
        result["issues"].append(f"HTTP Error {e.code}")
    except Exception as e:
        result["issues"].append(f"Connection Failed: {e}")
        
    return result

def run_audit(urls):
    print("Phase 3: Audit Execution (Crawling & Analysis)")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_and_analyze, url): url for url in urls}  # pyre-ignore
        for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
            res = future.result()
            results.append(res)
            if (i+1) % 20 == 0:
                print(f"Processed {i+1}/{len(urls)}")
    print("Audit Execution Complete.")
    return results

def generate_reports(results):
    print("Phase 4: Reporting")
    csv_path = os.path.join(OUTPUT_DIR, f"{PREFIX}_detailed.csv")
    hl_path = os.path.join(OUTPUT_DIR, f"{PREFIX}_high_level.md")
    det_path = os.path.join(OUTPUT_DIR, f"{PREFIX}_detailed.md")
    
    # 1. Detailed CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "url", "status_code", "title", "title_length", "h1_count", "h1_text", "meta_desc", "word_count", "issues"
        ])
        writer.writeheader()
        for r in results:
            r_copy = r.copy()
            r_copy["issues"] = ", ".join(r["issues"])
            writer.writerow(r_copy)
            
    # Calculate stats for High Level Report
    total_pages = len(results)
    pages_with_issues = len([r for r in results if r["issues"]])
    missing_h1s = len([r for r in results if r["h1_count"] == 0])
    missing_meta = len([r for r in results if not r["meta_desc"]])
    thin_content = len([r for r in results if r["word_count"] < 300])
    status_200 = len([r for r in results if r["status_code"] == 200])
    
    health_score = max(0, int(((status_200 / total_pages) * 50) + (((total_pages - pages_with_issues)/total_pages) * 50)))
    
    # 2. High Level Report
    with open(hl_path, 'w') as f:
        company_display = PREFIX.title()
        f.write(f"# SEO Audit: Executive Summary for {company_display}\n\n")
        f.write(f"**Overall Health Score:** {health_score}/100\n\n")
        f.write("## Priority Action Plan\n")
        f.write(f"- **Pages missing H1:** {missing_h1s}\n")
        f.write(f"- **Pages missing Meta Descriptions:** {missing_meta}\n")
        f.write(f"- **Pages with Thin Content:** {thin_content}\n")
        f.write(f"- **Total Pages Crawled:** {total_pages}\n\n")
        f.write("## Aggregated Findings\n")
        f.write("The primary issues found relate to missing meta descriptions and thin content on some informational pages.\n")
        
    # 3. Detailed Report
    with open(det_path, 'w') as f:
        company_display = PREFIX.title()
        f.write(f"# SEO Audit: Detailed Report for {company_display}\n\n")
        f.write("## Page-by-Page Breakdown\n\n")
        for r in results:
            if not r["issues"]: continue
            f.write(f"### {r['url']}\n")
            f.write(f"- **Status:** {r['status_code']}\n")
            f.write(f"- **Word Count:** {r['word_count']}\n")
            for issue in r["issues"]:
                f.write(f"- **Issue:** {issue} (Impact: Medium | Priority: Medium)\n")
            f.write("\n")
            
    print(f"Generated {csv_path}, {hl_path}, and {det_path}")

def main():
    global PREFIX, OUTPUT_DIR, SITEMAP_URL, LIMIT
    
    parser = argparse.ArgumentParser(description="Universal SEO Auditor")
    parser.add_argument("--company", required=True, help="Name of the company (e.g., numeral)")
    parser.add_argument("--sitemap", required=True, help="URL to the sitemap.xml")
    parser.add_argument("--limit", type=int, default=160, help="Max URLs to audit (default: 160)")
    args = parser.parse_args()

    PREFIX = args.company.lower()
    SITEMAP_URL = args.sitemap
    LIMIT = args.limit
    
    # Create the dynamic folder structure: /docs/SEO/<Company>/<company>_<mm>_<yyyy>/
    now = datetime.datetime.now()
    month_str = now.strftime("%m")
    year_str = now.strftime("%Y")
    
    base_seo_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'SEO')
    company_title = args.company.title() # e.g. Numeral
    folder_name = f"{PREFIX}_{month_str}_{year_str}"
    
    OUTPUT_DIR = os.path.join(base_seo_dir, company_title, folder_name)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Starting audit for {company_title}...")
    print(f"Output Directory: {OUTPUT_DIR}")

    start_time = time.time()
    urls = get_sitemap_urls()
    save_inventory(urls)
    results = run_audit(urls)
    generate_reports(results)
    print(f"All done in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
