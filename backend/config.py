"""
Configuration classes for different environments
Simplified for Cosmos DB only
"""
import os


class Config:
    """Base configuration class with common settings"""
    # Environment identification
    ENV_NAME = os.environ.get('ENV_NAME', 'Development')
    
    # Server settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on')
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # Cosmos DB configuration (REQUIRED)
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
    COSMOS_KEY = os.environ.get('COSMOS_KEY')
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'picky')
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')


class DevelopmentConfig(Config):
    """Development environment configuration"""
    ENV_NAME = 'Development'
    DEBUG = True
    
    # Cosmos DB settings - must be provided via environment variables
    # No defaults to ensure explicit configuration
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
    COSMOS_KEY = os.environ.get('COSMOS_KEY')
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'picky-dev')
    
    # Specific ports for local development security
    CORS_ORIGINS = ['http://localhost:5001', 'http://127.0.0.1:5001']


class StagingConfig(Config):
    """Staging environment configuration"""
    ENV_NAME = 'Staging'
    DEBUG = False
    
    # Restricted CORS for staging
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://*.azurewebsites.net').split(',')


class ProductionConfig(Config):
    """Production environment configuration"""
    ENV_NAME = 'Production'
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
    'Development': DevelopmentConfig,
    'Staging': StagingConfig,
    'Production': ProductionConfig
}


def get_config():
    """Get the appropriate configuration class based on ENV_NAME"""
    env_name = os.environ.get('ENV_NAME', 'Development')
    return config_map.get(env_name, DevelopmentConfig)
