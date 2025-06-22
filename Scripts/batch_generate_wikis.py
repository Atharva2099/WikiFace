#!/usr/bin/env python3
"""
Batch Wiki Generator for Hugging Face Models

This script processes all models in the HF_listings directory structure and generates
enhanced wiki pages in HF_listings_MD using the new structured schema with Gemini integration.
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from dotenv import load_dotenv
from generate_model_wiki import ModelWikiGenerator


def find_model_directories(base_path: Path) -> List[Path]:
    """Find all model directories that contain metadata.json and model_info.md."""
    model_dirs = []
    
    for category_dir in base_path.iterdir():
        if not category_dir.is_dir():
            continue
            
        print(f"🔍 Scanning category: {category_dir.name}")
        
        for model_dir in category_dir.iterdir():
            if not model_dir.is_dir():
                continue
                
            # Check if this is a model directory with required files
            metadata_file = model_dir / "metadata.json"
            model_info_file = model_dir / "model_info.md"
            
            if metadata_file.exists() and model_info_file.exists():
                model_dirs.append(model_dir)
                print(f"  ✅ Found model: {model_dir.name}")
            else:
                print(f"  ⚠️ Skipping {model_dir.name} (missing required files)")
    
    return model_dirs


def find_pdf_files(model_dir: Path) -> List[Path]:
    """Find PDF files in the model directory."""
    pdf_files = []
    for file in model_dir.iterdir():
        if file.is_file() and file.suffix.lower() == '.pdf':
            pdf_files.append(file)
    return pdf_files


def is_already_processed(model_dir: Path, output_base: Path) -> bool:
    """Check if a model has already been processed."""
    category_name = model_dir.parent.name
    model_name = model_dir.name
    output_file = output_base / category_name / f"{model_name}.md"
    return output_file.exists()


def process_single_model(model_dir: Path, output_base: Path, generator: ModelWikiGenerator) -> Dict[str, Any]:
    """Process a single model and generate its wiki page."""
    try:
        print(f"🚀 Processing: {model_dir.name}")
        
        # Check if already processed
        if is_already_processed(model_dir, output_base):
            print(f"  ⏭️ Skipping {model_dir.name} (already processed)")
            return {
                "model": model_dir.name,
                "category": model_dir.parent.name,
                "status": "skipped",
                "output_file": str(output_base / model_dir.parent.name / f"{model_dir.name}.md"),
                "pdfs_processed": 0
            }
        
        # Find PDF files
        pdf_files = find_pdf_files(model_dir)
        if pdf_files:
            print(f"  📄 Found {len(pdf_files)} PDF(s): {[f.name for f in pdf_files]}")
        
        # Create output directory structure
        category_name = model_dir.parent.name
        output_dir = output_base / category_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate wiki
        output_file = generator.generate_wiki(
            model_dir=model_dir,
            pdf_files=pdf_files,
            output_dir=output_dir
        )
        
        return {
            "model": model_dir.name,
            "category": category_name,
            "status": "success",
            "output_file": str(output_file),
            "pdfs_processed": len(pdf_files)
        }
        
    except Exception as e:
        print(f"❌ Error processing {model_dir.name}: {e}")
        return {
            "model": model_dir.name,
            "category": model_dir.parent.name if model_dir.parent else "unknown",
            "status": "error",
            "error": str(e),
            "pdfs_processed": 0
        }


def create_summary_report(results: List[Dict[str, Any]], output_base: Path) -> None:
    """Create a summary report of the batch processing."""
    report_file = output_base / "batch_processing_report.md"
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "error"]
    skipped = [r for r in results if r["status"] == "skipped"]
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Batch Wiki Generation Report\n\n")
        f.write(f"**Generated on:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total models processed:** {len(results)}\n")
        f.write(f"**Successful:** {len(successful)}\n")
        f.write(f"**Failed:** {len(failed)}\n")
        f.write(f"**Skipped (already processed):** {len(skipped)}\n\n")
        
        if successful:
            f.write("## Successfully Processed Models\n\n")
            f.write("| Category | Model | Output File | PDFs Processed |\n")
            f.write("|----------|-------|-------------|----------------|\n")
            for result in successful:
                f.write(f"| {result['category']} | {result['model']} | [{result['model']}.md]({result['output_file']}) | {result['pdfs_processed']} |\n")
            f.write("\n")
        
        if skipped:
            f.write("## Skipped Models (Already Processed)\n\n")
            f.write("| Category | Model | Output File |\n")
            f.write("|----------|-------|-------------|\n")
            for result in skipped:
                f.write(f"| {result['category']} | {result['model']} | [{result['model']}.md]({result['output_file']}) |\n")
            f.write("\n")
        
        if failed:
            f.write("## Failed Models\n\n")
            f.write("| Category | Model | Error |\n")
            f.write("|----------|-------|-------|\n")
            for result in failed:
                f.write(f"| {result['category']} | {result['model']} | {result['error']} |\n")
    
    print(f"📊 Summary report saved to: {report_file}")


def main():
    """Main function to batch process all models."""
    parser = argparse.ArgumentParser(description="Batch generate wiki pages for all Hugging Face models")
    parser.add_argument("--input-dir", type=Path, default="HF_listings", help="Input directory containing model categories")
    parser.add_argument("--output-dir", type=Path, default="HF_listings_MD", help="Output directory for generated wiki pages")
    parser.add_argument("--max-workers", type=int, default=2, help="Maximum number of concurrent workers")
    parser.add_argument("--model", default="anthropic/claude-3.5-sonnet", help="OpenRouter model to use")
    parser.add_argument("--no-sidebar", action="store_true", help="Disable sidebar scraping")
    parser.add_argument("--resume", action="store_true", help="Resume processing, skip already processed models")
    parser.add_argument("--delay", type=int, default=20, help="Delay in seconds between processing each model (to avoid rate limits)")
    
    args = parser.parse_args()
    
    # Load environment
    load_dotenv()
    openrouter_api_key = os.getenv('OPEN_ROUTER_API')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not openrouter_api_key:
        print("❌ Error: OPEN_ROUTER_API not found in environment variables")
        sys.exit(1)
    
    if not gemini_api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        sys.exit(1)
    
    # Check input directory
    if not args.input_dir.exists():
        print(f"❌ Error: Input directory {args.input_dir} does not exist")
        sys.exit(1)
    
    # Create output directory
    args.output_dir.mkdir(exist_ok=True)
    
    # Initialize generator with OpenRouter and Gemini
    generator = ModelWikiGenerator(
        api_key=openrouter_api_key,  # Use OpenRouter API key
        model_name=args.model,
        enable_sidebar_scraping=not args.no_sidebar,
        gemini_api_key=gemini_api_key
    )
    
    # Find all model directories
    print(f"🔍 Scanning for models in: {args.input_dir}")
    model_dirs = find_model_directories(args.input_dir)
    
    if not model_dirs:
        print("❌ No model directories found")
        sys.exit(1)
    
    print(f"\n📋 Found {len(model_dirs)} models to process")
    
    # Filter out already processed models if resuming
    if args.resume:
        original_count = len(model_dirs)
        model_dirs = [md for md in model_dirs if not is_already_processed(md, args.output_dir)]
        skipped_count = original_count - len(model_dirs)
        print(f"⏭️ Skipping {skipped_count} already processed models")
        print(f"📋 Remaining models to process: {len(model_dirs)}")
    
    if not model_dirs:
        print("✅ All models already processed!")
        return
    
    # Process models with threading
    results = []
    
    for model_dir in model_dirs:
        result = process_single_model(model_dir, args.output_dir, generator)
        results.append(result)
        if result["status"] == "success":
            print(f"✅ Completed: {result['model']} -> {result['output_file']}")
        elif result["status"] == "skipped":
            print(f"⏭️ Skipped: {result['model']} (already processed)")
        else:
            print(f"❌ Failed: {result['model']} - {result['error']}")
        print(f"⏳ Waiting {args.delay} seconds before next model...")
        time.sleep(args.delay)
    
    # Create summary report
    successful = len([r for r in results if r["status"] == "success"])
    failed = len([r for r in results if r["status"] == "error"])
    skipped = len([r for r in results if r["status"] == "skipped"])
    
    print(f"\n📊 Processing complete! {successful} successful, {failed} failed, {skipped} skipped")
    create_summary_report(results, args.output_dir)
    
    # Save detailed results as JSON
    results_file = args.output_dir / "processing_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Detailed results saved to: {results_file}")


if __name__ == "__main__":
    main() 