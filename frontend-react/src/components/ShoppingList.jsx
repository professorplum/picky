import { useState } from 'react';

function ShoppingList({ items, onAddItem, onUpdateItem, onDeleteItem }) {
  const [newItemName, setNewItemName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newItemName.trim()) return;
    onAddItem(newItemName);
    setNewItemName('');
  };

  return (
    <section className="dashboard-section shopping-section">
      <h2>Chopin Liszt</h2>
      <div className="section-controls">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={newItemName}
            onChange={(e) => setNewItemName(e.target.value)}
            placeholder="New shopping item..."
          />
          <button className="btn" type="submit">
            Add Item
          </button>
        </form>
        <button className="btn">Clear Completed</button>
      </div>
      <table className="section-table">
        <thead>
          <tr>
            <th>Item</th>
            <th>In Cart</th>
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
                <td style={{ textAlign: 'center' }}>
                  <input
                    type="checkbox"
                    checked={item.inCart}
                    onChange={(e) =>
                      onUpdateItem(item.id, { inCart: e.target.checked })
                    }
                  />
                </td>
                <td>
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
              <td className="empty-message">No items yet</td>
              <td></td>
            </tr>
          )}
        </tbody>
      </table>
    </section>
  );
}

export default ShoppingList;
