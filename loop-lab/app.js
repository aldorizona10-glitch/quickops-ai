const STORAGE_KEY = 'loop-lab-items-v1';
const HISTORY_KEY = 'loop-lab-history-v1';

const form = document.querySelector('#loop-form');
const titleInput = document.querySelector('#title');
const areaInput = document.querySelector('#area');
const riskInput = document.querySelector('#risk');
const expectedInput = document.querySelector('#expected');
const list = document.querySelector('#loop-list');
const historyList = document.querySelector('#history-list');
const emptyState = document.querySelector('#empty-state');
const template = document.querySelector('#item-template');
const passRate = document.querySelector('#pass-rate');
const seedDemo = document.querySelector('#seed-demo');
const clearHistory = document.querySelector('#clear-history');
const filters = Array.from(document.querySelectorAll('.filter'));

let items = load(STORAGE_KEY, []);
let history = load(HISTORY_KEY, []);
let activeFilter = 'all';

function load(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

function addHistory(action, item) {
  history = [
    {
      id: crypto.randomUUID(),
      action,
      title: item.title,
      status: item.status,
      at: new Date().toLocaleString(),
    },
    ...history,
  ].slice(0, 12);
}

function render() {
  const visible = items.filter(item => activeFilter === 'all' || item.status === activeFilter);
  list.innerHTML = '';
  emptyState.hidden = visible.length > 0;

  for (const item of visible) {
    const node = template.content.firstElementChild.cloneNode(true);
    node.dataset.id = item.id;
    node.dataset.status = item.status;
    node.querySelector('.item-title').textContent = item.title;
    node.querySelector('.meta').textContent = `${item.area} / ${item.risk} risk / ${item.status}`;
    node.querySelector('.expected').textContent = item.expected;
    list.append(node);
  }

  historyList.innerHTML = '';
  for (const entry of history) {
    const node = document.createElement('li');
    node.innerHTML = `<strong>${entry.action}</strong>${entry.title}<br>${entry.at}`;
    historyList.append(node);
  }

  const total = items.length || 1;
  const passing = items.filter(item => item.status === 'passing').length;
  passRate.textContent = `${Math.round((passing / total) * 100)}%`;
}

form.addEventListener('submit', event => {
  event.preventDefault();
  const title = titleInput.value.trim();
  const expected = expectedInput.value.trim();
  if (!title || !expected) return;

  const item = {
    id: crypto.randomUUID(),
    title,
    area: areaInput.value,
    risk: riskInput.value,
    expected,
    status: 'failing',
  };
  items = [item, ...items];
  addHistory('Added failing check', item);
  save();
  form.reset();
  render();
});

list.addEventListener('click', event => {
  const button = event.target.closest('button');
  const row = event.target.closest('.loop-item');
  if (!button || !row) return;

  const item = items.find(candidate => candidate.id === row.dataset.id);
  if (!item) return;

  const action = button.dataset.action;
  if (action === 'remove') {
    items = items.filter(candidate => candidate.id !== item.id);
    addHistory('Removed check', item);
  } else {
    item.status = action === 'pass' ? 'passing' : 'failing';
    addHistory(action === 'pass' ? 'Marked passing' : 'Marked failing', item);
  }
  save();
  render();
});

filters.forEach(button => {
  button.addEventListener('click', () => {
    activeFilter = button.dataset.filter;
    filters.forEach(filter => filter.classList.toggle('active', filter === button));
    render();
  });
});

seedDemo.addEventListener('click', () => {
  const demo = [
    {
      id: crypto.randomUUID(),
      title: 'Lead form blocks empty email',
      area: 'Frontend',
      risk: 'High',
      expected: 'Submitting without an email should show an inline validation message.',
      status: 'failing',
    },
    {
      id: crypto.randomUUID(),
      title: 'Queue filter keeps failing checks visible',
      area: 'Data',
      risk: 'Medium',
      expected: 'Changing filters should not delete items or reset their status.',
      status: 'passing',
    },
  ];
  items = [...demo, ...items];
  demo.forEach(item => addHistory('Seeded demo check', item));
  save();
  render();
});

clearHistory.addEventListener('click', () => {
  history = [];
  save();
  render();
});

render();
