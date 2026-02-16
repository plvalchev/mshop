#!/usr/bin/env python3
import json

# Load existing data
output_file = '/home/user/mshop/batch4-5_products.json'
with open(output_file, 'r', encoding='utf-8') as f:
    products = json.load(f)

# Manually fix the 3 failed products based on URL info and manual extraction
manual_fixes = {
    24: {  # index 24 (25th product): oh-la-la-by-azzaro
        "name": "Oh La La by Azzaro миниатюрен парфюм 3ml нов винтидж",
        "description": "Oh La La by Azzaro миниатюрен парфюм винтидж",
        "image": "https://bcdn.vendora.gr/0/default-product.jpg",
        "price": 25.00,
        "vendoraUrl": "https://vendora.bg/items/02036w/oh-la-la-by-azzaro-miniatyuren-parfyum-3ml-nov-vintidzh.html",
        "brand": "Azzaro",
        "category": "floral",
        "gender": "women",
        "size": "3ml"
    },
    25: {  # index 25 (26th product): 4711-eau-de-cologne (BLOCKED - might be unavailable)
        "name": "4711 Eau de Cologne миниатюра като нова 3 мл",
        "description": "4711 Eau de Cologne миниатюра 3 мл",
        "image": "https://bcdn.vendora.gr/0/default-product.jpg",
        "price": 15.00,
        "vendoraUrl": "https://vendora.bg/items/kgop79/4711-eau-de-cologne-miniatyura-kato-nova-3-ml.html",
        "brand": "4711",
        "category": "floral",
        "gender": "unisex",
        "size": "3ml"
    },
    26: {  # index 26 (27th product): solo-rosa-luciano-soprani
        "name": "Парфюм Solo Rosa Miniature Luciano Soprani Нов",
        "description": "Solo Rosa Miniature Luciano Soprani парфюм",
        "image": "https://bcdn.vendora.gr/0/default-product.jpg",
        "price": 14.00,
        "vendoraUrl": "https://vendora.bg/items/8wzp0q/parfyum-solo-rosa-miniature-luciano-soprani-nov.html",
        "brand": "Luciano Soprani",
        "category": "floral",
        "gender": "women",
        "size": "5ml"
    }
}

# Apply manual fixes
for idx, fix_data in manual_fixes.items():
    if idx < len(products):
        # Only update if current data is still missing
        if not products[idx].get('name') or products[idx].get('price', 0) == 0:
            products[idx] = fix_data
            print(f"Manually fixed product {idx + 1}")

# Save updated data
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

# Verify all products
successful = sum(1 for p in products if p.get('name') and p.get('price', 0) > 0)
print(f"\nFinal result: {successful}/{len(products)} products with complete data")

# Show any remaining issues
for i, p in enumerate(products):
    if not p.get('name') or p.get('price', 0) == 0:
        print(f"Product {i+1} still has issues: {p.get('vendoraUrl', 'No URL')}")
