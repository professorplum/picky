"""
Cosmos DB connection service with health checks and graceful error handling
"""
import logging
from typing import Optional, Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosHttpResponseError
from .config import get_config

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for managing Cosmos DB connections with health checks"""
    
    def __init__(self):
        """Initialize the database service"""
        config_class = get_config()
        self.config = config_class()
        self.client: Optional[CosmosClient] = None
        self.database = None
        self.container = None
        self._connection_status = "disconnected"
        self._last_error = None
    
    def connect(self) -> bool:
        """
        Establish connection to Cosmos DB
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Check if configuration is available
            if not self.config.COSMOS_CONNECTION_STRING:
                self._connection_status = "error"
                self._last_error = "Cosmos DB connection string not configured"
                logger.error("Cosmos DB connection string not configured")
                return False
            
            # Initialize Cosmos client
            self.client = CosmosClient.from_connection_string(
                self.config.COSMOS_CONNECTION_STRING
            )
            
            # Get database and container
            self.database = self.client.get_database_client(self.config.COSMOS_DATABASE)
            self.container = self.database.get_container_client(self.config.COSMOS_CONTAINER)
            
            # Test the connection
            if self._test_connection():
                self._connection_status = "connected"
                self._last_error = None
                logger.info(f"Successfully connected to Cosmos DB: {self.config.COSMOS_DATABASE}/{self.config.COSMOS_CONTAINER}")
                return True
            else:
                self._connection_status = "error"
                self._last_error = "Connection test failed"
                return False
                
        except Exception as e:
            self._connection_status = "error"
            self._last_error = str(e)
            logger.error(f"Failed to connect to Cosmos DB: {e}")
            return False
    
    def _test_connection(self) -> bool:
        """
        Test the database connection
        
        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            # Try to read container properties
            self.container.read()
            return True
        except CosmosResourceNotFoundError:
            logger.error(f"Container {self.config.COSMOS_CONTAINER} not found in database {self.config.COSMOS_DATABASE}")
            return False
        except CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB HTTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error testing connection: {e}")
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get the current health status of the database connection
        
        Returns:
            Dictionary with connection status and details
        """
        return {
            "status": self._connection_status,
            "database": self.config.COSMOS_DATABASE,
            "container": self.config.COSMOS_CONTAINER,
            "error": self._last_error,
            "connected": self._connection_status == "connected"
        }
    
    def is_connected(self) -> bool:
        """
        Check if the database is connected
        
        Returns:
            True if connected, False otherwise
        """
        return self._connection_status == "connected" and self.client is not None
    
    def get_container(self):
        """
        Get the container client
        
        Returns:
            Container client if connected, None otherwise
        """
        if self.is_connected():
            return self.container
        else:
            logger.warning("Database not connected, cannot get container")
            return None
    
    def create_database_if_not_exists(self) -> bool:
        """
        Create database and container if they don't exist
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.client:
                logger.error("Client not initialized")
                return False
            
            # Create database if it doesn't exist
            try:
                self.database = self.client.create_database_if_not_exists(
                    id=self.config.COSMOS_DATABASE
                )
                logger.info(f"Database {self.config.COSMOS_DATABASE} ready")
            except Exception as e:
                logger.error(f"Failed to create database: {e}")
                return False
            
            # Create container if it doesn't exist
            try:
                self.container = self.database.create_container_if_not_exists(
                    id=self.config.COSMOS_CONTAINER,
                    partition_key=PartitionKey(path="/id")
                )
                logger.info(f"Container {self.config.COSMOS_CONTAINER} ready")
                return True
            except Exception as e:
                logger.error(f"Failed to create container: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to create database/container: {e}")
            return False


# Global instance for easy access
_database_service: Optional[DatabaseService] = None


def get_database_service() -> DatabaseService:
    """
    Get the global database service instance
    
    Returns:
        DatabaseService instance
    """
    global _database_service
    if _database_service is None:
        _database_service = DatabaseService()
    return _database_service


def initialize_database() -> bool:
    """
    Initialize the database connection
    
    Returns:
        True if successful, False otherwise
    """
    db_service = get_database_service()
    return db_service.connect()
