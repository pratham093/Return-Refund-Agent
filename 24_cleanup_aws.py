#!/usr/bin/env python3
"""
Script to safely delete all AWS resources created in the workshop.

WARNING: This permanently deletes all resources. Make sure you've saved any important data!
"""

import json
import boto3
import time
import os

REGION = "us-west-2"

print("=" * 80)
print("AWS RESOURCE CLEANUP")
print("=" * 80)
print("\n⚠️  WARNING: This will delete all AWS resources created in the workshop:")
print("  - Runtime agent (deployed agent)")
print("  - Gateway and targets")
print("  - Memory resource")
print("  - Lambda function")
print("  - Cognito user pool and domain")
print("  - IAM roles and policies")
print("  - ECR repository")
print("\nThis action CANNOT be undone!")
print("\n⏱️  Countdown: 5 seconds to cancel (Ctrl+C)...")

for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("\nStarting cleanup...\n")

# Initialize clients
bedrock_agentcore = boto3.client('bedrock-agentcore-control', region_name=REGION)
cognito = boto3.client('cognito-idp', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)
iam_client = boto3.client('iam', region_name=REGION)
ecr_client = boto3.client('ecr', region_name=REGION)

# Step 1: Delete Runtime Agent
print("Step 1: Deleting runtime agent...")
print("-" * 80)
try:
    if os.path.exists('runtime_config.json'):
        with open('runtime_config.json') as f:
            runtime_config = json.load(f)
        agent_arn = runtime_config['agent_arn']
        agent_id = agent_arn.split('/')[-1]
        
        bedrock_agentcore.delete_agent_runtime(agentRuntimeId=agent_id)
        print(f"✓ Runtime agent deleted: {agent_id}")
    else:
        print("⚠️  No runtime config found, skipping")
except Exception as e:
    print(f"⚠️  Error deleting runtime agent: {e}")
print()

# Step 2: Delete Gateway Targets
print("Step 2: Deleting gateway targets...")
print("-" * 80)
try:
    if os.path.exists('gateway_config.json'):
        with open('gateway_config.json') as f:
            gateway_config = json.load(f)
        gateway_id = gateway_config['gateway_id']
        
        # List and delete all targets
        targets_response = bedrock_agentcore.list_gateway_targets(gatewayIdentifier=gateway_id)
        for target in targets_response.get('targets', []):
            target_id = target['id']
            bedrock_agentcore.delete_gateway_target(
                gatewayIdentifier=gateway_id,
                targetId=target_id
            )
            print(f"✓ Gateway target deleted: {target_id}")
        
        if not targets_response.get('targets'):
            print("⚠️  No gateway targets found")
    else:
        print("⚠️  No gateway config found, skipping")
except Exception as e:
    print(f"⚠️  Error deleting gateway targets: {e}")
print()

# Wait for targets to be fully deleted
print("Waiting 5 seconds for targets to be fully deleted...")
time.sleep(5)

# Step 3: Delete Gateway
print("Step 3: Deleting gateway...")
print("-" * 80)
try:
    if os.path.exists('gateway_config.json'):
        with open('gateway_config.json') as f:
            gateway_config = json.load(f)
        gateway_id = gateway_config['gateway_id']
        
        bedrock_agentcore.delete_gateway(gatewayIdentifier=gateway_id)
        print(f"✓ Gateway deleted: {gateway_id}")
    else:
        print("⚠️  No gateway config found, skipping")
except Exception as e:
    print(f"⚠️  Error deleting gateway: {e}")
print()

# Step 4: Delete Memory
print("Step 4: Deleting memory...")
print("-" * 80)
try:
    if os.path.exists('memory_config.json'):
        with open('memory_config.json') as f:
            memory_config = json.load(f)
        memory_id = memory_config['memory_id']
        
        bedrock_agentcore.delete_memory(memoryId=memory_id)
        print(f"✓ Memory deleted: {memory_id}")
    else:
        print("⚠️  No memory config found, skipping")
except Exception as e:
    print(f"⚠️  Error deleting memory: {e}")
print()

# Step 5: Delete Lambda Function
print("Step 5: Deleting Lambda function...")
print("-" * 80)
try:
    if os.path.exists('lambda_config.json'):
        with open('lambda_config.json') as f:
            lambda_config = json.load(f)
        function_arn = lambda_config['function_arn']
        function_name = function_arn.split(':')[-1]
        
        lambda_client.delete_function(FunctionName=function_name)
        print(f"✓ Lambda function deleted: {function_name}")
    else:
        print("⚠️  No Lambda config found, skipping")
except Exception as e:
    print(f"⚠️  Error deleting Lambda: {e}")
print()

