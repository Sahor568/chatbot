const apiBaseInput = document.getElementById('apiBase');
const saveApiBtn = document.getElementById('saveApi');
const form = document.getElementById('queryForm');
const input = document.getElementById('queryInput');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');

const STORAGE_KEY = 'chatbot_api_base';

function getApiBase() {
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved || 'http://localhost:8000';
}

function setApiBase(url) {
  localStorage.setItem(STORAGE_KEY, url);
}

function renderStatus(msg, isError = false) {
  statusEl.textContent = msg || '';
  statusEl.classList.toggle('error', !!isError);
}

function renderResults(results) {
  resultsEl.innerHTML = '';
  if (!results || results.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'card';
    empty.textContent = 'No results.';
    resultsEl.appendChild(empty);
    return;
  }

  results.forEach((text, i) => {
    const card = document.createElement('div');
    card.className = 'card';

    const idx = document.createElement('div');
    idx.className = 'idx';
    idx.textContent = `Result ${i + 1}`;

    const body = document.createElement('div');
    body.className = 'text';
    body.textContent = text;

    card.appendChild(idx);
    card.appendChild(body);
    resultsEl.appendChild(card);
  });
}

async function doSearch(query) {
  const base = getApiBase().replace(/\/$/, '');
  const url = `${base}/search?${new URLSearchParams({ query })}`;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);

  renderStatus('Searching…');
  try {
    const res = await fetch(url, { method: 'GET', signal: controller.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderStatus('');
    renderResults(data.results);
  } catch (err) {
    if (err.name === 'AbortError') {
      renderStatus('Request timed out. Please try again.', true);
    } else {
      renderStatus(`Request failed: ${err.message}`, true);
    }
  } finally {
    clearTimeout(timeout);
  }
}

// Init
apiBaseInput.value = getApiBase();
saveApiBtn.addEventListener('click', () => {
  const url = apiBaseInput.value.trim();
  if (!url) return;
  try {
    // Basic validation
    const u = new URL(url);
    setApiBase(u.toString().replace(/\/$/, ''));
    renderStatus('API base saved.');
    setTimeout(() => renderStatus(''), 1200);
  } catch {
    renderStatus('Invalid URL for API base.', true);
  }
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if (!q) return;

  input.disabled = true;
  form.querySelector('button[type="submit"]').disabled = true;
  doSearch(q).finally(() => {
    input.disabled = false;
    form.querySelector('button[type="submit"]').disabled = false;
  });
});

// Allow Enter to submit when input focused (already handled by form)
input.focus();
