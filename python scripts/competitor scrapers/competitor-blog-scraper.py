import requests  # type: ignore[import-not-found]
from bs4 import BeautifulSoup  # type: ignore[import-not-found]
import pandas as pd  # type: ignore[import-not-found]
from datetime import datetime
import os
import csv
from typing import List, Any

# Configuration
# Adjust to current directory
CSV_FILE = os.path.join(os.path.dirname(__file__), '../../docs/competitor content tracker/blogs/competitor_content_tracker.csv')
DEFAULT_START_DATE = datetime(2024, 1, 1)


class ContentScorer:
    def __init__(self):
        # Weighted Scoring Configuration
        self.weights = {
            'relevance': 0.5,
            'impact': 0.3,
            'effort': 0.2
        }
        
        # Keyword Lists based on Command/Core Strategy
        self.keywords = {
            'relevance': [
                'newsletter', 'subscriber', 'email', 'open rate', 'curation',
                'tech news', 'daily', 'briefing', 'advertising', 'sponsored',
                'native ads', 'b2b', 'saas', 'audience', 'readership', 'media'
            ],
            'impact': [
                'strategy', 'case study', 'guide', 'playbook', 'how to',
                'framework', 'benchmark', 'trend', 'revenue', 'growth',
                'monetization', 'scaling', 'acquisition', 'retention', 'roi'
            ],
            'effort_high': [
                'api', 'python', 'code', 'script', 'technical', 'integration',
                'implementation', 'setup', 'tutorial', 'step-by-step', 'comprehensive'
            ]
        }

    def calculate_score(self, title: str, summary: str = "") -> dict:
        text = (title + " " + summary).lower()
        
        # 1. Relevance Score (0-10)
        # Based on product alignment (AI, Ads, Automation)
        relevance_hits = sum(1 for word in self.keywords['relevance'] if word in text)
        relevance_score = min(10, relevance_hits * 2) 
        
        # 2. Impact Score (0-10)
        # Based on strategic value (Case Studies, Guides)
        impact_hits = sum(1 for word in self.keywords['impact'] if word in text)
        impact_score = min(10, int(impact_hits * 2.5))
        
        # 3. Effort Score (0-10)
        # Lower score = Higher effort to replicate (Technical/Deep content)
        # We want to prioritize LOW effort wins, so we invert this in the final calc usually,
        # but here we score "Effort Required". 
        # Let's align with user request: "cumulative weighted score... prioritize creation"
        # Usually high effort = low priority for quick wins, or high priority for moats.
        # Let's assume Impact/Effort ratio. 
        # For this scaler, let's score "Ease of Creation" (10 = Easy, 0 = Hard)
        is_technical = any(word in text for word in self.keywords['effort_high'])
        word_count_est = len(text.split())
        
        if is_technical:
            effort_score = 3 # Hard execution
        elif "guide" in text or "comprehensive" in text:
            effort_score = 5 # Medium execution
        else:
            effort_score = 8 # Likely opinion/news (Easier)
            
        # Weighted Score
        # We want High Relevance + High Impact + Low Effort (Higher Ease Score)
        weighted_score = (
            (relevance_score * self.weights['relevance']) +
            (impact_score * self.weights['impact']) +
            (effort_score * self.weights['effort'])
        )
        
        return {
            'Relevance': relevance_score,
            'Impact': impact_score,
            'Effort': effort_score,
            'Weighted_Score': float(round(weighted_score, 2))  # type: ignore[call-overload]
        }

