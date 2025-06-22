#!/usr/bin/env python3
"""
Automated Hugging Face Model Wiki Page Generator

This script uses LLaMA 4 API to generate structured documentation for Hugging Face models,
validates the output with Pydantic schemas, and renders beautiful Markdown pages using Jinja2.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from llama_api_client import LlamaAPIClient
import PyPDF2
from huggingface_hub import hf_hub_url, get_hf_file_metadata

from templates.schemas import ModelWikiPage, FileEntry, PaperEntry

# Optional import for sidebar scraping
try:
    from hf_sidebar_scraper import scrape_hf_model_sidebar
    SIDEBAR_SCRAPING_AVAILABLE = True
except ImportError:
    SIDEBAR_SCRAPING_AVAILABLE = False
    print("⚠️ Warning: hf_sidebar_scraper not available. Sidebar data will be skipped.")


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
    
    def __init__(self, api_key: str, model_name: str = "Llama-4-Scout-17B-16E-Instruct-FP8", enable_sidebar_scraping: bool = True):
        """Initialize the wiki generator with LLaMA API client."""
        self.client = LlamaAPIClient(api_key=api_key)
        self.model_name = model_name
        self.enable_sidebar_scraping = enable_sidebar_scraping and SIDEBAR_SCRAPING_AVAILABLE
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
    
    def build_llama_prompt(self, model_data: Dict[str, Any], pdf_texts: List[str] = None) -> str:
        """Build the prompt for LLaMA 4 API to generate structured JSON."""
        
        schema_description = """
You are a technical documentation AI generating detailed, well-organized content for open-source machine learning models hosted on Hugging Face.

Your goal is to synthesize and explain, not just repeat the input. Generate a comprehensive JSON object matching this schema:

{
  "model_name": "string",
  "huggingface_url": "https://huggingface.co/...",
  "author": "string", 
  "last_updated": "YYYY-MM-DD",
  "license": "string or null",
  "tags": ["tag1", "tag2"],
  "overview": "High-level goals, approach, innovations - synthesized explanation",
  "architecture": "Structure, tokenization, vocabulary, training details - technical insights",
  "use_cases": ["practical use case 1", "practical use case 2"],
  "file_tree": [{"name": "filename", "size": 12345, "size_formatted": "12.1 KB", "url": "https://..."}],
  "papers": [{"title": "Paper Title", "url": "https://...", "summary": "Key insights and contributions", "citation": "Citation"}],
  "evaluation_summary": "Real metrics, benchmark results, performance insights",
  "references": ["Reference 1", "Reference 2"],
  "spaces_count": 88,
  "datasets_used": ["dataset1", "dataset2"],
  "adapter_count": 78,
  "finetune_count": 5362,
  "quantization_count": 13
}

Focus on:
- Explaining architectural innovations and training approaches
- Extracting real performance metrics and benchmarks
- Identifying practical use cases for developers
- Synthesizing insights from papers if provided
- Using the resolved file tree data with accurate sizes and URLs
- Being technical but accessible
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
"""
        
        if pdf_texts:
            prompt += "\n## Research Paper Content:\n"
            for i, text in enumerate(pdf_texts, 1):
                prompt += f"\n### Paper {i}:\n{text[:2000]}...\n"
        
        prompt += "\n\nGenerate the comprehensive JSON object now:"
        
        return prompt
    
    def call_llama_api(self, prompt: str) -> str:
        """Call LLaMA 4 API with the constructed prompt."""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a technical documentation AI generating detailed, well-organized content for machine learning models. Your goal is to synthesize and explain, not just repeat input. Always respond with valid JSON only. Do not include any explanatory text outside the JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            
            response_text = completion.completion_message.content.text
            
            # Extract JSON from response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                return json_text
            else:
                raise ValueError("No valid JSON found in LLaMA response")
                
        except Exception as e:
            raise Exception(f"LLaMA API call failed: {e}")
    
    def validate_and_parse(self, json_text: str) -> ModelWikiPage:
        """Validate the LLM response using Pydantic schema."""
        try:
            # Parse JSON
            data = json.loads(json_text)
            
            # Validate with Pydantic
            wiki_page = ModelWikiPage.parse_obj(data)
            
            return wiki_page
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from LLaMA: {e}")
        except Exception as e:
            raise ValueError(f"Pydantic validation failed: {e}")
    
    def render_mermaid_tree(self, file_tree: List[FileEntry]) -> str:
        """Generate a Mermaid diagram for the file structure."""
        if not file_tree:
            return ""
        
        mermaid = "```mermaid\ngraph TD\n    root[Model Files]\n"
        
        for i, file in enumerate(file_tree, 1):
            # Use formatted size if available, otherwise format the bytes
            if hasattr(file, 'size_formatted'):
                size_text = file.size_formatted
            else:
                size_text = format_size(file.size) if file.size else "unknown"
            
            mermaid += f'    root --> file{i}["{file.name}<br/>{size_text}"]\n'
        
        mermaid += "```"
        return mermaid
    
    def render_markdown(self, wiki_page: ModelWikiPage) -> str:
        """Render the validated data to Markdown using Jinja2."""
        try:
            template = self.jinja_env.get_template('wiki_template.md.j2')
            
            # Convert Pydantic model to dict for Jinja2
            template_data = wiki_page.dict()
            
            # Replace None file sizes with "unknown"
            for file_entry in template_data.get('file_tree', []):
                if file_entry.get('size') is None:
                    file_entry['size'] = None  # Template handles this
            
            rendered = template.render(**template_data)
            return rendered
            
        except Exception as e:
            raise Exception(f"Markdown rendering failed: {e}")
    
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
        
        # 2. Extract PDF content if provided
        pdf_texts = []
        if pdf_files:
            print(f"📄 Extracting text from {len(pdf_files)} PDF(s)...")
            for pdf_file in pdf_files:
                text = self.extract_pdf_text(pdf_file)
                if text:
                    pdf_texts.append(text)
        
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
        
        model_id = wiki_page.model_name.replace("/", "_").replace(" ", "_")
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
    parser.add_argument("--model", default="Llama-4-Scout-17B-16E-Instruct-FP8", help="LLaMA model to use")
    parser.add_argument("--no-sidebar", action="store_true", help="Disable sidebar scraping")
    
    args = parser.parse_args()
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('LLAMA_4_API_KEY')
    
    if not api_key:
        print("❌ Error: LLAMA_4_API_KEY not found in environment variables")
        sys.exit(1)
    
    # Initialize generator
    generator = ModelWikiGenerator(
        api_key=api_key, 
        model_name=args.model,
        enable_sidebar_scraping=not args.no_sidebar
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