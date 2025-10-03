import { useState } from 'react';

function MealPlanner({ items, onAddItem, onUpdateItem, onDeleteItem }) {
  const [newItemName, setNewItemName] = useState('');
  const [newItemIngredients, setNewItemIngredients] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newItemName.trim()) return;
    onAddItem(newItemName, newItemIngredients);
    setNewItemName('');
    setNewItemIngredients('');
  };

  return (
    <section className="dashboard-section meals-section">
      <h2>Meals</h2>
      <div className="section-controls">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={newItemName}
            onChange={(e) => setNewItemName(e.target.value)}
            placeholder="New meal name..."
          />
          <input
            type="text"
            value={newItemIngredients}
            onChange={(e) => setNewItemIngredients(e.target.value)}
            placeholder="Ingredients..."
          />
          <button className="btn" type="submit">
            Add Meal
          </button>
        </form>
      </div>
      <table className="section-table">
        <thead>
          <tr>
            <th>Meal</th>
            <th>Ingredients</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {items && items.length > 0 ? (
            items.map((item) => (
              <tr key={item.id}>
                <td>
                  <input
                    type="text"
                    value={item.name}
                    onChange={(e) =>
                      onUpdateItem(item.id, { name: e.target.value })
                    }
                  />
                </td>
                <td>
                  <input
                    type="text"
                    value={item.ingredients}
                    onChange={(e) =>
                      onUpdateItem(item.id, {
                        ingredients: e.target.value,
                      })
                    }
                  />
                </td>
                <td style={{ textAlign: 'center' }}>
                  <button
                    className="btn btn-small btn-danger"
                    onClick={() => onDeleteItem(item.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr className="empty-state">
              <td colSpan="3" className="empty-message">
                No meals yet
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </section>
  );
}

export default MealPlanner;
