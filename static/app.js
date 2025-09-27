// Grocery List Only Version
const API_BASE = `${window.location.origin}/api`;
let groceryItems = [];

document.addEventListener('DOMContentLoaded', function() {
    showStatus('Loading grocery list...', 'info');
    setupGroceryEventListeners();
    loadGroceryItems();
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

function setupGroceryEventListeners() {
    document.getElementById('addGroceryItem').addEventListener('click', addGroceryItem);
    document.getElementById('clearCompleted').addEventListener('click', clearCompletedItems);
}
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
    date.setDate(date.getDate() + (week - 1) * 7);
    date.setDate(date.getDate() - 7);
    const newYear = date.getFullYear();
    const newWeek = getWeekNumber(date);
    return `${newYear}-W${newWeek.toString().padStart(2, '0')}`;
}

function getNextWeek(weekKey) {
    const [year, week] = weekKey.split('-W').map(Number);
    const date = new Date(year, 0, 1);
    date.setDate(date.getDate() + (week - 1) * 7);
    date.setDate(date.getDate() + 7);
    const newYear = date.getFullYear();
    const newWeek = getWeekNumber(date);
    return `${newYear}-W${newWeek.toString().padStart(2, '0')}`;
}

function updateWeekDisplay() {
    const [year, week] = currentWeek.split('-W');
    const date = new Date(year, 0, 1);
    date.setDate(date.getDate() + (parseInt(week) - 1) * 7);
    
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - date.getDay() + 1); // Monday
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6); // Sunday
    
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    
    document.getElementById('currentWeek').textContent = 
        `${weekStart.toLocaleDateString('en-US', options)} - ${weekEnd.toLocaleDateString('en-US', options)}`;
    
    // Update "Go to this week" button based on current week
    updateThisWeekButton();
}

function isDayInPast(weekKey, dayIndex) {
    // Get the date for the specific day in the week
    const [year, week] = weekKey.split('-W').map(Number);
    const date = new Date(year, 0, 1);
    date.setDate(date.getDate() + (week - 1) * 7);
    
    // Get Monday of that week
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - date.getDay() + 1); // Monday
    
    // Get the specific day (0 = Monday, 1 = Tuesday, etc.)
    const dayDate = new Date(weekStart);
    dayDate.setDate(weekStart.getDate() + dayIndex);
    
    // Get today's date (start of day)
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    // Compare dates
    return dayDate < today;
}

function updateThisWeekButton() {
    const thisWeekBtn = document.getElementById('thisWeekBtn');
    const actualCurrentWeek = getCurrentWeek();
    
    if (currentWeek === actualCurrentWeek) {
        // We're viewing this week
        thisWeekBtn.textContent = 'This week';
        thisWeekBtn.disabled = true;
        thisWeekBtn.classList.add('disabled');
    } else {
        // We're viewing a different week
        thisWeekBtn.textContent = 'Go to this week';
        thisWeekBtn.disabled = false;
        thisWeekBtn.classList.remove('disabled');
    }
}

// Helper functions for tracking saved data
function getLastSavedValue(week, day, person) {
    return lastSavedData[week]?.[day]?.[person] || '';
}

function setLastSavedValue(week, day, person, value) {
    if (!lastSavedData[week]) {
        lastSavedData[week] = {};
    }
    if (!lastSavedData[week][day]) {
        lastSavedData[week][day] = {};
    }
    lastSavedData[week][day][person] = value;
}

function initializeLastSavedData() {
    // Initialize lastSavedData with current mealData
    lastSavedData = JSON.parse(JSON.stringify(mealData));
}

function findNextEditableCell(currentInput) {
    // Get all meal inputs in the table
    const allInputs = Array.from(document.querySelectorAll('.meal-input:not([disabled])'));
    const currentIndex = allInputs.indexOf(currentInput);
    
    // Return the next input, or the first one if we're at the end
    if (currentIndex >= 0 && currentIndex < allInputs.length - 1) {
        return allInputs[currentIndex + 1];
    } else if (allInputs.length > 0) {
        return allInputs[0]; // Wrap to beginning
    }
    
    return null;
}

