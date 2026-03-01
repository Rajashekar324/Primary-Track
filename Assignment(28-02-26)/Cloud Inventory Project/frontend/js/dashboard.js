const API_BASE = 'http://localhost:5000/api';
let currentView = 'products';
let productsList = [];

// App Initialization
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadDashboardInfo();
    switchView('products');
});

function checkAuth() {
    if (!localStorage.getItem('inventory_user_id')) {
        window.location.href = 'index.html';
    }
}

function loadDashboardInfo() {
    document.getElementById('user-display').textContent = localStorage.getItem('inventory_username') || 'User';
    document.getElementById('db-display').textContent = localStorage.getItem('inventory_db') || 'MySQL';
}

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

function switchView(viewName) {
    document.getElementById(`view-${currentView}`).classList.add('hidden');
    document.getElementById(`nav-${currentView}`).classList.remove('nav-active');

    currentView = viewName;

    document.getElementById(`view-${currentView}`).classList.remove('hidden');
    document.getElementById(`nav-${currentView}`).classList.add('nav-active');

    const titleMap = { 'products': 'Products Catalog', 'orders': 'Order History', 'logs': 'Activity Logs' };
    document.getElementById('page-title').textContent = titleMap[viewName];

    document.getElementById('header-actions').classList.toggle('hidden', viewName !== 'products');

    loadData(viewName);
}

function showLoading(show) { document.getElementById('loading').classList.toggle('hidden', !show); }
function showError(msg) {
    const el = document.getElementById('error-message');
    if (msg) { el.textContent = msg; el.classList.remove('hidden'); }
    else { el.classList.add('hidden'); }
}

async function loadData(view) {
    showLoading(true);
    showError(null);
    try {
        if (view === 'products') await fetchProducts();
        else if (view === 'orders') await fetchOrders();
        else if (view === 'logs') await fetchLogs();
    } catch (err) {
        showError(`Failed to load ${view}. Is the server running?`);
    } finally {
        showLoading(false);
    }
}

// --- PRODUCTS ---
async function fetchProducts() {
    const res = await fetch(`${API_BASE}/products/`);
    const data = await res.json();
    productsList = data.products || [];
    renderProducts();
}

function renderProducts() {
    const container = document.getElementById('products-grid');
    container.innerHTML = productsList.map(p => `
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
            <div class="h-48 bg-slate-100 flex items-center justify-center border-b border-slate-200 relative">
                <i class="fa-solid fa-box text-5xl text-slate-300"></i>
                <div class="absolute top-3 right-3 bg-white px-2 py-1 rounded-md text-xs font-bold shadow-sm ${p.quantity > 10 ? 'text-green-600' : 'text-orange-500'}">
                    Stock: ${p.quantity}
                </div>
            </div>
            <div class="p-5">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-slate-800 text-lg truncate pr-2">${p.name}</h3>
                    <span class="text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-md">$${p.price.toFixed(2)}</span>
                </div>
                <p class="text-slate-500 text-sm mb-4 line-clamp-2">${p.description}</p>
                <div class="flex gap-2">
                    <button onclick="openOrderModal(${p.id}, '${p.name.replace(/'/g, "\\'")}', ${p.price})" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors" ${p.quantity === 0 ? 'disabled class="opacity-50 cursor-not-allowed flex-1 bg-slate-400 text-white py-2 rounded-lg text-sm"' : ''}>
                        Order Now
                    </button>
                    <!-- Small delete button -->
                    <button onclick="deleteProduct(${p.id})" class="text-slate-400 hover:text-red-500 hover:bg-red-50 px-3 py-2 rounded-lg border border-slate-200 transition-colors">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('') || '<div class="col-span-full text-center py-10 text-slate-500">No products found. Add one!</div>';
}

// --- MODALS ---
function openModal(id) {
    const overlay = document.getElementById('modal-overlay');
    const modal = document.getElementById(id);
    overlay.classList.remove('hidden');
    modal.classList.remove('hidden');
    // Animate in
    requestAnimationFrame(() => {
        overlay.classList.remove('opacity-0');
        modal.classList.remove('scale-95');
    });
}

function closeModal() {
    const overlay = document.getElementById('modal-overlay');
    const modals = document.querySelectorAll('#modal-overlay > div');

    // Animate out
    overlay.classList.add('opacity-0');
    modals.forEach(m => m.classList.add('scale-95'));

    setTimeout(() => {
        overlay.classList.add('hidden');
        modals.forEach(m => m.classList.add('hidden'));
    }, 200);
}

// Add Product
document.getElementById('product-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('prod-name').value,
        description: document.getElementById('prod-desc').value,
        price: parseFloat(document.getElementById('prod-price').value),
        quantity: parseInt(document.getElementById('prod-qty').value)
    };

    try {
        const res = await fetch(`${API_BASE}/products/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) { showToast('Product added successfully!'); closeModal(); loadData('products'); e.target.reset(); }
        else { const d = await res.json(); alert(d.error || 'Failed to add product'); }
    } catch (err) { alert('Network error'); }
});

