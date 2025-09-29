"""
Configuration classes for different environments
"""
import os


class Config:
    """Base configuration class with common settings"""
    # Environment identification
    ENV_NAME = os.environ.get('ENV_NAME', 'Development')
    
    # Server settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on')
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # Data storage configuration
    USE_LOCAL_FILES = True  # Default to local files
    DATA_DIR = os.environ.get('DATA_DIR', 'data')
    
    # Database configuration (for future Cosmos DB)
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
    COSMOS_KEY = os.environ.get('COSMOS_KEY')
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'picky')
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')


class DevelopmentConfig(Config):
    """Development environment configuration"""
    ENV_NAME = 'Development'
    DEBUG = True
    
    # Local development uses file storage by default, but can be overridden
    USE_LOCAL_FILES = os.environ.get('USE_LOCAL_FILES', 'true').lower() in ('true', '1', 'yes', 'on')
    DATA_DIR = 'data'
    
    # Cosmos DB settings for local testing (emulator defaults)
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT', 'https://localhost:8081')
    COSMOS_KEY = os.environ.get('COSMOS_KEY', 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==')  # Emulator default key
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'picky-dev')
    
    # More permissive CORS for local development
    CORS_ORIGINS = ['http://localhost:*', 'http://127.0.0.1:*']


class StagingConfig(Config):
    """Staging environment configuration"""
    ENV_NAME = 'Staging'
    DEBUG = False
    
    # Staging uses Cosmos DB (when available)
    USE_LOCAL_FILES = False
    DATA_DIR = None  # Not used with Cosmos DB
    
    # Restricted CORS for staging
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://*.azurewebsites.net')


class ProductionConfig(Config):
    """Production environment configuration"""
    ENV_NAME = 'Production'
    DEBUG = False
    
    # Production uses Cosmos DB
    USE_LOCAL_FILES = False
    DATA_DIR = None  # Not used with Cosmos DB
    
    # Strict CORS for production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://your-production-domain.com')


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
