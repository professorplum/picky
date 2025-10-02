"""
Modern data layer using the new database service architecture
Provides clean interface for all CRUD operations
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .database_service import get_database_service
from azure.cosmos import exceptions

logger = logging.getLogger(__name__)


class DataLayer:
    """
    Modern data layer using the new database service architecture.
    Provides clean interface for all CRUD operations with proper error handling.
    """
    
    def __init__(self):
        """Initialize the data layer"""
        self.db_service = get_database_service()
        self.container = None
        self._ensure_connected()
    
    def _ensure_connected(self):
        """Ensure database connection is established"""
        if not self.db_service.is_connected():
            if not self.db_service.connect():
                raise Exception("Failed to connect to database")
        
        self.container = self.db_service.get_container()
        if not self.container:
            raise Exception("Database container not available")
        
        # Log connection details
        health = self.db_service.get_health_status()
        logger.info(f"DataLayer connected to: {health['database']}/{health['container']}")
    
    def _handle_database_error(self, operation: str, error: Exception) -> Dict[str, Any]:
        """Handle database errors gracefully"""
        logger.error(f"Database error in {operation}: {error}")
        return {
            "success": False,
            "error": f"Database operation failed: {str(error)}",
            "operation": operation
        }
    
    def _generate_id(self) -> str:
        """Generate a unique ID using timestamp + random component to prevent collisions"""
        import random
        timestamp = int(datetime.now().timestamp() * 1000)
        random_suffix = random.randint(1000, 9999)
        return f"{timestamp}-{random_suffix}"
    
    def _create_item(self, item_data: Dict[str, Any], item_type: str) -> Dict[str, Any]:
        """Create a new item in the database"""
        try:
            self._ensure_connected()
            
            # Create item with proper field mapping based on type
            new_item = {
                "id": self._generate_id(),
                "name": item_data.get("name", "").strip(),
                "type": item_type,
                "createdAt": datetime.now().isoformat(),
                "modifiedAt": datetime.now().isoformat()
            }
            
            # Add type-specific fields
            if item_type == "shopping":
                new_item["inCart"] = item_data.get("inCart", False)
            elif item_type == "larder":
                new_item["reorder"] = item_data.get("reorder", False)
            elif item_type == "meal":
                new_item["ingredients"] = item_data.get("ingredients", "")
            
            # Create item in Cosmos DB
            result = self.container.create_item(new_item)
            
            logger.info(f"Successfully created {item_type} item: {result['id']}")
            return {
                "success": True,
                "item": result,
                "message": f"{item_type.title()} item created successfully"
            }
            
        except Exception as e:
            return self._handle_database_error(f"create_{item_type}", e)
    
    def _get_items(self, item_type: str) -> Dict[str, Any]:
        """Get all items of a specific type"""
        try:
            self._ensure_connected()
            
            # Query for items of this type
            query = "SELECT * FROM c WHERE c.type = @type"
            parameters = [{"name": "@type", "value": item_type}]
            
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            logger.info(f"Retrieved {len(items)} {item_type} items")
            return {
                "success": True,
                "items": items,
                "count": len(items)
            }
            
        except Exception as e:
            return self._handle_database_error(f"get_{item_type}", e)
    
    def _update_item(self, item_id: str, update_data: Dict[str, Any], item_type: str) -> Dict[str, Any]:
        """Update an existing item"""
        try:
            self._ensure_connected()
            
            # Get existing item
            try:
                existing_item = self.container.read_item(item_id, partition_key=item_id)
            except exceptions.CosmosResourceNotFoundError:
                return {
                    "success": False,
                    "error": f"{item_type.title()} item not found",
                    "item_id": item_id
                }
            
            # Update fields with proper mapping
            for key, value in update_data.items():
                if key not in ['id', 'type']:  # Don't allow ID or type changes
                    existing_item[key] = value
            
            existing_item["modifiedAt"] = datetime.now().isoformat()
            
            # Save updated item
            result = self.container.replace_item(item_id, existing_item)
            
            logger.info(f"Successfully updated {item_type} item: {item_id}")
            return {
                "success": True,
                "item": result,
                "message": f"{item_type.title()} item updated successfully"
            }
            
        except Exception as e:
            return self._handle_database_error(f"update_{item_type}", e)
    
    def _delete_item(self, item_id: str, item_type: str) -> Dict[str, Any]:
        """Delete an item"""
        try:
            self._ensure_connected()
            
            # Delete item
            self.container.delete_item(item_id, partition_key=item_id)
            
            logger.info(f"Successfully deleted {item_type} item: {item_id}")
            return {
                "success": True,
                "message": f"{item_type.title()} item deleted successfully",
                "item_id": item_id
            }
            
        except exceptions.CosmosResourceNotFoundError:
            return {
                "success": False,
                "error": f"{item_type.title()} item not found",
                "item_id": item_id
            }
        except Exception as e:
            return self._handle_database_error(f"delete_{item_type}", e)
    
    # Larder items
    def get_larder_items(self) -> Dict[str, Any]:
        """Get all larder items"""
        return self._get_items("larder")
    
    def add_larder_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new larder item"""
        return self._create_item(item_data, "larder")
    
    def update_larder_item(self, item_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a larder item"""
        return self._update_item(item_id, update_data, "larder")
    
    def delete_larder_item(self, item_id: str) -> Dict[str, Any]:
        """Delete a larder item"""
        return self._delete_item(item_id, "larder")
    
    # Shopping items
    def get_shopping_items(self) -> Dict[str, Any]:
        """Get all shopping items"""
        return self._get_items("shopping")
    
    def add_shopping_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new shopping item"""
        return self._create_item(item_data, "shopping")
    
    def update_shopping_item(self, item_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a shopping item"""
        return self._update_item(item_id, update_data, "shopping")
    
    def delete_shopping_item(self, item_id: str) -> Dict[str, Any]:
        """Delete a shopping item"""
        return self._delete_item(item_id, "shopping")
    
    # Meal items
    def get_meal_items(self) -> Dict[str, Any]:
        """Get all meal items"""
        return self._get_items("meal")
    
    def add_meal_item(self, meal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new meal item"""
        return self._create_item(meal_data, "meal")
    
    def update_meal_item(self, item_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a meal item"""
        return self._update_item(item_id, update_data, "meal")
    
    def delete_meal_item(self, item_id: str) -> Dict[str, Any]:
        """Delete a meal item"""
        return self._delete_item(item_id, "meal")
