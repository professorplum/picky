// Shopping List Application - Simplified Version
const API_BASE = `${window.location.origin}/api`;
let shoppingItems = [];
let larderItems = [];
let mealItems = [];

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

  showStatus('Loading...', 'info');
  setupShoppingEventListeners();
  setupLarderEventListeners();
  setupMealsEventListeners();
  loadShoppingItems();
  loadLarderItems();
  loadMealItems();
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

function setupLarderEventListeners() {
  document.getElementById('addLarderItem').addEventListener('click', addLarderItem);
  document.getElementById('clearReorder').addEventListener('click', clearReorderItems);
}

function setupMealsEventListeners() {
  document.getElementById('addMealItem').addEventListener('click', addMealItem);
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
    const items = response.ok ? await response.json() : [];
    // Mark all loaded items as saved
    shoppingItems = items.map(item => ({ ...item, saved: true }));
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
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: item.name,
        inCart: item.checked || false
      })
    });
    if (!response.ok) throw new Error('Failed to save shopping item');
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
    checked: false,
    saved: false
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
        const savedItem = await saveShoppingItem(item);
        // Update the item with server data and mark as saved
        shoppingItems[index] = { ...savedItem, saved: true };
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

// === LARDER FUNCTIONALITY ===

async function loadLarderItems() {
  try {
    const response = await fetch(`${API_BASE}/larder-items`);
    const items = response.ok ? await response.json() : [];
    // Mark all loaded items as saved
    larderItems = items.map(item => ({ ...item, saved: true }));
    renderLarderTable();
  } catch (error) {
    console.error('Failed to load larder items:', error);
    larderItems = [];
    renderLarderTable();
    showStatus('Failed to load larder items', 'error');
  }
}

async function saveLarderItem(item) {
  try {
    const response = await fetch(`${API_BASE}/larder-items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: item.name,
        reorder: item.reorder || false
      })
    });
    if (!response.ok) throw new Error('Failed to save larder item');
    return await response.json();
  } catch (error) {
    console.error('Failed to save larder item:', error);
    showStatus('Failed to save larder item', 'error');
    throw error;
  }
}

function renderLarderTable() {
  const tbody = document.getElementById('pantryTableBody');
  if (!tbody) return;

  // Sort: items not needing reorder first, items needing reorder last
  const sortedItems = [...larderItems].sort((a, b) => {
    if (a.reorder && !b.reorder) return 1;
    if (!a.reorder && b.reorder) return -1;
    return 0;
  });

  if (sortedItems.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="2" class="empty-state">
          No larder items yet. Click "Add Item" to get started!
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = sortedItems.map((item, sortedIndex) => {
    // Find the original index in the unsorted array
    const originalIndex = larderItems.findIndex(originalItem => originalItem.id === item.id);
    return `
      <tr>
        <td>
          <input type="text"
                 class="larder-item-input"
                 value="${escapeHtml(item.name)}"
                 data-index="${originalIndex}"
                 data-field="name">
        </td>
        <td style="text-align: center;">
          <input type="checkbox"
                 class="larder-checkbox"
                 ${item.reorder ? 'checked' : ''}
                 data-index="${originalIndex}"
                 data-field="reorder">
        </td>
      </tr>
    `;
  }).join('');

  // Add event listeners to inputs
  tbody.querySelectorAll('.larder-item-input').forEach(input => {
    input.addEventListener('blur', saveLarderData);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        saveLarderData();
        input.blur();
      }
    });
  });

  tbody.querySelectorAll('.larder-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      saveLarderData(e);
      renderLarderTable(); // Re-sort after checking
    });
  });
}

async function addLarderItem() {
  const newItem = {
    id: crypto.randomUUID(),
    name: '',
    reorder: false,
    saved: false
  };
  larderItems.push(newItem);
  renderLarderTable();
  // Focus on the new item's name input
  const newInput = document.querySelector(`[data-index="${larderItems.length - 1}"][data-field="name"]`);
  if (newInput) {
    newInput.focus();
  }
  // No need to save empty item immediately - will save when user enters name
}

async function saveLarderData(event) {
  if (event) {
    const index = parseInt(event.target.dataset.index);
    const field = event.target.dataset.field;
    let value;
    if (event.target.type === 'checkbox') {
      value = event.target.checked;
    } else {
      value = event.target.value;
    }
    larderItems[index][field] = value;

    // Only save if item has a name
    const item = larderItems[index];
    if (item.name && item.name.trim()) {
      try {
        const savedItem = await saveLarderItem(item);
        // Update the item with server data and mark as saved
        larderItems[index] = { ...savedItem, saved: true };
      } catch (error) {
        // Error already handled in saveLarderItem
      }
    }
  }
}

async function clearReorderItems() {
  const reorderItems = larderItems.filter(item => item.reorder);
  if (reorderItems.length === 0) {
    showStatus('No items marked for reorder to clear', 'info');
    return;
  }
  if (confirm(`Clear ${reorderItems.length} item(s) marked for reorder?`)) {
    larderItems = larderItems.filter(item => !item.reorder);
    renderLarderTable();
    showStatus(`Cleared ${reorderItems.length} reorder item(s)`, 'success');
  }
}

// === MEALS FUNCTIONALITY ===

async function loadMealItems() {
  try {
    const response = await fetch(`${API_BASE}/meal-items`);
    const items = response.ok ? await response.json() : [];
    // Mark all loaded items as saved
    mealItems = items.map(item => ({ ...item, saved: true }));
    renderMealTable();
  } catch (error) {
    console.error('Failed to load meal items:', error);
    mealItems = [];
    renderMealTable();
    showStatus('Failed to load meal items', 'error');
  }
}

async function saveMealItem(item) {
  try {
    const response = await fetch(`${API_BASE}/meal-items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: item.name,
        ingredients: item.ingredients || ''
      })
    });
    if (!response.ok) throw new Error('Failed to save meal item');
    return await response.json();
  } catch (error) {
    console.error('Failed to save meal item:', error);
    showStatus('Failed to save meal item', 'error');
    throw error;
  }
}