class CompetitorScraper:
    def __init__(self):
        self.new_articles = []
        self.scorer = ContentScorer()
        self.existing_urls = set()
        self.init_csv_history()
        self.last_run_date = DEFAULT_START_DATE # Logic change: Rely on URL dedup mostly

    def init_csv_history(self):
        if os.path.exists(CSV_FILE):
            try:
                df = pd.read_csv(CSV_FILE)
                if not df.empty and 'Link URL' in df.columns:
                    self.existing_urls = set(df['Link URL'].dropna().tolist())
                    # Also set last_run_date logic if needed, but for now allow backfill
                    if 'Date' in df.columns:
                         df['Date'] = pd.to_datetime(df['Date'])
                         # self.last_run_date = df['Date'].max() 
            except Exception as e:
                print(f"⚠️ Error reading CSV: {e}")


    def backfill_scores(self):
        """Helper to score existing rows that have 0/missing scores."""
        if not os.path.exists(CSV_FILE):
            return

        print("🔄 Checking for articles needing scores...")
        try:
            df = pd.read_csv(CSV_FILE)
            
            # Ensure columns exist
            changed = False
            for col in ['Relevance', 'Impact', 'Effort', 'Weighted_Score']:
                if col not in df.columns:
                    df[col] = 0.0
                    changed = True
            
            # Find rows with 0 Weighted_Score
            mask = df['Weighted_Score'] == 0  # type: ignore[assignment]
            if mask.any():  # type: ignore[union-attr]
                print(f"   Found {mask.sum()} articles to score. calculating...")  # type: ignore[union-attr]
                
                # We need to apply the scorer. 
                # Note: ContentScorer is instance member, so we use self.scorer
                # We used df.apply with axis=1 before.
                
                # Function to apply
                def get_scores(row):
                    s = self.scorer.calculate_score(str(row['Title']), str(row.get('Summary', '')))
                    return pd.Series([s['Relevance'], s['Impact'], s['Effort'], s['Weighted_Score']])

                # Apply only to the masked rows
                # This is a bit tricky with pandas assignment on slice, so let's do global apply if needed
                # or iterate. Iteration is fine for 150 rows.
                # Actually apply on the slice is better.
                
                scored_data = df.loc[mask].apply(get_scores, axis=1)
                scored_data.columns = ['Relevance', 'Impact', 'Effort', 'Weighted_Score']
                
                df.update(scored_data)
                changed = True
                
            if changed:
                df.to_csv(CSV_FILE, index=False)
                print(f"✅ Backfilled scores for {mask.sum()} articles.")  # type: ignore[union-attr]
            else:
                print("   All articles already scored.")
                
        except Exception as e:
            print(f"⚠️ Error backfilling scores: {e}")

    @staticmethod
    def _is_junk_url(url: str) -> bool:
        """Filter out URLs that aren't real blog articles."""
        url_lower = url.lower()
        junk_patterns = [
            'youtube.com', 'youtu.be',
            '/author/', '/search?', '/tag/',
            '/category/', '/page/',
            '#', '/feed', '/rss',
        ]
        return any(pattern in url_lower for pattern in junk_patterns)

    def scrape_generic(self, competitor_name, url, selector_hint=None):
        """Scrapes a generic blog using common patterns or specific selectors."""
        print(f"🕵️‍♂️ Scanning {competitor_name}...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            response = requests.get(url, headers=headers, timeout=20)

            # Check for blocking
            if response.status_code == 403:
                print(f"   ⚠️ 403 Forbidden — {competitor_name} is blocking requests.")
                return
            if response.status_code != 200:
                print(f"   ⚠️ HTTP {response.status_code} from {competitor_name}.")
                return

            soup = BeautifulSoup(response.content, 'html.parser')

            # Identify articles using multiple strategies
            articles: List[Any] = []
            if selector_hint:
                articles = list(soup.select(selector_hint))
            
            if not articles:
                # Strategy 1: Semantic <article> tags
                articles = list(soup.find_all('article'))
            if not articles:
                # Strategy 2: Broadened class matching (no 'item' requirement)
                articles = list(soup.find_all(class_=lambda x: x and any(
                    kw in x for kw in ['post-card', 'blog-post', 'post-item', 'card-item',
                    'blog-item', 'blog_post', 'hs-blog-post', 'w-dyn-item',
                    'PostCard', 'BlogCard', 'article-card']
                )))
            if not articles:
                # Strategy 3: Link-based fallback — find all <a> pointing to /blog/
                blog_links = soup.find_all('a', href=lambda h: h and '/blog/' in h)
                # Deduplicate by href
                seen_hrefs = set()
                for link in blog_links:
                    href = link['href']
                    if href not in seen_hrefs:
                        seen_hrefs.add(href)
                        articles.append(link)

            found_count = 0
            for i, article in enumerate(articles):
                if i >= 25:  # Raised cap from 10 to 25 for broader coverage
                    break
                title_text = None
                link_url = None
                
                # Link — handle both container elements and bare <a> tags
                if article.name == 'a' and article.get('href'):
                    a_tag = article
                    link_url = article['href']
                else:
                    a_tag = article.find('a', href=True)
                    if a_tag:
                        link_url = a_tag['href']
                    else:
                        continue

                if not link_url: continue

                # Title — try multiple strategies
                heading = article.find(['h2', 'h3', 'h4', 'h5', 'h6'])
                if heading:
                    title_text = heading.get_text(strip=True)
                else:
                    title_text = a_tag.get_text(strip=True)

                # Fallback: check title/aria-label attributes
                if not title_text or len(title_text) < 5:
                    title_text = a_tag.get('title', '') or a_tag.get('aria-label', '')

                # Fallback: check parent container for a heading
                if not title_text or len(title_text) < 5:
                    parent = a_tag.find_parent(class_=lambda x: x and any(
                        k in x for k in ['card', 'post', 'item', 'blog']
                    ))
                    if parent:
                        parent_heading = parent.find(['h2', 'h3', 'h4', 'h5', 'h6'])
                        if parent_heading:
                            title_text = parent_heading.get_text(strip=True)

                if not title_text or len(title_text) < 5: continue

                # Normalize URL
                if not link_url.startswith('http'):
                    base_domain = '/'.join(url.split('/')[:3])
                    if link_url.startswith('/'):
                        link_url = base_domain + link_url
                    else:
                        link_url = base_domain + '/' + link_url

                # Date
                pub_date = datetime.now()
                time_tag = article.find(['time', 'span'], class_=lambda x: x and ('date' in x or 'time' in x))
                if time_tag:
                    try:
                        pub_date = pd.to_datetime(time_tag.get_text(strip=True))
                    except: pass
                
                # Filter out non-article URLs
                if self._is_junk_url(link_url):
                    continue

                # Check duplication
                if link_url not in self.existing_urls:
                     if not any(a['Link URL'] == link_url for a in self.new_articles):
                        self.new_articles.append({
                            'Date': pub_date.strftime('%Y-%m-%d'),
                            'Competitor': competitor_name,
                            'Title': title_text,
                            'Content Type': "Blog",
                            'Link URL': link_url
                        })
                        found_count += 1
            
            print(f"   found {found_count} new items.")

        except Exception as e:
            print(f"❌ Error scraping {competitor_name}: {e}")

    def save_data(self):
        if not self.new_articles:
            print("\n✨ No new unique articles to save.")
            return

        # Create DataFrame
        df_new = pd.DataFrame(self.new_articles)
        
        # Calculate scores for new articles
        if not df_new.empty:
            scores = df_new.apply(lambda x: self.scorer.calculate_score(x['Title'], x.get('Summary', '')), axis=1)
            score_df = pd.DataFrame(list(scores))
            df_new = pd.concat([df_new, score_df], axis=1)
        
        # Check if file exists to determine if we need header
        file_exists = os.path.isfile(CSV_FILE)
        
        if file_exists:
            try:
                # Read existing to deduplicate
                df_existing = pd.read_csv(CSV_FILE)
                
                # Check if existing file has score columns, if not, fill with 0/NaN
                for col in ['Relevance', 'Impact', 'Effort', 'Weighted_Score']:
                    if col not in df_existing.columns:
                        df_existing[col] = 0
                
                # Filter out duplicates based on Link URL
                existing_links = set(df_existing['Link URL'].tolist())
                df_new = df_new[~df_new['Link URL'].isin(existing_links)]
            except Exception as e:
                print(f"⚠️ Error reading existing CSV: {e}")
                # If error, maybe file is corrupt, proceed to append? 
                # Safer to just append new data
                pass
        
        if not df_new.empty:
            # Append mode
            try:
                df_new.to_csv(CSV_FILE, mode='a', header=not file_exists, index=False)
                print(f"🚀 Validated and saved. Added {len(df_new)} new articles.")
            except Exception as e:
                print(f"❌ Error saving CSV: {e}")
        else:
            print("✨ No new unique articles to save.")

if __name__ == "__main__":
    scraper = CompetitorScraper()

    scraper.backfill_scores()

    # Reader-side competitors (newsletter / content companies)
    scraper.scrape_generic("Morning Brew", "https://www.morningbrew.com/daily/stories")
    scraper.scrape_generic("The Hustle", "https://thehustle.co/")
    scraper.scrape_generic("Stratechery", "https://stratechery.com/")
    scraper.scrape_generic("Lenny's Newsletter", "https://www.lennysnewsletter.com/")
    scraper.scrape_generic("Benedict Evans", "https://www.ben-evans.com/benedictevans")
    scraper.scrape_generic("Bytes.dev", "https://bytes.dev/archives")

    # Advertiser-side competitors (newsletter ad platforms)
    scraper.scrape_generic("Beehiiv", "https://www.beehiiv.com/blog")
    scraper.scrape_generic("Paved", "https://www.paved.com/blog")

    scraper.save_data()
