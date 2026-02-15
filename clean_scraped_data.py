#!/usr/bin/env python3
"""
Clean and deduplicate scraped products data
"""

import json
import re

# Load scraped data
with open('scraped_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products loaded: {len(products)}")

# Clean and deduplicate
cleaned_products = []
seen_urls = set()

for product in products:
    url = product.get('url', '')

    # Skip invalid entries
    if '/items/create' in url:
        continue

    if not url or url in seen_urls:
        continue

    # Skip if missing essential data
    if not product.get('name_bg'):
        continue

    # Extract just the item ID from URL for consistency
    item_id_match = re.search(r'/items/([^/]+)', url)
    if not item_id_match:
        continue

    item_id = item_id_match.group(1)

    # Skip if we've seen this item ID
    if item_id in seen_urls:
        continue

    # Clean the name (remove price from name if it's there)
    name = product['name_bg']
    name = re.sub(r'€\s*\d+(?:[.,]\d+)?$', '', name).strip()
    product['name_bg'] = name

    # Simplify URL to just the path
    if 'items/' in url:
        product['url'] = '/' + url.split('/items/')[1].split('?')[0]
        if not product['url'].endswith('.html'):
            product['url'] = '/items/' + item_id + '/'

    cleaned_products.append(product)
    seen_urls.add(item_id)

print(f"Cleaned products: {len(cleaned_products)}")
print(f"Removed duplicates/invalid: {len(products) - len(cleaned_products)}")

# Save cleaned data
with open('cleaned_products.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_products, f, indent=2, ensure_ascii=False)

# Save as Python list
with open('cleaned_products.py', 'w', encoding='utf-8') as f:
    f.write("# Cleaned products from Vendora user profile\n")
    f.write(f"# Total unique products: {len(cleaned_products)}\n\n")
    f.write("raw_products = ")
    f.write(json.dumps(cleaned_products, indent=4, ensure_ascii=False))
    f.write("\n")

print("\nSaved to:")
print("  - cleaned_products.json")
print("  - cleaned_products.py")
print("\nSample products:")
for i, p in enumerate(cleaned_products[:5]):
    print(f"{i+1}. {p.get('name_bg', 'N/A')} - €{p.get('price', 0)}")