// Delete Product
async function deleteProduct(id) {
    if (!confirm("Are you sure you want to delete this product?")) return;
    try {
        const res = await fetch(`${API_BASE}/products/${id}`, { method: 'DELETE' });
        if (res.ok) { showToast('Product deleted!'); loadData('products'); }
        else { const d = await res.json(); alert(d.error || 'Cannot delete product (likely exists in an order)'); }
    } catch (err) { alert('Network error'); }
}

// Order Modal Setup
function openOrderModal(id = null) {
    const select = document.getElementById('order-product-select');
    select.innerHTML = productsList.map(p =>
        `<option value="${p.id}" ${p.id === id ? 'selected' : ''}>${p.name} - $${p.price.toFixed(2)} (${p.quantity} in stock)</option>`
    ).join('');

    document.getElementById('order-qty').value = 1;
    openModal('order-modal');
}

async function submitOrder() {
    const productId = document.getElementById('order-product-select').value;
    const qty = parseInt(document.getElementById('order-qty').value);

    if (!productId || qty < 1) return alert('Invalid selection');

    const payload = {
        user_id: parseInt(localStorage.getItem('inventory_user_id')) || 1, // Fallback to 1 for testing
        items: [{ product_id: parseInt(productId), quantity: qty }]
    };

    try {
        const res = await fetch(`${API_BASE}/orders/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const d = await res.json();

        if (res.ok) {
            showToast('Order placed successfully!');
            closeModal();
            // Automatically refresh products stock if we are on products view
            if (currentView === 'products') loadData('products');
        }
        else { alert(d.error || 'Order failed'); }
    } catch (err) { alert('Network error'); }
}

// --- LOGS ---
async function fetchLogs() {
    const res = await fetch(`${API_BASE}/logs/`);
    const data = await res.json();
    const list = document.getElementById('logs-list');

    list.innerHTML = (data.logs || []).map(log => `
        <li class="p-4 hover:bg-slate-50 transition-colors flex items-start gap-4">
             <div class="mt-1 flex-shrink-0 w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center">
                 <i class="fa-solid fa-bolt text-slate-500 text-xs"></i>
             </div>
             <div class="flex-1">
                 <div class="flex justify-between">
                     <p class="text-sm font-medium text-slate-900 border border-slate-200 inline-block px-2 py-0.5 rounded text-xs bg-white uppercase tracking-wide">
                        ${log.action}
                     </p>
                     <p class="text-xs text-slate-500">${new Date(log.timestamp).toLocaleString()}</p>
                 </div>
                 <p class="mt-1 text-sm text-slate-600">User ID: <span class="font-mono text-xs bg-slate-100 px-1 rounded">${log.user_id}</span></p>
                 <pre class="mt-2 text-xs bg-slate-800 text-slate-300 p-2 rounded overflow-x-auto">${JSON.stringify(log.details, null, 2)}</pre>
             </div>
        </li>
    `).join('') || '<li class="p-8 text-center text-slate-500">No activity logs found.</li>';
}

// --- ORDERS LIST (Fake placeholder since we didn't implement GET /orders/all) --
// For a complete dashboard, you'd add an API to fetch user's orders. Let's just mock it or fetch by specific ID.
async function fetchOrders() {
    const list = document.getElementById('orders-list');
    list.innerHTML = `<tr><td colspan="5" class="px-6 py-8 text-center text-slate-500">Make an order first! Use specific GET endpoint /api/orders/ID to fetch an order.</td></tr>`;
}

// Toasts
function showToast(msg) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'bg-slate-800 text-white px-4 py-3 rounded-lg shadow-lg text-sm flex items-center gap-3 transform translate-y-full opacity-0 transition-all duration-300';
    toast.innerHTML = `<i class="fa-solid fa-circle-check text-green-400"></i> ${msg}`;

    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-full', 'opacity-0');
    });

    // Remove after 3s
    setTimeout(() => {
        toast.classList.add('translate-y-full', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
