#!/usr/bin/env python3
"""
Script to create AgentCore Gateway.

Prerequisites:
- cognito_config.json (from Cognito setup)
- gateway_role_config.json (from IAM role setup)
"""

import json
import boto3

print("=" * 80)
print("CREATING AGENTCORE GATEWAY")
print("=" * 80)
print()

# Step 1: Load configuration
print("Step 1: Loading configuration...")
print("-" * 80)

try:
    with open('cognito_config.json') as f:
        cognito_config = json.load(f)
    print(f"✓ Loaded Cognito config")
    print(f"  Client ID: {cognito_config['client_id']}")
    print(f"  Discovery URL: {cognito_config['discovery_url']}")
    
    with open('gateway_role_config.json') as f:
        role_config = json.load(f)
    print(f"✓ Loaded IAM role config")
    print(f"  Role ARN: {role_config['role_arn']}")
    print()
    
except FileNotFoundError as e:
    print(f"✗ Error: Required config file not found: {e}")
    print("  Please run 08_create_cognito.py and 09_create_gateway_role.py first")
    exit(1)

# Step 2: Initialize AgentCore client
print("Step 2: Initializing AgentCore client...")
print("-" * 80)

gateway_client = boto3.client("bedrock-agentcore-control", region_name='us-west-2')
print(f"✓ AgentCore control plane client initialized")
print()

# Step 3: Build auth configuration
print("Step 3: Building authentication configuration...")
print("-" * 80)

auth_config = {
    "customJWTAuthorizer": {
        "allowedClients": [cognito_config["client_id"]],
        "discoveryUrl": cognito_config["discovery_url"]
    }
}

print(f"✓ Auth configuration built")
print(f"  Type: Custom JWT Authorizer")
print(f"  Allowed clients: {cognito_config['client_id']}")
print()

# Step 4: Create gateway
print("Step 4: Creating AgentCore Gateway...")
print("-" * 80)

try:
    create_response = gateway_client.create_gateway(
        name="ReturnsRefundsGateway",
        roleArn=role_config["role_arn"],
        protocolType="MCP",
        authorizerType="CUSTOM_JWT",
        authorizerConfiguration=auth_config,
        description="Gateway for returns and refunds agent to access order lookup tools"
    )
    
    # Extract gateway details
    gateway_id = create_response["gatewayId"]
    gateway_url = create_response["gatewayUrl"]
    gateway_arn = create_response["gatewayArn"]
    
    print(f"✓ Gateway created successfully!")
    print(f"  Name: ReturnsRefundsGateway")
    print(f"  Gateway ID: {gateway_id}")
    print(f"  Gateway URL: {gateway_url}")
    print(f"  Gateway ARN: {gateway_arn}")
    print()
    
except Exception as e:
    print(f"✗ Error creating gateway: {e}")
    exit(1)

# Step 5: Save gateway config
print("Step 5: Saving configuration...")
print("-" * 80)

config = {
    "id": gateway_id,
    "gateway_id": gateway_id,
    "gateway_url": gateway_url,
    "gateway_arn": gateway_arn,
    "name": "ReturnsRefundsGateway",
    "region": "us-west-2"
}

with open('gateway_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"✓ Configuration saved to gateway_config.json")
print()

# Summary
print("=" * 80)
print("GATEWAY CREATION COMPLETE")
print("=" * 80)
print()
print("Configuration Summary:")
print(f"  Gateway Name: ReturnsRefundsGateway")
print(f"  Gateway ID: {gateway_id}")
print(f"  Gateway URL: {gateway_url}")
print(f"  Protocol: MCP")
print(f"  Auth Type: Custom JWT (Cognito)")
print()
print("✓ Gateway is ready to accept targets!")
print("✓ Next: Register Lambda function as a gateway target")
