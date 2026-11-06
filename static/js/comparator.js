// GarajeCOL Dynamic Comparator Module (Max 3 Items Rule Enforced)

const MAX_COMPARE_ITEMS = 3;

document.addEventListener('DOMContentLoaded', () => {
  setupCompareButtons();
  updateFloatingComparatorBar();
  setupClearButtons();

  if (window.CURRENT_COMP_CATEGORY) {
    initComparatorPage(window.CURRENT_COMP_CATEGORY);
  }
});

function getCompareState() {
  const data = localStorage.getItem('garajecol_compare');
  if (!data) return { category: null, items: [] };
  try {
    return JSON.parse(data);
  } catch (e) {
    return { category: null, items: [] };
  }
}

function saveCompareState(state) {
  localStorage.setItem('garajecol_compare', JSON.stringify(state));
  updateFloatingComparatorBar();
}

// 1. Setup compare toggle buttons in cards and detail views
function setupCompareButtons() {
  const state = getCompareState();
  const currentIds = state.items.map(i => i.id);

  document.querySelectorAll('.comp-toggle-btn').forEach(btn => {
    const id = btn.getAttribute('data-id');
    const category = btn.getAttribute('data-category');
    const name = btn.getAttribute('data-name');

    if (currentIds.includes(id)) {
      btn.classList.add('bg-lime-400', 'text-black', 'border-lime-500');
      btn.innerHTML = '<i class="fa-solid fa-check"></i> En Comparador';
    } else {
      btn.classList.remove('bg-lime-400', 'text-black', 'border-lime-500');
      btn.innerHTML = '<i class="fa-solid fa-code-compare text-neutral-600"></i> Comparar';
    }

    const newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);

    newBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      handleCompareToggle(id, category, name, newBtn);
    });
  });
}
window.setupCompareButtons = setupCompareButtons;

function handleCompareToggle(id, category, name, btn) {
  let state = getCompareState();

  if (state.category && state.category !== category && state.items.length > 0) {
    const confirmReset = confirm(
      `Actualmente estás comparando productos de la categoría "${state.category}". ¿Deseas iniciar una nueva comparación para "${category}"?`
    );
    if (!confirmReset) return;
    state = { category: category, items: [] };
  }

  const existingIndex = state.items.findIndex(i => i.id === id);

  if (existingIndex > -1) {
    state.items.splice(existingIndex, 1);
    if (state.items.length === 0) state.category = null;
    saveCompareState(state);
    
    btn.classList.remove('bg-lime-400', 'text-black', 'border-lime-500');
    btn.innerHTML = '<i class="fa-solid fa-code-compare text-neutral-600"></i> Comparar';
  } else {
    if (state.items.length >= MAX_COMPARE_ITEMS) {
      alert(`⚠️ Límite del Comparador: La plataforma permite comparar un máximo de ${MAX_COMPARE_ITEMS} productos simultáneamente para mantener una visualización clara y óptima en pantalla.\n\nPor favor elimina uno de los productos seleccionados para poder añadir "${name}".`);
      return;
    }

    state.category = category;
    state.items.push({ id, category, name });
    saveCompareState(state);

    btn.classList.add('bg-lime-400', 'text-black', 'border-lime-500');
    btn.innerHTML = '<i class="fa-solid fa-check"></i> En Comparador';
  }
}

// 2. Clear buttons (Header & Floating Bar)
function setupClearButtons() {
  const clearHandler = () => {
    saveCompareState({ category: null, items: [] });
    setupCompareButtons();
    showEmptyComparatorState();
  };

  const headerClear = document.getElementById('headerClearBtn');
  if (headerClear) headerClear.onclick = clearHandler;

  const floatClear = document.getElementById('clearCompBtn');
  if (floatClear) floatClear.onclick = clearHandler;
}

function showEmptyComparatorState() {
  const tableWrapper = document.getElementById('comparatorTableWrapper');
  const emptyState = document.getElementById('comparatorEmptyState');
  const actions = document.getElementById('comparatorActions');

  if (tableWrapper) tableWrapper.classList.add('hidden');
  if (actions) actions.classList.add('hidden');
  if (emptyState) emptyState.classList.remove('hidden');
}

function showTableComparatorState() {
  const tableWrapper = document.getElementById('comparatorTableWrapper');
  const emptyState = document.getElementById('comparatorEmptyState');
  const actions = document.getElementById('comparatorActions');

  if (tableWrapper) tableWrapper.classList.remove('hidden');
  if (actions) actions.classList.remove('hidden');
  if (emptyState) emptyState.classList.add('hidden');
}

// 3. Floating Bar at bottom
function updateFloatingComparatorBar() {
  const bar = document.getElementById('floatingCompBar');
  const countBadge = document.getElementById('compBadgeCount');
  const listText = document.getElementById('compItemList');
  const goLink = document.getElementById('goToCompLink');

  if (!bar) return;

  const state = getCompareState();
  const count = state.items.length;

  if (countBadge) countBadge.textContent = count;

  if (count > 0) {
    bar.classList.remove('translate-y-full');
    if (listText) {
      listText.textContent = state.items.map(i => i.name).join(' · ');
    }
    if (goLink) {
      goLink.href = `/comparador?tipo=${state.category || 'motos'}`;
    }
  } else {
    bar.classList.add('translate-y-full');
  }
}

