#!/usr/bin/env python3
import subprocess
import json
import re
import sys
import time

def extract_product_data(url):
    """Fetch HTML and extract product data from a vendora.bg URL"""
    try:
        # Fetch HTML with curl
        result = subprocess.run(
            ['curl', '-s', '-L', url, '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '--max-time', '60'],
            capture_output=True,
            text=True,
            timeout=70
        )

        html = result.stdout

        if not html or len(html) < 100:
            print(f"Error fetching {url}: Empty response", file=sys.stderr)
            return None

        # Extract from page title
        title_match_from_title = re.search(r'<title>\s*([^-]+?)\s*-\s*€', html)
        page_title = title_match_from_title.group(1).strip() if title_match_from_title else ""

        # Extract data from meta tags
        product = {
            "name": "",
            "description": "",
            "image": "",
            "price": 0,
            "vendoraUrl": url,
            "brand": "",
            "category": "floral",
            "gender": "women",
            "size": ""
        }

        # Extract og:title (product name)
        title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if title_match:
            product["name"] = title_match.group(1)
        elif page_title:
            product["name"] = page_title

        # Extract og:description
        desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        if desc_match:
            product["description"] = desc_match.group(1)

        # Extract og:image
        image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if image_match:
            product["image"] = image_match.group(1)

        # Extract price (numeric value)
        price_match = re.search(r'<meta property="product:price:amount" content="([^"]+)"', html)
        if price_match:
            try:
                product["price"] = float(price_match.group(1))
            except ValueError:
                pass

        # Fallback: try to extract from title or JSON data
        if product["price"] == 0:
            title_price_match = re.search(r'€\s*(\d+[,.]?\d*)', html)
            if title_price_match:
                price_str = title_price_match.group(1).replace(',', '.')
                try:
                    product["price"] = float(price_str)
                except ValueError:
                    pass

        # Try extracting from dataLayer JSON
        if product["price"] == 0:
            json_price_match = re.search(r'"price":(\d+(?:\.\d+)?)', html)
            if json_price_match:
                try:
                    product["price"] = float(json_price_match.group(1))
                except ValueError:
                    pass

        # Extract brand from title
        name = product["name"]
        # Common perfume brands
        brands = ['Armani', 'Gucci', 'Chanel', 'Hermes', 'Chlo', 'Chloe', 'Ghost',
                  'Yves Saint Laurent', 'YSL', 'Givenchy', 'Estee Lauder', 'Trussardi',
                  'Karl Lagerfeld', 'Azzaro', '4711', 'Luciano Soprani', 'Moreni',
                  'Montana', 'Slava Zatsev', 'Salvador Dali', 'Rochas', 'Benetton',
                  'Sonia Rykiel', 'Lalique', 'Jacomo', 'Fendi', 'Armaf', 'Escada',
                  'Caron', 'Giorgio Armani', 'Perry', 'Alessandro', 'Regines']

        for brand in brands:
            if brand.lower() in name.lower():
                product["brand"] = brand
                break

        if not product["brand"]:
            # Try to extract first word as brand
            words = name.split()
            if words:
                product["brand"] = words[0]

        # Extract size from title (look for ml, ML, or other size indicators)
        size_match = re.search(r'(\d+\s*ml|\d+\s*ML|\d+\s*мл|\d+\s*x\s*\d+\s*ml)', name, re.IGNORECASE)
        if size_match:
            product["size"] = size_match.group(1).replace(' ', '')
        else:
            # Check description
            size_match = re.search(r'(\d+\s*ml|\d+\s*ML|\d+\s*мл)', product["description"], re.IGNORECASE)
            if size_match:
                product["size"] = size_match.group(1).replace(' ', '')

        # Determine gender
        name_lower = name.lower()
        desc_lower = product["description"].lower()
        combined = name_lower + " " + desc_lower

        if 'for her' in combined or 'woman' in combined or 'women' in combined or 'за жени' in combined:
            product["gender"] = "women"
        elif 'for him' in combined or 'man' in combined or 'men' in combined or 'за мъже' in combined:
            product["gender"] = "men"
        elif 'unisex' in combined:
            product["gender"] = "unisex"
        else:
            # Default to women for perfumes if not specified
            product["gender"] = "women"

        # Special handling for non-perfume items
        if 'pendant' in name_lower or 'neckless' in name_lower or 'чанта' in name_lower or 'chanta' in name_lower or 'kutiya' in name_lower or 'кутия' in name_lower:
            product["gender"] = "unisex"
            if not product["size"]:
                # Extract dimensions for accessories
                dim_match = re.search(r'(\d+\s*[xх]\s*\d+\s*[xх]?\s*\d*\s*см|\d+\s*см)', name + " " + product["description"])
                if dim_match:
                    product["size"] = dim_match.group(1).strip()

        return product

    except Exception as e:
        print(f"Error processing {url}: {str(e)}", file=sys.stderr)
        return None

def main():
    output_file = '/home/user/mshop/batch4-5_products.json'

    # Load existing data
    with open(output_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    print(f"Loaded {len(products)} existing products", file=sys.stderr)

    # Find products with missing data
    failed_indices = []
    for i, product in enumerate(products):
        if not product.get('name') or product.get('price', 0) == 0:
            failed_indices.append(i)

    print(f"Found {len(failed_indices)} products with missing data", file=sys.stderr)
    print(f"Indices: {failed_indices}", file=sys.stderr)

    # Re-fetch failed products
    for idx in failed_indices:
        url = products[idx]['vendoraUrl']
        print(f"Re-fetching product {idx + 1}: {url}", file=sys.stderr)

        new_data = extract_product_data(url)
        if new_data and new_data.get('name') and new_data.get('price', 0) > 0:
            products[idx] = new_data
            print(f"  ✓ Successfully updated product {idx + 1}", file=sys.stderr)
        else:
            print(f"  ✗ Still failed for product {idx + 1}", file=sys.stderr)

        # Small delay to avoid overwhelming the server
        time.sleep(1)

    # Save updated data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    # Count successful products
    successful = sum(1 for p in products if p.get('name') and p.get('price', 0) > 0)
    print(f"\nFinal result: {successful}/{len(products)} products with complete data", file=sys.stderr)

if __name__ == '__main__':
    main()
