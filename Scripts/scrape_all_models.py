#!/usr/bin/env python3
"""
Script to run the HuggingFace sidebar scraper for all models in HF_listings folder.
This script will:
1. Find all model directories in HF_listings
2. Extract model IDs from metadata.json files
3. Run the scraper for each model
4. Save results as sidebar_info.json in each model directory
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import time

# Import the scraper functions
from hf_sidebar_scraper import scrape_hf_model_sidebar, scrape_multiple_models

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_model_id_from_metadata(metadata_path: Path) -> Optional[str]:
    """
    Extract the model ID from a metadata.json file.
    
    Args:
        metadata_path: Path to the metadata.json file
        
    Returns:
        Model ID string or None if not found
    """
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
        # Try different possible keys for model ID
        model_id = (
            metadata.get('repo_id') or 
            metadata.get('model_id') or 
            metadata.get('id') or
            metadata.get('name')
        )
        
        if model_id:
            return model_id
            
    except Exception as e:
        logger.error(f"Error reading metadata from {metadata_path}: {e}")
    
    return None


def find_all_model_directories(hf_listings_dir: Path) -> List[Path]:
    """
    Find all model directories in HF_listings that contain metadata.json.
    
    Args:
        hf_listings_dir: Path to the HF_listings directory
        
    Returns:
        List of model directory paths
    """
    model_dirs = []
    
    if not hf_listings_dir.exists():
        logger.error(f"HF_listings directory not found: {hf_listings_dir}")
        return model_dirs
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(hf_listings_dir):
        root_path = Path(root)
        
        # Check if this directory contains metadata.json
        metadata_path = root_path / "metadata.json"
        if metadata_path.exists():
            model_dirs.append(root_path)
            logger.info(f"Found model directory: {root_path}")
    
    return model_dirs


def scrape_model_and_save(model_dir: Path, debug: bool = False) -> bool:
    """
    Scrape a single model and save the results.
    
    Args:
        model_dir: Path to the model directory
        debug: Enable debug mode
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get model ID from metadata
        metadata_path = model_dir / "metadata.json"
        model_id = get_model_id_from_metadata(metadata_path)
        
        if not model_id:
            logger.warning(f"Could not extract model ID from {metadata_path}")
            return False
        
        # Get task category for logging
        task_category = model_dir.parent.name
        model_name = model_dir.name
        
        logger.info(f"Scraping {task_category}/{model_name} (ID: {model_id})")
        
        # Run the scraper
        sidebar_data = scrape_hf_model_sidebar(
            model_id=model_id,
            debug=debug,
            headless=True,
            timeout=15000
        )
        
        # Add metadata to the scraped data
        sidebar_data.update({
            "model_id": model_id,
            "task_category": task_category,
            "model_name": model_name,
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Save to sidebar_info.json
        output_path = model_dir / "sidebar_info.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sidebar_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[SUCCESS] Saved sidebar info to {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"[ERROR] Error scraping {model_dir}: {e}")
        return False


def main():
    """
    Main function to scrape all models in HF_listings.
    """
    # Get the current directory and HF_listings path
    current_dir = Path.cwd()
    hf_listings_dir = current_dir / "HF_listings"
    
    if not hf_listings_dir.exists():
        logger.error(f"HF_listings directory not found at {hf_listings_dir}")
        return
    
    logger.info(f"Starting to scrape models in {hf_listings_dir}")
    
    # Find all model directories
    model_dirs = find_all_model_directories(hf_listings_dir)
    
    if not model_dirs:
        logger.warning("No model directories found in HF_listings")
        return
    
    logger.info(f"Found {len(model_dirs)} model directories to scrape")
    
    # Scrape each model
    successful_scrapes = 0
    failed_scrapes = 0
    
    for i, model_dir in enumerate(model_dirs, 1):
        logger.info(f"\n--- Processing {i}/{len(model_dirs)} ---")
        
        # Check if sidebar_info.json already exists
        sidebar_path = model_dir / "sidebar_info.json"
        if sidebar_path.exists():
            logger.info(f"Sidebar info already exists for {model_dir.name}, skipping...")
            continue
        
        # Scrape the model
        success = scrape_model_and_save(model_dir, debug=False)
        
        if success:
            successful_scrapes += 1
        else:
            failed_scrapes += 1
        
        # Add a small delay between requests to be respectful
        if i < len(model_dirs):
            logger.info("Waiting 2 seconds before next request...")
            time.sleep(2)
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("SCRAPING SUMMARY")
    logger.info("="*50)
    logger.info(f"Total models processed: {len(model_dirs)}")
    logger.info(f"Successful scrapes: {successful_scrapes}")
    logger.info(f"Failed scrapes: {failed_scrapes}")
    logger.info(f"Success rate: {successful_scrapes/len(model_dirs)*100:.1f}%" if model_dirs else "No models processed")
    
    if successful_scrapes > 0:
        logger.info(f"\n[SUCCESS] Successfully scraped {successful_scrapes} models!")
        logger.info("Sidebar info saved as 'sidebar_info.json' in each model directory.")
    
    if failed_scrapes > 0:
        logger.warning(f"\n[WARNING] {failed_scrapes} models failed to scrape. Check the log for details.")


if __name__ == "__main__":
    main() 