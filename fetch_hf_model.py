#!/usr/bin/env python3
"""
Enhanced HuggingFace Model Fetcher with Automatic Task Classification
Fetches top 3 trending models from each task category and automatically organizes them by task.
"""

import requests
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
import time
from huggingface_hub import model_info, hf_hub_download
from urllib.parse import urlparse
from collections import defaultdict

# Define task categories and their pipeline tags
TASK_CATEGORIES = {
    "Text Generation": ["text-generation", "text2text-generation"],
    "Text Classification": ["text-classification", "sentiment-analysis"],
    "Token Classification": ["token-classification", "fill-mask"],
    "Question Answering": ["question-answering"],
    "Translation": ["translation"],
    "Summarization": ["summarization"],
    "Image Classification": ["image-classification"],
    "Object Detection": ["object-detection"],
    "Image Segmentation": ["image-segmentation"],
    "Text-to-Image": ["text-to-image"],
    "Image-to-Text": ["image-to-text"],
    "Image-Text-to-Text": ["image-text-to-text"],
    "Text-to-Video": ["text-to-video"],
    "Text-to-Speech": ["text-to-speech"],
    "Audio Classification": ["audio-classification", "automatic-speech-recognition"],
    "Time Series": ["time-series-forecasting"],
    "Embeddings": ["feature-extraction"],
    "Multimodal": ["multimodal"],
    "Reinforcement Learning": ["reinforcement-learning"],
    "Code Generation": ["code-generation"],
    "Other": []
}

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

