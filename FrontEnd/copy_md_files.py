#!/usr/bin/env python3
"""
Script to copy .md files from HF_listings_MD to FrontEnd directory for web access.
"""

import shutil
from pathlib import Path

def copy_md_files():
    """
    Copy all .md files from HF_listings_MD to FrontEnd/md_files directory.
    """
    source_dir = Path("HF_listings_MD")
    target_dir = Path("FrontEnd/md_files")
    
    if not source_dir.exists():
        print("HF_listings_MD directory not found!")
        return
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(exist_ok=True)
    
    copied_count = 0
    
    # Iterate through all category directories
    for category_dir in source_dir.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            
            # Create category subdirectory in target
            category_target_dir = target_dir / category_name
            category_target_dir.mkdir(exist_ok=True)
            
            # Copy all .md files in this category
            for md_file in category_dir.glob("*.md"):
                target_file = category_target_dir / md_file.name
                shutil.copy2(md_file, target_file)
                copied_count += 1
                print(f"Copied: {md_file} -> {target_file}")
    
    print(f"\nCopied {copied_count} .md files to FrontEnd/md_files/")

if __name__ == "__main__":
    copy_md_files() 