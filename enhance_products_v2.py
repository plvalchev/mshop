#!/usr/bin/env python3
"""
Enhanced product name and description cleaner to match first 70 products
"""
import json
import re
import html

# Known fragrance names and their proper formatting
KNOWN_FRAGRANCES = {
    # Versace
    'red jeans': 'Red Jeans',
    'blue jeans': 'Blue Jeans',
    'green jeans': 'Green Jeans',
    'yellow diamond': 'Yellow Diamond',
    'vanitas': 'Vanitas',
    'versense': 'Versense',
    'dylan blue': 'Dylan Blue',
    'eros': 'Eros',

    # Karl Lagerfeld
    'sun moon stars': 'Sun Moon Stars',
    'chloe': 'Chloe',
    'chloe narcisse': 'Chloe Narcisse',

    # Designer brands
    'magie noir': 'Magie Noir',
    'tresor': 'Trésor',
    'miracle': 'Miracle',
    'invictus': 'Invictus',
    'silver rain': 'Silver Rain',
    'nocturnes': 'Nocturnes',
    'michelle': 'Michelle',
    'knowing': 'Knowing',
    'beautiful': 'Beautiful',
    'drakkar noir': 'Drakkar Noir',
    'vent vert': 'Vent Vert',
    'romeo': 'Romeo',
    'cabochard': 'Cabochard',
    'shafali': 'Shafali',
    'ispahan': 'Ispahan',
    'neblina': 'Neblina',
    'creature': 'Créature',
    'be bop': 'Be Bop',
    'ungaro diva': 'Ungaro Diva',
    'loulou blue': 'Loulou Blue',
    'signature': 'Signature',
    'dkny be delicious': 'DKNY Be Delicious',
    'signorina': 'Signorina',
    'sergio tacchini': 'Sergio Tacchini',
    'van gils': 'Van Gils',
    'lalique': 'Lalique',
    'nature': 'Nature',
    'trussardi': 'Trussardi',
    'opium': 'Opium',
    'escada acte': 'Escada Acte 2',
    'givenchy iii': 'Givenchy III',
    '4711': '4711 Cologne',
    'jadore': 'J\'adore',
    'le male': 'Le Male',
    'le beau': 'Le Beau',
    'divine': 'Divine',
    'eternity moment': 'Eternity Moment',
    'burberry her': 'Burberry Her',
    'ghost': 'Ghost',
    'amarige': 'Amarige',
    'ombre rose': 'Ombre Rose',
    'coco': 'Coco',
    'samba': 'Samba',
    'happy': 'Happy',
    'ysatis': 'Ysatis',
    'hot couture': 'Hot Couture',
    'truth': 'Truth',
    'popy moreni': 'Popy Moreni',
    'maroussia': 'Maroussia',
    'miss dior': 'Miss Dior',
    'light blue': 'Light Blue',
    'organza': 'Organza',
    'fahrenheit': 'Fahrenheit',
    'dolce vita': 'Dolce Vita',
    'daisy': 'Daisy',
    'my burberry': 'My Burberry',
    'oh de moschino': 'Oh de Moschino',
    'rochas fleur': 'Rochas Fleur d\'Eau',
    'toy 2': 'Toy 2 Bubble Gum',
    'cheap and chic': 'Cheap & Chic',
    'le parfum': 'Le Parfum',
    'paradox': 'Paradox',
    'lauren': 'Lauren',
    'ricci ricci': 'Ricci Ricci',
    'fendi': 'Fendi',
    'le roy soleil': 'Le Roy Soleil',
    'fiorucci': 'Fiorucci',
    'honeysuckle': 'Honeysuckle',
    'chopard casmir': 'Chopard Casmir',
    'oscar': 'Oscar',
    'blumarine': 'Blumarine',
    'prada la femme': 'Prada La Femme',
    'iceberg twice': 'Iceberg Twice',
    'h24': 'H24',
    'sicily': 'Sicily',
    'joop night flight': 'Joop Night Flight',
    'skin': 'Skin',
    'a scent': 'A Scent',
    'michael kors': 'Michael Kors',
    'cachet': 'Cachet',
    'anais anais': 'Anaïs Anaïs',
    'byzance': 'Byzance',
    'alchimie': 'Alchimie',
    'fleur de fleurs': 'Fleur de Fleurs',
    'dalistyle': 'Dalistyle',
    'pi': 'Pi',
    'roma': 'Roma',
    'rubylips': 'Rubylips',
    'andy warhol': 'Andy Warhol',
    'pink wish': 'Pink Wish',
    'la perla': 'La Perla',
    'boucheron': 'Boucheron',
    'mimmina': 'Mimmina',
    'pupa plumes': 'Pupa Plumes',
    'sky': 'Sky',
    'mcm': 'MCM',
    'christina aguilera': 'Christina Aguilera',
    'ariana grande': 'Ariana Grande',
}

