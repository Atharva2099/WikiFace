#!/usr/bin/env python3
"""
Automated Hugging Face Model Wiki Page Generator

This script uses LLaMA 4 API to generate structured documentation for Hugging Face models,
validates the output with Pydantic schemas, and renders beautiful Markdown pages using Jinja2.
"""

import json
import os
import sys
import requests
import time
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from llama_api_client import LlamaAPIClient
import PyPDF2
from huggingface_hub import hf_hub_url, get_hf_file_metadata

from templates.schemas import ModelWikiPage, FileMetadata, PaperInfo, GitHubStats, ModelMindMapNode

# Optional import for sidebar scraping
try:
    from hf_sidebar_scraper import scrape_hf_model_sidebar
    SIDEBAR_SCRAPING_AVAILABLE = True
except ImportError:
    SIDEBAR_SCRAPING_AVAILABLE = False
    print("⚠️ Warning: hf_sidebar_scraper not available. Sidebar data will be skipped.")


def extract_markdown_section(markdown_text: str, heading: str, level: int = 2) -> Optional[str]:
    """
    Extracts the content of a specific Markdown section up to the next heading of the same level.
    Assumes heading is unique at its level.
    """
    heading_pattern = r'^\s*' + '#' * level + r'\s*' + re.escape(heading) + r'\s*$'
    lines = markdown_text.splitlines()
    
    in_section = False
    section_lines = []
    
    for line in lines:
        if re.match(heading_pattern, line):
            in_section = True
            # Don't include the heading itself, just its content
            continue
        
        if in_section:
            next_heading_pattern = r'^\s*#' * level + r'\s*.*$'
            if re.match(next_heading_pattern, line):
                break # Found next heading of same level, end section
            section_lines.append(line)
            
    if section_lines:
        return "\n".join(section_lines).strip()
    return None


def resolve_file_size(repo_id, filename):
    try:
        url = hf_hub_url(repo_id, filename)
        meta = get_hf_file_metadata(url)
        return meta.size
    except Exception as e:
        print(f"[WARN] Could not get size for {filename}: {e}")
        return None


def format_size(bytesize: Optional[int]) -> str:
    """Format file size to human-readable form."""
    if bytesize is None:
        return "unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytesize < 1024:
            return f"{bytesize:.1f} {unit}"
        bytesize /= 1024
    return f"{bytesize:.1f} TB"


def resolve_and_enrich_file_tree(repo_id: str, file_info_list: List[Any]) -> List[Dict[str, Any]]:
    """Resolve file sizes and create enriched file tree data."""
    resolved_files = []
    
    print(f"🔍 Resolving file sizes for {len(file_info_list)} files...")
    
    for f in file_info_list:
        # Get file size
        size_bytes = resolve_file_size(repo_id, f.rfilename)
        size_formatted = format_size(size_bytes)
        
        resolved_files.append({
            "name": f.rfilename,
            "url": f"https://huggingface.co/{repo_id}/resolve/main/{f.rfilename}",
            "size": size_bytes,
            "size_formatted": size_formatted
        })
        
        print(f"  📄 {f.rfilename}: {size_formatted}")
    
    return resolved_files