# Step 6: Delete Cognito Domain
print("Step 6: Deleting Cognito domain...")
print("-" * 80)
try:
    if os.path.exists('cognito_config.json'):
        with open('cognito_config.json') as f:
            cognito_config = json.load(f)
        domain_prefix = cognito_config['domain_prefix']
        user_pool_id = cognito_config['user_pool_id']
        
        cognito.delete_user_pool_domain(
            Domain=domain_prefix,
            UserPoolId=user_pool_id
        )
        print(f"✓ Cognito domain deleted: {domain_prefix}")
        
        # Wait for domain deletion
        print("Waiting 10 seconds for domain deletion...")
        time.sleep(10)
    else:
        print("⚠️  No Cognito config found, skipping")
except Exception as e:
    print(f"⚠️  Error deleting Cognito domain: {e}")
print()

# Step 7: Delete Cognito User Pool
print("Step 7: Deleting Cognito user pool...")
print("-" * 80)
try:
    if os.path.exists('cognito_config.json'):
        with open('cognito_config.json') as f:
            cognito_config = json.load(f)
        user_pool_id = cognito_config['user_pool_id']
        
        cognito.delete_user_pool(UserPoolId=user_pool_id)
        print(f"✓ Cognito user pool deleted: {user_pool_id}")
    else:
        print("⚠️  No Cognito config found, skipping")
except Exception as e:
    print(f"⚠️  Error deleting Cognito user pool: {e}")
print()

# Step 8: Delete IAM Roles and Policies
print("Step 8: Deleting IAM roles and policies...")
print("-" * 80)

# Delete Gateway Role
try:
    if os.path.exists('gateway_role_config.json'):
        with open('gateway_role_config.json') as f:
            role_config = json.load(f)
        role_name = role_config['role_name']
        
        # Detach policies
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
        for policy in attached_policies['AttachedPolicies']:
            iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        
        # Delete inline policies
        inline_policies = iam_client.list_role_policies(RoleName=role_name)
        for policy_name in inline_policies['PolicyNames']:
            iam_client.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
        
        # Delete role
        iam_client.delete_role(RoleName=role_name)
        print(f"✓ Gateway role deleted: {role_name}")
except Exception as e:
    print(f"⚠️  Error deleting gateway role: {e}")

# Delete Runtime Execution Role
try:
    if os.path.exists('runtime_execution_role_config.json'):
        with open('runtime_execution_role_config.json') as f:
            role_config = json.load(f)
        role_name = role_config['role_name']
        policy_arn = role_config['policy_arn']
        
        # Detach policy
        iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        
        # Delete role
        iam_client.delete_role(RoleName=role_name)
        print(f"✓ Runtime execution role deleted: {role_name}")
        
        # Delete policy
        iam_client.delete_policy(PolicyArn=policy_arn)
        print(f"✓ Runtime execution policy deleted")
except Exception as e:
    print(f"⚠️  Error deleting runtime role: {e}")

# Delete Lambda Execution Role
try:
    lambda_role_name = "LambdaOrderLookupRole"
    
    # Detach policies
    attached_policies = iam_client.list_attached_role_policies(RoleName=lambda_role_name)
    for policy in attached_policies['AttachedPolicies']:
        iam_client.detach_role_policy(RoleName=lambda_role_name, PolicyArn=policy['PolicyArn'])
    
    # Delete role
    iam_client.delete_role(RoleName=lambda_role_name)
    print(f"✓ Lambda execution role deleted: {lambda_role_name}")
except Exception as e:
    print(f"⚠️  Error deleting Lambda role: {e}")

# Delete CodeBuild Role
try:
    codebuild_roles = iam_client.list_roles()
    for role in codebuild_roles['Roles']:
        if 'AmazonBedrockAgentCoreSDKCodeBuild' in role['RoleName']:
            role_name = role['RoleName']
            
            # Detach policies
            attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
            for policy in attached_policies['AttachedPolicies']:
                iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
            
            # Delete inline policies
            inline_policies = iam_client.list_role_policies(RoleName=role_name)
            for policy_name in inline_policies['PolicyNames']:
                iam_client.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
            
            # Delete role
            iam_client.delete_role(RoleName=role_name)
            print(f"✓ CodeBuild role deleted: {role_name}")
except Exception as e:
    print(f"⚠️  Error deleting CodeBuild role: {e}")

print()

# Step 9: Delete ECR Repository
print("Step 9: Deleting ECR repository...")
print("-" * 80)
try:
    repo_name = "bedrock-agentcore-returns_refunds_agent"
    ecr_client.delete_repository(repositoryName=repo_name, force=True)
    print(f"✓ ECR repository deleted: {repo_name}")
except Exception as e:
    print(f"⚠️  Error deleting ECR repository: {e}")
print()

# Summary
print("=" * 80)
print("AWS CLEANUP COMPLETE")
print("=" * 80)
print("\n✓ All AWS resources have been deleted")
print("\nNote: Some resources may take a few minutes to fully delete")
print("You can verify deletion in the AWS Console")
