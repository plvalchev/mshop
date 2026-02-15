#!/usr/bin/env python3
"""
Vendora Product Sync Script
This script fetches product information from Vendora URLs using OG tags
and updates the products.json file.

Usage:
    python sync-vendora.py --urls urls.txt
    python sync-vendora.py --url https://vendora.com/product/123

Requirements:
    pip install requests beautifulsoup4
"""

import json
import sys
import argparse
from urllib.parse import urlparse
import re

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)


class VendoraSync:
    def __init__(self):
        self.products = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def extract_og_tags(self, url):
        """Extract Open Graph tags from a Vendora product page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract OG tags
            og_tags = {}
            for meta in soup.find_all('meta'):
                property_attr = meta.get('property', '')
                content = meta.get('content', '')

                if property_attr.startswith('og:'):
                    key = property_attr.replace('og:', '')
                    og_tags[key] = content

            # Also check for standard meta tags
            meta_tags = {}
            for meta in soup.find_all('meta'):
                name = meta.get('name', '')
                content = meta.get('content', '')

                if name in ['description', 'keywords', 'price', 'brand']:
                    meta_tags[name] = content

            return og_tags, meta_tags

        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return {}, {}

    def parse_product(self, url, og_tags, meta_tags):
        """Parse product data from OG tags and meta tags"""
        product = {
            'vendoraUrl': url
        }

        # Extract title/name (og:title)
        product['name'] = og_tags.get('title', 'Unknown Product')

        # Extract description (og:description or meta description)
        product['description'] = og_tags.get('description',
                                            meta_tags.get('description',
                                                        'No description available'))

        # Extract image (og:image)
        product['image'] = og_tags.get('image',
                                      'https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Perfume')

        # Extract price (from various possible sources)
        price_str = (og_tags.get('price:amount', '') or
                    meta_tags.get('price', '') or
                    og_tags.get('product:price:amount', ''))

        try:
            # Extract numeric value from price string
            price_match = re.search(r'[\d.]+', price_str)
            if price_match:
                product['price'] = float(price_match.group())
            else:
                product['price'] = 0
        except:
            product['price'] = 0

        # Extract brand (og:brand or from title)
        brand = meta_tags.get('brand', '')
        if not brand and 'title' in og_tags:
            # Try to extract brand from title (usually first word)
            title_parts = og_tags['title'].split()
            if title_parts:
                brand = title_parts[0]
        product['brand'] = brand or 'Unknown'

        # Default values for fields that need manual categorization
        product['category'] = 'floral'  # Default, should be updated manually
        product['gender'] = 'unisex'    # Default, should be updated manually

        # Generate ID based on URL
        product['id'] = abs(hash(url)) % (10 ** 8)

        return product

    def fetch_product(self, url):
        """Fetch a single product from Vendora URL"""
        print(f"Fetching product from: {url}")
        og_tags, meta_tags = self.extract_og_tags(url)

        if not og_tags and not meta_tags:
            print(f"  Warning: No OG tags found for {url}")
            return None

        product = self.parse_product(url, og_tags, meta_tags)
        print(f"  Found: {product['name']} - ${product['price']}")

        return product

    def fetch_products_from_urls(self, urls):
        """Fetch multiple products from a list of URLs"""
        products = []

        for url in urls:
            url = url.strip()
            if not url or url.startswith('#'):
                continue

            product = self.fetch_product(url)
            if product:
                products.append(product)

        return products

    def load_existing_products(self, filepath='products.json'):
        """Load existing products from JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {filepath}, starting fresh")
            return []

    def save_products(self, products, filepath='products.json'):
        """Save products to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(products, f, indent=4)
        print(f"\nSaved {len(products)} products to {filepath}")

    def merge_products(self, existing, new_products):
        """Merge new products with existing ones, avoiding duplicates"""
        existing_urls = {p['vendoraUrl'] for p in existing if 'vendoraUrl' in p}

        merged = existing.copy()
        added = 0

        for product in new_products:
            if product['vendoraUrl'] not in existing_urls:
                # Assign new ID
                max_id = max([p.get('id', 0) for p in merged] + [0])
                product['id'] = max_id + 1
                merged.append(product)
                added += 1
                print(f"  Added: {product['name']}")

        print(f"\nAdded {added} new products")
        return merged


def main():
    parser = argparse.ArgumentParser(description='Sync products from Vendora')
    parser.add_argument('--url', help='Single Vendora product URL')
    parser.add_argument('--urls', help='File containing Vendora product URLs (one per line)')
    parser.add_argument('--output', default='products.json', help='Output JSON file')
    parser.add_argument('--replace', action='store_true',
                       help='Replace existing products instead of merging')

    args = parser.parse_args()

    if not args.url and not args.urls:
        parser.print_help()
        print("\nError: Please provide either --url or --urls")
        sys.exit(1)

    syncer = VendoraSync()

    # Collect URLs to fetch
    urls = []
    if args.url:
        urls.append(args.url)

    if args.urls:
        try:
            with open(args.urls, 'r') as f:
                urls.extend(f.readlines())
        except FileNotFoundError:
            print(f"Error: File {args.urls} not found")
            sys.exit(1)

    # Fetch products
    print(f"Fetching {len(urls)} product(s)...\n")
    new_products = syncer.fetch_products_from_urls(urls)

    if not new_products:
        print("No products fetched successfully")
        sys.exit(1)

    # Merge or replace
    if args.replace:
        final_products = new_products
    else:
        existing_products = syncer.load_existing_products(args.output)
        final_products = syncer.merge_products(existing_products, new_products)

    # Save
    syncer.save_products(final_products, args.output)

    print("\n" + "="*50)
    print("IMPORTANT: Please review and update the following fields manually:")
    print("  - category: (floral, woody, oriental, fresh, fruity, spicy)")
    print("  - gender: (women, men, unisex)")
    print("  - brand: Verify brand name is correct")
    print("="*50)


if __name__ == '__main__':
    main()
