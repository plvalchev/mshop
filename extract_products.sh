#!/bin/bash

# Script to extract product data from vendora.bg URLs

urls_file="/home/user/mshop/batch6-12_urls.txt"
output_file="/home/user/mshop/batch6-12_products.json"

echo "[" > "$output_file"
first=true

while IFS= read -r url; do
  # Skip empty lines
  [ -z "$url" ] && continue

  echo "Processing: $url" >&2

  # Fetch the page
  html=$(curl -s -L "$url")

  # Extract data using grep and sed
  title=$(echo "$html" | grep -oP '(?<=<meta property="og:title" content=")[^"]+' | head -1)
  description=$(echo "$html" | grep -oP '(?<=<meta property="og:description" content=")[^"]+' | head -1)
  image=$(echo "$html" | grep -oP '(?<=<meta property="og:image" content=")[^"]+' | head -1)
  price=$(echo "$html" | grep -oP '(?<=<meta property="product:price:amount" content=")[^"]+' | head -1)

  # Extract from JSON-LD schema if available
  if [ -z "$price" ]; then
    price=$(echo "$html" | grep -oP '"price":"[0-9.]+' | head -1 | cut -d'"' -f4)
  fi

  # Extract brand from title (first word usually)
  brand=$(echo "$title" | awk '{print $1}')

  # Extract size from title
  size=$(echo "$title" | grep -oP '[0-9]+[.,]?[0-9]*\s*(ml|ML)' | head -1)

  # Determine gender from title/description
  gender="women"
  if echo "$title $description" | grep -qi "pour homme\|for men\|мъже\|za mzhe"; then
    gender="men"
  elif echo "$title $description" | grep -qi "unisex"; then
    gender="unisex"
  fi

  # Clean up description (remove newlines and extra spaces)
  description=$(echo "$description" | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  # Build JSON object
  if [ "$first" = false ]; then
    echo "," >> "$output_file"
  fi
  first=false

  cat >> "$output_file" << EOF
  {
    "name": "$title",
    "description": "$description",
    "image": "$image",
    "price": ${price:-0},
    "vendoraUrl": "$url",
    "brand": "$brand",
    "category": "floral",
    "gender": "$gender",
    "size": "$size"
  }
EOF

done < "$urls_file"

echo "" >> "$output_file"
echo "]" >> "$output_file"

echo "Done! Output saved to $output_file" >&2
