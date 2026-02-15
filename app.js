// Mini Perfume Shop - Main Application
class PerfumeShop {
    constructor() {
        this.products = [];
        this.filteredProducts = [];
        this.brands = new Set();
        this.init();
    }

    async init() {
        await this.loadProducts();
        this.setupEventListeners();
        this.populateBrands();
        this.applyFilters();
    }

    async loadProducts() {
        const loading = document.getElementById('loading');
        try {
            // Try to load from products.json
            const response = await fetch('products.json');
            if (response.ok) {
                this.products = await response.json();
            } else {
                // If no products.json, use demo data
                this.products = this.getDemoProducts();
            }
            loading.style.display = 'none';
        } catch (error) {
            console.error('Error loading products:', error);
            // Use demo data as fallback
            this.products = this.getDemoProducts();
            loading.style.display = 'none';
        }
    }

    getDemoProducts() {
        // Demo data structure - replace with actual Vendora data
        return [
            {
                id: 1,
                name: "Chanel N°5",
                brand: "Chanel",
                category: "floral",
                gender: "women",
                price: 45,
                description: "The iconic fragrance in a collectible miniature. Timeless elegance in floral aldehydic notes.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Chanel+N°5",
                vendoraUrl: "#"
            },
            {
                id: 2,
                name: "Dior Sauvage",
                brand: "Dior",
                category: "fresh",
                gender: "men",
                price: 38,
                description: "A fresh and woody composition. Rare miniature edition perfect for collectors.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Dior+Sauvage",
                vendoraUrl: "#"
            },
            {
                id: 3,
                name: "Tom Ford Black Orchid",
                brand: "Tom Ford",
                category: "oriental",
                gender: "unisex",
                price: 65,
                description: "Luxurious and sensual oriental fragrance. Limited edition miniature.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Black+Orchid",
                vendoraUrl: "#"
            },
            {
                id: 4,
                name: "Versace Eros",
                brand: "Versace",
                category: "fresh",
                gender: "men",
                price: 32,
                description: "Fresh and masculine fragrance. Collectible miniature bottle.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Versace+Eros",
                vendoraUrl: "#"
            },
            {
                id: 5,
                name: "Yves Saint Laurent Black Opium",
                brand: "YSL",
                category: "oriental",
                gender: "women",
                price: 42,
                description: "Addictive coffee and vanilla notes. Rare miniature for collectors.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Black+Opium",
                vendoraUrl: "#"
            },
            {
                id: 6,
                name: "Gucci Bloom",
                brand: "Gucci",
                category: "floral",
                gender: "women",
                price: 40,
                description: "Rich white floral fragrance. Beautiful collectible miniature.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Gucci+Bloom",
                vendoraUrl: "#"
            },
            {
                id: 7,
                name: "Paco Rabanne 1 Million",
                brand: "Paco Rabanne",
                category: "spicy",
                gender: "men",
                price: 35,
                description: "Spicy leather fragrance. Iconic gold bar bottle in miniature.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=1+Million",
                vendoraUrl: "#"
            },
            {
                id: 8,
                name: "Jo Malone Wood Sage & Sea Salt",
                brand: "Jo Malone",
                category: "fresh",
                gender: "unisex",
                price: 55,
                description: "Fresh and earthy scent. Elegant miniature bottle.",
                image: "https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=Wood+Sage",
                vendoraUrl: "#"
            }
        ];
    }

    populateBrands() {
        this.products.forEach(product => {
            this.brands.add(product.brand);
        });

        const brandSelect = document.getElementById('brand');
        Array.from(this.brands).sort().forEach(brand => {
            const option = document.createElement('option');
            option.value = brand.toLowerCase();
            option.textContent = brand;
            brandSelect.appendChild(option);
        });
    }

