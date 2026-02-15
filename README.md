# Mini Perfume Collection - Static Website

A beautiful, modern static website for showcasing and organizing miniature perfume collections. Perfect for collectors who want to market their items on Vendora with better organization and filtering capabilities.

## Features

- **Responsive Design**: Beautiful layout that works on desktop, tablet, and mobile
- **Advanced Filtering**: Filter by category, brand, gender, price, and search by keywords
- **Sorting Options**: Sort products by name, price, or brand
- **Vendora Integration**: Each product links directly to Vendora for purchases
- **Easy Product Management**: Simple JSON-based product catalog
- **OG Tag Scraping**: Python script to automatically sync products from Vendora URLs

## Demo

Visit the live site: [Your GitHub Pages URL will be here]

## How It Works

1. **Marketing**: The website displays your miniature perfume collection with beautiful cards, filters, and categories
2. **Product Discovery**: Customers can easily browse and filter products
3. **Purchase**: When ready to buy, customers click "View on Vendora" to complete their order on your Vendora shop

## Setup

### 1. Clone or Download

```bash
git clone [your-repo-url]
cd mshop
```

### 2. Add Your Products

You have two options:

#### Option A: Manual Entry

Edit `products.json` and add your products:

```json
{
    "id": 1,
    "name": "Product Name",
    "brand": "Brand Name",
    "category": "floral",
    "gender": "women",
    "price": 45,
    "description": "Product description",
    "image": "https://your-image-url.com/image.jpg",
    "vendoraUrl": "https://vendora.com/your-product"
}
```

**Categories**: `floral`, `woody`, `oriental`, `fresh`, `fruity`, `spicy`
**Gender**: `women`, `men`, `unisex`

#### Option B: Sync from Vendora (Recommended)

1. Install Python dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```

2. Create a file `vendora-urls.txt` with your product URLs (one per line):
   ```
   https://vendora.com/product/your-product-1
   https://vendora.com/product/your-product-2
   https://vendora.com/product/your-product-3
   ```

3. Run the sync script:
   ```bash
   python sync-vendora.py --urls vendora-urls.txt
   ```

4. The script will:
   - Fetch OG tags from each URL
   - Extract product name, description, image, and price
   - Add products to `products.json`
   - Note: You'll need to manually update `category` and `gender` fields

### 3. Customize Branding

Edit `index.html` to update:
- Site title and tagline
- About section content
- Contact information
- Vendora shop link in footer

Edit `styles.css` to customize colors (see CSS variables in `:root`)

### 4. Deploy to GitHub Pages

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Initial setup of mini perfume shop"
   git push origin main
   ```

2. Enable GitHub Pages:
   - Go to your repository on GitHub
   - Click **Settings**
   - Scroll to **Pages** section
   - Under **Source**, select `main` branch and `/ (root)` folder
   - Click **Save**

3. Your site will be live at: `https://yourusername.github.io/repository-name/`

## File Structure

```
mshop/
├── index.html           # Main HTML file
├── styles.css          # Stylesheet
├── app.js              # JavaScript functionality
├── products.json       # Product catalog
├── sync-vendora.py     # Vendora sync script
└── README.md           # This file
```

## Syncing Products from Vendora

The `sync-vendora.py` script extracts product information from Vendora listing pages using Open Graph (OG) tags.

### What it extracts:
- Product name (og:title)
- Description (og:description)
- Image (og:image)
- Price (og:price or meta tags)
- Vendora URL

### Usage Examples:

**Sync a single product:**
```bash
python sync-vendora.py --url https://vendora.com/product/123
```

**Sync multiple products from a file:**
```bash
python sync-vendora.py --urls vendora-urls.txt
```

**Replace all products (not merge):**
```bash
python sync-vendora.py --urls vendora-urls.txt --replace
```

**Save to different file:**
```bash
python sync-vendora.py --urls vendora-urls.txt --output my-products.json
```

### After Syncing

The script automatically extracts most data, but you should manually review and update:

1. **category**: Assign proper category (floral, woody, oriental, fresh, fruity, spicy)
2. **gender**: Set target gender (women, men, unisex)
3. **brand**: Verify the brand name was extracted correctly
4. **description**: Enhance if needed for better marketing

## Customization

### Colors

Edit the CSS variables in `styles.css`:

```css
:root {
    --primary-color: #d4a574;      /* Main brand color */
    --secondary-color: #8b6f47;    /* Secondary brand color */
    --accent-color: #f4e4d7;       /* Accent background */
    /* ... */
}
```

### Categories

To add/remove categories:

1. Edit the `<select id="category">` options in `index.html`
2. Update the filter logic in `app.js` if needed
3. Add corresponding values to your products in `products.json`

### Layout

The site uses CSS Grid for responsive layouts. Breakpoints are defined in `styles.css`:
- Desktop: > 768px
- Tablet: 768px - 480px
- Mobile: < 480px

## Tips for Collectors

1. **Use High-Quality Images**: Product images should be at least 280x280px
2. **Write Detailed Descriptions**: Include notes about rarity, condition, and what makes each piece special
3. **Accurate Categorization**: Proper categories help customers find what they're looking for
4. **Competitive Pricing**: Research similar miniatures to price competitively
5. **Regular Updates**: Keep your collection fresh by regularly adding new items

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This is a proof-of-concept template for personal use. Feel free to customize and use for your miniature perfume collection.

## Support

For issues or questions:
1. Check that `products.json` is valid JSON
2. Ensure all images are accessible (HTTPS URLs work best)
3. Verify Vendora URLs are correct and accessible

## Roadmap

Potential future enhancements:
- Automatic sync on schedule
- Product availability status
- Customer reviews/ratings
- Wishlist functionality
- Currency conversion
- Multi-language support

---

**Happy Collecting! 🌸**
