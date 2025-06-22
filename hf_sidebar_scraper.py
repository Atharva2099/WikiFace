#!/usr/bin/env python3
"""
HuggingFace Sidebar Scraper

This module uses Playwright to scrape additional metadata from HuggingFace model pages
that is not available via the API, such as spaces count, datasets used, and adapter counts.
"""

import re
import time
from typing import Dict, List, Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


def scrape_hf_model_sidebar(
    model_id: str, 
    debug: bool = False, 
    headless: bool = True,
    timeout: int = 10000
) -> Dict:
    """
    Scrape additional metadata from a HuggingFace model page sidebar.
    
    Args:
        model_id: The HuggingFace model ID (e.g., "google-bert/bert-base-uncased")
        debug: If True, saves screenshots and shows browser
        headless: If True, runs browser in headless mode
        timeout: Timeout in milliseconds for page operations
        
    Returns:
        Dictionary containing scraped metadata:
        {
            "spaces_count": int,
            "datasets_used": List[str],
            "adapter_count": int,
            "finetune_count": int,
            "quantization_count": int
        }
    """
    
    url = f"https://huggingface.co/{model_id}"
    result = {
        "downloads_last_month": 0,
        "datasets_used": [],
        "adapter_count": 0,
        "finetune_count": 0,
        "quantization_count": 0
    }
    
    with sync_playwright() as p:
        # Launch browser
        browser: Browser = p.chromium.launch(headless=headless)
        context: BrowserContext = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page: Page = context.new_page()
        
        try:
            if debug:
                print(f"🌐 Navigating to: {url}")
            
            # Navigate to the model page
            page.goto(url, timeout=timeout)
            
            # Wait for the page to load - look for the main content
            page.wait_for_selector("main", timeout=timeout)
            
            if debug:
                page.screenshot(path=f"debug_{model_id.replace('/', '_')}.png")
                print(f"📸 Screenshot saved as debug_{model_id.replace('/', '_')}.png")
            
            # Scrape downloads count
            result["downloads_last_month"] = _scrape_spaces_count(page, debug)
            
            # Scrape datasets used
            result["datasets_used"] = _scrape_datasets_used(page, debug)
            
            # Scrape tab counts (adapters, finetunes, quantizations)
            tab_counts = _scrape_tab_counts(page, debug)
            result.update(tab_counts)
            
            if debug:
                print(f"✅ Scraped data: {result}")
                
        except Exception as e:
            if debug:
                print(f"❌ Error scraping {model_id}: {e}")
                page.screenshot(path=f"error_{model_id.replace('/', '_')}.png")
            # Return empty result on error
            pass
            
        finally:
            browser.close()
    
    return result


def _scrape_spaces_count(page: Page, debug: bool = False) -> int:
    """Scrape the number of spaces using this model."""
    try:
        # Look for downloads last month in the new HF layout
        download_selectors = [
            'dl:has-text("Downloads last month") dd',
            'dt:has-text("Downloads last month") + dd',
            '.text-gray-500:has-text("Downloads") + .font-semibold',
            'dl dt:has-text("Downloads") ~ dd'
        ]
        
        for selector in download_selectors:
            try:
                element = page.wait_for_selector(selector, timeout=2000)
                if element:
                    text = element.inner_text().strip()
                    # Remove commas and extract number
                    clean_text = text.replace(',', '').replace(' ', '')
                    numbers = re.findall(r'\d+', clean_text)
                    if numbers:
                        count = int(numbers[0])
                        if debug:
                            print(f"📥 Found downloads last month: {count:,}")
                        return count
            except:
                continue
        
        # Also try to find spaces specifically
        spaces_selectors = [
            'a[href*="/spaces"]:has-text("Spaces")',
            'div:has-text("Spaces") a',
            '.font-semibold:has-text("Spaces")'
        ]
        
        for selector in spaces_selectors:
            try:
                element = page.wait_for_selector(selector, timeout=1000)
                if element:
                    text = element.inner_text()
                    numbers = re.findall(r'\d+', text)
                    if numbers:
                        count = int(numbers[0])
                        if debug:
                            print(f"🚀 Found spaces count: {count}")
                        return count
            except:
                continue
                
    except Exception as e:
        if debug:
            print(f"⚠️ Could not scrape download/spaces count: {e}")
    
    return 0