    setupEventListeners() {
        // Filter inputs
        document.getElementById('search').addEventListener('input', () => this.applyFilters());
        document.getElementById('category').addEventListener('change', () => this.applyFilters());
        document.getElementById('brand').addEventListener('change', () => this.applyFilters());
        document.getElementById('gender').addEventListener('change', () => this.applyFilters());
        document.getElementById('price').addEventListener('change', () => this.applyFilters());
        document.getElementById('sort').addEventListener('change', () => this.applyFilters());

        // Reset button
        document.getElementById('reset-filters').addEventListener('click', () => this.resetFilters());
    }

    applyFilters() {
        const searchTerm = document.getElementById('search').value.toLowerCase();
        const categoryFilter = document.getElementById('category').value;
        const brandFilter = document.getElementById('brand').value;
        const genderFilter = document.getElementById('gender').value;
        const priceFilter = document.getElementById('price').value;
        const sortBy = document.getElementById('sort').value;

        // Filter products
        this.filteredProducts = this.products.filter(product => {
            const matchesSearch = product.name.toLowerCase().includes(searchTerm) ||
                                product.brand.toLowerCase().includes(searchTerm) ||
                                product.description.toLowerCase().includes(searchTerm);

            const matchesCategory = categoryFilter === 'all' || product.category === categoryFilter;
            const matchesBrand = brandFilter === 'all' || product.brand.toLowerCase() === brandFilter;
            const matchesGender = genderFilter === 'all' || product.gender === genderFilter;
            const matchesPrice = priceFilter === 'all' || product.price <= parseInt(priceFilter);

            return matchesSearch && matchesCategory && matchesBrand && matchesGender && matchesPrice;
        });

        // Sort products
        this.sortProducts(sortBy);

        // Render products
        this.renderProducts();
    }

    sortProducts(sortBy) {
        switch(sortBy) {
            case 'name':
                this.filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'price-low':
                this.filteredProducts.sort((a, b) => a.price - b.price);
                break;
            case 'price-high':
                this.filteredProducts.sort((a, b) => b.price - a.price);
                break;
            case 'brand':
                this.filteredProducts.sort((a, b) => a.brand.localeCompare(b.brand));
                break;
        }
    }

    renderProducts() {
        const grid = document.getElementById('products-grid');
        const noResults = document.getElementById('no-results');
        const resultsCount = document.getElementById('results-count');

        // Update results count
        resultsCount.textContent = this.filteredProducts.length;

        // Clear grid
        grid.innerHTML = '';

        if (this.filteredProducts.length === 0) {
            grid.style.display = 'none';
            noResults.style.display = 'block';
            return;
        }

        grid.style.display = 'grid';
        noResults.style.display = 'none';

        // Render product cards
        this.filteredProducts.forEach(product => {
            const card = this.createProductCard(product);
            grid.appendChild(card);
        });
    }

    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';

        card.innerHTML = `
            <img src="${product.image}" alt="${product.name}" class="product-image"
                 onerror="this.src='https://via.placeholder.com/280x280/f4e4d7/8b6f47?text=${encodeURIComponent(product.name)}'">
            <div class="product-info">
                <div class="product-brand">${product.brand}</div>
                <h3 class="product-name">${product.name}</h3>
                <div class="product-category">${this.formatCategory(product.category)} • ${this.formatGender(product.gender)}</div>
                <p class="product-description">${product.description}</p>
                <div class="product-footer">
                    <div class="product-price">€${product.price}</div>
                    <a href="${product.vendoraUrl}" target="_blank" rel="noopener" class="btn">View on Vendora</a>
                </div>
            </div>
        `;

        return card;
    }

    formatCategory(category) {
        return category.charAt(0).toUpperCase() + category.slice(1);
    }

    formatGender(gender) {
        return gender.charAt(0).toUpperCase() + gender.slice(1);
    }

    resetFilters() {
        document.getElementById('search').value = '';
        document.getElementById('category').value = 'all';
        document.getElementById('brand').value = 'all';
        document.getElementById('gender').value = 'all';
        document.getElementById('price').value = 'all';
        document.getElementById('sort').value = 'name';
        this.applyFilters();
    }
}

// Initialize the shop when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PerfumeShop();
});
