import { useState, useEffect } from 'react';

const API_BASE = `${window.location.origin}/api`;

export function usePicky() {
  const [shoppingItems, setShoppingItems] = useState([]);
  const [larderItems, setLarderItems] = useState([]);
  const [mealItems, setMealItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchAllData() {
      try {
        const [shopping, larder, meals] = await Promise.all([
          fetch(`${API_BASE}/shopping-items`).then((res) => res.json()),
          fetch(`${API_BASE}/larder-items`).then((res) => res.json()),
          fetch(`${API_BASE}/meal-items`).then((res) => res.json()),
        ]);
        setShoppingItems(shopping);
        setLarderItems(larder);
        setMealItems(meals);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }
    fetchAllData();
  }, []);

  async function addShoppingItem(name) {
    const newItem = { name, inCart: false };
    const response = await fetch(`${API_BASE}/shopping-items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newItem),
    });
    const savedItem = await response.json();
    setShoppingItems([...shoppingItems, savedItem]);
  }

  async function addLarderItem(name) {
    const newItem = { name, reorder: false };
    const response = await fetch(`${API_BASE}/larder-items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newItem),
    });
    const savedItem = await response.json();
    setLarderItems([...larderItems, savedItem]);
  }

  async function addMealItem(name, ingredients) {
    const newItem = { name, ingredients };
    const response = await fetch(`${API_BASE}/meal-items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newItem),
    });
    const savedItem = await response.json();
    setMealItems([...mealItems, savedItem]);
  }

  async function updateShoppingItem(id, updates) {
    const item = shoppingItems.find((i) => i.id === id);
    const updatedItem = { ...item, ...updates };
    const response = await fetch(`${API_BASE}/shopping-items/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedItem),
    });
    const savedItem = await response.json();
    setShoppingItems(
      shoppingItems.map((i) => (i.id === id ? savedItem : i)),
    );
  }

  async function updateLarderItem(id, updates) {
    const item = larderItems.find((i) => i.id === id);
    const updatedItem = { ...item, ...updates };
    const response = await fetch(`${API_BASE}/larder-items/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedItem),
    });
    const savedItem = await response.json();
    setLarderItems(larderItems.map((i) => (i.id === id ? savedItem : i)));
  }

  async function updateMealItem(id, updates) {
    const item = mealItems.find((i) => i.id === id);
    const updatedItem = { ...item, ...updates };
    const response = await fetch(`${API_BASE}/meal-items/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedItem),
    });
    const savedItem = await response.json();
    setMealItems(mealItems.map((i) => (i.id === id ? savedItem : i)));
  }

  async function deleteShoppingItem(id) {
    await fetch(`${API_BASE}/shopping-items/${id}`, { method: 'DELETE' });
    setShoppingItems(shoppingItems.filter((i) => i.id !== id));
  }

  async function deleteLarderItem(id) {
    await fetch(`${API_BASE}/larder-items/${id}`, { method: 'DELETE' });
    setLarderItems(larderItems.filter((i) => i.id !== id));
  }

  async function deleteMealItem(id) {
    await fetch(`${API_BASE}/meal-items/${id}`, { method: 'DELETE' });
    setMealItems(mealItems.filter((i) => i.id !== id));
  }

  return {
    shoppingItems,
    larderItems,
    mealItems,
    loading,
    error,
    addShoppingItem,
    addLarderItem,
    addMealItem,
    updateShoppingItem,
    updateLarderItem,
    updateMealItem,
    deleteShoppingItem,
    deleteLarderItem,
    deleteMealItem,
  };
}
