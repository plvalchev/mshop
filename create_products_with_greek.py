#!/usr/bin/env python3
"""
Create products.json keeping original Greek product names
This preserves the authentic Vendora product listings
"""

import json
import re

# Load cleaned products
with open('cleaned_products.json', 'r', encoding='utf-8') as f:
    raw_products = json.load(f)

print(f"Processing {len(raw_products)} products...")

products = []
for i, product in enumerate(raw_products, 1):
    # Extract the URL path to create vendoraUrl
    url = product.get('url', '')
    if url.startswith('/'):
        # Convert old format to new share format
        vendora_url = url
        # Extract the short code from URL like /n0m21yp/...
        match = re.search(r'/([a-z0-9]+)/', url)
        if match:
            short_code = match.group(1)
            vendora_url = f"https://vendora.bg/l/{short_code}"
        else:
            vendora_url = f"https://vendora.bg{url}"
    else:
        vendora_url = url

    # Clean the image URL
    image_url = product.get('image', '')
    if image_url and '?class=' in image_url:
        # Keep the full image URL with parameters
        image_url = image_url

    # Clean up name_bg - remove the price suffix if present (like "€ 35")
    name_bg = product.get('name_bg', '').strip()
    name_bg = re.sub(r'€\s*\d+(\.\d+)?$', '', name_bg).strip()

    # Create product entry with Greek name
    product_entry = {
        "id": i,
        "name": name_bg,  # Keep the original Greek name
        "price": product.get('price', 0),
        "image": image_url,
        "vendoraUrl": vendora_url
    }

    products.append(product_entry)

# Save to products.json
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print(f"Created products.json with {len(products)} products")
print("\nSample products:")
for i in range(min(5, len(products))):
    print(f"{i+1}. {products[i]['name']} - €{products[i]['price']}")