class ModelWikiGenerator:
    """Main class for generating model wiki pages."""
    
    def __init__(self, api_key: str, model_name: str = "anthropic/claude-3.5-sonnet", enable_sidebar_scraping: bool = True, gemini_api_key: Optional[str] = None):
        """Initialize the wiki generator with OpenRouter API client and optional Gemini API."""
        self.api_key = api_key  # Store API key directly for OpenRouter
        self.model_name = model_name
        self.enable_sidebar_scraping = enable_sidebar_scraping and SIDEBAR_SCRAPING_AVAILABLE
        self.gemini_api_key = gemini_api_key
        self.jinja_env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def load_model_data(self, model_dir: Path) -> Dict[str, Any]:
        """Load model_info.md and metadata.json from the model directory."""
        data = {}
        
        # Load metadata.json
        metadata_file = model_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                data['metadata'] = metadata
                
                # Resolve file sizes if file_tree data is available
                if 'file_tree' in metadata:
                    repo_id = metadata.get('repo_id', metadata.get('model_id', 'unknown/model'))
                    print(f"📦 Found {len(metadata['file_tree'])} files for {repo_id}")
                    
                    # Create mock file objects for resolve_and_enrich_file_tree
                    class MockFile:
                        def __init__(self, filename):
                            self.rfilename = filename
                    
                    mock_files = [MockFile(file_info['name']) for file_info in metadata['file_tree']]
                    data['resolved_files'] = resolve_and_enrich_file_tree(repo_id, mock_files)
                else:
                    data['resolved_files'] = []
        else:
            raise FileNotFoundError(f"metadata.json not found in {model_dir}")
        
        # Load model_info.md
        info_file = model_dir / "model_info.md"
        if info_file.exists():
            with open(info_file, 'r', encoding='utf-8') as f:
                data['readme'] = f.read()
        else:
            print(f"⚠️ Warning: model_info.md not found in {model_dir}")
            data['readme'] = ""
        
        return data
    
    def scrape_sidebar_data(self, repo_id: str) -> Dict[str, Any]:
        """Scrape additional metadata from the HuggingFace model page sidebar."""
        if not self.enable_sidebar_scraping:
            return {}
            
        try:
            print("🌐 Scraping additional sidebar data...")
            sidebar_data = scrape_hf_model_sidebar(repo_id, debug=False)
            
            # Filter out zero/empty values for cleaner output
            filtered_data = {}
            for key, value in sidebar_data.items():
                if key == "datasets_used" and value:
                    filtered_data[key] = value
                elif isinstance(value, int) and value > 0:
                    filtered_data[key] = value
                    
            if filtered_data:
                print(f"✅ Found sidebar data: {filtered_data}")
            else:
                print("ℹ️ No additional sidebar data found")
                
            return sidebar_data
            
        except Exception as e:
            print(f"⚠️ Warning: Could not scrape sidebar data: {e}")
            return {}
    
    def extract_pdf_text(self, pdf_path: Path, max_pages: int = 5) -> str:
        """Extract text from PDF files (e.g., research papers)."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for i, page in enumerate(reader.pages[:max_pages]):
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"⚠️ Warning: Could not extract text from {pdf_path}: {e}")
            return ""
    
    def _extract_known_image_urls(self, github_readme_content: str, hf_file_tree_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Extracts specific, known image URLs and their potential captions from README content
        and file tree, which LLM can then re-embed.
        """
        image_urls = []

        # 1. From GitHub README raw text (regex for specific patterns)
        # This is a simplified regex, might need to be more robust
        readme_image_pattern = r'img src="(https://raw.githubusercontent.com/amazon-science/chronos-forecasting/main/figures/[^"]+\.(?:png|svg))"'
        for match in re.findall(readme_image_pattern, github_readme_content):
            url = match
            # Try to infer a caption from surrounding text, or use filename
            caption = url.split('/')[-1].replace('-', ' ').replace('_', ' ').replace('.png', '').replace('.svg', '')
            if url not in [img['url'] for img in image_urls]:  # Avoid duplicates
                image_urls.append({"url": url, "caption": caption})

        # 2. From HF file_tree, looking for 'figures/'
        for f_info in hf_file_tree_data:
            if f_info['name'].startswith('figures/') and (f_info['name'].endswith('.png') or f_info['name'].endswith('.svg')):
                url = f_info['url']
                caption = f_info['name'].split('/')[-1].replace('-', ' ').replace('_', ' ').replace('.png', '').replace('.svg', '')
                if url not in [img['url'] for img in image_urls]:
                    image_urls.append({"url": url, "caption": caption})

        return image_urls

    def build_llama_prompt(self, model_data: Dict[str, Any], pdf_texts: List[str] = None) -> str:
        """Build the prompt for LLaMA 4 API to generate structured JSON."""
        
        schema_description = """
You are a technical documentation expert and AI model analyst. Your task is to generate a detailed, structured JSON object for a Hugging Face model wiki page.

You are provided with:
- Hugging Face metadata (README, config, tags, file tree, metrics)
- GitHub repo data (README, repo stats, topic tags, external links)
- One or more research papers (if available, with extracted text)

Your job is to create a **complete, informative, and human-readable** JSON structure.
**Strictly adhere to the provided JSON schema and instructions below for each field.**

Generate a JSON object matching this exact schema:

{
  "model_id": "string",
  "author": "string",
  "license": "string",
  "last_modified": "YYYY-MM-DD",
  "huggingface_url": "https://huggingface.co/...",
  "overview": "Rich explanation of what the model is, what problem it solves, how it works, and why it matters",
  "architecture": "Technical architecture explanation summarizing papers and config - focus on innovations, design choices, and tradeoffs.",
  "tags": ["tag1", "tag2"],
  "use_cases": ["contextual use case 1 with explanation of its application", "contextual use case 2 with explanation of its application"],
  "files": [{"name": "filename", "size_bytes": 12345, "size_human": "12.1 KB", "url": "https://..."}],
  "papers": [{"title": "Paper Title", "url": "https://...", "summary": "Key insights and contributions from this paper", "citation": "Proper BibTeX citation format"}],
  "github": {"repo_name": "owner/repo", "url": "https://github.com/...", "stars": 123, "forks": 45, "open_issues": 12, "contributors": ["user1", "user2"], "created_at": "YYYY-MM-DD", "last_updated": "YYYY-MM-DD", "topics": ["topic1", "topic2"], "description": "Interpretive summary of repo purpose, key modules, and design patterns. If contributor roles/key areas are inferable from the README, mention them here."},
  "downloads_last_month": 123456,
  "datasets_used": ["dataset1", "dataset2"],
  "adapter_count": 78,
  "finetune_count": 5362,
  "quantization_count": 13,

  "usage_guides": [ # Synthesize multiple sections from the 'Usage' or 'Installation' parts of READMEs.
    {
      "title": "Installation",
      "description": "Explanation of how to install the model's package and dependencies, explaining why these steps are needed.",
      "code_example": "pip install package\n# more code"
    },
    {
      "title": "Basic Forecasting",
      "description": "Explanation of how to perform a basic forecast with a code example, including data preparation and model loading, and explaining the purpose of each step.",
      "code_example": "import pandas\n# more code",
      "image_url": "https://raw.githubusercontent.com/.../main-figure.png", # IF an image is explicitly mentioned and linked in the README associated with this usage. ONLY provide URLs from the provided external_links_in_readme or file_tree lists.
      "image_caption": "High-level depiction of Chronos workflow."
    },
    # ... other usage sections like 'Extracting Embeddings', 'Fine-tuning Custom Data', 'Deployment' (from README tips)
  ],
  "benchmarks": [ # Parse detailed benchmark tables from papers (e.g., Figures 4 & 5 / Tables 7-10 from 2403.07815.pdf).
    {
      "title": "Performance on Benchmark I (In-domain)",
      "description": "Interpretive paragraph explaining the results of this benchmark, e.g., which models performed best and why. May include image embeds if directly mentioned and linked to this benchmark from source files.",
      "markdown_table": "| Header1 | Header2 |\n|---|---|\n| Value1 | Value2 |", # The raw Markdown table content
      "image_url": "https://raw.githubusercontent.com/.../zero_shot-agg_scaled_score.svg", # IF an image is explicitly mentioned and linked in the README (like zero_shot-agg_scaled_score.svg) and directly illustrates this benchmark. ONLY provide URLs from the provided external_links_in_readme or file_tree lists.
      "image_caption": "Aggregated relative scores on Benchmark I."
    },
    # ... other benchmark tables ...
  ],
  "limitations": "Concise Markdown paragraph summarizing model limitations (e.g., from paper sections like 'Qualitative Analysis and Limitations').",
  "ethical_considerations": "Concise Markdown paragraph for ethical considerations, if explicitly mentioned in the documents. If not mentioned, return empty string.",
  "future_work": "Concise Markdown paragraph outlining future work or research directions (e.g., from paper sections like 'Discussion').",
  "key_hyperparameters": [ # Extract key training/model hyperparameters (name-value pairs) from paper sections like 'Training Corpus and Protocols' or 'Baselines'.
    {"name": "Learning Rate", "value": "0.001"},
    {"name": "Context Length", "value": "512"},
    # ... other key parameters ...
  ],
  "external_resources": [ # External URLs mentioned in READMEs or papers, with titles if available.
    {"title": "Amazon Science Blog Post", "url": "https://www.amazon.science/blog/..."}
  ],
  "mindmap": [
    {"id": "root", "label": "Model Name", "children": [...] } # As currently generated
  ]
}

**Instructions for LLaMA 4:**
1.  **Strict JSON Output:** Only output the JSON object. No conversational text or extraneous characters.
2.  **Synthesis over Repetition:** Do not just copy-paste. Synthesize, interpret, and explain.
3.  **Detailed Section Generation:**
    * **`usage_guides`**: Create multiple `UsageGuideSection` objects. Each `title` should be a clear action (e.g., "Installation," "Basic Forecasting"). `description` should explain the *purpose* or *why* someone would use this feature. `code_example` should be the actual, runnable code. **Only include `image_url` and `image_caption` if the image is explicitly linked within the original README/paper *and* clearly illustrates that specific usage guide section. Prefer images from `github.com/amazon-science/chronos-forecasting/figures/` if relevant.**
    * **`benchmarks`**: Create multiple `BenchmarkTable` objects. Parse the detailed tables from the PDF (specifically, the content related to Figures 4 & 5, and Tables 7-10 in `2403.07815.pdf`). Provide an `image_url` and `image_caption` if the corresponding visual (`zero_shot-agg_scaled_score.svg`, `main-figure.png` or others from the `figures/` folder linked in the README) *directly* represents that benchmark table. The `description` should be a brief interpretation of the results shown in that specific `markdown_table`.
    * **`limitations`**: Synthesize from Sections like 5.7 ("Qualitative Analysis and Limitations") of `2403.07815.pdf`.
    * **`ethical_considerations`**: Scan all provided documents for explicit mentions of ethical considerations, biases, or societal impact. If none are found, return an empty string for this field.
    * **`future_work`**: Synthesize from Sections like 6 ("Discussion") of `2403.07815.pdf`.
    * **`key_hyperparameters`**: Extract key parameters from Section 5.2 ("Training Corpus and Protocols") and Appendix C ("Baselines", Table 5) of `2403.07815.pdf`. Provide distinct `name` and `value` pairs.
    * **`external_resources`**: Collect all external links from `github_data.md`'s `external_links_in_readme` and `model_info.md`'s `external_links`. For each, provide a meaningful `title` (e.g., "Amazon Science Blog Post") if inferable, otherwise use the URL as title.

**Data Sources:**
* Model metadata: `metadata.json`
* README content, external links: `model_info.md`, `github_data.md`
* Paper content, benchmarks, limitations, future work, hyperparameters: `2403.07815.pdf`, `1910.10683.pdf`

Focus on synthesis and insight, not repetition. Be technical but accessible.

Create a multi-level Mermaid mind map that represents the full modeling pipeline, including architecture, preprocessing, training, inference, evaluation, and applications. Use meaningful labels, and ensure each level logically flows from parent to child. Use max width constraints — avoid flattening everything under a single node.

Your goal is not to summarize, but to distill. Write like a technical author who understands the codebase, its papers, and its architecture. Use academic insight and engineering interpretation.

Where benchmarks are mentioned, convert to structured Markdown tables with specific metrics, baselines, and interpretive notes.

Where architecture is discussed, explain not just what was used, but why it was chosen and what design tradeoffs were made.

Render all visual elements (file trees, mind maps) in compact, semantic Mermaid blocks.
"""
        
        prompt = f"""{schema_description}

Given the following Hugging Face model data, generate a comprehensive structured JSON object. Only output valid JSON.

## Model Metadata:
{json.dumps(model_data.get('metadata', {}), indent=2)}

## README Content:
{model_data.get('readme', 'No README available')}

## File Tree with Sizes:
{json.dumps(model_data.get('resolved_files', []), indent=2)}

## Additional Sidebar Data:
{json.dumps(model_data.get('sidebar', {}), indent=2)}

## Known Image URLs:
{json.dumps(model_data.get('known_images', []), indent=2)}
"""
        
        if pdf_texts:
            prompt += "\n## Research Paper Content:\n"
            for i, text in enumerate(pdf_texts, 1):
                prompt += f"\n### Paper {i}:\n{text[:2000]}...\n"
        
        prompt += "\n\nGenerate the comprehensive JSON object now:"
        
        return prompt
    
    def call_llama_api(self, prompt: str) -> str:
        """Call OpenRouter API with the constructed prompt."""
        try:
            messages = [
                {
                    "role": "system", 
                    "content": "You are a technical documentation expert and AI model analyst creating comprehensive wiki pages for ML researchers and engineers. Focus on synthesis, insight, and readability - avoid regurgitating input text. Generate detailed multi-level mind maps representing the full modeling pipeline. Write like a technical author who understands the codebase and papers. Convert benchmarks to structured tables with metrics and baselines. Explain architectural choices and design tradeoffs, not just what was used. Always respond with valid JSON only. Do not include any explanatory text outside the JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Use OpenRouter API format
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo/llamathon",
                "X-Title": "HuggingFace Model Wiki Generator"
            }
            
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 4000
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            response_text = result['choices'][0]['message']['content']
            
            # Extract JSON from response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                return json_text
            else:
                raise ValueError("No valid JSON found in OpenRouter response")
                
        except Exception as e:
            raise Exception(f"OpenRouter API call failed: {e}")
    
    def validate_and_parse(self, json_text: str) -> ModelWikiPage:
        """Validate the LLM response using Pydantic schema."""
        try:
            # Parse JSON
            data = json.loads(json_text)
            
            # Validate with Pydantic
            wiki_page = ModelWikiPage.model_validate(data)
            
            return wiki_page
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from LLaMA: {e}")
        except Exception as e:
            raise ValueError(f"Pydantic validation failed: {e}")
    
    def render_markdown(self, wiki_page: ModelWikiPage) -> str:
        """Render the validated data to Markdown using Jinja2."""
        try:
            template = self.jinja_env.get_template('wiki_template.md.j2')
            
            # Convert Pydantic model to dict for Jinja2
            template_data = wiki_page.model_dump()
            
            rendered = template.render(**template_data)
            return rendered
            
        except Exception as e:
            raise Exception(f"Markdown rendering failed: {e}")
    
    def call_gemini_api(self, prompt: str, model: str = "gemini-2.5-pro", max_retries: int = 3) -> str:
        """Call Gemini API for summarization tasks with retry logic."""
        if not self.gemini_api_key:
            raise ValueError("Gemini API key not provided")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    params={'key': self.gemini_api_key}
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract text from Gemini response
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        parts = candidate['content']['parts']
                        if len(parts) > 0 and 'text' in parts[0]:
                            return parts[0]['text']
                
                raise ValueError("No valid response from Gemini API")
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 5  # Exponential backoff: 5, 10, 20 seconds
                        print(f"⏳ Rate limited. Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(f"Gemini API rate limit exceeded after {max_retries} attempts")
                else:
                    raise Exception(f"Gemini API HTTP error: {e}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Gemini API call failed: {e}")
            except Exception as e:
                raise Exception(f"Gemini API error: {e}")
        
        raise Exception("Gemini API call failed after all retries")
    
    def generate_paper_summary_with_gemini(self, pdf_texts: List[str]) -> List[str]:
        """Generate paper summaries using Gemini API."""
        if not pdf_texts or not self.gemini_api_key:
            return []
            
        summaries = []
        
        for i, pdf_text in enumerate(pdf_texts, 1):
            print(f"🤖 Generating summary for paper {i} using Gemini...")
            
            prompt = f"""
Analyze this research paper excerpt and provide a concise technical summary focusing on:

1. Main contribution and innovation
2. Key methodology or approach
3. Important results or findings
4. Significance for the field

Paper content:
{pdf_text[:3000]}...

Provide a 2-3 paragraph technical summary suitable for ML researchers:
"""
            
            try:
                summary = self.call_gemini_api(prompt)
                summaries.append(summary)
                print(f"✅ Generated summary for paper {i}")
            except Exception as e:
                print(f"⚠️ Warning: Could not generate summary for paper {i}: {e}")
                summaries.append("Summary generation failed.")
        
        return summaries
    
    def generate_wiki(self, model_dir: Path, pdf_files: List[Path] = None, output_dir: Path = None) -> Path:
        """Main method to generate a complete wiki page."""
        
        print(f"🚀 Generating wiki for model in: {model_dir}")
        
        # 1. Load inputs
        print("📁 Loading model data...")
        model_data = self.load_model_data(model_dir)
        
        # 1.5. Scrape sidebar data
        repo_id = model_data['metadata'].get('repo_id', model_data['metadata'].get('model_id', 'unknown/model'))
        sidebar_data = self.scrape_sidebar_data(repo_id)
        model_data['sidebar'] = sidebar_data
        
        # 1.7. Extract known image URLs for LLaMA to use
        print("🖼️ Extracting known image URLs...")
        # Load GitHub data if available
        github_data_file = model_dir / "github_data.md"
        github_readme_content = ""
        if github_data_file.exists():
            try:
                with open(github_data_file, 'r', encoding='utf-8') as f:
                    github_readme_content = f.read()
            except Exception as e:
                print(f"⚠️ Warning: Could not read github_data.md: {e}")
        
        known_images = self._extract_known_image_urls(
            github_readme_content,
            model_data.get('resolved_files', [])
        )
        model_data['known_images'] = known_images
        if known_images:
            print(f"✅ Found {len(known_images)} known images")
        else:
            print("ℹ️ No known images found")
        
        # 2. Extract PDF content if provided
        pdf_texts = []
        if pdf_files:
            print(f"📄 Extracting text from {len(pdf_files)} PDF(s)...")
            for pdf_file in pdf_files:
                text = self.extract_pdf_text(pdf_file)
                if text:
                    pdf_texts.append(text)
        
        # 2.5. Generate paper summaries with Gemini if enabled
        gemini_summaries = []
        if self.gemini_api_key and pdf_texts:
            print("🧠 Generating paper summaries with Gemini...")
            gemini_summaries = self.generate_paper_summary_with_gemini(pdf_texts)
            model_data['gemini_summaries'] = gemini_summaries
        
        # 3. Build prompt and call LLaMA 4
        print("🧠 Building prompt for LLaMA 4...")
        prompt = self.build_llama_prompt(model_data, pdf_texts)
        
        print("🤖 Calling LLaMA 4 API...")
        json_response = self.call_llama_api(prompt)
        
        # 4. Validate output
        print("✅ Validating response with Pydantic...")
        wiki_page = self.validate_and_parse(json_response)
        
        # 5. Render Markdown
        print("📝 Rendering Markdown...")
        markdown_content = self.render_markdown(wiki_page)
        
        # 6. Write output
        if output_dir is None:
            output_dir = Path("docs")
        
        output_dir.mkdir(exist_ok=True)
        
        model_id = wiki_page.model_id.replace("/", "_").replace(" ", "_")
        output_file = output_dir / f"{model_id}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"🎉 Wiki page generated: {output_file}")
        return output_file


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate Hugging Face model wiki pages using LLaMA 4")
    parser.add_argument("model_dir", type=Path, help="Directory containing model_info.md and metadata.json")
    parser.add_argument("--pdf", type=Path, action="append", help="PDF files to extract content from (can be used multiple times)")
    parser.add_argument("--output-dir", type=Path, default="docs", help="Output directory for generated wiki pages")
    parser.add_argument("--model", default="anthropic/claude-3.5-sonnet", help="LLaMA model to use")
    parser.add_argument("--no-sidebar", action="store_true", help="Disable sidebar scraping")
    parser.add_argument("--use-gemini", action="store_true", help="Use Gemini API for paper summarization")
    
    args = parser.parse_args()
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('LLAMA_4_API_KEY')
    gemini_api_key = os.getenv('GEMINI_API_KEY') if args.use_gemini else None
    
    if not api_key:
        print("❌ Error: LLAMA_4_API_KEY not found in environment variables")
        sys.exit(1)
    
    if args.use_gemini and not gemini_api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        sys.exit(1)
    
    # Initialize generator
    generator = ModelWikiGenerator(
        api_key=api_key, 
        model_name=args.model,
        enable_sidebar_scraping=not args.no_sidebar,
        gemini_api_key=gemini_api_key
    )
    
    try:
        # Generate wiki
        output_file = generator.generate_wiki(
            model_dir=args.model_dir,
            pdf_files=args.pdf or [],
            output_dir=args.output_dir
        )
        
        print(f"\n✨ Success! Wiki page saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 