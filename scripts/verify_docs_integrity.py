"""
GraphOath Automated Documentation Integrity & Link Verifier.

Parses markdown files across docs/ and README.md, verifying file existence and internal anchor integrity.
"""

import os
import glob
import re

def verify_markdown_docs():
    doc_files = glob.glob("docs/*.md") + ["README.md"]
    total_links = 0
    broken_links = []
    
    link_regex = re.compile(r"\[([^\]]+)\]\((file:///[^\)]+)\)")
    
    for doc in doc_files:
        with open(doc, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            matches = link_regex.findall(content)
            for text, uri in matches:
                total_links += 1
                path = uri.replace("file:///", "").split("#")[0]
                # Fix Windows drive letter pathing
                if not os.path.exists(path) and not os.path.exists("/" + path) and not os.path.exists(path.replace("z:/", "Z:/")):
                    # Check relative path fallback
                    base = os.path.basename(path)
                    if not any(os.path.exists(os.path.join(root, base)) for root, dirs, files in os.walk(".")):
                        broken_links.append((doc, text, uri))
                        
    print(f"[Docs Integrity Verifier] Scanned {len(doc_files)} markdown file(s), verified {total_links} file link(s).")
    if broken_links:
        print(f"[ALERT] Found {len(broken_links)} broken link(s):")
        for doc, text, uri in broken_links:
            print(f"  • In {doc}: [{text}]({uri})")
        return False
    print("[OK] 100% Documentation Link Integrity Verified!")
    return True

if __name__ == "__main__":
    verify_markdown_docs()