def _scrape_datasets_used(page: Page, debug: bool = False) -> List[str]:
    """Scrape the list of datasets used to train this model."""
    datasets = []
    
    try:
        # Look for datasets section in various locations
        dataset_selectors = [
            '.dataset-tag',
            'a[href*="/datasets/"]',
            '[data-testid="dataset-link"]',
            '.tag:has-text("dataset")',
            'section:has-text("Dataset") a[href*="/datasets/"]'
        ]
        
        for selector in dataset_selectors:
            try:
                elements = page.query_selector_all(selector)
                for element in elements:
                    href = element.get_attribute("href")
                    if href and "/datasets/" in href:
                        # Extract dataset name from URL
                        dataset_name = href.split("/datasets/")[-1].split("?")[0]
                        if dataset_name and dataset_name not in datasets:
                            datasets.append(dataset_name)
                            
                if datasets:
                    break
                    
            except:
                continue
        
        # Also look for dataset mentions in text content
        if not datasets:
            try:
                # Look for common dataset patterns in page text
                page_text = page.inner_text("main")
                dataset_patterns = [
                    r'trained on ([^,\.\n]+(?:dataset|corpus))',
                    r'using the ([^,\.\n]+) dataset',
                    r'fine-tuned on ([^,\.\n]+)'
                ]
                
                for pattern in dataset_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    for match in matches:
                        clean_match = match.strip()
                        if len(clean_match) < 50 and clean_match not in datasets:
                            datasets.append(clean_match)
                            
            except:
                pass
        
        if debug and datasets:
            print(f"📚 Found datasets: {datasets}")
            
    except Exception as e:
        if debug:
            print(f"⚠️ Could not scrape datasets: {e}")
    
    return datasets[:5]  # Limit to first 5 datasets


