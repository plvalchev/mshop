#!/usr/bin/env python3
"""
Add new products from pages 2-6 to process_products.py
"""

import re

# Read the current process_products.py
with open('process_products.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the new products to add
with open('bg_cleaned.py', 'r', encoding='utf-8') as f:
    new_products_lines = f.readlines()

# Extract just the product lines (skip comments/headers)
products_to_add = []
for line in new_products_lines:
    if line.strip().startswith('{"name_bg":'):
        products_to_add.append(line)

print(f"Found {len(products_to_add)} new products to add")

# Find the closing bracket of raw_products list
# It should be after the last Page 1 product and before the "# Brand extraction" comment
pattern = r'(\{"name_bg": "Vent Vent Pierre Balmain мини парфюм нов, колекционерска опаковка".*?\},)\n(\])'

# Add the new products before the closing bracket
new_products_text = ''.join(products_to_add)

replacement = r'\1\n' + new_products_text + r'\2'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if new_content == content:
    print("ERROR: Could not find insertion point!")
else:
    # Write the updated file
    with open('process_products.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully added {len(products_to_add)} new products to process_products.py")

# Verify the count
count = new_content.count('"name_bg":')
print(f"Total products in process_products.py: {count}")
