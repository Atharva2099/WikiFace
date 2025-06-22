#!/usr/bin/env python3
"""
Script to scan HF_listings_MD folder and identify which models have .md documentation files.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set

def scan_md_files() -> Dict[str, Set[str]]:
    """
    Scan the HF_listings_MD directory and find all available .md files.
    
    Returns:
        Dictionary mapping category names to sets of model names that have .md files
    """
    md_listings_path = Path("HF_listings_MD")
    
    if not md_listings_path.exists():
        print("HF_listings_MD directory not found!")
        return {}
    
    available_md_files = {}
    
    # Iterate through all category directories
    for category_dir in md_listings_path.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            available_md_files[category_name] = set()
            
            # Find all .md files in this category
            for md_file in category_dir.glob("*.md"):
                # Extract model name from filename (remove .md extension)
                model_name = md_file.stem
                available_md_files[category_name].add(model_name)
    
    return available_md_files

def update_categories_data():
    """
    Update the categories_data.json to include information about available .md files.
    """
    # Load existing categories data
    categories_data_path = Path("FrontEnd/categories_data.json")
    if not categories_data_path.exists():
        print("categories_data.json not found! Run generate_categories_data.py first.")
        return
    
    with open(categories_data_path, 'r', encoding='utf-8') as f:
        categories_data = json.load(f)
    
    # Scan for available .md files
    available_md_files = scan_md_files()
    
    # Update each model with md_file_available flag
    for category in categories_data["categories"]:
        category_name = category["name"]
        available_models = available_md_files.get(category_name, set())
        
        for model in category["models"]:
            # Check if this model has an .md file available
            model_has_md = model["name"] in available_models
            model["md_file_available"] = model_has_md
            
            if model_has_md:
                model["md_file_path"] = f"md_files/{category_name}/{model['name']}.md"
    
    # Save updated data
    with open(categories_data_path, 'w', encoding='utf-8') as f:
        json.dump(categories_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    total_models = sum(len(cat["models"]) for cat in categories_data["categories"])
    total_with_md = sum(
        sum(1 for model in cat["models"] if model.get("md_file_available", False))
        for cat in categories_data["categories"]
    )
    
    print(f"Updated categories data:")
    print(f"Total models: {total_models}")
    print(f"Models with .md files: {total_with_md}")
    print(f"Coverage: {total_with_md/total_models*100:.1f}%")
    
    # Print breakdown by category
    print("\nBreakdown by category:")
    for category in categories_data["categories"]:
        category_name = category["name"]
        total_in_category = len(category["models"])
        with_md = sum(1 for model in category["models"] if model.get("md_file_available", False))
        print(f"  {category_name}: {with_md}/{total_in_category} models have .md files")

if __name__ == "__main__":
    update_categories_data() 