#!/usr/bin/env python3
"""
Script to extract GitHub data from repositories linked in model_info.md files.
This script finds GitHub links in model_info.md files and extracts comprehensive
repository data including metadata, contributors, issues, commits, and more.
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
from github import Github
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_github_links(content: str) -> List[str]:
    """
    Extract GitHub repository links from the content of model_info.md file.
    
    Args:
        content (str): The content of the model_info.md file
        
    Returns:
        list: List of GitHub repository URLs found in the content
    """
    github_links = []
    
    # Pattern 1: Find links in the format [github.com](https://github.com/...)
    pattern1 = r'\[github\.com\]\(https://github\.com/([^)]+)\)'
    matches1 = re.findall(pattern1, content, re.IGNORECASE)
    
    # Pattern 2: Find direct GitHub URLs
    pattern2 = r'https://github\.com/([^\s\)]+)'
    matches2 = re.findall(pattern2, content, re.IGNORECASE)
    
    # Pattern 3: Find GitHub links in various formats
    pattern3 = r'github\.com/([^\s\)]+)'
    matches3 = re.findall(pattern3, content, re.IGNORECASE)
    
    # Combine all matches and create full URLs
    all_matches = set(matches1 + matches2 + matches3)
    
    for match in all_matches:
        # Clean up the match (remove any trailing characters)
        clean_match = match.split(')')[0].split(' ')[0].split('\n')[0].split('#')[0]
        # Ensure it's a valid repository format (owner/repo)
        if '/' in clean_match and not clean_match.endswith('/'):
            github_url = f"https://github.com/{clean_match}"
            github_links.append(github_url)
    
    return list(set(github_links))  # Remove duplicates

def extract_repo_name_from_url(github_url: str) -> Optional[str]:
    """
    Extract repository name from GitHub URL.
    
    Args:
        github_url (str): GitHub repository URL
        
    Returns:
        str: Repository name in format 'owner/repo' or None if invalid
    """
    try:
        # Parse the URL
        parsed = urlparse(github_url)
        if parsed.netloc == 'github.com':
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) >= 2:
                return f"{path_parts[0]}/{path_parts[1]}"
    except Exception as e:
        logger.error(f"Error parsing GitHub URL {github_url}: {e}")
    
    return None

def extract_github_data(github_client: Github, repo_name: str) -> Dict[str, Any]:
    """
    Extract comprehensive data from a GitHub repository.
    
    Args:
        github_client (Github): Authenticated GitHub client
        repo_name (str): Repository name in format 'owner/repo'
        
    Returns:
        dict: Comprehensive repository data
    """
    try:
        repo = github_client.get_repo(repo_name)
        
        # Basic metadata
        info = {
            "id": repo.id,
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "html_url": repo.html_url,
            "clone_url": repo.clone_url,
            "ssh_url": repo.ssh_url,
            "homepage": repo.homepage,
            "topics": repo.get_topics(),
            "default_branch": repo.default_branch,
            "created_at": repo.created_at.isoformat() if repo.created_at else None,
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
            "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
            "size_kb": repo.size,
            "watchers_count": repo.watchers_count,
            "stargazers_count": repo.stargazers_count,
            "forks_count": repo.forks_count,
            "open_issues_count": repo.open_issues_count,
        }
        
        # License information
        try:
            lic = repo.get_license()
            info["license"] = {
                "key": lic.license.key,
                "name": lic.license.name,
                "spdx_id": lic.license.spdx_id,
                "url": lic.html_url
            }
        except Exception as e:
            logger.warning(f"Could not fetch license for {repo_name}: {e}")
            info["license"] = None
        
        # Language breakdown
        try:
            info["languages"] = repo.get_languages()
        except Exception as e:
            logger.warning(f"Could not fetch languages for {repo_name}: {e}")
            info["languages"] = {}
        
        # Top contributors
        try:
            info["top_contributors"] = [
                {"login": c.login, "contributions": c.contributions}
                for c in repo.get_contributors()[:20]
            ]
        except Exception as e:
            logger.warning(f"Could not fetch contributors for {repo_name}: {e}")
            info["top_contributors"] = []
        
        # File tree (sample)
        try:
            branch = repo.get_branch(repo.default_branch)
            tree = repo.get_git_tree(branch.commit.sha, recursive=True).tree
            info["file_tree_count"] = len(tree)
            info["file_tree_sample"] = [{"path": t.path, "type": t.type} for t in tree[:10]]
        except Exception as e:
            logger.warning(f"Could not fetch file tree for {repo_name}: {e}")
            info["file_tree_count"] = 0
            info["file_tree_sample"] = []
        
        # Issues and pull requests
        try:
            info["issues_count"] = repo.get_issues(state="all").totalCount
            info["pulls_count"] = repo.get_pulls(state="all").totalCount
        except Exception as e:
            logger.warning(f"Could not fetch issues/PRs for {repo_name}: {e}")
            info["issues_count"] = 0
            info["pulls_count"] = 0
        
        # Recent issues (sample)
        try:
            info["recent_issues"] = [
                {"number": i.number, "title": i.title, "state": i.state}
                for i in repo.get_issues(state="all", sort="created", direction="desc")[:5]
            ]
        except Exception as e:
            logger.warning(f"Could not fetch recent issues for {repo_name}: {e}")
            info["recent_issues"] = []
        
        # Recent pull requests (sample)
        try:
            info["recent_pulls"] = [
                {"number": p.number, "title": p.title, "state": p.state}
                for p in repo.get_pulls(state="all", sort="created", direction="desc")[:5]
            ]
        except Exception as e:
            logger.warning(f"Could not fetch recent PRs for {repo_name}: {e}")
            info["recent_pulls"] = []
        
        # Recent commits
        try:
            info["recent_commits"] = [
                {
                    "sha": c.sha,
                    "author": c.commit.author.name if c.commit.author else "Unknown",
                    "date": c.commit.author.date.isoformat() if c.commit.author and c.commit.author.date else None,
                    "message": c.commit.message.split("\n")[0] if c.commit.message else ""
                }
                for c in repo.get_commits()[:20]
            ]
        except Exception as e:
            logger.warning(f"Could not fetch recent commits for {repo_name}: {e}")
            info["recent_commits"] = []
        
        # README and external links
        try:
            readme = repo.get_readme()
            content = readme.decoded_content.decode("utf-8", errors="ignore")
            info["readme_text"] = content
            info["external_links_in_readme"] = list(set(
                re.findall(r"https?://[^\s)]+", content)
            ))
        except Exception as e:
            logger.warning(f"Could not fetch README for {repo_name}: {e}")
            info["readme_text"] = ""
            info["external_links_in_readme"] = []
        
        return info
        
    except Exception as e:
        logger.error(f"Error extracting data from {repo_name}: {e}")
        return {"error": str(e)}

def format_github_data_as_markdown(github_data: Dict[str, Any], repo_url: str) -> str:
    """
    Format GitHub data as a readable Markdown file.
    
    Args:
        github_data (dict): GitHub repository data
        repo_url (str): Original GitHub repository URL
        
    Returns:
        str: Formatted Markdown content
    """
    if "error" in github_data:
        return f"# GitHub Data Extraction Error\n\nError: {github_data['error']}\n\nRepository: {repo_url}"
    
    markdown = f"""# GitHub Repository Data

