function showPopup(title, msg) {
    // create and show popup modal
    const overlay = document.createElement('div');
    overlay.className = 'popup-overlay';
    
    const popup = document.createElement('div');
    popup.className = 'popup';
    popup.innerHTML = `<div class="popup-title">${title}</div><div class="popup-message">${msg}</div><button class="popup-button" onclick="closePopup()">OK</button>`;
    
    overlay.appendChild(popup);
    document.body.appendChild(overlay);
    overlay.style.display = 'block';
    
    overlay.addEventListener('click', e => { if (e.target === overlay) closePopup(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closePopup(); });
}

function closePopup() {
    const overlay = document.querySelector('.popup-overlay');
    if (overlay) overlay.remove();
}

function validateForm() {
    // validate website input
    const input = document.querySelector('input[name="website"]');
    const val = input.value.trim();
    
    if (!val) {
        showPopup('Required Field', 'Please enter a website URL to check.');
        input.focus();
        return false;
    }
    return true;
}

function initDarkMode() {
    // initialize dark mode toggle
    const toggles = [document.querySelector('#mode-switch'), document.querySelector('#theme-mode-switch')].filter(Boolean);
    if (toggles.length === 0) return;
    
    // default to dark mode if no preference is set
    const isDark = localStorage.getItem('darkMode') === null ? true : localStorage.getItem('darkMode') === 'true';
    
    const setMode = dark => {
        document.body.classList.toggle('darkMode', dark);
        toggles.forEach(t => { t.checked = dark; t.setAttribute('aria-checked', dark); });
        localStorage.setItem('darkMode', dark);
    };
    
    setMode(isDark);
    
    toggles.forEach(t => {
        t.addEventListener('change', () => setMode(t.checked));
        t.addEventListener('keypress', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                t.checked = !t.checked;
                t.dispatchEvent(new Event('change'));
                e.preventDefault();
            }
        });
    });
    
    window.addEventListener('storage', e => { if (e.key === 'darkMode') setMode(e.newValue === 'true'); });
}

function initResultPage() {
    // Load result page functions if needed
    if (typeof checkAnother === 'undefined') {
        const script = document.createElement('script');
        script.src = '/static/js/result.js';
        document.head.appendChild(script);
    }
}

function checkAnother() {
    // Redirect to home page
    window.location.href = '/';
}

function downloadJSON() {
    // Download json data as file
    const jsonEl = document.getElementById('json-data');
    if (!jsonEl || !jsonEl.textContent) {
        showPopup('Error', 'No JSON data available to download.');
        return;
    }
    
    try {
        const jsonData = jsonEl.textContent;
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'tabayyun_result.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        showPopup('Success', 'JSON data downloaded successfully!');
    } catch (error) {
        console.error('Download error:', error);
        showPopup('Error', 'Failed to download JSON data.');
    }
}

function handleSubmit(e) {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    const form = e.target;
    const formData = new FormData(form);
    const btn = form.querySelector('.submit-button');
    const origText = btn.textContent;
    btn.textContent = 'Checking...';
    btn.disabled = true;
    
    fetch('/check', { method: 'POST', body: formData })
    .then(res => {
        console.log('Response status:', res.status);
        console.log('Response headers:', res.headers);
        
        const contentType = res.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return res.json();
        }
        
        if (res.ok) {
            return res.text().then(html => {
                document.documentElement.innerHTML = html;
                setTimeout(() => { initDarkMode(); initResultPage(); }, 100);
                return null;
            });
        }
        
        return res.text().then(text => { throw new Error('Server error: ' + text.substring(0, 100)); });
    })
    .then(data => {
        if (data && data.error) showPopup('Error', data.error);
    })
    .catch(error => {
        console.error('Fetch error:', error);
        showPopup('Error', `Request failed: ${error.message}`);
    })
    .finally(() => {
        btn.textContent = origText;
        btn.disabled = false;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) form.addEventListener('submit', handleSubmit);
    
    initDarkMode();
    
    if (document.querySelector('.action-buttons')) initResultPage();
}); 