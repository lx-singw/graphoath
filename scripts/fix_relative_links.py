"""
Fixes all absolute file:/// links in markdown files by converting them to clean relative paths.
"""

import glob
import re

PREFIX = "file:///z:/home/lx_singw/projects/graphoath/"

def fix_links():
    md_files = glob.glob("docs/*.md") + glob.glob("examples/*.md") + ["README.md"]
    modified_count = 0
    
    for filepath in md_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if PREFIX in content:
            new_content = content.replace(PREFIX, "")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified_count += 1
            print(f"[Fixed Links] Converted file:/// links to relative paths in {filepath}")
            
    print(f"\n[Summary] Fixed relative links across {modified_count} file(s).")

if __name__ == "__main__":
    fix_links()
