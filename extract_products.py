#!/usr/bin/env python3

import json
import re
import subprocess
import time
from html import unescape

def extract_product_data(url):
    """Extract product data from a vendora.bg URL"""

    # Fetch the HTML content
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '30', url],
            capture_output=True,
            timeout=35
        )
        html = result.stdout.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None

    if not html or len(html) < 100:
        print(f"  WARNING: Empty or invalid response for {url}")
        return None

    # Extract metadata
    title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    price_match = re.search(r'<meta property="product:price:amount" content="([^"]+)"', html)

    # Extract price - try multiple sources
    price = 0.0
    if price_match:
        price = float(price_match.group(1))
    else:
        # Try to find price in JSON-LD schema
        schema_price_match = re.search(r'"price":"([0-9.]+)"', html)
        if schema_price_match:
            price = float(schema_price_match.group(1))
        else:
            # Try to find price in GTM events
            gtm_price_match = re.search(r'"price":(\d+(?:\.\d+)?)', html)
            if gtm_price_match:
                price = float(gtm_price_match.group(1))

    # Unescape HTML entities
    title = unescape(title_match.group(1)) if title_match else ""
    description = unescape(desc_match.group(1)) if desc_match else ""
    image = image_match.group(1) if image_match else ""

    # Debug: Print if title is empty
    if not title:
        print(f"  WARNING: No title found for {url}")

    # Clean description (remove newlines and extra spaces)
    description = ' '.join(description.split())

    # Extract brand from title
    # Try to extract brand as first 1-3 words before common keywords
    brand = ""
    brand_patterns = [
        r'^([A-Z][A-Za-z\'\-&]+(?:\s+[A-Z][A-Za-z\'\-&]+){0,2})',  # Brand names
        r'^([A-Za-z]+)',  # Fallback: first word
    ]
    for pattern in brand_patterns:
        brand_match = re.match(pattern, title)
        if brand_match:
            brand = brand_match.group(1)
            break

    # Extract size from title or description
    size_match = re.search(r'(\d+[.,]?\d*)\s*(ml|мл)', title + " " + description, re.IGNORECASE)
    if size_match:
        size_num = size_match.group(1).replace(',', '.')
        size = f"{size_num}ml"
    else:
        size = ""

    # Determine gender
    gender = "women"
    text_lower = (title + " " + description).lower()
    if any(term in text_lower for term in ['pour homme', 'for men', 'мъже', 'za mzhe']):
        gender = "men"
    elif 'unisex' in text_lower:
        gender = "unisex"

    return {
        "name": title,
        "description": description,
        "image": image,
        "price": price,
        "vendoraUrl": url,
        "brand": brand,
        "category": "floral",
        "gender": gender,
        "size": size
    }

def main():
    urls_file = "/home/user/mshop/batch6-12_urls.txt"
    output_file = "/home/user/mshop/batch6-12_products.json"

    products = []

    with open(urls_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    for i, url in enumerate(urls, 1):
        print(f"Processing {i}/{len(urls)}: {url}", flush=True)
        product = extract_product_data(url)
        if product:
            products.append(product)
        # Add small delay to avoid rate limiting
        time.sleep(0.5)

    # Write JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Extracted {len(products)} products to {output_file}")

if __name__ == "__main__":
    main()
