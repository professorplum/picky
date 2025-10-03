"""
Configuration classes for different environments
Simplified for Cosmos DB only
"""
import os
import logging
from typing import Optional
from .secrets_service import get_secrets_service

logger = logging.getLogger(__name__)


class Config:
    """Base configuration class with common settings"""
    # Environment identification - use ENV (dev|stage|prod)
    ENV = os.environ.get('ENV', 'dev')
    
    # Server settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on')
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # Azure Key Vault configuration
    KEY_VAULT_URL = os.environ.get('KEY_VAULT_URL')
    APP_NAME = os.environ.get('APP_NAME', 'picky')
    
    # Cosmos DB configuration - will be loaded from Key Vault
    COSMOS_CONNECTION_STRING: Optional[str] = None
    COSMOS_DATABASE: Optional[str] = None
    COSMOS_CONTAINER: Optional[str] = None
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    def __init__(self):
        """Initialize configuration and load secrets from Key Vault"""
        self._load_cosmos_config()
    
    def _load_cosmos_config(self):
        """Load Cosmos DB configuration from Key Vault"""
        try:
            # Get environment name for secret lookup
            env_name = self._get_environment_name()
            
            # Initialize secrets service
            secrets_service = get_secrets_service()
            
            # Load Cosmos DB configuration
            self.COSMOS_CONNECTION_STRING = secrets_service.get_cosmos_connection_string(env_name)
            self.COSMOS_DATABASE = secrets_service.get_database_name(self.APP_NAME, env_name)
            self.COSMOS_CONTAINER = secrets_service.get_container_name(env_name)
            
        except Exception as e:
            # Log the error and set connection to None for graceful handling
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"SHOWSTOPPER: Failed to load Cosmos DB configuration: {e}")
            logger.error("SHOWSTOPPER: Cannot start application without Key Vault access")
            logger.error("SHOWSTOPPER: Exiting to prevent serving broken application")
            import sys
            sys.exit(1)
    
    def _get_environment_name(self) -> str:
        """Get environment name for secret lookup"""
        # ENV is already in the correct format (dev|stage|prod)
        return self.ENV


class DevelopmentConfig(Config):
    """Development environment configuration"""
    ENV = 'dev'
    DEBUG = True
    
    # Specific ports for local development security
    CORS_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']


class StagingConfig(Config):
    """Staging environment configuration"""
    ENV = 'stage'
    DEBUG = False
    
    # Restricted CORS for staging
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://*.azurewebsites.net').split(',')


class ProductionConfig(Config):
    """Production environment configuration"""
    ENV = 'prod'
    DEBUG = False
    
    # Production requires explicit CORS configuration
    def __init__(self):
        super().__init__()  # Call parent constructor first
        cors_origins = os.environ.get('CORS_ORIGINS')
        if not cors_origins:
            raise ValueError("CORS_ORIGINS environment variable must be set in production")
        self.CORS_ORIGINS = cors_origins.split(',')


# Configuration mapping
config_map = {
    'dev': DevelopmentConfig,
    'stage': StagingConfig,
    'prod': ProductionConfig
}


def get_config():
    """Get the appropriate configuration class based on ENV"""
    env = os.environ.get('ENV', 'dev')
    config_class = config_map.get(env, DevelopmentConfig)
    
    # Only log config details in development
    if env == 'dev':
        logger.info(f"🔧 get_config() called with ENV: {env}")
        logger.info(f"🔧 Using config class: {config_class.__name__}")
    
    return config_class
