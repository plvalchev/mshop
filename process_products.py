#!/usr/bin/env python3
"""
Process all scraped Vendora products and create a comprehensive products.json
This script organizes and categorizes all products from the scraping results.
"""

import json
import re

# All scraped products data (combined from all pages)
raw_products = [
    # Page 1
    {"name_bg": "Мини парфюми Neblina и Dilly's нови, автентични", "price": 35, "url": "/items/n0m21yp/", "image": "https://bcdn.vendora.gr/0/10/2b/102bb779bebe784bfd9388cab7e2391ebb06eeb9.jpg"},
    {"name_bg": "Мини парфюм Sun Moon Stars Karl Lagerfeld нов, 3,5 мл", "price": 15, "url": "/items/jpqwgok/", "image": "https://bcdn.vendora.gr/0/42/75/42752e93d8226ee1d59a6100e3bbc8ca9b2fc6aa.jpg"},
    {"name_bg": "Be Bop Kesling мини парфюм нов, тоалетна вода 7.5 ml", "price": 10, "url": "/items/qqy53w1/", "image": "https://bcdn.vendora.gr/0/6e/76/6e76af87573824867915f083d35cfaa6e8ef1c6d.jpg"},
    {"name_bg": "Romeo di Romeo Gigli мини парфюм нов, 7.5 ml", "price": 13, "url": "/items/2oqkw09/", "image": "https://bcdn.vendora.gr/0/f9/d9/f9d9364def1fa0b6d4e02b1dc710a5d9f1394a28.jpg"},
    {"name_bg": "Red Jeans Versace мини парфюм нов, 7.5 ml тоалетна вода", "price": 20, "url": "/items/114ezg8/", "image": "https://bcdn.vendora.gr/0/32/77/327758ce145652ba830a1369899a31f13c19828c.jpg"},
    {"name_bg": "Cabochard Great мини парфюм нов, 1,8 мл", "price": 12, "url": "/items/n0m5znp/", "image": "https://bcdn.vendora.gr/0/d2/62/d26226e78a4b3e80313bbc6d95991fab3ef99d26.jpg"},
    {"name_bg": "Shafali Fleur Rare Yves Rocher мини парфюм нов 7,5 ml", "price": 7, "url": "/items/114keyz/", "image": "https://bcdn.vendora.gr/0/4f/20/4f202b2dd83fda7785f553a6c89a7ceac8599f1f.jpg"},
    {"name_bg": "Мини парфюм Créature by Gilles Cantuel 4,5 мл нов, тоалетна вода", "price": 13, "url": "/items/dyoe5mj/", "image": "https://bcdn.vendora.gr/0/ac/c1/acc1fcd47819dec1e6e7717ca1e4acac93b46449.jpg"},
    {"name_bg": "Magie Noir Lancome мини парфюм нов, 7.5 ml", "price": 30, "url": "/items/7y56p2j/", "image": "https://bcdn.vendora.gr/0/dd/2f/dd2f3e0156e18f0ccdcb45ae7e8a35a04fead508.jpg"},
    {"name_bg": "Ispahan Yves Rocher миниатюрен парфюм 15 ml нов", "price": 16, "url": "/items/kyz3wm0/", "image": "https://bcdn.vendora.gr/0/52/be/52be432451b3df19a3bdeebc9354af1731bdbfe9.jpg"},
    {"name_bg": "Green Jeans Versace мини парфюм нов, 7,5 ml", "price": 20, "url": "/items/dyoj690/", "image": "https://bcdn.vendora.gr/0/28/64/2864b0189977a6e318c65491b7e827914004062f.jpg"},
    {"name_bg": "Invictus Paco Rabanne мини парфюм нов, 5 ml", "price": 20, "url": "/items/qqy5qwz/", "image": "https://bcdn.vendora.gr/0/92/d7/92d7ca35e24d908efeac5cd723c7f1ea192a5b5a.jpg"},
    {"name_bg": "Мини парфюм Silver Rain La Prairie 2 ml нов", "price": 22, "url": "/items/xqgp3m8/", "image": "https://bcdn.vendora.gr/0/1c/af/1caf7380ab7635ffb95e743eac55f55031680bcb.jpg"},
    {"name_bg": "Nocturnes de Caron мини парфюм нов, тоалетна вода 5 ml", "price": 17, "url": "/items/dyoex0p/", "image": "https://bcdn.vendora.gr/0/8d/8d/8d8d843d1d932ed8c16e14cda6230048d72274cf.jpg"},
    {"name_bg": "Michelle Balenciaga мини парфюм нов, рядък колекционерски екземпляр 5 ml", "price": 15, "url": "/items/ojy5gqw/", "image": "https://bcdn.vendora.gr/0/6d/a8/6da8ed88339b503314ce7bb036e2057d32079590.jpg"},
    {"name_bg": "Knowing Estèe Lauder мини парфюм нов, 3,5 мл", "price": 13, "url": "/items/mmp7y68/", "image": "https://bcdn.vendora.gr/0/db/7a/db7a2b5676d8e40782834b996f99ce33c0c7acdf.jpg"},
    {"name_bg": "Drakkar Noir Guy Laroche мини парфюм нов, 5 ml тоалетна вода", "price": 15, "url": "/items/4ep832m/", "image": "https://bcdn.vendora.gr/0/a9/17/a91737da2986432e1589bc52051e6d16c35c80f4.jpg"},
    {"name_bg": "Blue Jeans Versace мини парфюм нов, 7.5 ml", "price": 20, "url": "/items/114ez28/", "image": "https://bcdn.vendora.gr/0/be/70/be702f9ad072383e5eeff02c8891284fdab1911e.jpg"},
    {"name_bg": "Vent Vent Pierre Balmain мини парфюм нов, тоалетна вода 4 мл", "price": 12, "url": "/items/zjqmw11/", "image": "https://bcdn.vendora.gr/0/5b/1c/5b1ccf0a892346e837adfd2d8bc7ddf405488b77.jpg"},
    {"name_bg": "Vent Vent Pierre Balmain мини парфюм нов, колекционерска опаковка", "price": 30, "url": "/items/9xze501/", "image": "https://bcdn.vendora.gr/0/3e/93/3e9395536b4e2f94cfd716c77085f729beb066e5.jpg"},
]

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
    if any(word in name_lower for word in ["pour homme", "men", "мъже", "man", "male", "noir"]):
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
    # Look for patterns like "5 ml", "5ml", "3,5 мл"
    match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:ml|мл)', name, re.I)
    if match:
        size = match.group(1).replace(',', '.')
        return f"{size}ml"
    return "5ml"  # Default

def simplify_name(name_bg):
    """Extract English product name from Bulgarian text"""
    # Common patterns to remove
    patterns_to_remove = [
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
        r'по?у?р? ?femme',
        r'pour homme',
    ]

    name = name_bg
    for pattern in patterns_to_remove:
        name = re.sub(pattern, '', name, flags=re.I)

    # Clean up
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'^(?:by|от)\s+', '', name, flags=re.I)
    name = name.strip(' ,-')

    return name

print("Processing products...")
print(f"Total products to process: {len(raw_products)}")

# This is a starter - you'll need to add all the scraped products here
# For now, this script shows the structure
