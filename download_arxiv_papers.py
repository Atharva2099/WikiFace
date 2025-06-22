#!/usr/bin/env python3
"""
Script to download arXiv research papers from model_info.md files in HF_listings folder.
"""

import os
import re
import requests
import time
from pathlib import Path
from urllib.parse import urlparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_arxiv_links(content):
    """
    Extract arXiv links from the content of model_info.md file.
    
    Args:
        content (str): The content of the model_info.md file
        
    Returns:
        list: List of arXiv URLs found in the content
    """
    arxiv_links = []
    
    # Pattern 1: Find links in the format [arxiv.org](https://arxiv.org/abs/...)
    pattern1 = r'\[arxiv\.org\]\(https://arxiv\.org/abs/([^)]+)\)'
    matches1 = re.findall(pattern1, content, re.IGNORECASE)
    
    # Pattern 2: Find direct arXiv URLs
    pattern2 = r'https://arxiv\.org/abs/([^\s\)]+)'
    matches2 = re.findall(pattern2, content, re.IGNORECASE)
    
    # Pattern 3: Find arXiv IDs in tags (format: arxiv:1234.5678)
    pattern3 = r'arxiv:([0-9]+\.[0-9]+)'
    matches3 = re.findall(pattern3, content, re.IGNORECASE)
    
    # Combine all matches and create full URLs
    all_matches = set(matches1 + matches2 + matches3)
    
    for match in all_matches:
        # Clean up the match (remove any trailing characters)
        clean_match = match.split(')')[0].split(' ')[0].split('\n')[0]
        arxiv_url = f"https://arxiv.org/abs/{clean_match}"
        arxiv_links.append(arxiv_url)
    
    return list(set(arxiv_links))  # Remove duplicates

def download_arxiv_paper(arxiv_url, output_dir):
    """
    Download an arXiv paper as PDF.
    
    Args:
        arxiv_url (str): The arXiv URL (e.g., https://arxiv.org/abs/2403.07815)
        output_dir (str): Directory to save the PDF
        
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        # Extract arXiv ID from URL
        arxiv_id = arxiv_url.split('/')[-1]
        
        # Construct PDF URL
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        # Create output filename
        output_filename = f"{arxiv_id}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # Check if file already exists
        if os.path.exists(output_path):
            logger.info(f"Paper {arxiv_id} already exists, skipping...")
            return True
        
        # Download the PDF
        logger.info(f"Downloading {arxiv_id}...")
        response = requests.get(pdf_url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Save the PDF
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Successfully downloaded {arxiv_id} to {output_path}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {arxiv_url}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error downloading {arxiv_url}: {e}")
        return False

def process_model_folder(model_folder_path):
    """
    Process a single model folder to extract and download arXiv papers.
    
    Args:
        model_folder_path (str): Path to the model folder
        
    Returns:
        tuple: (model_name, num_papers_found, num_papers_downloaded)
    """
    model_name = os.path.basename(model_folder_path)
    # Get the task category (parent directory name)
    task_category = os.path.basename(os.path.dirname(model_folder_path))
    model_info_path = os.path.join(model_folder_path, "model_info.md")
    
    if not os.path.exists(model_info_path):
        logger.warning(f"model_info.md not found in {task_category}/{model_name}")
        return model_name, 0, 0
    
    try:
        # Read the model_info.md file
        with open(model_info_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract arXiv links
        arxiv_links = extract_arxiv_links(content)
        
        if not arxiv_links:
            logger.info(f"No arXiv links found in {task_category}/{model_name}")
            return model_name, 0, 0
        
        logger.info(f"Found {len(arxiv_links)} arXiv links in {task_category}/{model_name}: {arxiv_links}")
        
        # Download each paper
        successful_downloads = 0
        for arxiv_url in arxiv_links:
            if download_arxiv_paper(arxiv_url, model_folder_path):
                successful_downloads += 1
            # Add a small delay to be respectful to arXiv servers
            time.sleep(1)
        
        return model_name, len(arxiv_links), successful_downloads
        
    except Exception as e:
        logger.error(f"Error processing {task_category}/{model_name}: {e}")
        return model_name, 0, 0

def main():
    """
    Main function to process all model folders in HF_listings.
    """
    # Get the current directory
    current_dir = os.getcwd()
    hf_listings_dir = os.path.join(current_dir, "HF_listings")
    
    if not os.path.exists(hf_listings_dir):
        logger.error(f"HF_listings directory not found at {hf_listings_dir}")
        return
    
    logger.info(f"Starting to process models in {hf_listings_dir}")
    
    # Get all model folders recursively (search through task subdirectories)
    model_folders = []
    for root, dirs, files in os.walk(hf_listings_dir):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # Check if this directory contains a model_info.md file (indicating it's a model folder)
            model_info_path = os.path.join(dir_path, "model_info.md")
            if os.path.exists(model_info_path):
                model_folders.append(dir_path)
    
    if not model_folders:
        logger.warning("No model folders found in HF_listings")
        return
    
    logger.info(f"Found {len(model_folders)} model folders to process")
    
    # Process each model folder
    total_papers_found = 0
    total_papers_downloaded = 0
    
    for model_folder in model_folders:
        model_name, papers_found, papers_downloaded = process_model_folder(model_folder)
        task_category = os.path.basename(os.path.dirname(model_folder))
        total_papers_found += papers_found
        total_papers_downloaded += papers_downloaded
        
        logger.info(f"Processed {task_category}/{model_name}: {papers_downloaded}/{papers_found} papers downloaded")
    
    # Summary
    logger.info("=" * 50)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total models processed: {len(model_folders)}")
    logger.info(f"Total arXiv papers found: {total_papers_found}")
    logger.info(f"Total papers successfully downloaded: {total_papers_downloaded}")
    logger.info(f"Success rate: {total_papers_downloaded/total_papers_found*100:.1f}%" if total_papers_found > 0 else "No papers found")

if __name__ == "__main__":
    main() 