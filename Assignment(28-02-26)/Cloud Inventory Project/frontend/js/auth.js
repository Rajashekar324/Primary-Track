const API_BASE = 'http://localhost:5000/api';
let currentMode = 'login';

function toggleMode(mode) {
    currentMode = mode;
    const loginBtn = document.getElementById('tab-login');
    const registerBtn = document.getElementById('tab-register');
    const emailGroup = document.getElementById('email-group');
    const submitBtn = document.getElementById('submit-btn');
    const errorMsg = document.getElementById('error-msg');

    errorMsg.classList.add('hidden');

    if (mode === 'login') {
        loginBtn.className = 'flex-1 py-2 px-4 rounded-md text-sm font-medium bg-blue-500 text-white shadow transition-all';
        registerBtn.className = 'flex-1 py-2 px-4 rounded-md text-sm font-medium text-slate-300 hover:text-white transition-all';
        emailGroup.classList.add('hidden');
        document.getElementById('email').removeAttribute('required');
        submitBtn.textContent = 'Sign In';
    } else {
        registerBtn.className = 'flex-1 py-2 px-4 rounded-md text-sm font-medium bg-blue-500 text-white shadow transition-all';
        loginBtn.className = 'flex-1 py-2 px-4 rounded-md text-sm font-medium text-slate-300 hover:text-white transition-all';
        emailGroup.classList.remove('hidden');
        document.getElementById('email').setAttribute('required', 'true');
        submitBtn.textContent = 'Create Account';
    }
}

document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorMsg = document.getElementById('error-msg');
    errorMsg.classList.add('hidden');
    
    const db_choice = document.querySelector('input[name="db_choice"]:checked').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;

    const payload = { db_choice, username, password };
    if (currentMode === 'register') payload.email = email;

    try {
        const response = await fetch(`${API_BASE}/auth/${currentMode}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            // Save to localStorage
            localStorage.setItem('inventory_user_id', data.user_id || data.user?._id || data.user?.id);
            localStorage.setItem('inventory_db', data.db);
            localStorage.setItem('inventory_username', username);
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        } else {
            errorMsg.textContent = data.error || 'Authentication failed';
            errorMsg.classList.remove('hidden');
        }
    } catch (err) {
        errorMsg.textContent = 'Network error. Is the server running?';
        errorMsg.classList.remove('hidden');
    }
});
