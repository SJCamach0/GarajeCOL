// GarajeCOL Application Client Script

document.addEventListener('DOMContentLoaded', () => {
  setupUserMenu();
  setupMobileMenu();
  setupGlobalSearch();
  setupFavorites();
  setupCatalogFilters();
});

// Helper for Colombian Peso formatting with dots (.)
function formatCOP(amount) {
  if (!amount && amount !== 0) return '$ 0';
  const parts = Math.round(amount).toString().split('');
  let result = '';
  let count = 0;
  for (let i = parts.length - 1; i >= 0; i--) {
    result = parts[i] + result;
    count++;
    if (count % 3 === 0 && i !== 0) {
      result = '.' + result;
    }
  }
  return '$ ' + result;
}
window.formatCOP = formatCOP;

// 1. User Menu Dropdown Toggle on Click (Persistent)
function setupUserMenu() {
  const btn = document.getElementById('userMenuBtn');
  const dropdown = document.getElementById('userDropdown');
  const container = document.getElementById('userMenuContainer');

  if (btn && dropdown) {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', (e) => {
      if (container && !container.contains(e.target)) {
        dropdown.classList.add('hidden');
      }
    });
  }
}

// 2. Mobile Menu Toggle
function setupMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const menu = document.getElementById('mobileMenu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      menu.classList.toggle('hidden');
    });
  }
}

// 3. Global Search Modal
function setupGlobalSearch() {
  const openBtn = document.getElementById('searchOpenBtn');
  const closeBtn = document.getElementById('searchCloseBtn');
  const modal = document.getElementById('searchModal');
  const input = document.getElementById('globalSearchInput');
  const resultsContainer = document.getElementById('searchResults');

  if (!modal || !openBtn) return;

  openBtn.addEventListener('click', () => {
    modal.classList.remove('hidden');
    if (input) input.focus();
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.classList.add('hidden');
    });
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.add('hidden');
  });

  let allProducts = [];
  fetch('/api/products')
    .then(r => r.json())
    .then(data => { allProducts = data.products || []; })
    .catch(console.error);

  if (input && resultsContainer) {
    input.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (q.length < 2) {
        resultsContainer.innerHTML = '<p class="text-xs text-neutral-500">Escribe al menos 2 letras para buscar en todo el catálogo oficial.</p>';
        return;
      }

      const matches = allProducts.filter(p => 
        p.name.toLowerCase().includes(q) || 
        p.brand.toLowerCase().includes(q) || 
        p.category_name.toLowerCase().includes(q) ||
        (p.badge && p.badge.toLowerCase().includes(q))
      );

      if (matches.length === 0) {
        resultsContainer.innerHTML = '<p class="text-xs text-neutral-400 py-3">No encontramos productos coincidentes con "' + q + '".</p>';
        return;
      }

      resultsContainer.innerHTML = matches.map(p => `
        <a href="/producto/${p.id}" class="flex items-center gap-3 p-2.5 rounded-xl bg-[#181a20] hover:bg-neutral-800 transition-colors border border-neutral-700/50">
          <img src="${p.image}" class="w-12 h-12 object-contain p-1 rounded-lg bg-white flex-shrink-0" alt="${p.name}">
          <div class="flex-grow">
            <span class="text-[10px] text-limeBrand uppercase font-bold tracking-wider">${p.brand} · ${p.category_name}</span>
            <h4 class="text-xs font-bold text-white">${p.name}</h4>
          </div>
          <span class="text-xs font-black text-white">${p.price_formatted}</span>
        </a>
      `).join('');
    });
  }
}

// 4. Favorites State Management
function setupFavorites() {
  updateFavoritesCount();

  document.querySelectorAll('.fav-toggle-btn').forEach(btn => {
    const id = btn.getAttribute('data-id');
    const favs = getFavorites();
    const icon = btn.querySelector('i');

    if (favs.includes(id) && icon) {
      icon.className = 'fa-solid fa-heart text-red-500';
    }

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleFavorite(id, btn);
    });
  });
}

function getFavorites() {
  return JSON.parse(localStorage.getItem('garajecol_favs') || '[]');
}

function toggleFavorite(id, btn) {
  let favs = getFavorites();
  const icon = btn.querySelector('i');

  if (favs.includes(id)) {
    favs = favs.filter(x => x !== id);
    if (icon) icon.className = 'fa-regular fa-heart text-white';
  } else {
    favs.push(id);
    if (icon) icon.className = 'fa-solid fa-heart text-red-500';
  }

  localStorage.setItem('garajecol_favs', JSON.stringify(favs));
  updateFavoritesCount();
}

