"""
Cosmos DB Data Layer for Picky Meal Planner
Implements the same interface as DataLayer but uses Azure Cosmos DB for storage
"""
import ssl
import urllib3
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from azure.cosmos import CosmosClient, PartitionKey, exceptions

logger = logging.getLogger(__name__)


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
            "shopping_items": "/id",     # Shopping list items (inCart)
            "larder_items": "/id",       # Larder/pantry items (reorder) 
            "meal_items": "/id"          # Future meal items
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
                logger.info(f"Container '{container_name}' ready")
            except exceptions.CosmosHttpResponseError as e:
                raise RuntimeError(f"Failed to create container '{container_name}': {e}")
    
    def _generate_id(self) -> str:
        """Generate a unique ID using timestamp + random component to prevent collisions"""
        import random
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        random_suffix = random.randint(1000, 9999)
        return f"{timestamp}-{random_suffix}"
    
    # === Inventory Items (Larder) Methods ===
    def get_larder_items(self) -> List[Dict[str, Any]]:
        """Get all larder items from Cosmos DB"""
        try:
            container = self.containers["larder_items"]
            items = list(container.read_all_items())
            
            # Remove Cosmos DB metadata fields for clean response
            clean_items = []
            for item in items:
                clean_item = {k: v for k, v in item.items() 
                             if not k.startswith('_') and k != 'ttl'}
                clean_items.append(clean_item)
            
            return clean_items
        except exceptions.CosmosHttpResponseError as e:
            raise RuntimeError(f"Failed to get larder items: {e}")
    
    def add_larder_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new larder item to Cosmos DB"""
        try:
            container = self.containers["larder_items"]
            
            # Create new item matching current JSON structure
            new_item = {
                "id": self._generate_id(),
                "name": item_data.get("name", "").strip(),
                "reorder": item_data.get("reorder", False),
                "createdAt": datetime.utcnow().isoformat(),
                "modifiedAt": datetime.utcnow().isoformat()
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
            raise RuntimeError(f"Failed to add larder item: {e}")
    
    # === Grocery Items (Shopping) Methods ===
    def get_shopping_items(self) -> List[Dict[str, Any]]:
        """Get all shopping items from Cosmos DB"""
        try:
            container = self.containers["shopping_items"]
            items = list(container.read_all_items())
            
            # Remove Cosmos DB metadata fields for clean response
            clean_items = []
            for item in items:
                clean_item = {k: v for k, v in item.items() 
                             if not k.startswith('_') and k != 'ttl'}
                clean_items.append(clean_item)
            
            return clean_items
        except exceptions.CosmosHttpResponseError as e:
            raise RuntimeError(f"Failed to get shopping items: {e}")
    
    def add_shopping_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new shopping item to Cosmos DB"""
        try:
            container = self.containers["shopping_items"]
            
            # Create new item matching current JSON structure
            new_item = {
                "id": self._generate_id(),
                "name": item_data.get("name", "").strip(),
                "inCart": item_data.get("inCart", False),
                "createdAt": datetime.utcnow().isoformat(),
                "modifiedAt": datetime.utcnow().isoformat()
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
            raise RuntimeError(f"Failed to add shopping item: {e}")
    
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
            raise RuntimeError(f"Failed to get meal items: {e}")
    
    def add_meal_item(self, meal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new meal item to Cosmos DB"""
        try:
            container = self.containers["meal_items"]
            
            # Create new meal with ID and default values
            new_meal = {
                "id": self._generate_id(),
                "name": meal_data.get("name", "").strip(),
                "ingredients": meal_data.get("ingredients", "").strip(),
                "createdAt": datetime.utcnow().isoformat(),
                "modifiedAt": datetime.utcnow().isoformat()
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
            raise RuntimeError(f"Failed to add meal item: {e}")
    
    # === Update Operations ===
    def update_shopping_item(self, item_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a shopping item in Cosmos DB"""
        return self._update_item(
            container_name="shopping_items",
            item_id=item_id,
            updates=updates,
            success_message="Grocery item updated successfully",
            not_found_message="Grocery item not found",
            error_context="shopping item"
        )
    
    def _update_item(self, container_name: str, item_id: str, updates: Dict[str, Any], success_message: str, not_found_message: str, error_context: str) -> Dict[str, Any]:
        """Helper to update an item in a specified container"""
        try:
            container = self.containers[container_name]

            # Read existing item
            existing_item = container.read_item(item=item_id, partition_key=item_id)

            # Apply updates
            for key, value in updates.items():
                if key not in ['id']:  # Don't allow ID changes
                    existing_item[key] = value

            existing_item['modifiedAt'] = datetime.utcnow().isoformat()

            # Replace item
            updated_item = container.replace_item(item=existing_item, body=existing_item)

            # Clean response
            clean_item = {k: v for k, v in updated_item.items()
                         if not k.startswith('_') and k != 'ttl'}

            return {
                "success": True,
                "message": success_message,
                "item": clean_item
            }

        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": not_found_message}
        except exceptions.CosmosHttpResponseError as e:
            raise RuntimeError(f"Failed to update {error_context}: {e}")

    def update_larder_item(self, item_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a larder item in Cosmos DB"""
        return self._update_item(
            container_name="larder_items",
            item_id=item_id,
            updates=updates,
            success_message="Inventory item updated successfully",
            not_found_message="Inventory item not found",
            error_context="larder item"
        )
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
            
            existing_item['modifiedAt'] = datetime.utcnow().isoformat()
            
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
            raise RuntimeError(f"Failed to update meal item: {e}")
    
    # === Delete Operations ===
    def delete_shopping_item(self, item_id: str) -> Dict[str, Any]:
        """Delete a shopping item from Cosmos DB"""
        try:
            container = self.containers["shopping_items"]
            container.delete_item(item=item_id, partition_key=item_id)
            
            return {
                "success": True,
                "message": "Grocery item deleted successfully"
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Grocery item not found"}
        except exceptions.CosmosHttpResponseError as e:
            raise RuntimeError(f"Failed to delete shopping item: {e}")
    
    def delete_larder_item(self, item_id: str) -> Dict[str, Any]:
        """Delete a larder item from Cosmos DB"""
        try:
            container = self.containers["larder_items"]
            container.delete_item(item=item_id, partition_key=item_id)
            
            return {
                "success": True,
                "message": "Inventory item deleted successfully"
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Inventory item not found"}
        except exceptions.CosmosHttpResponseError as e:
            raise RuntimeError(f"Failed to delete larder item: {e}")
    
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
            raise RuntimeError(f"Failed to delete meal item: {e}")
    
    # === Get Single Item Operations ===
    def get_shopping_item(self, item_id: str) -> Dict[str, Any]:
        """Get a single shopping item by ID"""
        try:
            container = self.containers["shopping_items"]
            item = container.read_item(item=item_id, partition_key=item_id)
            
            # Clean response
            clean_item = {k: v for k, v in item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {"success": True, "item": clean_item}
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Grocery item not found"}
        except exceptions.CosmosHttpResponseError as e:
            raise RuntimeError(f"Failed to get shopping item: {e}")
    
    def get_larder_item(self, item_id: str) -> Dict[str, Any]:
        """Get a single larder item by ID"""
        try:
            container = self.containers["larder_items"]
            item = container.read_item(item=item_id, partition_key=item_id)
            
            # Clean response
            clean_item = {k: v for k, v in item.items() 
                         if not k.startswith('_') and k != 'ttl'}
            
            return {"success": True, "item": clean_item}
            
        except exceptions.CosmosResourceNotFoundError:
            return {"success": False, "message": "Inventory item not found"}
        except exceptions.CosmosHttpResponseError as e:
            raise RuntimeError(f"Failed to get larder item: {e}")
    
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
            raise RuntimeError(f"Failed to get meal item: {e}")
