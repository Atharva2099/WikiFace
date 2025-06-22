#!/usr/bin/env python3
"""
Script to generate categories data for the FrontEnd categories page.
This script reads the HF_listings folder structure and creates JSON data
that can be used by the categories.html page.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any

def get_model_info(model_dir: Path) -> Dict[str, Any]:
    """
    Extract information about a model from its directory.
    
    Args:
        model_dir: Path to the model directory
        
    Returns:
        Dictionary containing model information
    """
    model_info = {
        "name": model_dir.name,
        "path": str(model_dir.relative_to(Path("HF_listings"))),
        "metadata": {},
        "sidebar_info": {},
        "github_data": {},
        "model_info": {}
    }
    
    # Read metadata.json
    metadata_path = model_dir / "metadata.json"
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                model_info["metadata"] = json.load(f)
        except Exception as e:
            print(f"Error reading metadata for {model_dir.name}: {e}")
    
    # Read sidebar_info.json
    sidebar_path = model_dir / "sidebar_info.json"
    if sidebar_path.exists():
        try:
            with open(sidebar_path, 'r', encoding='utf-8') as f:
                model_info["sidebar_info"] = json.load(f)
        except Exception as e:
            print(f"Error reading sidebar info for {model_dir.name}: {e}")
    
    # Read github_data.md
    github_path = model_dir / "github_data.md"
    if github_path.exists():
        try:
            with open(github_path, 'r', encoding='utf-8') as f:
                model_info["github_data"] = {"content": f.read()}
        except Exception as e:
            print(f"Error reading GitHub data for {model_dir.name}: {e}")
    
    # Read model_info.md
    model_info_path = model_dir / "model_info.md"
    if model_info_path.exists():
        try:
            with open(model_info_path, 'r', encoding='utf-8') as f:
                model_info["model_info"] = {"content": f.read()}
        except Exception as e:
            print(f"Error reading model info for {model_dir.name}: {e}")
    
    return model_info

def scan_hf_listings() -> Dict[str, Any]:
    """
    Scan the HF_listings directory and extract all categories and models.
    
    Returns:
        Dictionary containing categories and their models
    """
    hf_listings_path = Path("HF_listings")
    
    if not hf_listings_path.exists():
        print("HF_listings directory not found!")
        return {}
    
    categories_data = {}
    
    # Iterate through all category directories
    for category_dir in hf_listings_path.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            categories_data[category_name] = {
                "name": category_name,
                "models": []
            }
            
            # Iterate through all model directories in this category
            for model_dir in category_dir.iterdir():
                if model_dir.is_dir():
                    model_info = get_model_info(model_dir)
                    categories_data[category_name]["models"].append(model_info)
    
    return categories_data

def generate_categories_json():
    """
    Generate the categories data and save it as JSON.
    """
    print("Scanning HF_listings directory...")
    categories_data = scan_hf_listings()
    
    # Create a simplified version for the frontend
    frontend_data = {
        "categories": [],
        "total_models": 0
    }
    
    for category_name, category_info in categories_data.items():
        models = category_info["models"]
        frontend_data["total_models"] += len(models)
        
        # Create simplified model data for frontend
        simplified_models = []
        for model in models:
            simplified_model = {
                "name": model["name"],
                "path": model["path"],
                "downloads": "N/A",
                "adapters": 0,
                "finetunes": 0,
                "quantizations": 0
            }
            
            # Extract data from sidebar_info if available
            if model["sidebar_info"]:
                sidebar = model["sidebar_info"]
                simplified_model["downloads"] = f"{sidebar.get('downloads_last_month', 0):,}"
                simplified_model["adapters"] = sidebar.get("adapter_count", 0)
                simplified_model["finetunes"] = sidebar.get("finetune_count", 0)
                simplified_model["quantizations"] = sidebar.get("quantization_count", 0)
            
            simplified_models.append(simplified_model)
        
        frontend_data["categories"].append({
            "name": category_name,
            "model_count": len(models),
            "models": simplified_models
        })
    
    # Save the data
    output_path = Path("FrontEnd/categories_data.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated categories data with {len(frontend_data['categories'])} categories and {frontend_data['total_models']} models")
    print(f"Data saved to {output_path}")
    
    return frontend_data

if __name__ == "__main__":
    generate_categories_json() 