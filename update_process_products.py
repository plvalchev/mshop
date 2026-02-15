#!/usr/bin/env python3
"""
Update process_products.py with new scraped data
"""

import json

# Read the cleaned products
with open('cleaned_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Loaded {len(products)} products")

# Create the new process_products.py content
new_content = '''#!/usr/bin/env python3
"""
Process all scraped Vendora products and create a comprehensive products.json
This script organizes and categorizes all products from the scraping results.
"""

import json
import re

# All scraped products data (combined from all 6 pages)
# Total unique products: ''' + str(len(products)) + '''
raw_products = '''

# Add the products data
new_content += json.dumps(products, indent=4, ensure_ascii=False)

# Add the rest of the file
new_content += '''

# Brand extraction and categorization
perfume_database = {
    # Versace products
    "Red Jeans": {"brand": "Versace", "category": "fruity", "gender": "women"},
    "Blue Jeans": {"brand": "Versace", "category": "fresh", "gender": "women"},
    "Green Jeans": {"brand": "Versace", "category": "fresh", "gender": "women"},
    "Yellow Diamond": {"brand": "Versace", "category": "floral", "gender": "women"},
    "Vanitas": {"brand": "Versace", "category": "floral", "gender": "women"},
    "Versense": {"brand": "Versace", "category": "fresh", "gender": "women"},
    "Dylan Blue": {"brand": "Versace", "category": "fresh", "gender": "men"},
    "Eros": {"brand": "Versace", "category": "fresh", "gender": "men"},

    # Designer brands
    "Sun Moon Stars": {"brand": "Karl Lagerfeld", "category": "floral", "gender": "women"},
    "Chloe": {"brand": "Karl Lagerfeld", "category": "floral", "gender": "women"},
    "Magie Noir": {"brand": "Lancôme", "category": "oriental", "gender": "women"},
    "Trésor": {"brand": "Lancôme", "category": "floral", "gender": "women"},
    "Miracle": {"brand": "Lancôme", "category": "floral", "gender": "women"},
    "Invictus": {"brand": "Paco Rabanne", "category": "fresh", "gender": "men"},
    "Silver Rain": {"brand": "La Prairie", "category": "fresh", "gender": "unisex"},
    "Nocturnes": {"brand": "Caron", "category": "oriental", "gender": "women"},
    "Michelle": {"brand": "Balenciaga", "category": "floral", "gender": "women"},
    "Knowing": {"brand": "Estée Lauder", "category": "floral", "gender": "women"},
    "Beautiful": {"brand": "Estée Lauder", "category": "floral", "gender": "women"},
    "Drakkar Noir": {"brand": "Guy Laroche", "category": "fresh", "gender": "men"},
    "Vent Vert": {"brand": "Pierre Balmain", "category": "fresh", "gender": "women"},
    "Romeo": {"brand": "Romeo Gigli", "category": "oriental", "gender": "women"},
    "Cabochard": {"brand": "Grès", "category": "woody", "gender": "women"},
    "Shafali": {"brand": "Yves Rocher", "category": "floral", "gender": "women"},
    "Ispahan": {"brand": "Yves Rocher", "category": "floral", "gender": "women"},
    "Neblina": {"brand": "Yves Rocher", "category": "fresh", "gender": "women"},
    "Créature": {"brand": "Gilles Cantuel", "category": "oriental", "gender": "women"},
}

def extract_brand_from_name(name):
    """Extract brand from product name"""
    brands = [
        "Versace", "Lancôme", "Karl Lagerfeld", "Paco Rabanne", "La Prairie",
        "Caron", "Balenciaga", "Estée Lauder", "Guy Laroche", "Pierre Balmain",
        "Romeo Gigli", "Grès", "Yves Rocher", "Gilles Cantuel", "Givenchy",
        "DKNY", "Salvatore Ferragamo", "Burberry", "Prada", "Dior", "Chanel",
        "Calvin Klein", "Moschino", "Dolce & Gabbana", "Nina Ricci",
        "Marc Jacobs", "Ralph Lauren", "Jean Paul Gaultier", "Hermès",
        "Salvador Dali", "Chopard", "Rochas", "Fendi", "Lalique",
        "Oscar de la Renta", "Trussardi", "Boucheron", "Laura Biagiotti",
        "Cacharel", "Azzaro", "Clinique", "Ungaro", "S.T. Dupont",
        "Sergio Tacchini", "Sonia Rykiel", "Van Gils", "Kesling",
        "Marks & Spencer", "Regine's", "Luciano Soprani", "Montana",
        "Slava Zaïtsev", "Michael Kors", "Ferre", "Iceberg", "Blumarine",
        "Anna Sui", "Ariana Grande", "Christina Aguilera", "MCM",
        "Prince Matchabelli", "Nino Cerruti", "Jacomo", "Benetton"
    ]

    for brand in brands:
        if brand.lower() in name.lower():
            return brand
    return "Unknown"

def categorize_perfume(name):
    """Categorize perfume by scent type and gender"""
    name_lower = name.lower()

    # Default values
    category = "floral"
    gender = "women"

    # Check against database
    for key_name, data in perfume_database.items():
        if key_name.lower() in name_lower:
            return data["category"], data["gender"]

    # Men's indicators
    if any(word in name_lower for word in ["pour homme", "men", "μάνδρες", "man", "male", "noir"]):
        gender = "men"
        category = "fresh"

    # Scent category hints
    if any(word in name_lower for word in ["fresh", "aqua", "sport", "marine"]):
        category = "fresh"
    elif any(word in name_lower for word in ["wood", "oud", "leather", "tobacco"]):
        category = "woody"
    elif any(word in name_lower for word in ["orient", "spice", "amber", "musk"]):
        category = "oriental"
    elif any(word in name_lower for word in ["fruit", "berry", "apple", "peach", "cherry"]):
        category = "fruity"

    return category, gender

def extract_size(name):
    """Extract size from product name"""
    # Look for patterns like "5 ml", "5ml", "3,5 ml"
    match = re.search(r'(\\d+(?:[.,]\\d+)?)\\s*(?:ml)', name, re.I)
    if match:
        size = match.group(1).replace(',', '.')
        return f"{size}ml"
    return "5ml"  # Default

def simplify_name(name_bg):
    """Extract English product name from Greek/Bulgarian text"""
    # Common patterns to remove (Greek and Bulgarian)
    patterns_to_remove = [
        r'[μΜ]ίνι(?:ατούρα)?\\s+(?:άρωμα|αρώματος|αρωματικό|παρφούμ)',
        r'[μΜ]ίνι\\s+[αά]ρώματα',
        r'τοαλέτ\\s+νερό',
        r'eau de (?:toilette|parfum)',
        r'\\d+(?:[.,]\\d+)?\\s*(?:ml)',
        r'[νΝ]έο(?:ς|α)?',
        r'[κΚ]αινούρι(?:ος|α|ο)?',
        r'vintage',
        r'[μΜ]εταχειρισμέν(?:ο|η)',
        r'[πΠ]λήρης',
        r'[αΑ]υθεντικ(?:ό|ή|ός|ά)',
        r'[σΣ]υλλεκτικ(?:ό|ή|ός)',
        r'[σΣ]πάνι(?:ο|α)',
        r'[αΑ]ντικείμενο',
        r'για\\s+(?:γυναίκες|άντρες)',
        r'po?u?r? ?femme',
        r'pour homme',
        r'test',
        r'τεστ',
    ]

    name = name_bg
    for pattern in patterns_to_remove:
        name = re.sub(pattern, '', name, flags=re.I)

    # Clean up
    name = re.sub(r'\\s+', ' ', name).strip()
    name = re.sub(r'^(?:by|από)\\s+', '', name, flags=re.I)
    name = name.strip(' ,-')

    return name

print("Processing products...")
print(f"Total products to process: {len(raw_products)}")

# This is a starter - you'll need to add all the scraped products here
# For now, this script shows the structure
'''

# Write the new file
with open('process_products.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated process_products.py with {len(products)} products!")