def get_trending_models_by_task(pipeline_tag, limit=3):
    """
    Get top models from HuggingFace for a specific task using downloads as the sort order.
    
    Args:
        pipeline_tag (str): The pipeline tag to filter by
        limit (int): Number of top models to fetch (default: 3)
    
    Returns:
        list: List of top model information
    """
    
    # HuggingFace models API endpoint
    url = "https://huggingface.co/api/models"
    
    try:
        print(f"Fetching top {limit} downloaded models for {pipeline_tag}...")
        
        # Get top models for specific pipeline tag
        response = requests.get(url, params={
            "pipeline_tag": pipeline_tag,
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
                            'pipeline_tag': pipeline_tag,
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
            print(f"Error fetching models for {pipeline_tag}: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return []
            
    except Exception as e:
        print(f"Error fetching {pipeline_tag}: {str(e)}")
        return []

def determine_primary_task(api_info, metadata):
    """
    Determine the primary task of a model based on API info and metadata.
    
    Args:
        api_info (dict): Model information from Hugging Face API
        metadata (dict): Local metadata from metadata.json
        
    Returns:
        str: Primary task category
    """
    # Check pipeline_tag first (most reliable)
    if api_info and api_info.get('pipeline_tag'):
        pipeline_tag = api_info['pipeline_tag'].lower()
        
        # Map pipeline tags to our categories
        for category, category_tags in TASK_CATEGORIES.items():
            if pipeline_tag in category_tags:
                return category
    
    # Check tags for specific indicators
    tags = []
    if api_info:
        tags.extend(api_info.get('tags', []))
    if metadata:
        tags.extend(metadata.get('tags', []))
    
    tags_lower = [tag.lower() for tag in tags]
    
    # Specific model type checks (highest priority)
    if "sentence-transformers" in tags_lower:
        return "Embeddings"
    
    if "clip" in tags_lower:
        return "Multimodal"
    
    if any(tag in tags_lower for tag in ["time-series", "forecasting", "chronos"]):
        return "Time Series"
    
    if any(tag in tags_lower for tag in ["rlhf", "ppo", "dpo", "reward-modeling"]):
        return "Reinforcement Learning"
    
    if any(tag in tags_lower for tag in ["text2text-generation", "text-generation"]):
        return "Text Generation"
    
    if any(tag in tags_lower for tag in ["text-classification", "sentiment-analysis"]):
        return "Text Classification"
    
    if any(tag in tags_lower for tag in ["fill-mask", "token-classification"]):
        return "Token Classification"
    
    if any(tag in tags_lower for tag in ["image-classification"]):
        return "Image Classification"
    
    if any(tag in tags_lower for tag in ["segmentation"]):
        return "Image Segmentation"
    
    if any(tag in tags_lower for tag in ["object-detection", "detection"]):
        return "Object Detection"
    
    if any(tag in tags_lower for tag in ["question-answering", "qa"]):
        return "Question Answering"
    
    if any(tag in tags_lower for tag in ["translation"]):
        return "Translation"
    
    if any(tag in tags_lower for tag in ["summarization"]):
        return "Summarization"
    
    if any(tag in tags_lower for tag in ["text-to-image", "diffusion", "stable-diffusion"]):
        return "Text-to-Image"
    
    if any(tag in tags_lower for tag in ["image-to-text", "image-captioning"]):
        return "Image-to-Text"
    
    if any(tag in tags_lower for tag in ["audio", "speech"]):
        return "Audio Classification"
    
    if any(tag in tags_lower for tag in ["code", "programming"]):
        return "Code Generation"
    
    # Check for general patterns
    if any(tag in tags_lower for tag in ["generation", "generative"]):
        return "Text Generation"
    
    if any(tag in tags_lower for tag in ["classification"]):
        return "Text Classification"
    
    if any(tag in tags_lower for tag in ["vision", "computer-vision"]):
        return "Image Classification"
    
    if any(tag in tags_lower for tag in ["multimodal", "vision-language"]):
        return "Multimodal"
    
    # Default fallback
    return "Other"

def fetch_and_save_model_data(repo_id, output_dir, pipeline_tag=None):
    """
    Fetch model data and save to a specific directory.
    
    Args:
        repo_id (str): The model repository ID
        output_dir (str): Output directory path
        pipeline_tag (str): The pipeline tag for this model
    
    Returns:
        tuple: (success, primary_task, metadata)
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
            'last_modified': str(info.lastModified) if info.lastModified else None,
            'tags': info.tags,
            'pipeline_tag': pipeline_tag,
            'files_count': len(info.siblings),
            'file_tree': file_tree,
            'external_links': external_links,
            'has_readme': readme_file is not None,
            'scraped_at': datetime.now().isoformat()
        }
        
        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Determine primary task
        primary_task = determine_primary_task({'pipeline_tag': pipeline_tag, 'tags': info.tags}, metadata)
        
        print(f"  ✅ Saved to: {output_dir}")
        print(f"  📁 Files: {len(file_tree)}")
        print(f"  🔗 External links: {len(external_links)}")
        print(f"  🏷️  Primary task: {primary_task}")
        
        return True, primary_task, metadata
        
    except Exception as e:
        print(f"  ❌ Error processing {repo_id}: {str(e)}")
        return False, "Other", None

def create_task_directories(base_dir, task_counts):
    """
    Create task directories and return the mapping.
    
    Args:
        base_dir (str): Base directory for task folders
        task_counts (dict): Dictionary with task counts
        
    Returns:
        dict: Mapping of task names to directory paths
    """
    task_dirs = {}
    
    for task in task_counts.keys():
        if task_counts[task] > 0:  # Only create directories for tasks that have models
            task_dir = os.path.join(base_dir, task)
            os.makedirs(task_dir, exist_ok=True)
            task_dirs[task] = task_dir
            print(f"Created task directory: {task_dir}")
    
    return task_dirs

def main():
    """Main function to fetch trending models by task and organize them."""
    
    # Create output directory
    output_base = "HF_listings"
    Path(output_base).mkdir(exist_ok=True)
    
    print("🚀 Starting Enhanced HuggingFace Model Fetcher with Task Classification")
    print(f"📁 Output directory: {output_base}")
    print("-" * 60)
    
    # Get models from each task category
    all_models = []
    task_counts = defaultdict(int)
    model_task_mapping = {}
    
    # Fetch top 3 models from each task category
    for category, pipeline_tags in TASK_CATEGORIES.items():
        if pipeline_tags:  # Skip "Other" category for fetching
            for pipeline_tag in pipeline_tags:
                print(f"\n📊 Fetching {category} models (pipeline: {pipeline_tag})...")
                models = get_trending_models_by_task(pipeline_tag, limit=3)
                
                for model in models:
        # Create directory for this model
        safe_name = model['repo_id'].replace("/", "_")
        model_dir = os.path.join(output_base, safe_name)
        Path(model_dir).mkdir(exist_ok=True)
        
        # Fetch and save model data
                    success, primary_task, metadata = fetch_and_save_model_data(
                        model['repo_id'], 
                        model_dir, 
                        pipeline_tag
                    )
                    
                    if success:
                        all_models.append(model)
                        task_counts[primary_task] += 1
                        model_task_mapping[safe_name] = {
                            'primary_task': primary_task,
                            'folder_path': model_dir,
                            'metadata': metadata,
                            'original_pipeline': pipeline_tag
                        }
        
        # Add a small delay to be respectful to the API
        time.sleep(1)
    
    # Create task-based organization
    print(f"\n📂 Creating task-based organization...")
    task_dirs = create_task_directories(output_base, task_counts)
    
    # Organize models into task directories
    print(f"🔄 Organizing models into task directories...")
    
    for model_name, info in model_task_mapping.items():
        primary_task = info['primary_task']
        source_path = info['folder_path']
        
        if primary_task in task_dirs:
            target_path = os.path.join(task_dirs[primary_task], model_name)
            
            try:
                if os.path.exists(target_path):
                    print(f"Model {model_name} already exists in {primary_task}, skipping...")
                else:
                    shutil.move(source_path, target_path)
                    print(f"Moved {model_name} to {primary_task}")
            except Exception as e:
                print(f"Error moving {model_name}: {e}")
        else:
            print(f"No directory found for task: {primary_task}")
    
    # Create summary file
    summary_path = os.path.join(output_base, "organization_summary.json")
    summary = {
        "total_models": len(all_models),
        "task_counts": dict(task_counts),
        "model_mappings": model_task_mapping,
        "operation": "fetch_and_organize",
        "categories_fetched": list(TASK_CATEGORIES.keys())
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎉 Enhanced fetching and organization completed!")
    print(f"✅ Total models processed: {len(all_models)}")
    print(f"📁 Output directory: {output_base}")
    print("\nTask distribution:")
    
    for task, count in sorted(task_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {task}: {count} models")
    
    print(f"\n📄 Summary saved to: {summary_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
