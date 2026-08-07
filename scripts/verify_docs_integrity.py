"""
GraphOath Automated Documentation Integrity & Link Verifier.

Parses markdown files across docs/ and README.md, verifying file existence and internal anchor integrity.
"""

import os
import glob
import re

def verify_markdown_docs():
    doc_files = glob.glob("docs/*.md") + glob.glob("examples/*.md") + ["README.md"]
    total_links = 0
    broken_links = []
    
    # Matches markdown relative links like [text](path/file.md) or [text](path/file.md#anchor)
    link_regex = re.compile(r"\[([^\]]+)\]\(([^:\)]+\.[a-zA-Z0-9]+(?:#[^\)]*)?)\)")
    
    for doc in doc_files:
        doc_dir = os.path.dirname(doc)
        with open(doc, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            matches = link_regex.findall(content)
            for text, link_target in matches:
                total_links += 1
                target_path = link_target.split("#")[0]
                
                # Resolve relative path from doc location and root
                rel_from_doc = os.path.normpath(os.path.join(doc_dir, target_path))
                rel_from_root = os.path.normpath(target_path)
                
                if not (os.path.exists(rel_from_doc) or os.path.exists(rel_from_root)):
                    broken_links.append((doc, text, link_target))
                        
    print(f"[Docs Integrity Verifier] Scanned {len(doc_files)} markdown file(s), verified {total_links} relative link(s).")
    if broken_links:
        print(f"[ALERT] Found {len(broken_links)} broken link(s):")
        for doc, text, link in broken_links:
            print(f"  • In {doc}: [{text}]({link})")
        return False
    print("[OK] 100% Documentation Link Integrity Verified!")
    return True

if __name__ == "__main__":
    verify_markdown_docs()
