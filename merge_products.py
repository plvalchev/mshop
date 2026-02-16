#!/usr/bin/env python3
"""
Merge new products into products.json
Handles deduplication by vendoraUrl item ID
"""
import json
import sys

def extract_item_id(url):
    """Extract item ID from Vendora URL"""
    if '/l/' in url:
        return url.split('/l/')[-1]
    elif '/items/' in url:
        return url.split('/items/')[-1].split('/')[0]
    return None

def merge_products(existing_file, new_products_data):
    """Merge new products into existing products.json"""

    # Load existing products
    try:
        with open(existing_file, 'r') as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = []

    # Get existing item IDs
    existing_ids = set()
    for product in existing:
        if 'vendoraUrl' in product:
            item_id = extract_item_id(product['vendoraUrl'])
            if item_id:
                existing_ids.add(item_id)

    # Get max ID for new products
    max_id = max([p.get('id', 0) for p in existing] + [0])

    # Add new products
    added = 0
    for product in new_products_data:
        if 'vendoraUrl' in product:
            item_id = extract_item_id(product['vendoraUrl'])
            if item_id and item_id not in existing_ids:
                max_id += 1
                product['id'] = max_id
                existing.append(product)
                existing_ids.add(item_id)
                added += 1
                print(f"  Added: {product.get('name', 'Unknown')} (ID: {max_id})")

    # Save merged products
    with open(existing_file, 'w') as f:
        json.dump(existing, f, indent=4)

    print(f"\n✅ Added {added} new products")
    print(f"📊 Total products: {len(existing)}")

    return existing

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python merge_products.py <new_products.json>")
        sys.exit(1)

    new_file = sys.argv[1]

    try:
        with open(new_file, 'r') as f:
            new_products = json.load(f)
    except FileNotFoundError:
        print(f"Error: {new_file} not found")
        sys.exit(1)

    merge_products('products.json', new_products)
