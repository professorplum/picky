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
        self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
    
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
    
    def _write_json_file(self, filename: str, data: Dict[str, Any]) -> bool:
        """Write data to JSON file"""
        try:
            file_path = self._get_file_path(filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    # Meal planner methods removed
    def get_persons(self) -> List[str]:
        """Get list of persons"""
        data = self._read_json_file("persons")
        return data.get("persons", [])
    
    def add_person(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new person to the list"""
        data = self._read_json_file("persons")
        persons = data.get("persons", [])
        
        person_name = person_data.get("name", "").strip()
        if person_name and person_name not in persons:
            persons.append(person_name)
            data["persons"] = persons
            data["lastUpdated"] = datetime.utcnow().isoformat()
            
            if self._write_json_file("persons", data):
                return {"success": True, "message": "Person added successfully", "persons": persons}
            else:
                return {"success": False, "message": "Failed to add person"}
        else:
            return {"success": False, "message": "Person already exists or invalid name"}
    
    def _get_default_week_structure(self) -> Dict[str, Any]:
        """Return default week structure with empty meals"""
        current_week = self._get_current_week_key()
        return {
            "weekData": {
                current_week: {
                    "Monday": "",
                    "Tuesday": "",
                    "Wednesday": "",
                    "Thursday": "",
                    "Friday": "",
                    "Saturday": "",
                    "Sunday": ""
                }
            }
        }
    
    def _get_current_week_key(self) -> str:
        """Get current week key in format YYYY-W##"""
        now = datetime.now()
        year, week, _ = now.isocalendar()
        return f"{year}-W{week:02d}"
    
    def get_grocery_items(self) -> List[Dict[str, Any]]:
        """Get all grocery items"""
        data = self._read_json_file("grocery_items")
        return data.get("items", [])
    
    def save_grocery_items(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Save grocery items"""
        data = {
            "items": items,
            "lastUpdated": datetime.utcnow().isoformat()
        }
        
        if self._write_json_file("grocery_items", data):
            return {"success": True, "message": "Grocery items saved successfully"}
        else:
            return {"success": False, "message": "Failed to save grocery items"}


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
