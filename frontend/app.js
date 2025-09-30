// Shopping List Application - Simplified Version
const API_BASE = `${window.location.origin}/api`;
let shoppingItems = [];

// Placeholder variables for future functionality
let currentUser = 'default';
let persons = [];
let mealData = {};
let lastSavedData = {};
let currentWeek = getCurrentWeek();

// Initialize app
document.addEventListener('DOMContentLoaded', function () {
  // Set current year in footer
  document.getElementById('currentYear').textContent = new Date().getFullYear();

  showStatus('Loading shopping list...', 'info');
  setupShoppingEventListeners();
  loadShoppingItems();
});

function showStatus(message, type = 'info') {
  const statusDiv = document.getElementById('status');
  if (statusDiv) {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
  } else {
    console.log(`Status: ${message}`);
  }
}

function setupShoppingEventListeners() {
  document.getElementById('addShoppingItem').addEventListener('click', addShoppingItem);
  document.getElementById('clearCompleted').addEventListener('click', clearCompletedItems);
}

// Week utility functions (for future meal planning)
function getCurrentWeek() {
  const now = new Date();
  const year = now.getFullYear();
  const week = getWeekNumber(now);
  return `${year}-W${week.toString().padStart(2, '0')}`;
}

function getWeekNumber(date) {
  const firstJan = new Date(date.getFullYear(), 0, 1);
  const pastDaysOfYear = (date - firstJan) / 86400000;
  return Math.ceil((pastDaysOfYear + firstJan.getDay() + 1) / 7);
}

function getPreviousWeek(weekKey) {
  const [year, week] = weekKey.split('-W').map(Number);
  const date = new Date(year, 0, 1);
  date.setDate(date.getDate() + (week - 1) * 7 - 7);
  return getCurrentWeekFromDate(date);
}

function getNextWeek(weekKey) {
  const [year, week] = weekKey.split('-W').map(Number);
  const date = new Date(year, 0, 1);
  date.setDate(date.getDate() + (week - 1) * 7 + 7);
  return getCurrentWeekFromDate(date);
}

function getCurrentWeekFromDate(date) {
  const year = date.getFullYear();
  const week = getWeekNumber(date);
  return `${year}-W${week.toString().padStart(2, '0')}`;
}

// Placeholder functions for meal planning (inactive)
function updateWeekDisplay() {
  // Placeholder - meal planning not active
  console.log('Meal planning functionality is not active');
}

function isDayInPast(weekKey, dayIndex) {
  // Placeholder - meal planning not active
  return false;
}

function updateThisWeekButton() {
  // Placeholder - meal planning not active
  console.log('Meal planning functionality is not active');
}

function getLastSavedValue(week, day, person) {
  // Placeholder - meal planning not active
  return '';
}

function setLastSavedValue(week, day, person, value) {
  // Placeholder - meal planning not active
}

function initializeLastSavedData() {
  // Placeholder - meal planning not active
}

function findNextEditableCell(currentInput) {
  // Placeholder - meal planning not active
  return null;
}

function findNextCellDown(currentInput) {
  // Placeholder - meal planning not active
  return null;
}

// Placeholder functions for persons management (inactive)
async function loadPersons() {
  // Placeholder - persons management not active
  console.log('Persons management functionality is not active');
}

async function loadMealData() {
  // Placeholder - meal planning not active
  console.log('Meal planning functionality is not active');
}

async function saveMealData(silent = true) {
  // Placeholder - meal planning not active
  console.log('Meal planning functionality is not active');
}

function renderMealTable() {
  // Placeholder - meal planning not active
  console.log('Meal planning functionality is not active');
}

async function addPerson() {
  // Placeholder - persons management not active
  showStatus('Persons management functionality is not active', 'info');
}

// === ACTIVE SHOPPING LIST FUNCTIONALITY ===