**Repository:** [{github_data['full_name']}]({github_data['html_url']})

## Basic Information

- **Description:** {github_data.get('description', 'No description')}
- **Created:** {github_data.get('created_at', 'Unknown')}
- **Last Updated:** {github_data.get('updated_at', 'Unknown')}
- **Last Pushed:** {github_data.get('pushed_at', 'Unknown')}
- **Default Branch:** {github_data.get('default_branch', 'Unknown')}
- **Size:** {github_data.get('size_kb', 0)} KB

## Statistics

- **Stars:** {github_data.get('stargazers_count', 0):,}
- **Forks:** {github_data.get('forks_count', 0):,}
- **Watchers:** {github_data.get('watchers_count', 0):,}
- **Open Issues:** {github_data.get('open_issues_count', 0):,}
- **Total Issues:** {github_data.get('issues_count', 0):,}
- **Pull Requests:** {github_data.get('pulls_count', 0):,}

## License

"""
    
    if github_data.get('license'):
        lic = github_data['license']
        markdown += f"- **Type:** {lic.get('name', 'Unknown')}\n"
        markdown += f"- **SPDX ID:** {lic.get('spdx_id', 'Unknown')}\n"
        markdown += f"- **URL:** [License]({lic.get('url', '#')})\n"
    else:
        markdown += "- **Type:** No license specified\n"
    
    # Languages
    languages = github_data.get('languages', {})
    if languages:
        markdown += "\n## Languages\n\n"
        for lang, bytes_count in languages.items():
            markdown += f"- **{lang}:** {bytes_count:,} bytes\n"
    
    # Topics
    topics = github_data.get('topics', [])
    if topics:
        markdown += "\n## Topics\n\n"
        for topic in topics:
            markdown += f"- `{topic}`\n"
    
    # Top Contributors
    contributors = github_data.get('top_contributors', [])
    if contributors:
        markdown += "\n## Top Contributors\n\n"
        for i, contrib in enumerate(contributors[:10], 1):
            markdown += f"{i}. **{contrib['login']}** - {contrib['contributions']} contributions\n"
    
    # File Tree Sample
    file_tree = github_data.get('file_tree_sample', [])
    if file_tree:
        markdown += f"\n## File Structure (Sample of {len(file_tree)} files)\n\n"
        markdown += f"Total files: {github_data.get('file_tree_count', 0):,}\n\n"
        for file_info in file_tree:
            markdown += f"- `{file_info['path']}` ({file_info['type']})\n"
    
    # Recent Issues
    recent_issues = github_data.get('recent_issues', [])
    if recent_issues:
        markdown += "\n## Recent Issues\n\n"
        for issue in recent_issues:
            status_emoji = "🟢" if issue['state'] == 'open' else "🔴"
            markdown += f"- {status_emoji} **#{issue['number']}** {issue['title']} ({issue['state']})\n"
    
    # Recent Pull Requests
    recent_pulls = github_data.get('recent_pulls', [])
    if recent_pulls:
        markdown += "\n## Recent Pull Requests\n\n"
        for pr in recent_pulls:
            status_emoji = "🟢" if pr['state'] == 'open' else "🔴"
            markdown += f"- {status_emoji} **#{pr['number']}** {pr['title']} ({pr['state']})\n"
    
    # Recent Commits
    recent_commits = github_data.get('recent_commits', [])
    if recent_commits:
        markdown += "\n## Recent Commits\n\n"
        for commit in recent_commits[:10]:
            markdown += f"- **{commit['sha'][:8]}** {commit['message']} - {commit['author']} ({commit.get('date', 'Unknown date')})\n"
    
    # External Links from README
    external_links = github_data.get('external_links_in_readme', [])
    if external_links:
        markdown += "\n## External Links Found in README\n\n"
        for link in external_links[:20]:  # Limit to first 20 links
            markdown += f"- {link}\n"
    
    # Raw JSON data (collapsed)
    markdown += f"\n## Raw Data\n\n<details>\n<summary>Click to expand raw JSON data</summary>\n\n```json\n{json.dumps(github_data, indent=2)}\n```\n\n</details>\n"
    
    return markdown

def process_model_folder(model_folder_path: str, github_client: Github) -> tuple:
    """
    Process a single model folder to extract GitHub data.
    
    Args:
        model_folder_path (str): Path to the model folder
        github_client (Github): Authenticated GitHub client
        
    Returns:
        tuple: (model_name, num_github_links_found, num_github_data_extracted)
    """
    model_name = os.path.basename(model_folder_path)
    task_category = os.path.basename(os.path.dirname(model_folder_path))
    model_info_path = os.path.join(model_folder_path, "model_info.md")
    
    if not os.path.exists(model_info_path):
        logger.warning(f"model_info.md not found in {task_category}/{model_name}")
        return model_name, 0, 0
    
    try:
        # Read the model_info.md file
        with open(model_info_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract GitHub links
        github_links = extract_github_links(content)
        
        if not github_links:
            logger.info(f"No GitHub links found in {task_category}/{model_name}")
            return model_name, 0, 0
        
        logger.info(f"Found {len(github_links)} GitHub links in {task_category}/{model_name}: {github_links}")
        
        # Extract data from each GitHub repository
        successful_extractions = 0
        all_github_data = []
        
        for github_url in github_links:
            repo_name = extract_repo_name_from_url(github_url)
            if repo_name:
                logger.info(f"Extracting data from {repo_name}...")
                github_data = extract_github_data(github_client, repo_name)
                all_github_data.append({
                    "repo_name": repo_name,
                    "repo_url": github_url,
                    "data": github_data
                })
                successful_extractions += 1
            else:
                logger.warning(f"Could not extract repo name from {github_url}")
        
        # Save combined GitHub data as markdown
        if all_github_data:
            github_data_path = os.path.join(model_folder_path, "github_data.md")
            
            # Combine all GitHub data into one markdown file
            combined_markdown = f"# GitHub Data for {model_name}\n\n"
            combined_markdown += f"**Task Category:** {task_category}\n\n"
            
            for i, repo_data in enumerate(all_github_data, 1):
                combined_markdown += f"## Repository {i}: {repo_data['repo_name']}\n\n"
                combined_markdown += format_github_data_as_markdown(repo_data['data'], repo_data['repo_url'])
                combined_markdown += "\n\n---\n\n"
            
            with open(github_data_path, 'w', encoding='utf-8') as f:
                f.write(combined_markdown)
            
            logger.info(f"GitHub data saved to {github_data_path}")
        
        return model_name, len(github_links), successful_extractions
        
    except Exception as e:
        logger.error(f"Error processing {task_category}/{model_name}: {e}")
        return model_name, 0, 0

def main():
    """
    Main function to process all model folders in HF_listings.
    """
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        logger.error("GITHUB_TOKEN not found in environment variables")
        logger.info("Please set GITHUB_TOKEN in your .env file")
        return
    
    # Initialize GitHub client
    try:
        github_client = Github(github_token)
        # Test the connection
        user = github_client.get_user()
        logger.info(f"Authenticated as GitHub user: {user.login}")
    except Exception as e:
        logger.error(f"Failed to authenticate with GitHub: {e}")
        return
    
    # Get the current directory
    current_dir = os.getcwd()
    hf_listings_dir = os.path.join(current_dir, "HF_listings")
    
    if not os.path.exists(hf_listings_dir):
        logger.error(f"HF_listings directory not found at {hf_listings_dir}")
        return
    
    logger.info(f"Starting to process models in {hf_listings_dir}")
    
    # Get all model folders recursively
    model_folders = []
    for root, dirs, files in os.walk(hf_listings_dir):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # Check if this directory contains a model_info.md file
            model_info_path = os.path.join(dir_path, "model_info.md")
            if os.path.exists(model_info_path):
                model_folders.append(dir_path)
    
    if not model_folders:
        logger.warning("No model folders found in HF_listings")
        return
    
    logger.info(f"Found {len(model_folders)} model folders to process")
    
    # Process each model folder
    total_github_links_found = 0
    total_github_data_extracted = 0
    
    for model_folder in model_folders:
        model_name, github_links_found, github_data_extracted = process_model_folder(model_folder, github_client)
        task_category = os.path.basename(os.path.dirname(model_folder))
        total_github_links_found += github_links_found
        total_github_data_extracted += github_data_extracted
        
        logger.info(f"Processed {task_category}/{model_name}: {github_data_extracted}/{github_links_found} GitHub repos extracted")
    
    # Summary
    logger.info("=" * 50)
    logger.info("GITHUB DATA EXTRACTION SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total models processed: {len(model_folders)}")
    logger.info(f"Total GitHub links found: {total_github_links_found}")
    logger.info(f"Total GitHub repositories successfully extracted: {total_github_data_extracted}")
    logger.info(f"Success rate: {total_github_data_extracted/total_github_links_found*100:.1f}%" if total_github_links_found > 0 else "No GitHub links found")

if __name__ == "__main__":
    main() 