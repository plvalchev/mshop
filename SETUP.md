# Quick Setup Guide

## Step 1: Add Your Vendora Products

### Method 1: Automatic Sync (Recommended)

1. Create a file called `vendora-urls.txt`:
   ```bash
   cp vendora-urls.txt.example vendora-urls.txt
   ```

2. Edit `vendora-urls.txt` and add your Vendora product URLs:
   ```
   https://vendora.com/listing/your-product-1
   https://vendora.com/listing/your-product-2
   https://vendora.com/listing/your-product-3
   ```

3. Install Python requirements:
   ```bash
   pip install requests beautifulsoup4
   ```

4. Run the sync script:
   ```bash
   python sync-vendora.py --urls vendora-urls.txt
   ```

5. Edit `products.json` and update the `category` and `gender` fields for each product

### Method 2: Manual Entry

1. Open `products.json` in a text editor

2. Add your products following this format:
   ```json
   {
       "id": 1,
       "name": "Chanel N°5",
       "brand": "Chanel",
       "category": "floral",
       "gender": "women",
       "price": 45,
       "description": "The iconic fragrance in a collectible miniature.",
       "image": "https://your-image-url.com/chanel.jpg",
       "vendoraUrl": "https://vendora.com/your-listing"
   }
   ```

## Step 2: Customize the Site

1. Edit `index.html`:
   - Update the site title in `<h1>` tag
   - Update the tagline
   - Update the About section
   - Add your contact information
   - Update Vendora shop link in footer

2. Edit `styles.css` (optional):
   - Customize colors by changing CSS variables at the top

## Step 3: Test Locally

1. Open `index.html` in your web browser to preview
2. Test all filters and sorting
3. Make sure product links work

## Step 4: Deploy to GitHub Pages

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Setup mini perfume shop"
   git push
   ```

2. Go to GitHub repository Settings > Pages
3. Set source to `main` branch and `/ (root)` folder
4. Click Save
5. Wait a few minutes for deployment

Your site will be live at: `https://yourusername.github.io/mshop/`

## Updating Products

To add new products later:

1. Add new Vendora URLs to `vendora-urls.txt`
2. Run: `python sync-vendora.py --urls vendora-urls.txt`
3. Update categories and gender in `products.json`
4. Commit and push:
   ```bash
   git add products.json
   git commit -m "Add new products"
   git push
   ```

Your site will automatically update in a few minutes!

## Troubleshooting

**Products not showing:**
- Check `products.json` is valid JSON (use jsonlint.com)
- Check browser console for errors (F12)

**Images not loading:**
- Make sure image URLs are HTTPS
- Check URLs are publicly accessible

**Vendora sync not working:**
- Make sure Python packages are installed
- Check that Vendora URLs are correct and accessible
- Some pages may not have OG tags - add those manually

**GitHub Pages not updating:**
- Wait 5-10 minutes after pushing
- Check Settings > Pages for deployment status
- Make sure branch and folder are correct

## Need Help?

Check the full README.md for detailed documentation.
