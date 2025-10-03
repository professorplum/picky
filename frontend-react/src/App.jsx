import LarderList from './components/LarderList';
import ShoppingList from './components/ShoppingList';
import MealPlanner from './components/MealPlanner';
import { usePicky } from './api/usePicky';

function App() {
  const currentYear = new Date().getFullYear();
  const {
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
  } = usePicky();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className="container">
      <header>
        <h1>🍽️ Picky</h1>
        <div className="user-info">
          <span>Local User</span>
        </div>
      </header>

      <main className="dashboard">
        <div className="dashboard-top">
          <LarderList
            items={larderItems}
            onAddItem={addLarderItem}
            onUpdateItem={updateLarderItem}
            onDeleteItem={deleteLarderItem}
          />
          <ShoppingList
            items={shoppingItems}
            onAddItem={addShoppingItem}
            onUpdateItem={updateShoppingItem}
            onDeleteItem={deleteShoppingItem}
          />
        </div>
        <MealPlanner
          items={mealItems}
          onAddItem={addMealItem}
          onUpdateItem={updateMealItem}
          onDeleteItem={deleteMealItem}
        />
      </main>

      <footer>
        <p>&copy; {currentYear} Plum Industries</p>
      </footer>
    </div>
  );
}

export default App;
