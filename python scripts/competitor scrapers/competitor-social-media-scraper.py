import re
import os
import pandas as pd
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeoutError
import time
import random
from typing import List, Dict, Optional, Set

# Configuration
CSV_FILE = os.path.join(os.path.dirname(__file__), '../../docs/competitor content tracker/competitor_socialmedia_tracker.csv')

class SocialMediaScraper:
    def __init__(self):
        self.new_posts: List[Dict] = []
        self.existing_links: Set[str] = set()
        self.ensure_directory_exists()
        self.init_csv_history()

    def ensure_directory_exists(self):
        """Ensure the directory for the CSV file exists."""
        os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    def init_csv_history(self):
        """Load existing CSV history to prevent duplicates."""
        if os.path.exists(CSV_FILE):
            try:
                df = pd.read_csv(CSV_FILE)
                if not df.empty and 'Link URL' in df.columns:
                    self.existing_links = set(df['Link URL'].dropna().tolist())
            except Exception as e:
                print(f"⚠️ Error reading CSV: {e}")

    def parse_date(self, snippet: str) -> datetime:
        """Extract and parse date from the snippet."""
        now = datetime.now()
        
        # 1. Relative time: "3 days ago", "2 hours ago"
        if "days ago" in snippet:
            match = re.search(r'(\d+)\s+days ago', snippet)
            if match:
                return now - timedelta(days=int(match.group(1)))
        if "hours ago" in snippet:
            return now # Treat as today

        # 2. Absolute dates: "Jan 15, 2024", "15 Jan 2024"
        # Regex for "Mon DD, YYYY" (e.g., Jan 15, 2024)
        match = re.search(r'([A-Z][a-z]{2}\s\d{1,2},\s\d{4})', snippet)
        if match:
            try:
                return datetime.strptime(match.group(1), "%b %d, %Y")
            except: pass
            
        # Regex for "DD Mon YYYY" (e.g., 15 Jan 2024)
        match = re.search(r'(\d{1,2}\s[A-Z][a-z]{2}\s\d{4})', snippet)
        if match:
             try:
                return datetime.strptime(match.group(1), "%d %b %Y")
             except: pass

        return now # Default to now if not found (or maybe None?)

    def scrape_google_search(self, page: Page, site_query: str, competitor_name: str, platform: str):
        print(f"🔎 Searching Google for {competitor_name} on {platform}...")
        try:
            # Search query: site:linkedin.com/company/...
            page.goto("https://www.google.com", timeout=60000)
            
            # Handle cookie banner if exists (BeforeAccept)
            try:
                reject_btn = page.get_by_role("button", name="Reject all")
                if reject_btn.is_visible():
                    reject_btn.click(timeout=2000)
            except:
                pass

            search_box_selectors = ["textarea[name='q']", "input[name='q']"]
            for selector in search_box_selectors:
                if page.is_visible(selector):
                    page.fill(selector, site_query)
                    page.press(selector, "Enter")
                    break
            else:
                 print("⚠️ Could not find search box.")
                 return

            try:
                page.wait_for_selector("#search", timeout=10000)
            except:
                 print("⚠️ CAPTCHA or blocking detected.")
                 print("   Please solve the CAPTCHA in the browser window.")
                 print("   Waiting 45 seconds for manual resolution...")
                 time.sleep(45) 
                 # Check again
                 if page.locator("#search").is_visible():
                     print("   ✅ Resuming...")
                 else:
                     print("   ❌ Still blocked or selector changed. Skipping...")
                     return

            # Filter by "Past Month" to get recent content - optional, complicated by UI changes
            # For now, we rely on natural relevance and date parsing.

            # Scrape results
            # Wait for results to load
            try:
                 page.wait_for_selector(".g", state="attached", timeout=5000)
            except:
                 print("   No results found or selector changed.")
                 return

            results = page.locator(".g")
            count = int(results.count())
            
            found_count: int = 0
            for i in range(min(count, 10)): # Check top 10
                try:
                    res = results.nth(i)
                    link_elem = res.locator("a").first
                    title_elem = res.locator("h3").first
                    snippet_elem = res.locator(".VwiC3b").first # Common snippet class for description

                    if not link_elem.is_visible(): continue

                    link = link_elem.get_attribute("href")
                    if not link: continue
                    
                    title = title_elem.inner_text() if title_elem.is_visible() else "No Title"
                    snippet = snippet_elem.inner_text() if snippet_elem.is_visible() else title
                    
                    # Clean up snippet
                    words = snippet.split()
                    summary_phrase = ' '.join(words[:15]) + "..." if words else title # Increased context
                    
                    # Determine Post Type based on snippet keywords
                    post_type = "Text"
                    lower_snip = snippet.lower()
                    if "video" in lower_snip: post_type = "Video"
                    elif "photo" in lower_snip or "image" in lower_snip or "instagram photo" in lower_snip: post_type = "Image"
                    elif "article" in lower_snip: post_type = "Article"

                    pub_date = self.parse_date(snippet)

                    if link not in self.existing_links and "google.com" not in link:
                         self.new_posts.append({
                            'Date': pub_date.strftime('%Y-%m-%d'),
                            'Competitor': competitor_name,
                            'Title': summary_phrase,
                            'Content Type': "Social Post",
                            'Link URL': link,
                            'Post Type': post_type,
                            'Platform': platform
                        })
                         found_count = found_count + 1
                except Exception as e:
                    # print(f"   Error parsing result {i}: {e}")
                    continue
            
            print(f"   found {found_count} items via Google.")

        except Exception as e:
            print(f"❌ Error searching Google for {competitor_name}: {e}")
            try:
                page.screenshot(path="google_error.png")
            except: pass

    def run(self):
        with sync_playwright() as p:
            # HEADFUL MODE for User CAPTCHA Solving
            print("🌐 Launching browser... (If a CAPTCHA appears, please solve it manually)")
            browser = p.chromium.launch(headless=False) 
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()

            targets = [
                ("site:linkedin.com/company/get-ryze-ai", "Ryze AI", "LinkedIn"),
                ("site:linkedin.com/company/smartly-io", "Smartly.io", "LinkedIn"),
                ("site:instagram.com/smartlyio", "Smartly.io", "Instagram"),
                ("site:linkedin.com/company/funnel-io", "Funnel.io", "LinkedIn"),
                ("site:linkedin.com/company/supermetrics", "Supermetrics", "LinkedIn"),
                ("site:linkedin.com/company/adzooma", "Adzooma", "LinkedIn"),
                ("site:linkedin.com/company/albert-ai", "Albert.ai", "LinkedIn"),
                ("site:linkedin.com/company/adscale", "AdScale", "LinkedIn"),
                ("site:linkedin.com/company/madgicx", "Madgicx", "LinkedIn"),
                ("site:linkedin.com/company/adpulse-app", "AdPulse", "LinkedIn"),
                ("site:linkedin.com/company/improvado", "Improvado", "LinkedIn"),
                ("site:linkedin.com/company/roadway-ai", "Roadway AI", "LinkedIn")
            ]

            for query, name, platform in targets:
                self.scrape_google_search(page, query, name, platform)
                # Intelligent wait or random delay to be polite
                page.wait_for_timeout(random.randint(2000, 5000))

            browser.close()
            self.save_data()

    def save_data(self):
        if not self.new_posts:
            print("\n✅ No new social posts found.")
            return

        new_df = pd.DataFrame(self.new_posts)
        if new_df.empty: return

        if os.path.exists(CSV_FILE):
            try:
                existing_df = pd.read_csv(CSV_FILE)
                # Normalize columns if needed
                if 'Date' in existing_df.columns: existing_df['Date'] = pd.to_datetime(existing_df['Date'])
                if 'Date' in new_df.columns: new_df['Date'] = pd.to_datetime(new_df['Date'])
                
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            except Exception as e:
                print(f"⚠️ Error determining existing data: {e}")
                combined_df = new_df
        else:
            combined_df = new_df

        # Ensure new columns exist
        if 'Post Type' not in combined_df.columns: combined_df['Post Type'] = None
        if 'Platform' not in combined_df.columns: combined_df['Platform'] = None

        # Deduplicate
        if 'Link URL' in combined_df.columns:
            combined_df = combined_df.drop_duplicates(subset=['Link URL'], keep='first')
        
        # Sort
        if 'Date' in combined_df.columns:
            combined_df = combined_df.sort_values(by='Date', ascending=False)
            combined_df['Date'] = combined_df['Date'].dt.strftime('%Y-%m-%d')
            
        # Write
        try:
            combined_df.to_csv(CSV_FILE, index=False)
            print(f"\n🚀 Saved {len(self.new_posts)} new posts to tracker.")
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")

if __name__ == "__main__":
    scraper = SocialMediaScraper()
    scraper.run()
