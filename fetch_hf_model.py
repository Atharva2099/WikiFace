#!/usr/bin/env python3
"""
HuggingFace Trending Models Scraper - Enhanced Version
Scrapes the top 10 trending models from HuggingFace and saves each in its own folder.
Enhanced with file tree, external links extraction, and bug fixes.
"""

import requests
import json
import os
import re
from datetime import datetime
from pathlib import Path
import time
from huggingface_hub import model_info, hf_hub_download
from urllib.parse import urlparse

def extract_external_links(readme_content):
    """
    Extract external links from README content.
    
    Args:
        readme_content (str): The README content
    
    Returns:
        list: List of external URLs found
    """
    # Regex pattern to find URLs in markdown
    url_pattern = r'\[([^\]]+)\]\(([^)]+)\)|https?://[^\s\)]+'
    
    links = []
    
    # Find all markdown links and direct URLs
    matches = re.findall(url_pattern, readme_content)
    
    for match in matches:
        if isinstance(match, tuple):
            # Markdown link format [text](url)
            if len(match) == 2 and match[1]:
                url = match[1]
                if url.startswith('http'):
                    links.append(url)
        else:
            # Direct URL
            if match.startswith('http'):
                links.append(match)
    
    # Remove duplicates and sort
    unique_links = list(set(links))
    unique_links.sort()
    
    return unique_links

def get_trending_models(limit=10):
    """
    Get trending models from HuggingFace.
    
    Args:
        limit (int): Number of trending models to fetch (default: 10)
    
    Returns:
        list: List of trending model information
    """
    
    # HuggingFace models API endpoint
    url = "https://huggingface.co/api/models"
    
    try:
        print(f"Fetching top {limit} trending models...")
        
        # Get trending models
        response = requests.get(url, params={
            "sort": "downloads",
            "direction": "-1",
            "limit": limit
        })
        
        if response.status_code == 200:
            models = response.json()
            
            trending_models = []
            
            for model in models:
                if 'id' in model:
                    repo_id = model['id']
                    
                    try:
                        # Get detailed model information
                        info = model_info(repo_id, revision="main")
                        trending_models.append({
                            'repo_id': repo_id,
                            'name': info.modelId,
                            'author': info.author or model.get('author', {}).get('name', 'Unknown'),
                            'last_modified': info.lastModified,
                            'tags': info.tags,
                            'downloads': model.get('downloads', 0),
                            'likes': model.get('likes', 0),
                            'description': model.get('description', '')
                        })
                    except Exception as e:
                        print(f"  Skipping {repo_id}: {str(e)}")
                        continue
                    
                    if len(trending_models) >= limit:
                        break
            
            return trending_models
        else:
            print(f"Error fetching trending models: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def fetch_and_save_model_data(repo_id, output_dir):
    """
    Fetch model data and save to a specific directory.
    
    Args:
        repo_id (str): The model repository ID
        output_dir (str): Output directory path
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        print(f"Processing: {repo_id}")
        
        # Get model information
        info = model_info(repo_id, revision="main")
        
        # Prepare file tree with download URLs
        file_tree = []
        for file in info.siblings:
            file_tree.append({
                'name': file.rfilename,
                'size': file.size,
                'url': f"https://huggingface.co/{repo_id}/resolve/main/{file.rfilename}"
            })
        
        # Try to fetch and include README content
        readme_file = next((f for f in info.siblings if f.rfilename.lower() == "readme.md"), None)
        readme_content = ""
        external_links = []
        
        if readme_file:
            try:
                print(f"  Fetching README.md for {repo_id}...")
                readme_path = hf_hub_download(repo_id=repo_id, filename=readme_file.rfilename)
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                # Extract external links from README
                external_links = extract_external_links(readme_content)
                
            except Exception as e:
                print(f"  Error fetching README.md: {str(e)}")
        
        # Create markdown content
        markdown_content = f"""# {info.modelId}

## Model Information

- **Model ID**: {info.modelId}
- **Author**: {info.author or "—"}
- **Last Updated**: {info.lastModified}
- **Repository**: https://huggingface.co/{repo_id}

## Tags

{', '.join(info.tags) if info.tags else "No tags"}

## File Tree

"""
        
        # Add file tree with download links
        for file in file_tree:
            markdown_content += f"- **{file['name']}** ({file['size']} bytes)\n  - Download: [{file['url']}]({file['url']})\n"
        
        # Add external links section if any found
        if external_links:
            markdown_content += f"""

## External Links

"""
            for link in external_links:
                domain = urlparse(link).netloc
                markdown_content += f"- [{domain}]({link})\n"
        
        # Add README content
        if readme_content:
            markdown_content += f"""

## README.md

```markdown
{readme_content}
```
"""
        else:
            markdown_content += """

## README.md

*No README.md found in the repository*
"""
        
        # Add metadata
        markdown_content += f"""

---

*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*Source: https://huggingface.co/{repo_id}*
"""
        
        # Write to file
        output_file = os.path.join(output_dir, "model_info.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save enhanced metadata as JSON
        metadata = {
            'repo_id': repo_id,
            'model_id': info.modelId,
            'author': info.author,
            'last_modified': str(info.lastModified) if info.lastModified else None,  # Fixed: keep as string
            'tags': info.tags,
            'files_count': len(info.siblings),
            'file_tree': file_tree,  # Enhanced: full file tree with URLs
            'external_links': external_links,  # New: extracted external links
            'has_readme': readme_file is not None,
            'scraped_at': datetime.now().isoformat()
        }
        
        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Saved to: {output_dir}")
        print(f"  📁 Files: {len(file_tree)}")
        print(f"  �� External links: {len(external_links)}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {repo_id}: {str(e)}")
        return False

def main():
    """Main function to scrape trending models and save them."""
    
    # Create output directory
    output_base = "HF_listings"
    Path(output_base).mkdir(exist_ok=True)
    
    print("🚀 Starting Enhanced HuggingFace Trending Models Scraper")
    print(f"📁 Output directory: {output_base}")
    print("-" * 50)
    
    # Get trending models
    trending_models = get_trending_models(10)
    
    if not trending_models:
        print("❌ No trending models found or error occurred.")
        return
    
    print(f"📊 Found {len(trending_models)} trending models")
    print("-" * 50)
    
    # Process each model
    successful = 0
    for i, model in enumerate(trending_models, 1):
        print(f"\n[{i}/{len(trending_models)}] Processing: {model['repo_id']}")
        
        # Create directory for this model
        safe_name = model['repo_id'].replace("/", "_")
        model_dir = os.path.join(output_base, safe_name)
        Path(model_dir).mkdir(exist_ok=True)
        
        # Fetch and save model data
        if fetch_and_save_model_data(model['repo_id'], model_dir):
            successful += 1
        
        # Add a small delay to be respectful to the API
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"🎉 Enhanced scraping completed!")
    print(f"✅ Successfully processed: {successful}/{len(trending_models)} models")
    print(f"📁 All data saved in: {output_base}/")
    print("=" * 50)

if __name__ == "__main__":
    main()