async function loadShoppingItems() {
  try {
    const response = await fetch(`${API_BASE}/shopping-items`);
    if (response.ok) {
      shoppingItems = await response.json();
    } else {
      shoppingItems = [];
    }
    renderShoppingTable();
    showStatus('Ready!', 'success');
  } catch (error) {
    console.error('Failed to load shopping items:', error);
    shoppingItems = [];
    renderShoppingTable();
    showStatus('Failed to load shopping items', 'error');
  }
}

async function saveShoppingItem(item) {
  try {
    const response = await fetch(`${API_BASE}/shopping-items`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: item.name,
        inCart: item.checked || false
      })
    });
    if (!response.ok) {
      throw new Error('Failed to save shopping item');
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to save shopping item:', error);
    showStatus('Failed to save shopping item', 'error');
    throw error;
  }
}

function renderShoppingTable() {
  const tbody = document.getElementById('shoppingTableBody');
  if (!tbody) return;

  // Sort: unchecked first, checked last
  const sortedItems = [...shoppingItems].sort((a, b) => {
    if (a.checked && !b.checked) return 1;
    if (!a.checked && b.checked) return -1;
    return 0;
  });

  if (sortedItems.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="2" class="empty-state">
          No shopping items yet. Click "Add Item" to get started!
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = sortedItems.map((item, sortedIndex) => {
    // Find the original index in the unsorted array
    const originalIndex = shoppingItems.findIndex(originalItem => originalItem.id === item.id);
    return `
      <tr>
        <td>
          <input type="text"
                 class="shopping-item-input"
                 value="${escapeHtml(item.name)}"
                 data-index="${originalIndex}"
                 data-field="name">
        </td>
        <td style="text-align: center;">
          <input type="checkbox"
                 class="shopping-checkbox"
                 ${item.checked ? 'checked' : ''}
                 data-index="${originalIndex}"
                 data-field="checked">
        </td>
      </tr>
    `;
  }).join('');

  // Add event listeners to inputs
  tbody.querySelectorAll('.shopping-item-input').forEach(input => {
    input.addEventListener('blur', saveShoppingData);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        saveShoppingData();
        input.blur();
      }
    });
  });

  tbody.querySelectorAll('.shopping-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      saveShoppingData(e);
      renderShoppingTable(); // Re-sort after checking
    });
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

async function addShoppingItem() {
  const newItem = {
    id: Date.now(),
    name: '',
    checked: false
  };
  shoppingItems.push(newItem);
  renderShoppingTable();
  // Focus on the new item's name input
  const newInput = document.querySelector(`[data-index="${shoppingItems.length - 1}"][data-field="name"]`);
  if (newInput) {
    newInput.focus();
  }
  // No need to save empty item immediately - will save when user enters name
}

async function saveShoppingData(event) {
  if (event) {
    const index = parseInt(event.target.dataset.index);
    const field = event.target.dataset.field;
    let value;
    if (event.target.type === 'checkbox') {
      value = event.target.checked;
    } else {
      value = event.target.value;
    }
    shoppingItems[index][field] = value;

    // Only save if item has a name
    const item = shoppingItems[index];
    if (item.name && item.name.trim()) {
      try {
        await saveShoppingItem(item);
      } catch (error) {
        // Error already handled in saveShoppingItem
      }
    }
  }
}

async function clearCompletedItems() {
  const completedItems = shoppingItems.filter(item => item.checked);
  if (completedItems.length === 0) {
    showStatus('No completed items to clear', 'info');
    return;
  }
  if (confirm(`Clear ${completedItems.length} completed item(s)?`)) {
    shoppingItems = shoppingItems.filter(item => !item.checked);
    renderShoppingTable();

    // Persist changes to backend by saving the updated shopping items
    try {
      const response = await fetch(`${API_BASE}/shopping-items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(shoppingItems)
      });

      if (!response.ok) {
        throw new Error('Failed to persist cleared items');
      }

      showStatus(`Cleared ${completedItems.length} completed item(s)`, 'success');
    } catch (error) {
      console.error('Failed to persist cleared items:', error);
      showStatus('Items cleared locally but failed to save to server', 'error');
    }
  }
}
