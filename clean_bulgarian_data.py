#!/usr/bin/env python3
"""
Clean Bulgarian scraped data and format to match process_products.py structure
"""

import json
import re

# Load scraped data
with open('bg_scraped.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products loaded: {len(products)}")

# Clean and deduplicate
cleaned_products = []
seen_urls = set()
existing_page1_urls = set()

# URLs from page 1 that already exist in process_products.py (to skip)
page1_items = [
    "n0m21yp", "jpqwgok", "qqy53w1", "2oqkw09", "114ezg8", "n0m5znp",
    "114keyz", "dyoe5mj", "7y56p2j", "kyz3wm0", "dyoj690", "qqy5qwz",
    "xqgp3m8", "dyoex0p", "ojy5gqw", "mmp7y68", "4ep832m", "114ez28",
    "zjqmw11", "9xze501"
]
existing_page1_urls = set(page1_items)

for product in products:
    url = product.get('url', '')

    # Skip invalid entries
    if '/items/create' in url or not url:
        continue

    # Extract item ID from URL
    item_id_match = re.search(r'/items/([^/]+)', url)
    if not item_id_match:
        continue

    item_id = item_id_match.group(1)

    # Skip if already in page 1 (already in process_products.py)
    if item_id in existing_page1_urls:
        continue

    # Skip duplicates
    if item_id in seen_urls:
        continue

    # Skip if missing essential data
    if not product.get('name_bg'):
        continue

    # Format the data to match original structure
    cleaned_product = {}

    # Clean the name (remove price from end)
    name = product['name_bg']
    name = re.sub(r'€\s*\d+(?:[.,]\d+)?$', '', name).strip()
    cleaned_product['name_bg'] = name

    # Add price
    if 'price' in product:
        cleaned_product['price'] = product['price']

    # Format URL as "/items/xxxxx/"
    cleaned_product['url'] = f"/items/{item_id}/"

    # Add image URL
    if 'image' in product:
        # Keep the full image URL
        cleaned_product['image'] = product['image']

    cleaned_products.append(cleaned_product)
    seen_urls.add(item_id)

print(f"Cleaned products (excluding page 1): {len(cleaned_products)}")
print(f"Removed duplicates/existing: {len(products) - len(cleaned_products)}")

# Save cleaned data
with open('bg_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_products, f, indent=4, ensure_ascii=False)

# Save as Python list for easy insertion into process_products.py
with open('bg_cleaned.py', 'w', encoding='utf-8') as f:
    f.write("# Products from pages 2-6 (Page 1 already exists in process_products.py)\n")
    f.write(f"# Total new products: {len(cleaned_products)}\n\n")
    f.write("# Add these after the existing Page 1 products in process_products.py:\n")
    for i, p in enumerate(cleaned_products):
        if i == 0:
            f.write("    # Page 2-6\n")
        f.write("    " + json.dumps(p, ensure_ascii=False) + ",\n")

print("\nSaved to:")
print("  - bg_cleaned.json")
print("  - bg_cleaned.py")
print("\nSample new products:")
for i, p in enumerate(cleaned_products[:10]):
    print(f"{i+1}. {p.get('name_bg', 'N/A')} - {p.get('price', 0)} лв - {p.get('url', 'N/A')}")