def extract_fragrance_name(text):
    """Extract proper fragrance name from text"""

    text_lower = text.lower()

    # Try to match known fragrances
    for key, proper_name in KNOWN_FRAGRANCES.items():
        if key in text_lower:
            return proper_name

    # If not found, try to extract brand + fragrance
    # Remove common words
    clean = text
    patterns = [
        r'мини.*?парфюм.*?', r'mini.*?perfume?.*?', r'miniatyura?.*?',
        r'тоалетна вода', r'eau de (?:toilette|parfum)', r'eau de perfume',
        r'\d+(?:[.,]\d+)?\s*(?:ml|мл)', r'нов.*?', r'винтидж',
        r'като нов.*?', r'пълен', r'автентичн.*?', r'колекционерск.*?',
        r'рядък', r'екземпляр', r'за (?:жени|мъже)', r'употребяван.*?',
        r'pour (?:femme|homme)', r'new', r'authentic', r'vintage',
        r'collector.*?', r'rare', r'full', r'used', r'set', r'komplekt',
        r'tester', r'original', r'limited edition', r'roll.?on',
    ]

    for pattern in patterns:
        clean = re.sub(pattern, ' ', clean, flags=re.I)

    # Remove Cyrillic
    clean = re.sub(r'[а-яА-Я]+', ' ', clean)

    # Clean up
    clean = re.sub(r'\s+', ' ', clean).strip()
    clean = re.sub(r'[^\w\s\'-]', '', clean)
    clean = html.unescape(clean)

    # Title case
    clean = clean.title()

    return clean.strip() if clean else text

def generate_elegant_description(name, brand, category, gender, size):
    """Generate elegant description matching first 70 products"""

    # Fragrance descriptions by category
    descriptions = {
        'floral': [
            'Elegant floral fragrance',
            'Beautiful floral bouquet',
            'Delicate floral scent',
            'Fresh floral fragrance',
            'Luxurious floral perfume'
        ],
        'fresh': [
            'Fresh and vibrant scent',
            'Crisp and invigorating fragrance',
            'Light and refreshing perfume',
            'Clean and fresh scent',
            'Sparkling fresh fragrance'
        ],
        'oriental': [
            'Warm oriental fragrance',
            'Exotic oriental scent',
            'Rich oriental perfume',
            'Mysterious oriental fragrance',
            'Sensual oriental scent'
        ],
        'woody': [
            'Sophisticated woody scent',
            'Warm woody fragrance',
            'Classic woody perfume',
            'Elegant woody scent',
            'Rich woody fragrance'
        ],
        'fruity': [
            'Fresh fruity fragrance',
            'Vibrant fruity scent',
            'Sweet fruity perfume',
            'Playful fruity fragrance',
            'Sparkling fruity scent'
        ],
    }

    # Select appropriate description
    desc_list = descriptions.get(category, descriptions['floral'])
    main_desc = desc_list[0]

    # Add brand context
    if brand and brand != 'Unknown':
        if 'Versace' in brand:
            ending = 'Iconic Versace miniature.'
        elif 'Dior' in brand:
            ending = 'Elegant Dior collector\'s miniature.'
        elif 'Chanel' in brand:
            ending = 'Classic Chanel miniature perfume.'
        elif 'Givenchy' in brand:
            ending = 'Sophisticated Givenchy miniature.'
        elif 'Prada' in brand:
            ending = 'Modern Prada miniature.'
        else:
            ending = f'Refined {brand} miniature perfume.'
    else:
        ending = 'Collector\'s miniature perfume.'

    return f"{main_desc}. {ending}"

def enhance_products(products):
    """Enhance products to match quality of first 70"""

    enhanced = 0

    for product in products:
        if product.get('id', 0) < 71:
            continue

        original_name = product.get('name', '')
        brand = product.get('brand', '')
        category = product.get('category', 'floral')
        gender = product.get('gender', 'women')
        size = product.get('size', '')

        # Extract clean name
        clean_name = extract_fragrance_name(original_name)

        # If name is too short or same as brand, try harder
        if len(clean_name) < 3 or clean_name == brand:
            # Keep trying with original name
            clean_name = re.sub(r'мини.*', '', original_name, flags=re.I)
            clean_name = extract_fragrance_name(clean_name)

        # Generate description
        new_desc = generate_elegant_description(clean_name, brand, category, gender, size)

        # Update
        if clean_name and clean_name != original_name:
            product['name'] = clean_name
            product['description'] = new_desc
            enhanced += 1
            print(f"  ✓ #{product['id']}: {clean_name} ({brand})")

    return enhanced

def main():
    with open('products.json', 'r') as f:
        products = json.load(f)

    print(f"📦 Total products: {len(products)}")
    print(f"🔧 Enhancing products 71-{len(products)}...\n")

    count = enhance_products(products)

    with open('products.json', 'w') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Enhanced {count} products!")

if __name__ == '__main__':
    main()
