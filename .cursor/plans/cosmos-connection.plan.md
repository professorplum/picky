# Azure Cosmos DB Connection Plan

## Overview

Connect the application to Azure Cosmos DB using Key Vault for secure credential management across all environments (local, dev, production).

## Architecture

### Environments

- **Dev**: App runs locally or in Azure, connects to Azure Cosmos DB
- **Stage**: App runs in Azure, connects to Azure Cosmos DB
- **Production**: App runs in Azure, connects to Azure Cosmos DB

### Database Strategy

- **Single Cosmos DB account** with environment-specific containers:
  - `dev-container` (dev environment)
  - `stage-container` (staging environment)
  - `prod-container` (production environment)

## Implementation Strategy

### Phase 1: Dev Environment (Simpler - No MI Required)

#### 1. Azure Key Vault Setup

- Store dev secrets:
  - `cosmos-connection-string-dev`

#### 2. Dev Authentication

- **Local**: Developer runs `az login` to authenticate with Azure
- **Dev (Azure)**: Uses `az login` approach (no MI setup needed)
- App uses `DefaultAzureCredential` which automatically:
  - Uses Azure CLI credentials (from `az login`)
  - No secrets stored in code

### Phase 2: Stage Environment (Add MI)

#### 3. Add Stage Secrets

- Store stage secrets:
  - `cosmos-connection-string-stage`

#### 4. Stage Authentication

- **Stage**: Uses Managed Identity for Key Vault access
- App gets Azure identity that can access Key Vault
- No secrets needed in code - Azure handles authentication

### 5. Code Structure

```typescript
// Environment detection
const environment = process.env.NODE_ENV || 'development';
const containerName = environment === 'production' ? 'prod-container' : 
                     environment === 'staging' ? 'stage-container' : 'dev-container';
const databaseName = `${process.env.APP_NAME}-${environment}-db`;
const secretName = `cosmos-connection-string-${environment}`;

// Authentication
const credential = new DefaultAzureCredential();
const keyVaultClient = new SecretClient(vaultUrl, credential);
```

### 6. Key Components

- **Secrets Service**: Utility class for Key Vault access
- **Database Connection**: Environment-aware Cosmos client
- **Connection Pooling**: For production performance
- **Error Handling**: Retry logic and graceful degradation
- **Health Checks**: Connection status verification

### 7. Testing Strategy

- **Unit Tests**: Mock Key Vault calls
- **Integration Tests**: Actual Key Vault in dev environment
- **Connection Health Checks**: Verify database connectivity
- **Fallback Mechanisms**: Handle connection failures

## Security Benefits

- ✅ No secrets in code
- ✅ Environment-specific data isolation
- ✅ Secure local development
- ✅ Secure production deployment
- ✅ Azure-managed authentication

## Next Steps

### Phase 1: Dev Environment

1. Set up Azure Key Vault with dev secrets
2. Implement secrets service and database connection code
3. Test connection flow with `az login` authentication
4. Add connection health checks and error handling

### Phase 2: Stage Environment  

5. Add stage secrets to Key Vault
6. Configure managed identity for stage resources
7. Test connection flow with managed identity authentication
8. Verify stage-specific container isolation

## Success Criteria

- App starts and successfully connects to appropriate Cosmos DB container
- No hardcoded secrets in codebase
- Environment-specific data isolation maintained
- Secure authentication across all environments