	// End of file
// Global variables
// Auto-detect port from current URL, fallback to 5001
const currentPort = window.location.port || '5001';
const API_BASE = `http://localhost:${currentPort}/api`;
let currentUser = 'local-user'; // For local development
let currentWeek = getCurrentWeek();
let mealData = {};
let persons = [];
let lastSavedData = {}; // Track what was last saved to avoid unnecessary API calls
let groceryItems = [];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
	initializeApp();
});

async function initializeApp() {
	try {
		showStatus('Loading meal planner...', 'info');
		setupEventListeners();
		updateWeekDisplay();
        
		// Load persons first (this will render the table with empty meal data)
		await loadPersons();
        
		// Then load meal data (this will re-render with actual data)
		await loadMealData();
		await loadGroceryItems();
        
		showStatus('Ready!', 'success');
	} catch (error) {
		console.error('Failed to initialize app:', error);
		showStatus('Failed to load app. Check if server is running.', 'error');
	}
}

// Event listeners
function setupEventListeners() {
	document.getElementById('prevWeek').addEventListener('click', () => {
		currentWeek = getPreviousWeek(currentWeek);
		updateWeekDisplay();
		loadMealData();
	});
    
	document.getElementById('nextWeek').addEventListener('click', () => {
		currentWeek = getNextWeek(currentWeek);
		updateWeekDisplay();
		loadMealData();
	});
    
	document.getElementById('thisWeekBtn').addEventListener('click', () => {
		currentWeek = getCurrentWeek();
		updateWeekDisplay();
		loadMealData();
	});
    
	document.getElementById('addPersonBtn').addEventListener('click', addPerson);
	document.getElementById('loadBtn').addEventListener('click', async () => {
		try {
			showStatus('Reloading data...', 'info');
			await Promise.all([loadMealData(), loadPersons(), loadGroceryItems()]);
			showStatus('Data reloaded successfully!', 'success');
		} catch (error) {
			console.error('Failed to reload data:', error);
			showStatus('Failed to reload data', 'error');
		}
	});
    
	// Grocery list event listeners
	document.getElementById('addGroceryItem').addEventListener('click', addGroceryItem);
	document.getElementById('clearCompleted').addEventListener('click', clearCompletedItems);
}

// Week management
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
	// ...existing code...
}