function updateFavoritesCount() {
  const badge = document.getElementById('favCountBadge');
  if (!badge) return;
  const favs = getFavorites();
  if (favs.length > 0) {
    badge.textContent = favs.length;
    badge.classList.remove('hidden');
    badge.classList.add('flex');
  } else {
    badge.classList.add('hidden');
    badge.classList.remove('flex');
  }
}
window.updateFavoritesCount = updateFavoritesCount;

// 5. Catalog Sidebar & Search Filters
function setupCatalogFilters() {
  const searchInput = document.getElementById('catalogSearchInput');
  const priceRange = document.getElementById('priceRange');
  const priceRangeVal = document.getElementById('priceRangeVal');
  const sortSelect = document.getElementById('sortSelect');
  const resetBtn = document.getElementById('resetFiltersBtn');
  const grid = document.getElementById('productGrid');
  const noProducts = document.getElementById('noProductsFound');
  const countBadge = document.getElementById('productCount');

  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll('.product-card'));

  function filterProducts() {
    const q = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const maxPrice = priceRange ? parseInt(priceRange.value) : 150000000;
    
    // Checked brands
    const checkedBrands = Array.from(document.querySelectorAll('input[name="filter_brand"]:checked')).map(cb => cb.value.toUpperCase());
    const checkedTypes = Array.from(document.querySelectorAll('input[name="filter_type"]:checked')).map(cb => cb.value.toLowerCase());
    const checkedDisps = Array.from(document.querySelectorAll('input[name="filter_disp"]:checked')).map(cb => cb.value);

    let visibleCount = 0;

    cards.forEach(card => {
      const name = (card.getAttribute('data-name') || '').toLowerCase();
      const brand = (card.getAttribute('data-brand') || '').toUpperCase();
      const badge = (card.getAttribute('data-badge') || '').toLowerCase();
      const price = parseInt(card.getAttribute('data-price') || '0');
      const disp = parseInt(card.getAttribute('data-disp') || '0');
      const type = (card.getAttribute('data-type') || '').toLowerCase();

      const matchesSearch = !q || name.includes(q) || brand.toLowerCase().includes(q) || badge.includes(q);
      const matchesBrand = checkedBrands.length === 0 || checkedBrands.includes(brand);
      const matchesPrice = price <= maxPrice;
      
      let matchesType = true;
      if (checkedTypes.length > 0) {
        matchesType = checkedTypes.some(t => type.includes(t) || name.includes(t) || badge.includes(t));
      }

      let matchesDisp = true;
      if (checkedDisps.length > 0) {
        matchesDisp = checkedDisps.some(d => {
          if (d === '150') return disp <= 150;
          if (d === '450') return disp > 150 && disp <= 450;
          if (d === '600') return disp > 450;
          return true;
        });
      }

      if (matchesSearch && matchesBrand && matchesPrice && matchesType && matchesDisp) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (countBadge) countBadge.textContent = visibleCount;
    if (noProducts) {
      if (visibleCount === 0) {
        noProducts.classList.remove('hidden');
      } else {
        noProducts.classList.add('hidden');
      }
    }
  }

  // Event bindings
  if (searchInput) searchInput.addEventListener('input', filterProducts);
  
  if (priceRange && priceRangeVal) {
    priceRange.addEventListener('input', () => {
      const val = parseInt(priceRange.value);
      priceRangeVal.textContent = formatCOP(val) + ' COP';
      filterProducts();
    });
  }

  document.querySelectorAll('.filter-checkbox').forEach(cb => {
    cb.addEventListener('change', filterProducts);
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      if (priceRange) {
        priceRange.value = 150000000;
        priceRangeVal.textContent = '$ 150.000.000 COP';
      }
      document.querySelectorAll('.filter-checkbox').forEach(cb => cb.checked = false);
      filterProducts();
    });
  }

  if (sortSelect) {
    sortSelect.addEventListener('change', () => {
      const val = sortSelect.value;
      const sorted = [...cards].sort((a, b) => {
        const pA = parseInt(a.getAttribute('data-price') || '0');
        const pB = parseInt(b.getAttribute('data-price') || '0');
        const nA = (a.getAttribute('data-name') || '').toLowerCase();
        const nB = (b.getAttribute('data-name') || '').toLowerCase();

        if (val === 'precio-asc') return pA - pB;
        if (val === 'precio-desc') return pB - pA;
        if (val === 'nombre') return nA.localeCompare(nB);
        return 0;
      });

      sorted.forEach(c => grid.appendChild(c));
    });
  }
}
