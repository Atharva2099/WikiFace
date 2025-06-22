import re
import requests
from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def fetch_api_stats(model_id: str) -> Dict[str, any]:
    """Fetch downloads + safetensors info from HF JSON API."""
    url = f"https://huggingface.co/api/models/{model_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    downloads = data.get("downloads")
    safetensors = data.get("safetensors", {})
    bf16 = safetensors.get("parameters", {}).get("BF16")
    total = safetensors.get("total")
    tensor_types = list(safetensors.get("parameters", {}).keys())

    return {
        "downloads_last_month": downloads,
        "bf16_params": bf16,
        "total_params": total,
        "model_size_b": (total / 1e9) if total else None,
        "tensor_types": tensor_types,
    }

def parse_model_tree(html: str) -> Dict[str, str]:
    """Given rendered HTML, extract the Model-tree rows."""
    soup = BeautifulSoup(html, "html.parser")
    # find the container with both text-smd and flex-col classes
    container = soup.find(
        "div",
        class_=lambda c: c and "text-smd" in c.split() and "flex-col" in c.split()
    )
    if not container:
        return {}
    # each row has a class like h-[28px]
    rows = container.find_all(
        "div",
        class_=lambda c: c and any(cls.startswith("h-[28px]") for cls in c.split())
    )
    tree = {}
    for row in rows:
        label_div = row.find("div", class_="font-semibold")
        link      = row.find("a")
        if label_div and link:
            tree[label_div.get_text(strip=True)] = link.get_text(strip=True)
    return tree

def fetch_model_tree(model_url: str, headless: bool = True) -> Dict[str, str]:
    """Render the model page and return its Model-tree."""
    opts = Options()
    if headless:
        opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(model_url)
        # wait for the container to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.text-smd.flex.flex-col")
            )
        )
        html = driver.page_source
    finally:
        driver.quit()
    return parse_model_tree(html)

def extract_model_id(url: str) -> str:
    """Turn https://huggingface.co/author/model-name → author/model-name."""
    m = re.match(r"https?://huggingface\.co/([^/]+/[^/]+)", url)
    if not m:
        raise ValueError(f"Invalid HF model URL: {url}")
    return m.group(1)

if __name__ == "__main__":

    urls = [
        "https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
        "https://huggingface.co/google/gemma-3n-E4B-it-litert-preview",
    ]
    for url in urls:
        print(f"\n=== {url} ===")
        model_id = extract_model_id(url)

        # 1) API stats
        stats = fetch_api_stats(model_id)
        print(f"Downloads last month: {stats['downloads_last_month']}")
        print(f"Safetensors BF16 params: {stats['bf16_params']}")
        print(f"Total params: {stats['total_params']}")
        if stats["model_size_b"] is not None:
            print(f"Model size: {stats['model_size_b']:.2f}B params")
        print(f"Tensor types: {stats['tensor_types']}")

        # 2) Model tree
        tree = fetch_model_tree(url)
        print("\nModel tree:")
        for label, count in tree.items():
            print(f"  {label}: {count}")
