import requests
from bs4 import BeautifulSoup
import json
import sys
import os

def scrape_landing_page(url):
    """
    Scrapes a landing page to extract product context:
    - Title & Meta Description
    - Headings (H1-H3)
    - Pricing Information (heuristic)
    - Main Content/Benefits
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Basic Metadata
        title = soup.title.string if soup.title else "No Title"
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '')
            
        # 2. Headings (Structure/Benefits)
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3']):
            text = h.get_text(strip=True)
            if text:
                headings.append(f"{h.name.upper()}: {text}")
                
        # 3. Content Summary (Paragraphs)
        # We only take the first 5-10 substantial paragraphs to avoid footer clutter
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if len(text) > 50: # Filter out short snippets
                paragraphs.append(text)
        
        # 4. Pricing Detection (Heuristic)
        pricing_info = []
        # Look for common pricing keywords in text or classes
        pricing_keywords = ['price', 'pricing', 'subscription', 'tier', 'plan', '$', 'free', 'pro', 'enterprise']
        # Simple scan of page text for pricing context
        # In a real scraper, we might parse specific tables. Here we grab text blocks containing '$'
        for text in soup.stripped_strings:
            if '$' in text and len(text) < 100:
                pricing_info.append(text)
                
        # 5. Extract Links/CTAs
        ctas = []
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            if text and len(text) < 30:
                # Check if it looks like a CTA
                cta_keywords = ['sign up', 'get started', 'try', 'buy', 'join']
                if any(k in text.lower() for k in cta_keywords):
                    ctas.append({"text": text, "link": a['href']})

        data = {
            "url": url,
            "title": title,
            "description": meta_desc,
            "structure": headings[:20], # Limit to top 20 headings
            "key_benefits": paragraphs[:10], # Limit to top 10 paragraphs
            "pricing_signals": pricing_info[:15], # Limit to top 15 prices found
            "ctas": ctas[:5]
        }
        
        return data

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python landing_page_scraper.py <url>")
        # Default test URL if none provided (e.g. valid site)
        # But for now, just exit
        sys.exit(1)
        
    target_url = sys.argv[1]
    result = scrape_landing_page(target_url)
    print(json.dumps(result, indent=2))
