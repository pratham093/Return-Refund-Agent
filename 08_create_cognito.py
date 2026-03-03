#!/usr/bin/env python3
"""
Script to create Cognito User Pool for Gateway authentication.

This script sets up OAuth authentication for AgentCore Gateway.
"""

import boto3
import json
import time
import uuid

# Configuration
REGION = 'us-west-2'
POOL_NAME = 'returns-gateway-pool'
DOMAIN_PREFIX = f'returns-gateway-{uuid.uuid4().hex[:8]}'
RESOURCE_SERVER_IDENTIFIER = 'returns-gateway-api'

print("=" * 80)
print("CREATING COGNITO USER POOL FOR GATEWAY AUTHENTICATION")
print("=" * 80)
print()

# Create Cognito client
cognito_client = boto3.client('cognito-idp', region_name=REGION)

# Step 1: Create User Pool
print("Step 1: Creating Cognito User Pool...")
print("-" * 80)

try:
    user_pool_response = cognito_client.create_user_pool(
        PoolName=POOL_NAME,
        Policies={
            'PasswordPolicy': {
                'MinimumLength': 8,
                'RequireUppercase': False,
                'RequireLowercase': False,
                'RequireNumbers': False,
                'RequireSymbols': False
            }
        },
        AutoVerifiedAttributes=['email']
    )
    
    user_pool_id = user_pool_response['UserPool']['Id']
    print(f"✓ User Pool created: {user_pool_id}")
    print(f"  Name: {POOL_NAME}")
    print()
    
except Exception as e:
    print(f"✗ Error creating user pool: {e}")
    exit(1)

# Step 2: Create User Pool Domain
print("Step 2: Creating User Pool Domain...")
print("-" * 80)

try:
    domain_response = cognito_client.create_user_pool_domain(
        Domain=DOMAIN_PREFIX,
        UserPoolId=user_pool_id
    )
    
    print(f"✓ Domain created: {DOMAIN_PREFIX}")
    print(f"  Full domain: {DOMAIN_PREFIX}.auth.{REGION}.amazoncognito.com")
    print()
    
except Exception as e:
    print(f"✗ Error creating domain: {e}")
    exit(1)

# Step 3: Create Resource Server with scopes
print("Step 3: Creating Resource Server with OAuth scopes...")
print("-" * 80)

try:
    resource_server_response = cognito_client.create_resource_server(
        UserPoolId=user_pool_id,
        Identifier=RESOURCE_SERVER_IDENTIFIER,
        Name='Returns Gateway API',
        Scopes=[
            {
                'ScopeName': 'read',
                'ScopeDescription': 'Read access to gateway'
            },
            {
                'ScopeName': 'write',
                'ScopeDescription': 'Write access to gateway'
            },
            {
                'ScopeName': 'invoke',
                'ScopeDescription': 'Invoke gateway tools'
            }
        ]
    )
    
    print(f"✓ Resource server created: {RESOURCE_SERVER_IDENTIFIER}")
    print(f"  Scopes: read, write, invoke")
    print()
    
except Exception as e:
    print(f"✗ Error creating resource server: {e}")
    exit(1)

# Wait a moment for resource server to be ready
time.sleep(2)

# Step 4: Create App Client with client credentials flow
print("Step 4: Creating App Client for machine-to-machine authentication...")
print("-" * 80)

try:
    app_client_response = cognito_client.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName='returns-gateway-client',
        GenerateSecret=True,
        ExplicitAuthFlows=[],
        AllowedOAuthFlows=['client_credentials'],
        AllowedOAuthScopes=[
            f'{RESOURCE_SERVER_IDENTIFIER}/read',
            f'{RESOURCE_SERVER_IDENTIFIER}/write',
            f'{RESOURCE_SERVER_IDENTIFIER}/invoke'
        ],
        AllowedOAuthFlowsUserPoolClient=True,
        SupportedIdentityProviders=['COGNITO']
    )
    
    client_id = app_client_response['UserPoolClient']['ClientId']
    client_secret = app_client_response['UserPoolClient']['ClientSecret']
    
    print(f"✓ App client created: {client_id}")
    print(f"  OAuth flows: client_credentials")
    print(f"  Scopes: read, write, invoke")
    print()
    
except Exception as e:
    print(f"✗ Error creating app client: {e}")
    exit(1)

# Step 5: Build configuration
print("Step 5: Building configuration...")
print("-" * 80)

# Token endpoint
token_endpoint = f"https://{DOMAIN_PREFIX}.auth.{REGION}.amazoncognito.com/oauth2/token"

# Discovery URL (IDP-based format)
discovery_url = f"https://cognito-idp.{REGION}.amazonaws.com/{user_pool_id}/.well-known/openid-configuration"

# Save configuration
config = {
    "user_pool_id": user_pool_id,
    "domain_prefix": DOMAIN_PREFIX,
    "client_id": client_id,
    "client_secret": client_secret,
    "token_endpoint": token_endpoint,
    "discovery_url": discovery_url,
    "region": REGION,
    "resource_server_identifier": RESOURCE_SERVER_IDENTIFIER
}

with open('cognito_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"✓ Configuration saved to cognito_config.json")
print()

# Summary
print("=" * 80)
print("COGNITO SETUP COMPLETE")
print("=" * 80)
print()
print("Configuration Summary:")
print(f"  User Pool ID: {user_pool_id}")
print(f"  Domain Prefix: {DOMAIN_PREFIX}")
print(f"  Client ID: {client_id}")
print(f"  Token Endpoint: {token_endpoint}")
print(f"  Discovery URL: {discovery_url}")
print()
print("✓ Gateway authentication is ready!")
print("✓ Use these credentials to configure your gateway")
