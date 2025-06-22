"""
Pydantic schemas for Hugging Face model wiki pages.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl


class FileMetadata(BaseModel):
    """Metadata for a file in the model repository."""
    name: str
    url: str
    size: Optional[int] = None
    size_human: Optional[str] = None


class PaperInfo(BaseModel):
    """Information about a research paper."""
    title: str
    url: str
    summary: str
    citation: Optional[str] = None


class GitHubStats(BaseModel):
    """GitHub repository statistics."""
    repo_name: str
    url: str
    stars: int
    forks: int
    open_issues: int
    contributors: List[str] = []
    created_at: str
    last_updated: str
    topics: List[str] = []
    description: str


class ModelMindMapNode(BaseModel):
    """A node in the model mind map."""
    id: str
    label: str
    children: List['ModelMindMapNode'] = []


class UsageGuideSection(BaseModel):
    """Represents a structured section within the usage guide."""
    title: str
    description: str
    code_example: Optional[str] = None  # Raw code block string (e.g., Python, Bash)
    # Assuming images directly linked in README/paper can be found and associated by LLM
    image_url: Optional[HttpUrl] = None  # URL to an image relevant to this usage section
    image_caption: Optional[str] = None


class BenchmarkTable(BaseModel):
    """Represents a structured benchmark table with interpretation."""
    title: str  # E.g., "Performance on Benchmark I (In-domain)"
    description: Optional[str] = None  # Interpretive text for this specific table, may include image embeds
    markdown_table: str  # The raw markdown table content (e.g., from PDF table parsing)
    # Assuming LLM can identify and provide image URLs from the input documents that are relevant to this benchmark.
    image_url: Optional[HttpUrl] = None  # URL to an image (e.g., benchmark plot)
    image_caption: Optional[str] = None


class KeyHyperparameter(BaseModel):
    """Represents a single key hyperparameter name and its value."""
    name: str
    value: str  # Can be string for various types (e.g., "0.001", "AdamW", "512")


class ModelWikiPage(BaseModel):
    """Complete schema for a Hugging Face model wiki page."""
    model_id: str
    author: str
    license: str
    last_modified: str
    huggingface_url: HttpUrl
    overview: str
    architecture: str
    tags: List[str] = []
    use_cases: List[str] = []
    files: List[FileMetadata] = []
    papers: List[PaperInfo] = []
    github: Optional[GitHubStats] = None
    # `benchmarks` now uses the new structured type
    benchmarks: List[BenchmarkTable] = []
    variants: Optional[List[dict]] = None
    # `references` might contain URLs (like the old external_links_in_readme) or specific paper titles
    # Assuming references should be a list of objects if they need titles, otherwise just URLs.
    # For simplicity in this prompt, let's assume they are structured like PaperInfo for consistency
    # if LLaMA can provide titles, or just plain strings for URLs if titles are not available.
    # Let's keep it flexible and just rename the `references` field in the prompt.
    external_resources: List[Dict[str, str]] = []  # E.g., [{"title": "Blog Post Title", "url": "https://..."}]

    mindmap: List[ModelMindMapNode] = []

    downloads_last_month: Optional[int] = None
    datasets_used: List[str] = []
    adapter_count: Optional[int] = None
    finetune_count: Optional[int] = None
    quantization_count: Optional[int] = None

    # New fields for detailed sections
    usage_guides: List[UsageGuideSection] = []  # List of structured usage sections
    limitations: Optional[str] = None  # Markdown text summarizing limitations
    ethical_considerations: Optional[str] = None  # Markdown text for ethical aspects
    future_work: Optional[str] = None  # Markdown text for future work/roadmap
    key_hyperparameters: List[KeyHyperparameter] = []  # List of key training/model hyperparameters 