#!/usr/bin/env python3
"""
Scrape all products from a Vendora user profile with pagination support.
This script handles multiple pages and includes safeguards against getting stuck.

Usage:
    python scrape_user_profile.py --user 214xqq --max-pages 6
"""

import json
import sys
import argparse
import time
import re
from urllib.parse import urljoin, urlparse, parse_qs

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)


class VendoraUserScraper:
    def __init__(self, user_id, max_pages=10):
        self.user_id = user_id
        self.max_pages = max_pages
        self.base_url = f"http://vendora.bg/users/{user_id}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        self.products = []
        self.pages_scraped = 0

    def extract_products_from_page(self, soup, page_num):
        """Extract all product listings from a user profile page"""
        products = []

        # Look for product listings - they're typically in divs or article elements
        # Vendora uses specific class names for product items
        product_items = soup.find_all('div', class_=lambda x: x and 'item' in x.lower())

        if not product_items:
            # Try alternative selectors
            product_items = soup.find_all('article')

        if not product_items:
            # Try finding links to /items/
            links = soup.find_all('a', href=re.compile(r'/items/[^/]+'))
            product_items = [link.find_parent() for link in links if link.find_parent()]
            product_items = list(set(filter(None, product_items)))

        print(f"  Found {len(product_items)} potential product elements on page {page_num}")

        for item in product_items:
            try:
                product = self.parse_product_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"  Warning: Error parsing product item: {str(e)}")
                continue

        return products

    def parse_product_item(self, item):
        """Parse a single product item from the HTML"""
        product = {}

        # Find product link (URL)
        link = item.find('a', href=re.compile(r'/items/[^/]+'))
        if not link:
            return None

        product['url'] = link.get('href', '')
        if not product['url'].startswith('http'):
            product['url'] = urljoin('http://vendora.bg', product['url'])

        # Find product name/title
        # Try different possible elements
        title = item.find('h3') or item.find('h2') or item.find('h4')
        if title:
            product['name_bg'] = title.get_text(strip=True)
        else:
            # Try to get from link text
            product['name_bg'] = link.get_text(strip=True)

        # Find price
        price_elem = item.find(string=re.compile(r'лв|BGN|€'))
        if price_elem:
            price_text = price_elem.strip()
            # Extract numeric value
            price_match = re.search(r'(\d+(?:[.,]\d+)?)', price_text)
            if price_match:
                product['price'] = float(price_match.group(1).replace(',', '.'))
        else:
            # Try finding in parent
            price_elem = item.find(class_=lambda x: x and 'price' in x.lower())
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'(\d+(?:[.,]\d+)?)', price_text)
                if price_match:
                    product['price'] = float(price_match.group(1).replace(',', '.'))

        # Find image
        img = item.find('img')
        if img:
            product['image'] = img.get('src', '') or img.get('data-src', '')
            if product['image'] and not product['image'].startswith('http'):
                product['image'] = urljoin('http://vendora.bg', product['image'])

        # Only return if we have at least name and URL
        if product.get('name_bg') and product.get('url'):
            return product

        return None

    def get_page(self, page_num):
        """Fetch a specific page from the user's profile"""
        if page_num == 1:
            url = self.base_url
        else:
            # Vendora typically uses ?page=2 format
            url = f"{self.base_url}?page={page_num}"

        print(f"\nFetching page {page_num}: {url}")

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"  Error fetching page {page_num}: {str(e)}")
            return None

    def has_next_page(self, soup):
        """Check if there's a next page"""
        # Look for pagination links
        next_link = soup.find('a', string=re.compile(r'(Next|Следваща|›|»)', re.I))
        if next_link:
            return True

        # Check for pagination with page numbers
        page_links = soup.find_all('a', href=re.compile(r'[?&]page=\d+'))
        if page_links:
            return True

        return False

    def scrape_all_pages(self):
        """Scrape all pages from the user profile"""
        print(f"Starting scrape of user {self.user_id}")
        print(f"Maximum pages to scrape: {self.max_pages}")
        print("=" * 60)

        page_num = 1

        while page_num <= self.max_pages:
            # Fetch the page
            html = self.get_page(page_num)

            if not html:
                print(f"Failed to fetch page {page_num}, stopping.")
                break

            # Parse the HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Extract products
            page_products = self.extract_products_from_page(soup, page_num)

            if not page_products:
                print(f"  No products found on page {page_num}, stopping.")
                break

            print(f"  Extracted {len(page_products)} products from page {page_num}")
            self.products.extend(page_products)
            self.pages_scraped = page_num

            # Check if there's a next page
            if page_num < self.max_pages:
                if not self.has_next_page(soup):
                    print(f"  No next page link found, stopping at page {page_num}")
                    break

            # Important: Add delay to avoid getting blocked
            if page_num < self.max_pages:
                delay = 2
                print(f"  Waiting {delay} seconds before next page...")
                time.sleep(delay)

            page_num += 1

        print("\n" + "=" * 60)
        print(f"Scraping complete!")
        print(f"Pages scraped: {self.pages_scraped}")
        print(f"Total products found: {len(self.products)}")

        return self.products

    def save_to_json(self, filepath='scraped_products.json'):
        """Save scraped products to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(self.products)} products to {filepath}")

    def save_to_python(self, filepath='scraped_products.py'):
        """Save as Python list for easy copy-paste into process_products.py"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Scraped products from Vendora user profile\n")
            f.write(f"# User ID: {self.user_id}\n")
            f.write(f"# Pages scraped: {self.pages_scraped}\n")
            f.write(f"# Total products: {len(self.products)}\n\n")
            f.write("raw_products = ")
            f.write(json.dumps(self.products, indent=4, ensure_ascii=False))
            f.write("\n")
        print(f"Saved Python format to {filepath}")


def main():
    parser = argparse.ArgumentParser(description='Scrape products from Vendora user profile')
    parser.add_argument('--user', default='214xqq', help='Vendora user ID (default: 214xqq)')
    parser.add_argument('--max-pages', type=int, default=10,
                       help='Maximum number of pages to scrape (default: 10)')
    parser.add_argument('--output', default='scraped_products.json',
                       help='Output JSON file (default: scraped_products.json)')
    parser.add_argument('--python-output', default='scraped_products.py',
                       help='Output Python file (default: scraped_products.py)')

    args = parser.parse_args()

    # Create scraper
    scraper = VendoraUserScraper(args.user, max_pages=args.max_pages)

    # Scrape all pages
    products = scraper.scrape_all_pages()

    if not products:
        print("No products were scraped!")
        sys.exit(1)

    # Save results
    scraper.save_to_json(args.output)
    scraper.save_to_python(args.python_output)

    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Review the scraped data in", args.output)
    print("2. Copy the products from", args.python_output)
    print("3. Update process_products.py with the new data")
    print("=" * 60)


if __name__ == '__main__':
    main()
