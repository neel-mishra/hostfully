import sys
import os
import re
from pathlib import Path
from collections import Counter
import math

def get_words(text):
    return [w.lower() for w in re.findall(r'[a-zA-Z0-9_]+', text) if len(w) > 2]

def score_file(file_path, prompt_words, root_dir):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        content_words = get_words(content)
        path_str = str(file_path.relative_to(root_dir))
        path_words = get_words(path_str)
        
        content_counter = Counter(content_words)
        path_counter = Counter(path_words)
        
        score = 0
        for word in prompt_words:
            # Term Frequency in content
            score += content_counter.get(word, 0)
            # Massive boost if the word is in the filename/path
            if path_counter.get(word, 0) > 0:
                score += 50
                
        return score
    except Exception as e:
        return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_context.py \"<user_prompt>\"")
        return

    prompt_args = [arg for i, arg in enumerate(sys.argv) if i > 0]
    prompt = " ".join(prompt_args)
    prompt_words = get_words(prompt)

    stop_words = {
        'the', 'and', 'for', 'with', 'about', 'like', 'through', 'over', 'before', 'between', 
        'after', 'since', 'without', 'under', 'within', 'along', 'following', 'across', 
        'behind', 'beyond', 'plus', 'except', 'but', 'out', 'around', 'down', 'off', 'above', 
        'near', 'what', 'who', 'how', 'when', 'where', 'why', 'are', 'was', 'were', 
        'have', 'has', 'had', 'does', 'did', 'can', 'could', 'should', 'would', 'may', 
        'might', 'must', 'that', 'this', 'these', 'those', 'build', 'make', 'create', 
        'update', 'fix', 'write', 'read', 'show', 'tell', 'use', 'using', 'run', 'running',
        'script', 'code', 'file', 'files', 'directory', 'project', 'workspace'
    }
    
    # Filter prompt words
    prompt_words = [w for w in prompt_words if w not in stop_words]

    if not prompt_words:
        print("No specific keywords identified for context retrieval.")
        return

    workspace_root = Path(os.getcwd())
    md_files = []
    
    skipped_dirs = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.gemini', '.claude'}

    # Collect all markdown files
    for root, dirs, files in os.walk(workspace_root):
        valid_dirs = [d for d in dirs if d not in skipped_dirs and not d.startswith('.')]
        dirs.clear()
        dirs.extend(valid_dirs)
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)

    scored_files = []
    for f in md_files:
        score = score_file(f, prompt_words, workspace_root)
        if score > 0:
            scored_files.append((score, f))

    # Sort by score descending
    scored_files.sort(key=lambda x: x[0], reverse=True)

    # Return top 3-5 relevant files based on score
    top_files = [scored_files[i] for i in range(min(5, len(scored_files)))]
    
    if not top_files:
        print("No highly relevant markdown files found.")
        return

    print("=== AUTOMATIC CONTEXT RETRIEVAL ===")
    print("Agent: Please read the following relevant files using your view_file tool before proceeding:\n")
    for score, f in top_files:
        rel_path = f.relative_to(workspace_root)
        print(f"- {rel_path} (Relevance Score: {score})")

if __name__ == "__main__":
    main()
