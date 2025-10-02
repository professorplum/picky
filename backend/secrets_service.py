"""
Azure Key Vault secrets service for secure credential management
Handles authentication and secret retrieval across environments
"""
import os
import logging
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import AzureError

logger = logging.getLogger(__name__)


class SecretsService:
    """Service for securely accessing Azure Key Vault secrets"""
    
    def __init__(self, vault_url: Optional[str] = None):
        """
        Initialize the secrets service
        
        Args:
            vault_url: Azure Key Vault URL. If None, will use KEY_VAULT_URL env var
        """
        self.vault_url = vault_url or os.environ.get('KEY_VAULT_URL')
        if not self.vault_url:
            raise ValueError("KEY_VAULT_URL environment variable must be set")
        
        # Initialize Azure credential and Key Vault client
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
        logger.info(f"SecretsService initialized for vault: {self.vault_url}")
    
    def get_secret(self, secret_name: str) -> str:
        """
        Retrieve a secret from Azure Key Vault
        
        Args:
            secret_name: Name of the secret to retrieve
            
        Returns:
            Secret value as string
            
        Raises:
            AzureError: If secret retrieval fails
            ValueError: If secret is not found
        """
        try:
            logger.info(f"Retrieving secret: {secret_name}")
            secret = self.client.get_secret(secret_name)
            logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret.value
            
        except AzureError as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving secret {secret_name}: {e}")
            raise
    
    def get_cosmos_connection_string(self, environment: str) -> str:
        """
        Get Cosmos DB connection string for the specified environment
        
        Args:
            environment: Environment name (dev, stage, prod)
            
        Returns:
            Cosmos DB connection string
        """
        secret_name = f"cosmos-connection-string-{environment}"
        return self.get_secret(secret_name)
    
    def get_database_name(self, app_name: str, environment: str) -> str:
        """
        Get database name for the specified environment
        
        Args:
            app_name: Application name
            environment: Environment name (dev|stage|prod)
            
        Returns:
            Database name
        """
        # Special handling for dev environment
        if environment == 'dev':
            # Check if using local emulator
            try:
                connection_string = self.get_cosmos_connection_string('dev')
                if 'localhost:8081' in connection_string:
                    # Using local emulator - use dev database
                    return f"{app_name}-dev-db"
                else:
                    # Using Azure - use stage database to avoid RU limits
                    return f"{app_name}-stage-db"
            except:
                # Fallback to stage if can't determine
                return f"{app_name}-stage-db"
        else:
            # Stage and prod use their own databases
            return f"{app_name}-{environment}-db"
    
    def get_container_name(self, environment: str) -> str:
        """
        Get container name for the specified environment
        
        Args:
            environment: Environment name (dev|stage|prod)
            
        Returns:
            Container name
        """
        # Special handling for dev environment
        if environment == 'dev':
            # Check if using local emulator
            try:
                connection_string = self.get_cosmos_connection_string('dev')
                if 'localhost:8081' in connection_string:
                    # Using local emulator - use dev container
                    return "dev-container"
                else:
                    # Using Azure - use stage container to avoid RU limits
                    return "stage-container"
            except:
                # Fallback to stage if can't determine
                return "stage-container"
        else:
            # Stage and prod use their own containers
            return f"{environment}-container"
    
    def test_connection(self) -> bool:
        """
        Test the connection to Azure Key Vault
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to list secrets to test connection
            secrets = list(self.client.list_properties_of_secrets())
            logger.info("Key Vault connection test successful")
            return True
        except Exception as e:
            logger.error(f"Key Vault connection test failed: {e}")
            return False


# Global instance for easy access
_secrets_service: Optional[SecretsService] = None


def get_secrets_service() -> SecretsService:
    """
    Get the global secrets service instance
    
    Returns:
        SecretsService instance
    """
    global _secrets_service
    if _secrets_service is None:
        _secrets_service = SecretsService()
    return _secrets_service


def initialize_secrets_service(vault_url: Optional[str] = None) -> SecretsService:
    """
    Initialize the global secrets service
    
    Args:
        vault_url: Azure Key Vault URL
        
    Returns:
        Initialized SecretsService instance
    """
    global _secrets_service
    _secrets_service = SecretsService(vault_url)
    return _secrets_service
