import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataLayer:
    """
    Extensible data layer that starts with JSON files but can be easily
    extended to support MongoDB Atlas and later Cosmos DB.
    """
    
    def __init__(self, data_dir: str = "data"):
        # If relative path, make it relative to project root (not backend/)
        if not os.path.isabs(data_dir):
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), data_dir)
        else:
            self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist - fail if unable to create"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create data directory '{self.data_dir}': {e}")
    
    def _get_file_path(self, filename: str) -> str:
        """Get full path for a data file"""
        return os.path.join(self.data_dir, f"{filename}.json")
    
    def _read_json_file(self, filename: str) -> Dict[str, Any]:
        """Read JSON file, return empty dict if file doesn't exist"""
        file_path = self._get_file_path(filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading {file_path}: {e}")
                return {}
        return {}
    
    def _write_json_file(self, filename: str, data: Dict[str, Any]) -> None:
        """Write data to JSON file - fail if unable to write"""
        file_path = self._get_file_path(filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            raise IOError(f"Failed to write {file_path}: {e}")
    
    # === Larder Liszt (Inventory) Methods ===
    def get_larder_items(self) -> List[Dict[str, Any]]:
        """Get all larder items"""
        data = self._read_json_file("larder_items")
        return data.get("items", [])
    
    def add_larder_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new larder item"""
        data = self._read_json_file("larder_items")
        items = data.get("items", [])
        
        # Create new item with ID and default values
        new_item = {
            "id": self._generate_id(),
            "name": item_data.get("name", "").strip(),
            "inStock": item_data.get("inStock", False),
            "createdAt": datetime.utcnow().isoformat()
        }
        
        if new_item["name"]:
            items.append(new_item)
            data = {
                "items": items,
                "lastUpdated": datetime.utcnow().isoformat()
            }
            
            self._write_json_file("larder_items", data)
            return {"success": True, "message": "Larder item added successfully", "item": new_item}
        else:
            return {"success": False, "message": "Item name is required"}

    # === Chopin Liszt (Shopping) Methods ===
    def get_shopping_items(self) -> List[Dict[str, Any]]:
        """Get all shopping items"""
        data = self._read_json_file("shopping_items")
        return data.get("items", [])
    
    def add_shopping_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new shopping item"""
        data = self._read_json_file("shopping_items")
        items = data.get("items", [])
        
        # Create new item with ID and default values
        new_item = {
            "id": self._generate_id(),
            "name": item_data.get("name", "").strip(),
            "inCart": item_data.get("inCart", False),
            "createdAt": datetime.utcnow().isoformat()
        }
        
        if new_item["name"]:
            items.append(new_item)
            data = {
                "items": items,
                "lastUpdated": datetime.utcnow().isoformat()
            }
            
            self._write_json_file("shopping_items", data)
            return {"success": True, "message": "Shopping item added successfully", "item": new_item}
        else:
            return {"success": False, "message": "Item name is required"}

    # === Meals Methods ===
    def get_meal_items(self) -> List[Dict[str, Any]]:
        """Get all meal items"""
        data = self._read_json_file("meal_items")
        return data.get("items", [])
    
    def add_meal_item(self, meal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new meal item"""
        data = self._read_json_file("meal_items")
        items = data.get("items", [])
        
        # Create new meal with ID and default values
        new_meal = {
            "id": self._generate_id(),
            "name": meal_data.get("name", "").strip(),
            "ingredients": meal_data.get("ingredients", "").strip(),
            "createdAt": datetime.utcnow().isoformat()
        }
        
        if new_meal["name"]:
            items.append(new_meal)
            data = {
                "items": items,
                "lastUpdated": datetime.utcnow().isoformat()
            }
            
            self._write_json_file("meal_items", data)
            return {"success": True, "message": "Meal added successfully", "item": new_meal}
        else:
            return {"success": False, "message": "Meal name is required"}


    def _generate_id(self) -> str:
        """Generate a unique ID using timestamp + random component to prevent collisions"""
        import random
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        random_suffix = random.randint(1000, 9999)
        return f"{timestamp}-{random_suffix}"


# Future: MongoDB Atlas Data Layer
class MongoDBDataLayer(DataLayer):
    """
    Future implementation for MongoDB Atlas
    This will replace the JSON file operations with MongoDB operations
    """
    
    def __init__(self, connection_string: str, database_name: str = "picky"):
        # TODO: Implement MongoDB connection
        # self.client = pymongo.MongoClient(connection_string)
        # self.db = self.client[database_name]
        super().__init__()
        print("MongoDB DataLayer not yet implemented")


# Future: Cosmos DB Data Layer  
class CosmosDBDataLayer(DataLayer):
    """
    Future implementation for Azure Cosmos DB
    This will replace the JSON file operations with Cosmos DB operations
    """
    
    def __init__(self, connection_string: str):
        # TODO: Implement Cosmos DB connection
        # self.client = CosmosClient.from_connection_string(connection_string)
        super().__init__()
        print("Cosmos DB DataLayer not yet implemented")