function renderMealTable() {
  const tbody = document.getElementById('mealsTableBody');
  if (!tbody) return;

  if (mealItems.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="3" class="empty-state">
          No meals yet. Click "Add Meal" to get started!
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = mealItems.map((item, index) => {
    return `
      <tr>
        <td>
          <input type="text"
                 class="meal-name-input"
                 value="${escapeHtml(item.name)}"
                 data-index="${index}"
                 data-field="name">
        </td>
        <td>
          <input type="text"
                 class="meal-ingredients-input"
                 value="${escapeHtml(item.ingredients)}"
                 data-index="${index}"
                 data-field="ingredients"
                 placeholder="Enter ingredients...">
        </td>
        <td style="text-align: center;">
          <button class="btn btn-small btn-danger" onclick="deleteMealItem(${index})">Delete</button>
        </td>
      </tr>
    `;
  }).join('');

  // Add event listeners to inputs
  tbody.querySelectorAll('.meal-name-input').forEach(input => {
    input.addEventListener('blur', saveMealData);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        saveMealData();
        input.blur();
      }
    });
  });

  tbody.querySelectorAll('.meal-ingredients-input').forEach(input => {
    input.addEventListener('blur', saveMealData);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        saveMealData();
        input.blur();
      }
    });
  });
}

async function addMealItem() {
  const newItem = {
    id: Date.now(),
    name: '',
    ingredients: '',
    saved: false
  };
  mealItems.push(newItem);
  renderMealTable();
  // Focus on the new meal's name input
  const newInput = document.querySelector(`[data-index="${mealItems.length - 1}"][data-field="name"]`);
  if (newInput) {
    newInput.focus();
  }
  // No need to save empty item immediately - will save when user enters name
}

async function saveMealData(event) {
  if (event) {
    const index = parseInt(event.target.dataset.index);
    const field = event.target.dataset.field;
    const value = event.target.value;
    mealItems[index][field] = value;

    // Only save if meal has a name
    const item = mealItems[index];
    if (item.name && item.name.trim()) {
      try {
        const savedItem = await saveMealItem(item);
        // Update the item with server data and mark as saved
        mealItems[index] = { ...savedItem, saved: true };
      } catch (error) {
        // Error already handled in saveMealItem
      }
    }
  }
}

async function deleteMealItem(index) {
  const item = mealItems[index];
  if (confirm(`Delete meal "${item.name}"?`)) {
    mealItems.splice(index, 1);
    renderMealTable();
    showStatus('Meal deleted', 'success');
    
    // If the item was saved to the server, delete it there too
    if (item.saved && item.id) {
      try {
        const response = await fetch(`${API_BASE}/meal-items/${item.id}`, {
          method: 'DELETE'
        });
        if (!response.ok) {
          throw new Error('Failed to delete meal from server');
        }
      } catch (error) {
        console.error('Failed to delete meal from server:', error);
        showStatus('Meal deleted locally but failed to delete from server', 'error');
      }
    }
  }
}
