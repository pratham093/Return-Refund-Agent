#!/usr/bin/env python3
"""
Script to create IAM role for AgentCore Gateway.

This script creates an IAM role with permissions to invoke Lambda functions.
"""

import boto3
import json
import time

# Configuration
REGION = 'us-west-2'
ROLE_NAME = 'GatewayExecutionRole'
POLICY_NAME = 'GatewayLambdaInvokePolicy'

print("=" * 80)
print("CREATING IAM ROLE FOR GATEWAY")
print("=" * 80)
print()

# Create IAM client
iam_client = boto3.client('iam', region_name=REGION)
sts_client = boto3.client('sts', region_name=REGION)

# Get account ID
account_id = sts_client.get_caller_identity()['Account']
print(f"AWS Account ID: {account_id}")
print()

# Step 1: Create IAM Role with trust policy
print("Step 1: Creating IAM Role...")
print("-" * 80)

# Trust policy allowing AgentCore Gateway to assume this role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock-agentcore.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    role_response = iam_client.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description='Execution role for AgentCore Gateway to invoke Lambda functions',
        MaxSessionDuration=3600
    )
    
    role_arn = role_response['Role']['Arn']
    print(f"✓ Role created: {ROLE_NAME}")
    print(f"  ARN: {role_arn}")
    print()
    
except iam_client.exceptions.EntityAlreadyExistsException:
    print(f"⚠️  Role {ROLE_NAME} already exists, retrieving ARN...")
    role_response = iam_client.get_role(RoleName=ROLE_NAME)
    role_arn = role_response['Role']['Arn']
    print(f"  ARN: {role_arn}")
    print()
except Exception as e:
    print(f"✗ Error creating role: {e}")
    exit(1)

# Step 2: Create policy for Lambda invocation
print("Step 2: Creating Lambda invoke policy...")
print("-" * 80)

# Policy allowing Lambda invocation
lambda_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": f"arn:aws:lambda:{REGION}:{account_id}:function:*"
        }
    ]
}

try:
    policy_response = iam_client.create_policy(
        PolicyName=POLICY_NAME,
        PolicyDocument=json.dumps(lambda_policy),
        Description='Policy allowing Gateway to invoke Lambda functions'
    )
    
    policy_arn = policy_response['Policy']['Arn']
    print(f"✓ Policy created: {POLICY_NAME}")
    print(f"  ARN: {policy_arn}")
    print()
    
except iam_client.exceptions.EntityAlreadyExistsException:
    print(f"⚠️  Policy {POLICY_NAME} already exists, retrieving ARN...")
    policy_arn = f"arn:aws:iam::{account_id}:policy/{POLICY_NAME}"
    print(f"  ARN: {policy_arn}")
    print()
except Exception as e:
    print(f"✗ Error creating policy: {e}")
    exit(1)

# Step 3: Attach policy to role
print("Step 3: Attaching policy to role...")
print("-" * 80)

try:
    iam_client.attach_role_policy(
        RoleName=ROLE_NAME,
        PolicyArn=policy_arn
    )
    
    print(f"✓ Policy attached to role")
    print(f"  Role: {ROLE_NAME}")
    print(f"  Policy: {POLICY_NAME}")
    print()
    
except Exception as e:
    print(f"✗ Error attaching policy: {e}")
    exit(1)

# Wait for IAM propagation
print("Waiting for IAM propagation (5 seconds)...")
time.sleep(5)
print("✓ IAM propagation complete")
print()

# Step 4: Save configuration
print("Step 4: Saving configuration...")
print("-" * 80)

config = {
    "role_arn": role_arn,
    "role_name": ROLE_NAME,
    "policy_arn": policy_arn,
    "policy_name": POLICY_NAME,
    "region": REGION,
    "account_id": account_id
}

with open('gateway_role_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"✓ Configuration saved to gateway_role_config.json")
print()

# Summary
print("=" * 80)
print("GATEWAY IAM ROLE SETUP COMPLETE")
print("=" * 80)
print()
print("Configuration Summary:")
print(f"  Role Name: {ROLE_NAME}")
print(f"  Role ARN: {role_arn}")
print(f"  Policy Name: {POLICY_NAME}")
print(f"  Permissions: Lambda invoke")
print()
print("✓ Gateway can now invoke Lambda functions!")
print("✓ Use this role ARN when creating your gateway")
