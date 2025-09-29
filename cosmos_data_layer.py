"""
Cosmos DB Data Layer for Picky Meal Planner
Implements the same interface as DataLayer but uses Azure Cosmos DB for storage
"""
import ssl
import urllib3
from datetime import datetime
from typing import Dict, List, Any, Optional
from azure.cosmos import CosmosClient, PartitionKey, exceptions


class CosmosDataLayer:
    """
    Cosmos DB implementation of the data layer.
    Provides the same interface as DataLayer but stores data in Cosmos DB.
    """
    
    def __init__(self, endpoint: str, key: str, database_name: str):
        """
        Initialize Cosmos DB connection
        
        Args:
            endpoint: Cosmos DB endpoint URL
            key: Cosmos DB primary key
            database_name: Name of the database to use
        """
        self.endpoint = endpoint
        self.key = key
        self.database_name = database_name
        
        # Handle local emulator SSL certificate issues
        self._setup_ssl_for_emulator()
        
        # Initialize Cosmos client
        self.client = CosmosClient(self.endpoint, self.key)
        
        # Get or create database
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        
        # Initialize containers
        self._setup_containers()
    
    def _setup_ssl_for_emulator(self):
        """
        Configure SSL settings for local Cosmos DB emulator
        The emulator uses self-signed certificates which need special handling
        """
        if "localhost" in self.endpoint or "127.0.0.1" in self.endpoint:
            # Disable SSL warnings for local emulator
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            # Create unverified SSL context for emulator
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
    
    def _setup_containers(self):
        """
        Create containers (collections) for each data type if they don't exist
        Using flexible /id partition key for all containers
        """
        # Container configurations with flexible partition keys
        containers_config = {
            "grocery_items": "/id",      # Shopping list items (inCart)
            "inventory_items": "/id",    # Larder/inventory items (reorder) 
            "meal_items": "/id",         # Future meal items
            "persons": "/id"             # Person management
        }
        
        self.containers = {}
        
        for container_name, partition_key in containers_config.items():
            try:
                container = self.database.create_container_if_not_exists(
                    id=container_name,
                    partition_key=PartitionKey(path=partition_key),
                    offer_throughput=400  # Minimum throughput for development
                )
                self.containers[container_name] = container
                print(f"✅ Container '{container_name}' ready")
            except exceptions.CosmosHttpResponseError as e:
                print(f"❌ Error setting up container '{container_name}': {e}")
                raise
    
    def _generate_id(self) -> str:
        """Generate a unique ID using timestamp + random component to prevent collisions"""
        import random
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        random_suffix = random.randint(1000, 9999)
        return f"{timestamp}-{random_suffix}"
    
    # === Inventory Items (Larder) Methods ===
    def get_larder_items(self) -> List[Dict[str, Any]]:
        """Get all inventory items from Cosmos DB"""
        try:
            container = self.containers["inventory_items"]
            items = list(container.read_all_items())
            
            # Remove Cosmos DB metadata fields for clean response
            clean_items = []
            for item in items:
                clean_item = {k: v for k, v in item.items() 
                             if not k.startswith('_') and k != 'ttl'}
                clean_items.append(clean_item)
            
            return clean_items
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error getting inventory items: {e}")
            return []
    
    def add_larder_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new inventory item to Cosmos DB"""
        try:
            container = self.containers["inventory_items"]
            
            # Create new item matching current JSON structure
            new_item = {
                "id": self._generate_id(),
                "name": item_data.get("name", "").strip(),
                "reorder": item_data.get("reorder", False),
                "createdAt": datetime.utcnow().isoformat()
            }
            
            if new_item["name"]:
                # Insert item into Cosmos DB
                created_item = container.create_item(body=new_item)
                
                # Remove Cosmos metadata for response
                clean_item = {k: v for k, v in created_item.items() 
                             if not k.startswith('_') and k != 'ttl'}
                
                return {
                    "success": True, 
                    "message": "Inventory item added successfully", 
                    "item": clean_item
                }
            else:
                return {"success": False, "message": "Item name is required"}
                
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error adding inventory item: {e}")
            return {"success": False, "message": f"Failed to add inventory item: {str(e)}"}
    
    # === Grocery Items (Shopping) Methods ===
    def get_shopping_items(self) -> List[Dict[str, Any]]:
        """Get all grocery items from Cosmos DB"""
        try:
            container = self.containers["grocery_items"]
            items = list(container.read_all_items())
            
            # Remove Cosmos DB metadata fields for clean response
            clean_items = []
            for item in items:
                clean_item = {k: v for k, v in item.items() 
                             if not k.startswith('_') and k != 'ttl'}
                clean_items.append(clean_item)
            
            return clean_items
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error getting grocery items: {e}")
            return []
    
    def add_shopping_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new grocery item to Cosmos DB"""
        try:
            container = self.containers["grocery_items"]
            
            # Create new item matching current JSON structure
            new_item = {
                "id": self._generate_id(),
                "name": item_data.get("name", "").strip(),
                "inCart": item_data.get("inCart", False),
                "createdAt": datetime.utcnow().isoformat()
            }
            
            if new_item["name"]:
                # Insert item into Cosmos DB
                created_item = container.create_item(body=new_item)
                
                # Remove Cosmos metadata for response
                clean_item = {k: v for k, v in created_item.items() 
                             if not k.startswith('_') and k != 'ttl'}
                
                return {
                    "success": True, 
                    "message": "Grocery item added successfully", 
                    "item": clean_item
                }
            else:
                return {"success": False, "message": "Item name is required"}
                
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error adding grocery item: {e}")
            return {"success": False, "message": f"Failed to add grocery item: {str(e)}"}
    
    # === Meals Methods ===
    def get_meal_items(self) -> List[Dict[str, Any]]:
        """Get all meal items from Cosmos DB"""
        try:
            container = self.containers["meal_items"]
            items = list(container.read_all_items())
            
            # Remove Cosmos DB metadata fields for clean response
            clean_items = []
            for item in items:
                clean_item = {k: v for k, v in item.items() 
                             if not k.startswith('_') and k != 'ttl'}
                clean_items.append(clean_item)
            
            return clean_items
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error getting meal items: {e}")
            return []
    
    def add_meal_item(self, meal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new meal item to Cosmos DB"""
        try:
            container = self.containers["meal_items"]
            
            # Create new meal with ID and default values
            new_meal = {
                "id": self._generate_id(),
                "name": meal_data.get("name", "").strip(),
                "ingredients": meal_data.get("ingredients", "").strip(),
                "createdAt": datetime.utcnow().isoformat()
            }
            
            if new_meal["name"]:
                # Insert meal into Cosmos DB
                created_meal = container.create_item(body=new_meal)
                
                # Remove Cosmos metadata for response
                clean_meal = {k: v for k, v in created_meal.items() 
                             if not k.startswith('_') and k != 'ttl'}
                
                return {
                    "success": True, 
                    "message": "Meal added successfully", 
                    "item": clean_meal
                }
            else:
                return {"success": False, "message": "Meal name is required"}
                
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error adding meal item: {e}")
            return {"success": False, "message": f"Failed to add meal: {str(e)}"}
    
    # === Update Operations ===
    def update_grocery_item(self, item_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a grocery item in Cosmos DB"""
        try:
            container = self.containers["grocery_items"]
            
            # Read existing item
            existing_item = container.read_item(item=item_id, partition_key=item_id)
            
            # Apply updates
            for key, value in updates.items():
                if key not in ['id']:  # Don't allow ID changes
                    existing_item[key] = value
            
            existing_item['updatedAt'] = datetime.utcnow().isoformat()
            
            # Replace item
            updated_item = container.replace_item(item=existing_item, body=existing_item)
            
            # Clean response
            clean_item = {k: v for k, v in updated_item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {
                "success": True,
                "message": "Grocery item updated successfully",
                "item": clean_item
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Grocery item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error updating grocery item: {e}")
            return {"success": False, "message": f"Failed to update grocery item: {str(e)}"}
    
    def update_inventory_item(self, item_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an inventory item in Cosmos DB"""
        try:
            container = self.containers["inventory_items"]
            
            # Read existing item
            existing_item = container.read_item(item=item_id, partition_key=item_id)
            
            # Apply updates
            for key, value in updates.items():
                if key not in ['id']:  # Don't allow ID changes
                    existing_item[key] = value
            
            existing_item['updatedAt'] = datetime.utcnow().isoformat()
            
            # Replace item
            updated_item = container.replace_item(item=existing_item, body=existing_item)
            
            # Clean response
            clean_item = {k: v for k, v in updated_item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {
                "success": True,
                "message": "Inventory item updated successfully",
                "item": clean_item
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Inventory item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error updating inventory item: {e}")
            return {"success": False, "message": f"Failed to update inventory item: {str(e)}"}
    
    def update_meal_item(self, item_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a meal item in Cosmos DB"""
        try:
            container = self.containers["meal_items"]
            
            # Read existing item
            existing_item = container.read_item(item=item_id, partition_key=item_id)
            
            # Apply updates
            for key, value in updates.items():
                if key not in ['id']:  # Don't allow ID changes
                    existing_item[key] = value
            
            existing_item['updatedAt'] = datetime.utcnow().isoformat()
            
            # Replace item
            updated_item = container.replace_item(item=existing_item, body=existing_item)
            
            # Clean response
            clean_item = {k: v for k, v in updated_item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {
                "success": True,
                "message": "Meal item updated successfully",
                "item": clean_item
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Meal item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error updating meal item: {e}")
            return {"success": False, "message": f"Failed to update meal item: {str(e)}"}
    
    # === Delete Operations ===
    def delete_grocery_item(self, item_id: str) -> Dict[str, Any]:
        """Delete a grocery item from Cosmos DB"""
        try:
            container = self.containers["grocery_items"]
            container.delete_item(item=item_id, partition_key=item_id)
            
            return {
                "success": True,
                "message": "Grocery item deleted successfully"
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Grocery item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error deleting grocery item: {e}")
            return {"success": False, "message": f"Failed to delete grocery item: {str(e)}"}
    
    def delete_inventory_item(self, item_id: str) -> Dict[str, Any]:
        """Delete an inventory item from Cosmos DB"""
        try:
            container = self.containers["inventory_items"]
            container.delete_item(item=item_id, partition_key=item_id)
            
            return {
                "success": True,
                "message": "Inventory item deleted successfully"
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Inventory item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error deleting inventory item: {e}")
            return {"success": False, "message": f"Failed to delete inventory item: {str(e)}"}
    
    def delete_meal_item(self, item_id: str) -> Dict[str, Any]:
        """Delete a meal item from Cosmos DB"""
        try:
            container = self.containers["meal_items"]
            container.delete_item(item=item_id, partition_key=item_id)
            
            return {
                "success": True,
                "message": "Meal item deleted successfully"
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Meal item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error deleting meal item: {e}")
            return {"success": False, "message": f"Failed to delete meal item: {str(e)}"}
    
    # === Get Single Item Operations ===
    def get_grocery_item(self, item_id: str) -> Dict[str, Any]:
        """Get a single grocery item by ID"""
        try:
            container = self.containers["grocery_items"]
            item = container.read_item(item=item_id, partition_key=item_id)
            
            # Clean response
            clean_item = {k: v for k, v in item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {"success": True, "item": clean_item}
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Grocery item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error getting grocery item: {e}")
            return {"success": False, "message": f"Failed to get grocery item: {str(e)}"}
    
    def get_inventory_item(self, item_id: str) -> Dict[str, Any]:
        """Get a single inventory item by ID"""
        try:
            container = self.containers["inventory_items"]
            item = container.read_item(item=item_id, partition_key=item_id)
            
            # Clean response
            clean_item = {k: v for k, v in item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {"success": True, "item": clean_item}
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Inventory item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error getting inventory item: {e}")
            return {"success": False, "message": f"Failed to get inventory item: {str(e)}"}
    
    def get_meal_item(self, item_id: str) -> Dict[str, Any]:
        """Get a single meal item by ID"""
        try:
            container = self.containers["meal_items"]
            item = container.read_item(item=item_id, partition_key=item_id)
            
            # Clean response
            clean_item = {k: v for k, v in item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {"success": True, "item": clean_item}
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Meal item not found"}
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error getting meal item: {e}")
            return {"success": False, "message": f"Failed to get meal item: {str(e)}"}