// 4. Comparator Page Dynamic Renderer
async function initComparatorPage(category) {
  const state = getCompareState();
  let ids = [];

  // Check if there are user-selected items for this category
  if (state.category === category && state.items.length > 0) {
    ids = state.items.map(i => i.id);
  } else {
    // If empty, show the empty state right away
    showEmptyComparatorState();
    return;
  }

  try {
    const res = await fetch('/api/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category, ids, allow_default: false })
    });
    const data = await res.json();
    
    if (data.is_empty || !data.products || data.products.length === 0) {
      showEmptyComparatorState();
    } else {
      showTableComparatorState();
      renderComparatorTable(data);
    }
  } catch (err) {
    console.error('Error fetching comparator data:', err);
    showEmptyComparatorState();
  }

  // Save comparison button handler
  const saveBtn = document.getElementById('saveComparisonBtn');
  const toast = document.getElementById('saveToast');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      const savedComps = JSON.parse(localStorage.getItem('garajecol_saved_comparisons') || '[]');
      savedComps.push({
        category: category,
        date: new Date().toISOString(),
        items: state.items
      });
      localStorage.setItem('garajecol_saved_comparisons', JSON.stringify(savedComps));
      
      if (toast) {
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 3000);
      }
    });
  }
}

function renderComparatorTable(data) {
  const products = data.products || [];
  const attributes = data.attributes || [];
  const tbody = document.getElementById('comparatorBody');

  // Fill up to 3 product columns in the header
  for (let i = 0; i < 3; i++) {
    const colIndex = i + 1;
    const colEl = document.getElementById(`compCol${colIndex}`);
    const imgEl = document.getElementById(`compImg${colIndex}`);
    const brandEl = document.getElementById(`compBrand${colIndex}`);
    const nameEl = document.getElementById(`compName${colIndex}`);
    const linkEl = document.getElementById(`compLink${colIndex}`);

    if (i < products.length) {
      const p = products[i];
      if (colEl) colEl.style.display = '';
      if (imgEl) {
        imgEl.src = p.image_large || p.image;
        imgEl.alt = p.name;
      }
      if (brandEl) brandEl.textContent = p.brand;
      if (nameEl) nameEl.textContent = p.name;
      if (linkEl) linkEl.href = `/producto/${p.id}`;

      if (p.best_value) {
        if (colEl) colEl.className = 'p-6 w-1/4 align-top border-l border-neutral-100 relative bg-[#f4fbe8]';
        const badge = document.getElementById('compBestValBadge');
        if (badge) badge.classList.remove('hidden');
      } else {
        if (colEl) colEl.className = 'p-6 w-1/4 align-top border-l border-neutral-100 relative bg-white';
      }
    } else {
      if (colEl) colEl.style.display = 'none';
    }
  }

  // Build Attribute Rows
  let rowsHtml = '';

  // Row 1: Precio
  rowsHtml += `
    <tr class="hover:bg-neutral-50 transition-colors">
      <td class="p-6 font-bold text-neutral-900 border-t border-neutral-100">Precio</td>
      ${products.map(p => `
        <td class="p-6 border-l border-neutral-100 font-black text-neutral-900 text-sm ${p.best_value ? 'bg-[#f4fbe8]' : ''}">
          ${p.price_formatted}
        </td>
      `).join('')}
    </tr>
  `;

  // Specs Rows
  attributes.forEach(attr => {
    rowsHtml += `
      <tr class="hover:bg-neutral-50 transition-colors">
        <td class="p-6 font-semibold text-neutral-600 border-t border-neutral-100 capitalize">${attr}</td>
        ${products.map(p => `
          <td class="p-6 border-l border-neutral-100 text-neutral-800 leading-relaxed whitespace-pre-line ${p.best_value ? 'bg-[#f4fbe8] font-medium' : ''}">
            ${(p.specs && p.specs[attr]) ? p.specs[attr] : '—'}
          </td>
        `).join('')}
      </tr>
    `;
  });

  // Official Store Link Row
  rowsHtml += `
    <tr class="hover:bg-neutral-50 transition-colors bg-neutral-50/50">
      <td class="p-6 font-bold text-neutral-900 border-t border-neutral-100">Tienda Oficial</td>
      ${products.map(p => `
        <td class="p-6 border-l border-neutral-100 ${p.best_value ? 'bg-[#f4fbe8]' : ''}">
          <a href="${p.official_url}" target="_blank" rel="noopener noreferrer" class="btn-garaje-lime px-3 py-1.5 rounded text-[11px] font-bold inline-flex items-center gap-1.5">
            <span>${p.official_store_name || 'Ver Oficial'}</span>
            <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
          </a>
        </td>
      `).join('')}
    </tr>
  `;

  if (tbody) tbody.innerHTML = rowsHtml;

  // Setup column remove buttons
  document.querySelectorAll('.remove-col-btn').forEach(btn => {
    btn.onclick = () => {
      const colIdx = parseInt(btn.getAttribute('data-col'));
      if (products[colIdx]) {
        let state = getCompareState();
        state.items = state.items.filter(i => i.id !== products[colIdx].id);
        if (state.items.length === 0) state.category = null;
        saveCompareState(state);
        initComparatorPage(window.CURRENT_COMP_CATEGORY);
      }
    };
  });
}
