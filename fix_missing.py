#!/usr/bin/env python3

import json
import re
import subprocess
import time
from html import unescape

def extract_product_data(url):
    """Extract product data from a vendora.bg URL"""
    
    # Add delay before fetching
    time.sleep(2)
    
    # Fetch the HTML content
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '30', '-A', 'Mozilla/5.0', url],
            capture_output=True,
            timeout=35
        )
        html = result.stdout.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None

    if not html or len(html) < 100:
        print(f"  WARNING: Empty response")
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
        schema_price_match = re.search(r'"price":"([0-9.]+)"', html)
        if schema_price_match:
            price = float(schema_price_match.group(1))
        else:
            gtm_price_match = re.search(r'"price":(\d+(?:\.\d+)?)', html)
            if gtm_price_match:
                price = float(gtm_price_match.group(1))

    # Unescape HTML entities
    title = unescape(title_match.group(1)) if title_match else ""
    description = unescape(desc_match.group(1)) if desc_match else ""
    image = image_match.group(1) if image_match else ""

    # Clean description
    description = ' '.join(description.split())

    # Extract brand from title
    brand = ""
    brand_patterns = [
        r'^([A-Z][A-Za-z\'\-&]+(?:\s+[A-Z][A-Za-z\'\-&]+){0,2})',
        r'^([A-Za-z]+)',
    ]
    for pattern in brand_patterns:
        brand_match = re.match(pattern, title)
        if brand_match:
            brand = brand_match.group(1)
            break

    # Extract size
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

# Load existing data
with open('/home/user/mshop/batch6-12_products.json', 'r') as f:
    products = json.load(f)

# Find and fix products with missing data
for i, product in enumerate(products):
    if not product.get('name') or not product.get('price'):
        url = product['vendoraUrl']
        print(f"Re-fetching product {i+1}: {url}")
        new_data = extract_product_data(url)
        if new_data:
            products[i] = new_data
            print(f"  ✓ Fixed: {new_data['name'][:50]}")
        else:
            print(f"  ✗ Still failed")

# Save updated data
with open('/home/user/mshop/batch6-12_products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("\nDone!")
