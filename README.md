# Hugging Face Model Wiki

Hugging Face Model Wiki is an LLM-powered project that builds a structured, readable reference for open-source models hosted on the Hugging Face Hub. The goal is to transform raw model documentation into consistent, multi-level summaries and reference pages that are easier to navigate, compare, and explore.

This project is not a scraper frontend. It is a content generation toolchain built around long-context summarization, documentation parsing, and structured metadata analysis.

---

## Project Objectives

- Generate clean, readable summaries of top Hugging Face models
- Build pages that mirror a Wikipedia-style layout: factual, modular, and hierarchical
- Extract and display each model's structure, files, and linked references
- Highlight practical metadata: author, tags, downloads, license, pipeline type
- Include source links (papers, GitHub, demos) directly in the summary
- Provide different summary modes: TLDR, technical overview, plain-English explanations
- Use long-context models to ingest full README files and associated materials

---

## Page Structure

Each model page is generated in Markdown and includes:

- Model name and identifier (e.g. `meta-llama/Llama-2-7b`)
- Overview summary (1-liner, paragraph, full technical description)
- Author, creation date, update history
- Tags and pipeline category (e.g. `text-generation`, `vision`, `audio`)
- Full file list with download links and sizes
- External references:
  - Linked papers (ArXiv, OpenReview)
  - GitHub repositories
  - Chatbots or API demos
- Extracted highlights from the README
- (Optional) Benchmarks and quantitative comparisons
- (Planned) Similar model suggestions and comparisons

---

## Workflow

1. Select trending or representative models via Hugging Face's public API
2. Fetch metadata, file list, and README contents
3. Parse file structure and extract all outbound URLs
4. Pass this information into a long-context language model
5. Generate a clean, structured wiki entry in Markdown
6. (Planned) Render the wiki as static HTML or push to a frontend

---

## Current Focus

The project currently prioritizes breadth over scale: the goal is to cover one strong example from each major model category (text, vision, multimodal, speech, time-series) and validate the pipeline.

Later iterations will focus on automation, comparisons, and frontend UX.

---

## Roadmap

- Define model categories and representative samples
- Expand to cover long-context and agentic model types
- Add support for PDF summarization (technical reports)
- Create table-based comparisons across models
- Explore frontend rendering (Notion, HTML, static site generator)

---

## Notes

- All model data is fetched using the official Hugging Face API
- Long-context summarization is done using models like LLaMA 4 Scout
- This project is research and reference-oriented and does not generate or run models

