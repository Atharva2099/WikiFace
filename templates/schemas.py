"""
Pydantic schemas for Hugging Face model wiki pages.
"""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class FileEntry(BaseModel):
    """Represents a file in the model repository."""
    name: str
    size: Optional[int] = None
    size_formatted: Optional[str] = None
    url: Optional[HttpUrl] = None


class PaperEntry(BaseModel):
    """Represents a research paper related to the model."""
    title: str
    url: HttpUrl
    summary: str
    citation: Optional[str] = None


class ModelWikiPage(BaseModel):
    """Complete schema for a Hugging Face model wiki page."""
    model_name: str
    huggingface_url: HttpUrl
    author: str
    last_updated: str
    license: Optional[str] = None
    tags: List[str] = []
    overview: str
    architecture: str
    use_cases: List[str] = []
    file_tree: List[FileEntry] = []
    papers: List[PaperEntry] = []
    evaluation_summary: Optional[str] = None
    references: List[str] = []
    
    # Additional scraped metadata from sidebar
    spaces_count: Optional[int] = None
    datasets_used: List[str] = []
    adapter_count: Optional[int] = None
    finetune_count: Optional[int] = None
    quantization_count: Optional[int] = None 