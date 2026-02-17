#!/usr/bin/env python3
"""
Enhance product names and descriptions to match the quality of the first 70 products
"""
import json
import re

def clean_product_name(name, brand):
    """Extract clean English product name from Bulgarian text"""

    # Remove Bulgarian text patterns
    patterns_to_remove = [
        r'[а-яА-Я]+',  # Remove all Cyrillic characters
        r'мини(?:атюр(?:ен|на))?\s+парфюм(?:и)?',
        r'тоалетна вода',
        r'eau de (?:toilette|parfum)',
        r'\d+(?:[.,]\d+)?\s*(?:ml|мл)',
        r'нов(?:и|а)?',
        r'винтидж',
        r'като нов(?:и|а)?',
        r'пълен',
        r'автентичн(?:и|а)',
        r'колекционерск(?:и|а)',
        r'рядък',
        r'екземпляр',
        r'за (?:жени|мъже)',
        r'употребяван(?:а)?',
        r'pour femme',
        r'pour homme',
        r'mini(?:\s+perfume)?',
        r'miniature',
        r'new',
        r'authentic',
        r'vintage',
        r'collector\'?s?',
        r'rare',
        r'full',
        r'set',
    ]

    clean = name
    for pattern in patterns_to_remove:
        clean = re.sub(pattern, '', clean, flags=re.I)

    # Clean up whitespace and punctuation
    clean = re.sub(r'\s+', ' ', clean).strip()
    clean = re.sub(r'^[,\s-]+|[,\s-]+$', '', clean)
    clean = re.sub(r'\s*,\s*', ', ', clean)

    # If name is mostly cleaned out, use brand as base
    if len(clean) < 3:
        clean = brand

    # Capitalize properly
    clean = clean.title()

    return clean

def generate_description(name, brand, category, gender, size):
    """Generate elegant product description"""

    # Fragrance family descriptions
    category_descriptions = {
        'floral': 'Elegant floral fragrance',
        'fresh': 'Fresh and invigorating scent',
        'oriental': 'Warm oriental fragrance',
        'woody': 'Sophisticated woody scent',
        'fruity': 'Vibrant fruity fragrance',
        'spicy': 'Bold spicy fragrance'
    }

    # Gender-specific adjectives
    gender_adj = {
        'women': 'Feminine and elegant',
        'men': 'Masculine and sophisticated',
        'unisex': 'Versatile and timeless'
    }

    # Build description
    parts = []

    # Add category description
    if category in category_descriptions:
        parts.append(category_descriptions[category])

    # Add brand context
    parts.append(f'from {brand}')

    # Add size note for miniatures
    if size and ('ml' in size.lower() or 'mini' in size.lower()):
        parts.append(f'Collector\'s miniature perfume')

    # Add gender context
    if gender in gender_adj:
        parts.append(gender_adj[gender] + ' scent')

    # Combine into flowing description
    if len(parts) >= 3:
        description = f"{parts[0]} {parts[1]}. {parts[2]}."
    else:
        description = '. '.join(parts) + '.'

    return description

def enhance_products(products):
    """Enhance products 71-176 to match the quality of products 1-70"""

    enhanced_count = 0

    for product in products:
        # Only enhance products with IDs 71-176 (the new ones)
        if product.get('id', 0) < 71:
            continue

        original_name = product.get('name', '')
        brand = product.get('brand', '')
        category = product.get('category', 'floral')
        gender = product.get('gender', 'women')
        size = product.get('size', '')

        # Clean the name
        clean_name = clean_product_name(original_name, brand)

        # Generate elegant description
        new_description = generate_description(clean_name, brand, category, gender, size)

        # Update product
        if clean_name != original_name:
            product['name'] = clean_name
            enhanced_count += 1

        # Update description if it's basic/literal translation
        if len(product.get('description', '')) < 50 or 'mini perfume' in product.get('description', '').lower():
            product['description'] = new_description

        print(f"  Enhanced #{product['id']}: {clean_name}")

    return enhanced_count

def main():
    # Load products
    with open('products.json', 'r') as f:
        products = json.load(f)

    print(f"Total products: {len(products)}")
    print(f"Enhancing products 71-{len(products)}...\n")

    # Enhance products
    count = enhance_products(products)

    # Save enhanced products
    with open('products.json', 'w') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Enhanced {count} products!")
    print(f"📊 Total products: {len(products)}")

if __name__ == '__main__':
    main()
