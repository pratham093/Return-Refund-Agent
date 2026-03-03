#!/usr/bin/env python3
"""
Script to add Lambda target to AgentCore Gateway.

Prerequisites:
- gateway_config.json (from gateway creation)
- lambda_config.json (from Lambda creation)
"""

import json
import boto3

print("=" * 80)
print("ADDING LAMBDA TARGET TO GATEWAY")
print("=" * 80)
print()

# Step 1: Load configuration
print("Step 1: Loading configuration...")
print("-" * 80)

try:
    with open('gateway_config.json') as f:
        gateway_config = json.load(f)
    print(f"✓ Loaded gateway config")
    print(f"  Gateway ID: {gateway_config['gateway_id']}")
    
    with open('lambda_config.json') as f:
        lambda_config = json.load(f)
    print(f"✓ Loaded Lambda config")
    print(f"  Function ARN: {lambda_config['function_arn']}")
    print(f"  Tool: {lambda_config['tool_schema']['name']}")
    print()
    
except FileNotFoundError as e:
    print(f"✗ Error: Required config file not found: {e}")
    exit(1)

# Step 2: Initialize AgentCore client
print("Step 2: Initializing AgentCore client...")
print("-" * 80)

gateway_client = boto3.client("bedrock-agentcore-control", region_name='us-west-2')
print(f"✓ AgentCore control plane client initialized")
print()

# Step 3: Build Lambda target configuration
print("Step 3: Building Lambda target configuration...")
print("-" * 80)

# Build Lambda target configuration with MCP protocol
lambda_target_config = {
    "mcp": {
        "lambda": {
            "lambdaArn": lambda_config['function_arn'],
            "toolSchema": {
                "inlinePayload": [lambda_config['tool_schema']]
            }
        }
    }
}

# Use gateway's IAM role for Lambda invocation
credential_config = [{"credentialProviderType": "GATEWAY_IAM_ROLE"}]

print(f"✓ Target configuration built")
print(f"  Protocol: MCP")
print(f"  Type: Lambda")
print(f"  Credentials: Gateway IAM Role")
print()

# Step 4: Create target
print("Step 4: Registering Lambda as gateway target...")
print("-" * 80)

try:
    create_response = gateway_client.create_gateway_target(
        gatewayIdentifier=gateway_config["gateway_id"],
        name="OrderLookup",
        description="Lambda function to look up order details by order ID",
        targetConfiguration=lambda_target_config,
        credentialProviderConfigurations=credential_config
    )
    
    target_id = create_response["targetId"]
    
    print(f"✓ Lambda target added successfully!")
    print(f"  Target ID: {target_id}")
    print(f"  Target Name: OrderLookup")
    print(f"  Tool: lookup_order")
    print()
    
except Exception as e:
    print(f"✗ Error creating target: {e}")
    exit(1)

# Summary
print("=" * 80)
print("LAMBDA TARGET REGISTRATION COMPLETE")
print("=" * 80)
print()
print("Configuration Summary:")
print(f"  Gateway: {gateway_config['name']}")
print(f"  Target Name: OrderLookup")
print(f"  Target ID: {target_id}")
print(f"  Lambda Function: OrderLookupFunction")
print(f"  Tool Available: lookup_order")
print()
print("✓ Your agent can now call lookup_order through the gateway!")
print("✓ Next: Verify the target is registered correctly")
