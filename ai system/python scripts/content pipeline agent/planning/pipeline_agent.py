import pandas as pd  # type: ignore[import-not-found]
from typing import Dict, List
import os
import glob

# Constants
TRACKER_CSV = "../../../../docs/competitor content tracker/blogs/competitor_content_tracker.csv"
PIPELINE_CSV = "../../../../docs/competitor content tracker/blogs/content_pipeline.csv"
CORE_CONTEXT_DIR = "../../../../commands/core/"
IDENTITY_CONTEXT_DIR = "../../../../commands/identity/"

class PipelineAgent:
    def __init__(self):
        self.context_keywords = self._load_context_keywords()

    def _load_context_keywords(self) -> Dict[str, List[str]]:
        """
        Loads keywords from markdown files in core/identity folders to help with concept mapping.
        Simple logic: Extract headers or bold terms as keywords.
        """
        keywords: Dict[str, List[str]] = {
            'strategy': [],
            'tactical': [],
            'technical': [],
            'messaging': []
        }
        
        # Heuristic mapping based on file names or content
        # For now, we manually map some high-value terms based on file existence/content scan
        # Real implementation would parse MD files.
        # Let's seed with known good keywords from Product DNA / ICP.
        keywords['strategy'] = ['revenue', 'growth', 'subscriber', 'monetization', 'open rate', 'retention', 'acquisition', 'network effect', 'flywheel', 'roi']
        keywords['tactical'] = ['email', 'newsletter', 'curation', 'editorial', 'ads', 'sponsored', 'placement', 'copywriting', 'campaign', 'native']
        keywords['technical'] = ['api', 'analytics', 'tracking', 'automation', 'data', 'infrastructure', 'integration', 'platform']
        keywords['messaging'] = ['media', 'brand', 'audience', 'engagement', 'community', 'trust', 'thought leadership', 'content']
        
        return keywords

    def generate_concept(self, title, summary=""):
        """
        Generates a concept/angle based on the title and our context.
        """
        text = (title + " " + summary).lower()
        concept = "General Industry News" # Default
        
        # Check against context buckets
        scores = {k: 0 for k in self.context_keywords}
        for category, terms in self.context_keywords.items():
            for term in terms:
                if term in text:
                    scores[category] += 1
        
        # Determine dominant category
        best_cat = max(scores.keys(), key=lambda k: scores[k])
        if scores[best_cat] > 0:
            if best_cat == 'strategy':
                concept = f"Strategic Deep Dive: {title.split(':')[0]}"
            elif best_cat == 'tactical':
                concept = f"Tactical Playbook: How to leverage {title.split(':')[0]} features"
            elif best_cat == 'technical':
                concept = f"Technical Implementation: {title.split(':')[0]}"
            elif best_cat == 'messaging':
                concept = f"Thought Leadership: The Future of {title.split(':')[0]}"
        
        return concept

    def run(self):
        print("🚀 Pipeline Agent Starting...")
        
        # Paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        tracker_path = os.path.join(base_dir, TRACKER_CSV)
        pipeline_path = os.path.join(base_dir, PIPELINE_CSV)
        
        if not os.path.exists(tracker_path):
            print(f"⚠️ Tracker CSV not found at {tracker_path}")
            return

        try:
            # Load Data
            df_tracker = pd.read_csv(tracker_path)
            
            # Filter High Scoring (Weighted Score > 1.0)
            # Ensure col exists
            if 'Weighted_Score' not in df_tracker.columns:
                print("⚠️ Weighted_Score column missing in tracker.")
                return

            high_value_df = df_tracker[df_tracker['Weighted_Score'] > 1.0].copy()
            
            if high_value_df.empty:
                print("✨ No high-scoring articles found to pipeline.")
                return

            # Load existing pipeline to deduplicate
            existing_urls = set()
            if os.path.exists(pipeline_path):
                try:
                    df_pipeline = pd.read_csv(pipeline_path)
                    if 'Competitor URL' in df_pipeline.columns:
                        existing_urls = set(df_pipeline['Competitor URL'].tolist())
                except Exception:
                    pass # File exists but maybe empty or corrupt

            # Filter out existing
            new_candidates = high_value_df[~high_value_df['Link URL'].isin(existing_urls)].copy()
            
            if new_candidates.empty:
                print("✨ No NEW high-scoring articles to pipeline.")
                return
            
            print(f"🔍 Found {len(new_candidates)} new high-value articles. Generating concepts...")

            # Generate Pipeline Entries
            pipeline_entries = []
            for _, row in new_candidates.iterrows():
                concept = self.generate_concept(str(row['Title']), str(row.get('Summary', '')))
                
                entry = {
                    'Concept': concept,
                    'Article Title': row['Title'],
                    'Competitor URL': row['Link URL'],
                    'Relevance': row.get('Relevance', 0),
                    'Impact': row.get('Impact', 0),
                    'Effort': row.get('Effort', 0),
                    'Weighted_Score': row.get('Weighted_Score', 0),
                    'Status': 'Not Started'
                }
                pipeline_entries.append(entry)
            
            # Save
            df_new_pipeline = pd.DataFrame(pipeline_entries)
            
            # Sort by Weighted Score Descending
            df_new_pipeline = df_new_pipeline.sort_values(by='Weighted_Score', ascending=False)

            header_needed = not os.path.exists(pipeline_path) or os.stat(pipeline_path).st_size == 0
            df_new_pipeline.to_csv(pipeline_path, mode='a', header=header_needed, index=False)
            
            print(f"✅ Added {len(df_new_pipeline)} new ideas to Content Pipeline.")

        except Exception as e:
            print(f"❌ Pipeline Agent Error: {e}")

if __name__ == "__main__":
    agent = PipelineAgent()
    agent.run()