def _scrape_tab_counts(page: Page, debug: bool = False) -> Dict[str, int]:
    """Scrape counts from model tree and derivative sections."""
    counts = {
        "adapter_count": 0,
        "finetune_count": 0,
        "quantization_count": 0
    }
    
    try:
        # Look for the new model tree structure with finetunes/adapters
        model_tree_selectors = [
            '.font-semibold:has-text("Finetunes") ~ a',
            'div:has-text("Finetunes") a',
            '.font-semibold:has-text("Adapters") ~ a',
            'div:has-text("Adapters") a',
            '.font-semibold:has-text("Quantizations") ~ a',
            'div:has-text("Quantizations") a'
        ]
        
        for selector in model_tree_selectors:
            try:
                elements = page.query_selector_all(selector)
                for element in elements:
                    text = element.inner_text().lower()
                    href = element.get_attribute("href") or ""
                    
                    # Extract numbers from text like "1 model" or "5 models"
                    numbers = re.findall(r'(\d+)\s*models?', text)
                    if not numbers:
                        numbers = re.findall(r'\d+', text)
                    
                    if numbers:
                        count = int(numbers[0])
                        
                        # Determine type based on the preceding text or href
                        parent_text = ""
                        try:
                            parent = element.locator("..")
                            if parent:
                                parent_text = parent.inner_text().lower()
                        except:
                            pass
                        
                        if any(word in parent_text for word in ['finetune', 'fine-tune']) or 'finetune' in href:
                            counts["finetune_count"] = max(counts["finetune_count"], count)
                            if debug:
                                print(f"🔧 Found finetunes: {count}")
                        elif any(word in parent_text for word in ['adapter', 'lora', 'peft']) or 'adapter' in href:
                            counts["adapter_count"] = max(counts["adapter_count"], count)
                            if debug:
                                print(f"🔌 Found adapters: {count}")
                        elif any(word in parent_text for word in ['quantiz', 'quant', 'gguf', 'gptq']) or 'quant' in href:
                            counts["quantization_count"] = max(counts["quantization_count"], count)
                            if debug:
                                print(f"⚖️ Found quantizations: {count}")
                        
            except Exception as e:
                if debug:
                    print(f"⚠️ Error with selector {selector}: {e}")
                continue
        
        # Also try to find sections by looking for specific headings
        try:
            heading_selectors = [
                '.font-semibold:has-text("Finetunes")',
                '.font-semibold:has-text("Adapters")', 
                '.font-semibold:has-text("Quantizations")'
            ]
            
            for selector in heading_selectors:
                elements = page.query_selector_all(selector)
                for element in elements:
                    heading_text = element.inner_text().lower()
                    
                    # Look for the link in the same container
                    try:
                        container = element.locator("..")
                        link = container.locator("a").first
                        if link:
                            link_text = link.inner_text()
                            numbers = re.findall(r'(\d+)', link_text)
                            if numbers:
                                count = int(numbers[0])
                                
                                if 'finetune' in heading_text:
                                    counts["finetune_count"] = max(counts["finetune_count"], count)
                                elif 'adapter' in heading_text:
                                    counts["adapter_count"] = max(counts["adapter_count"], count)
                                elif 'quantiz' in heading_text:
                                    counts["quantization_count"] = max(counts["quantization_count"], count)
                    except:
                        pass
                        
        except Exception as e:
            if debug:
                print(f"⚠️ Error with heading selectors: {e}")
        
        if debug and any(counts.values()):
            print(f"🏷️ Found derivative counts: {counts}")
            
    except Exception as e:
        if debug:
            print(f"⚠️ Could not scrape derivative counts: {e}")
    
    return counts


def scrape_multiple_models(
    model_ids: List[str], 
    debug: bool = False,
    delay_between_requests: float = 1.0
) -> Dict[str, Dict]:
    """
    Scrape multiple models with optional delay between requests.
    
    Args:
        model_ids: List of model IDs to scrape
        debug: Enable debug mode
        delay_between_requests: Seconds to wait between requests
        
    Returns:
        Dictionary mapping model_id to scraped data
    """
    results = {}
    
    for i, model_id in enumerate(model_ids):
        if debug:
            print(f"\n🔄 Scraping {i+1}/{len(model_ids)}: {model_id}")
            
        try:
            results[model_id] = scrape_hf_model_sidebar(model_id, debug=debug)
            
            # Add delay between requests to be respectful
            if i < len(model_ids) - 1 and delay_between_requests > 0:
                time.sleep(delay_between_requests)
                
        except Exception as e:
            if debug:
                print(f"❌ Failed to scrape {model_id}: {e}")
            results[model_id] = {
                "downloads_last_month": 0,
                "datasets_used": [],
                "adapter_count": 0,
                "finetune_count": 0,
                "quantization_count": 0
            }
    
    return results


if __name__ == "__main__":
    # Test the scraper
    import sys
    
    if len(sys.argv) > 1:
        model_id = sys.argv[1]
        debug_mode = "--debug" in sys.argv
        
        print(f"🧪 Testing scraper on: {model_id}")
        result = scrape_hf_model_sidebar(model_id, debug=debug_mode)
        
        print("\n📊 Results:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        # Default test models
        test_models = [
            "google-bert/bert-base-uncased",
            "amazon/chronos-t5-small"
        ]
        
        print("🧪 Testing scraper with default models...")
        for model_id in test_models:
            print(f"\n--- Testing {model_id} ---")
            result = scrape_hf_model_sidebar(model_id, debug=True)
            print(f"Result: {result}") 