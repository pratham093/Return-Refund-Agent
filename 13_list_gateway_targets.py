#!/usr/bin/env python3
"""
Script to list AgentCore Gateway targets.

Prerequisites:
- gateway_config.json (from gateway creation)
"""

import json
import boto3

print("=" * 80)
print("LISTING GATEWAY TARGETS")
print("=" * 80)
print()

# Step 1: Load configuration
print("Step 1: Loading gateway configuration...")
print("-" * 80)

try:
    with open('gateway_config.json') as f:
        gateway_config = json.load(f)
    print(f"✓ Loaded gateway config")
    print(f"  Gateway ID: {gateway_config['gateway_id']}")
    print(f"  Gateway Name: {gateway_config['name']}")
    print()
    
except FileNotFoundError as e:
    print(f"✗ Error: gateway_config.json not found")
    print("  Please run 11_create_gateway.py first")
    exit(1)

# Step 2: Initialize AgentCore client
print("Step 2: Initializing AgentCore client...")
print("-" * 80)

gateway_client = boto3.client("bedrock-agentcore-control", region_name='us-west-2')
print(f"✓ AgentCore control plane client initialized")
print()

# Step 3: List targets
print("Step 3: Retrieving gateway targets...")
print("-" * 80)

try:
    response = gateway_client.list_gateway_targets(
        gatewayIdentifier=gateway_config["gateway_id"]
    )
    
    targets = response.get("items", [])
    
    print(f"✓ Found {len(targets)} target(s)")
    print()
    
    if len(targets) == 0:
        print("⚠️  No targets registered yet")
        print("   This is normal if you haven't run 12_add_lambda_to_gateway.py")
        print("   Note: AWS eventual consistency may cause a brief delay")
    else:
        print("=" * 80)
        print("REGISTERED TARGETS")
        print("=" * 80)
        print()
        
        for i, target in enumerate(targets, 1):
            print(f"Target {i}:")
            print("-" * 80)
            print(f"  Name: {target.get('name', 'N/A')}")
            print(f"  Target ID: {target.get('targetId', 'N/A')}")
            print(f"  Status: {target.get('status', 'unknown')}")
            print(f"  Description: {target.get('description', 'N/A')}")
            print()
    
except Exception as e:
    print(f"✗ Error listing targets: {e}")
    exit(1)

# Summary
print("=" * 80)
print("TARGET LISTING COMPLETE")
print("=" * 80)
print()

if len(targets) > 0:
    print(f"✓ Gateway has {len(targets)} registered target(s)")
    print("✓ Targets are ready to be called by your agent")
else:
    print("⚠️  Gateway has no targets yet")
    print("   Run 12_add_lambda_to_gateway.py to register the Lambda function")
