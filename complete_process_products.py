#!/usr/bin/env python3
"""
Complete product processing: Convert raw Bulgarian data to refined English products.json
"""

import json
import re

# Load raw products from process_products.py
exec(open('process_products.py').read())

# Load existing products.json
try:
    with open('products.json', 'r', encoding='utf-8') as f:
        existing_products = json.load(f)
except FileNotFoundError:
    existing_products = []

print(f"Existing products in products.json: {len(existing_products)}")
print(f"Raw products to process: {len(raw_products)}")

# Get existing item IDs to avoid duplicates
existing_item_ids = set()
for p in existing_products:
    if 'vendoraUrl' in p:
        match = re.search(r'/l/([^/?]+)', p['vendoraUrl'])
        if match:
            existing_item_ids.add(match.group(1))

print(f"Existing item IDs: {len(existing_item_ids)}")

def generate_description(name, brand, category, gender):
    """Generate a descriptive text for the perfume"""
    descriptions = {
        "floral": "Elegant floral fragrance",
        "fresh": "Fresh and invigorating scent",
        "woody": "Rich woody fragrance",
        "oriental": "Exotic oriental fragrance",
        "fruity": "Vibrant fruity fragrance",
        "spicy": "Warm spicy fragrance"
    }

    base = descriptions.get(category, "Beautiful fragrance")

    if brand != "Unknown":
        return f"{base} from {brand}. Authentic miniature perfume, perfect for collectors or trying before buying full size."
    else:
        return f"{base}. Authentic miniature perfume, perfect for collectors or trying before buying full size."

# Process each raw product
new_products = []

for raw in raw_products:
    # Extract item ID from URL
    item_id_match = re.search(r'/items/([^/]+)', raw['url'])
    if not item_id_match:
        continue

    item_id = item_id_match.group(1)

    # Skip if already exists
    if item_id in existing_item_ids:
        continue

    name_bg = raw.get('name_bg', '')
    if not name_bg:
        continue

    # Extract English name
    name_en = simplify_name(name_bg)

    # Extract brand
    brand = extract_brand_from_name(name_bg)

    # Categorize
    category, gender = categorize_perfume(name_bg)

    # Extract size
    size = extract_size(name_bg)

    # Generate description (based on brand and type)
    description = generate_description(name_en, brand, category, gender)

    # Create vendora short URL
    vendora_url = f"https://vendora.bg/l/{item_id}"

    # Create product entry
    product = {
        "name": name_en,
        "brand": brand,
        "category": category,
        "gender": gender,
        "price": int(raw.get('price', 0)),
        "size": size,
        "description": description,
        "image": raw.get('image', ''),
        "vendoraUrl": vendora_url
    }

    new_products.append(product)

print(f"New products to add: {len(new_products)}")

# Assign IDs
max_id = max([p.get('id', 0) for p in existing_products] + [0])

for i, product in enumerate(new_products):
    product['id'] = max_id + i + 1

# Combine and save
all_products = existing_products + new_products

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, indent=4, ensure_ascii=False)

print(f"\nTotal products in products.json: {len(all_products)}")
print(f"Added {len(new_products)} new products")

# Show some examples
print("\nSample new products:")
for i, p in enumerate(new_products[:10]):
    print(f"{p['id']}. {p['name']} - {p['brand']} - €{p['price']} - {p['size']}")