function findNextCellDown(currentInput) {
    // Get the table row and cell index of current input
    const currentCell = currentInput.closest('td');
    const currentRow = currentInput.closest('tr');
    const currentCellIndex = Array.from(currentRow.children).indexOf(currentCell);
    
    // Find the next row (same column, next person)
    const tableBody = currentRow.closest('tbody');
    const allRows = Array.from(tableBody.children);
    const currentRowIndex = allRows.indexOf(currentRow);
    
    // Look for the next row in the same column
    for (let i = currentRowIndex + 1; i < allRows.length; i++) {
        const nextRow = allRows[i];
        const nextCell = nextRow.children[currentCellIndex];
        if (nextCell) {
            const nextInput = nextCell.querySelector('.meal-input:not([disabled])');
            if (nextInput) {
                return nextInput;
            }
        }
    }
    
    // If no next row found, go to top of next column
    const nextColumnIndex = currentCellIndex + 1;
    if (nextColumnIndex < currentRow.children.length) {
        const firstRow = allRows[0];
        const nextColumnCell = firstRow.children[nextColumnIndex];
        if (nextColumnCell) {
            const nextColumnInput = nextColumnCell.querySelector('.meal-input:not([disabled])');
            if (nextColumnInput) {
                return nextColumnInput;
            }
        }
    }
    
    // If no next column found, wrap to first column, first row
    if (allRows.length > 0) {
        const firstRow = allRows[0];
        const firstCell = firstRow.children[0];
        if (firstCell) {
            const firstInput = firstCell.querySelector('.meal-input:not([disabled])');
            if (firstInput) {
                return firstInput;
            }
        }
    }
    
    return null;
}

// Data management
async function loadPersons() {
    try {
        const response = await fetch(`${API_BASE}/persons`);
        if (response.ok) {
            persons = await response.json();
        } else {
            // Start with empty list
            persons = [];
        }
        // Re-render the table with updated persons
        renderMealTable();
    } catch (error) {
        console.error('Failed to load persons:', error);
        persons = [];
        // Still re-render to show empty state
        renderMealTable();
    }
}

async function loadMealData() {
    try {
        const response = await fetch(`${API_BASE}/meals/${currentUser}`);
        if (response.ok) {
            const data = await response.json();
            mealData = data.weekData || {};
        } else {
            mealData = {};
        }
        // Initialize tracking of what was last saved
        initializeLastSavedData();
        // Always render the table after loading meal data
        renderMealTable();
    } catch (error) {
        console.error('Failed to load meal data:', error);
        mealData = {};
        initializeLastSavedData();
        showStatus('Failed to load meal data', 'error');
        throw error; // Re-throw so reload button can catch it
    }
}

async function saveMealData(silent = true) {
    try {
        if (!silent) {
            showStatus('Saving...', 'info');
        }
        
        const response = await fetch(`${API_BASE}/meals/${currentUser}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                weekData: mealData
            })
        });
        
        if (response.ok) {
            if (!silent) {
                showStatus('Meal data saved successfully!', 'success');
            }
        } else {
            const error = await response.json();
            showStatus(`Failed to save: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Failed to save meal data:', error);
        showStatus('Failed to save meal data', 'error');
    }
}

function renderMealTable() {
    const tbody = document.getElementById('mealTableBody');
    tbody.innerHTML = '';
    
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    
    if (persons.length === 0) {
        // Show empty state
        const emptyRow = document.createElement('tr');
        const emptyCell = document.createElement('td');
        emptyCell.colSpan = 8;
        emptyCell.style.textAlign = 'center';
        emptyCell.style.padding = '40px';
        emptyCell.style.color = '#666';
        emptyCell.innerHTML = `
            <div style="font-size: 1.1rem; margin-bottom: 10px;">👥 No people added yet</div>
            <div style="font-size: 0.9rem;">Click "Add Person" to get started</div>
        `;
        emptyRow.appendChild(emptyCell);
        tbody.appendChild(emptyRow);
        return;
    }
    
    persons.forEach(person => {
        const row = document.createElement('tr');
        
        // Person name cell
        const nameCell = document.createElement('td');
        nameCell.className = 'person-name';
        nameCell.textContent = person;
        row.appendChild(nameCell);
        
        // Day cells
        days.forEach((day, dayIndex) => {
            const cell = document.createElement('td');
            const input = document.createElement('textarea');
            input.className = 'meal-input';
            input.rows = 2;
            
            // Check if this day is in the past
            const isPastDay = isDayInPast(currentWeek, dayIndex);
            
            if (isPastDay) {
                input.placeholder = `${day}`;
                input.disabled = true;
                input.classList.add('past-day');
            } else {
                input.placeholder = `Enter ${day}...`;
            }
            
            // Set current value
            const currentValue = mealData[currentWeek]?.[day]?.[person] || '';
            input.value = currentValue;
            
            // Only add event listeners for future days
            if (!isPastDay) {
                // Update data locally on change (no API call)
                input.addEventListener('input', (e) => {
                    if (!mealData[currentWeek]) {
                        mealData[currentWeek] = {};
                    }
                    if (!mealData[currentWeek][day]) {
                        mealData[currentWeek][day] = {};
                    }
                    mealData[currentWeek][day][person] = input.value;
                });

                // Save to API only on specific triggers and only if data changed
                const saveData = () => {
                    // Check if current data is different from what we last saved
                    const currentData = mealData[currentWeek]?.[day]?.[person] || '';
                    const lastSavedData = getLastSavedValue(currentWeek, day, person);
                    
                    if (currentData !== lastSavedData) {
                        setLastSavedValue(currentWeek, day, person, currentData);
                        saveMealData();
                    }
                };

                // Save on Enter key and move to next cell
                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault(); // Prevent newline in textarea
                        saveData();
                        
                        // Find next editable cell
                        const nextCell = findNextEditableCell(input);
                        if (nextCell) {
                            nextCell.focus();
                        }
                    }
                });

                // Save on Tab key and move down
                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Tab') {
                        e.preventDefault(); // Prevent default tab behavior
                        saveData();
                        
                        // Find next cell in the same column (down)
                        const nextCell = findNextCellDown(input);
                        if (nextCell) {
                            nextCell.focus();
                        }
                    }
                });

                // Save on focus away (blur)
                input.addEventListener('blur', () => {
                    saveData();
                });
            }
            
            cell.appendChild(input);
            row.appendChild(cell);
        });
        
        tbody.appendChild(row);
    });
}

