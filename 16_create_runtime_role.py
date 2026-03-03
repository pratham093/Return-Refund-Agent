#!/usr/bin/env python3
"""
Script to create IAM execution role for AgentCore Runtime.

This script creates an IAM role with all required permissions for running
agents in AgentCore Runtime, including Memory, Gateway, and Knowledge Base access.
"""

import json
import boto3
import time

# Configuration
REGION = "us-west-2"
ROLE_NAME = "AgentCoreRuntimeExecutionRole"
POLICY_NAME = "AgentCoreRuntimeExecutionPolicy"

print("=" * 80)
print("CREATING IAM EXECUTION ROLE FOR AGENTCORE RUNTIME")
print("=" * 80)
print()

# Create IAM client
iam_client = boto3.client('iam', region_name=REGION)
sts_client = boto3.client('sts', region_name=REGION)

# Get AWS account ID
account_id = sts_client.get_caller_identity()['Account']
print(f"AWS Account: {account_id}")
print(f"Region: {REGION}")
print()

# Step 1: Define trust policy for bedrock-agentcore.amazonaws.com
print("Step 1: Creating IAM role with trust policy...")
print("-" * 80)

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
        Description="Execution role for AgentCore Runtime with full permissions"
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

# Step 2: Create comprehensive permissions policy
print("Step 2: Creating permissions policy...")
print("-" * 80)

permissions_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockModelAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AgentCoreMemoryAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock-agentcore:GetMemory",
                "bedrock-agentcore:CreateEvent",
                "bedrock-agentcore:GetLastKTurns",
                "bedrock-agentcore:RetrieveMemory",
                "bedrock-agentcore:ListEvents",
                "bedrock-agentcore:GetMemoryRecord",
                "bedrock-agentcore:RetrieveMemoryRecords",
                "bedrock-agentcore:ListMemoryRecords"
            ],
            "Resource": f"arn:aws:bedrock-agentcore:{REGION}:{account_id}:*"
        },
        {
            "Sid": "KnowledgeBaseAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve",
                "bedrock-agent:Retrieve"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CloudWatchLogsAccess",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams",
                "logs:DescribeLogGroups"
            ],
            "Resource": [
                f"arn:aws:logs:{REGION}:{account_id}:log-group:/aws/bedrock-agentcore/*",
                f"arn:aws:logs:{REGION}:{account_id}:log-group:*"
            ]
        },
        {
            "Sid": "XRayAccess",
            "Effect": "Allow",
            "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords",
                "xray:GetSamplingRules",
                "xray:GetSamplingTargets"
            ],
            "Resource": "*"
        },
        {
            "Sid": "GatewayAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock-agentcore:InvokeGateway",
                "bedrock-agentcore:GetGateway",
                "bedrock-agentcore:ListGatewayTargets"
            ],
            "Resource": f"arn:aws:bedrock-agentcore:{REGION}:{account_id}:*"
        },
        {
            "Sid": "ECRAccess",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CloudWatchMetrics",
            "Effect": "Allow",
            "Action": "cloudwatch:PutMetricData",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "cloudwatch:namespace": "bedrock-agentcore"
                }
            }
        },
        {
            "Sid": "WorkloadIdentityAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock-agentcore:GetWorkloadAccessToken",
                "bedrock-agentcore:GetWorkloadAccessTokenForJWT",
                "bedrock-agentcore:GetWorkloadAccessTokenForUserId"
            ],
            "Resource": [
                f"arn:aws:bedrock-agentcore:{REGION}:{account_id}:workload-identity-directory/default",
                f"arn:aws:bedrock-agentcore:{REGION}:{account_id}:workload-identity-directory/default/workload-identity/*"
            ]
        }
    ]
}

try:
    policy_response = iam_client.create_policy(
        PolicyName=POLICY_NAME,
        PolicyDocument=json.dumps(permissions_policy),
        Description="Full permissions for AgentCore Runtime including Memory, Gateway, and Knowledge Base"
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
    print()
except Exception as e:
    print(f"✗ Error attaching policy: {e}")
    print()

# Step 4: Wait for role to propagate
print("Step 4: Waiting for IAM propagation...")
print("-" * 80)

time.sleep(10)
print(f"✓ Role propagation complete")
print()

# Save configuration
print("Step 5: Saving configuration...")
print("-" * 80)

config = {
    "role_name": ROLE_NAME,
    "role_arn": role_arn,
    "policy_name": POLICY_NAME,
    "policy_arn": policy_arn,
    "region": REGION,
    "account_id": account_id
}

with open('runtime_execution_role_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"✓ Configuration saved to runtime_execution_role_config.json")
print()

# Summary
print("=" * 80)
print("RUNTIME EXECUTION ROLE SETUP COMPLETE")
print("=" * 80)
print()
print("Configuration Summary:")
print(f"  Role Name: {ROLE_NAME}")
print(f"  Role ARN: {role_arn}")
print()
print("Permissions Granted:")
print("  ✓ Bedrock - Model invocation (InvokeModel, InvokeModelWithResponseStream)")
print("  ✓ Memory - Full access (GetMemory, CreateEvent, RetrieveMemory, etc.)")
print("  ✓ Knowledge Base - Retrieve access (bedrock-agent:Retrieve)")
print("  ✓ CloudWatch Logs - Full logging (CreateLogGroup, PutLogEvents, etc.)")
print("  ✓ X-Ray - Distributed tracing (PutTraceSegments, PutTelemetryRecords)")
print("  ✓ Gateway - Full access (InvokeGateway, GetGateway, ListGatewayTargets)")
print("  ✓ ECR - Container image access (GetAuthorizationToken, BatchGetImage)")
print("  ✓ CloudWatch Metrics - Performance monitoring")
print("  ✓ Workload Identity - Secure credential management")
print()
print("✓ Role is ready for AgentCore Runtime deployment!")