async function addPerson() {
    const name = prompt('Enter person name:');
    if (name && name.trim() && !persons.includes(name.trim())) {
        try {
            const response = await fetch(`${API_BASE}/persons`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name.trim()
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                persons = result.persons || persons;
                renderMealTable();
                showStatus('Person added successfully!', 'success');
            } else {
                showStatus('Failed to add person', 'error');
            }
        } catch (error) {
            console.error('Failed to add person:', error);
            showStatus('Failed to add person', 'error');
        }
    } else if (name && name.trim()) {
        showStatus('Person already exists', 'error');
    }
}

// --- Grocery List Management ---
async function loadGroceryItems() {
    try {
        const response = await fetch(`${API_BASE}/grocery-items`);
        if (response.ok) {
            groceryItems = await response.json();
        } else {
            groceryItems = [];
        }
        renderGroceryTable();
        showStatus('Ready!', 'success');
    } catch (error) {
        console.error('Failed to load grocery items:', error);
        groceryItems = [];
        renderGroceryTable();
        showStatus('Failed to load grocery items', 'error');
    }
}

async function saveGroceryItems() {
    try {
        const response = await fetch(`${API_BASE}/grocery-items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(groceryItems)
        });
        if (!response.ok) {
            throw new Error('Failed to save grocery items');
        }
    } catch (error) {
        console.error('Failed to save grocery items:', error);
        showStatus('Failed to save grocery items', 'error');
    }
}

function renderGroceryTable() {
    const tbody = document.getElementById('groceryTableBody');
    if (!tbody) return;

    // Sort: unchecked first, checked last
    const sortedItems = [...groceryItems].sort((a, b) => {
        if (a.checked && !b.checked) return 1;
        if (!a.checked && b.checked) return -1;
        return 0;
    });

    if (sortedItems.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="2" class="empty-state">
                    No grocery items yet. Click "Add Item" to get started!
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = sortedItems.map((item, index) => `
        <tr>
            <td>
                <input type="text" 
                       class="grocery-item-input" 
                       value="${escapeHtml(item.name)}" 
                       data-index="${index}" 
                       data-field="name">
            </td>
            <td style="text-align: center;">
                <input type="checkbox" 
                       class="grocery-checkbox" 
                       ${item.checked ? 'checked' : ''} 
                       data-index="${index}" 
                       data-field="checked">
            </td>
        </tr>
    `).join('');

    // Add event listeners to inputs
    tbody.querySelectorAll('.grocery-item-input').forEach(input => {
        input.addEventListener('blur', saveGroceryData);
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                saveGroceryData();
                input.blur();
            }
        });
    });

    tbody.querySelectorAll('.grocery-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            saveGroceryData(e);
            renderGroceryTable(); // Re-sort after checking
        });
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function addGroceryItem() {
    const newItem = {
        id: Date.now(),
        name: '',
        checked: false
    };
    groceryItems.push(newItem);
    renderGroceryTable();
    // Focus on the new item's name input
    const newInput = document.querySelector(`[data-index="${groceryItems.length - 1}"][data-field="name"]`);
    if (newInput) {
        newInput.focus();
    }
    await saveGroceryItems();
}

async function saveGroceryData(event) {
    if (event) {
        const index = parseInt(event.target.dataset.index);
        const field = event.target.dataset.field;
        let value;
        if (event.target.type === 'checkbox') {
            value = event.target.checked;
        } else {
            value = event.target.value;
        }
        groceryItems[index][field] = value;
    }
    await saveGroceryItems();
}

async function clearCompletedItems() {
    const completedItems = groceryItems.filter(item => item.checked);
    if (completedItems.length === 0) {
        showStatus('No completed items to clear', 'info');
        return;
    }
    if (confirm(`Clear ${completedItems.length} completed item(s)?`)) {
        groceryItems = groceryItems.filter(item => !item.checked);
        renderGroceryTable();
        await saveGroceryItems();
        showStatus(`Cleared ${completedItems.length} completed item(s)`, 'success');
    }
}
