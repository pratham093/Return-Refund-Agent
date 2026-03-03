#!/usr/bin/env python3
"""
Script to configure and launch agent to AgentCore Runtime.

This creates a CodeBuild pipeline, builds Docker container, pushes to ECR,
and deploys to runtime. Process takes 5-10 minutes.
"""

import json
import os
from bedrock_agentcore_starter_toolkit import Runtime

# Load configuration files
print("Loading configuration files...")
with open('memory_config.json') as f:
    memory_config = json.load(f)
with open('gateway_config.json') as f:
    gateway_config = json.load(f)
with open('cognito_config.json') as f:
    cognito_config = json.load(f)
with open('kb_config.json') as f:
    kb_config = json.load(f)
with open('runtime_execution_role_config.json') as f:
    role_config = json.load(f)

print("✓ All configuration files loaded")

# Initialize Runtime
runtime = Runtime()

# Build authorizer configuration for Cognito JWT
auth_config = {
    "customJWTAuthorizer": {
        "allowedClients": [cognito_config["client_id"]],
        "discoveryUrl": cognito_config["discovery_url"]
    }
}

# Configure runtime deployment
print("\nConfiguring AgentCore Runtime...")
runtime.configure(
    entrypoint="17_runtime_agent.py",
    agent_name="returns_refunds_agent",
    execution_role=role_config["role_arn"],
    auto_create_ecr=True,
    memory_mode="NO_MEMORY",
    requirements_file="requirements.txt",
    region="us-west-2",
    authorizer_configuration=auth_config
)
print("✓ Runtime configured successfully!")

# Build environment variables
env_vars = {
    "MEMORY_ID": memory_config["memory_id"],
    "KNOWLEDGE_BASE_ID": kb_config["knowledge_base_id"],
    "GATEWAY_URL": gateway_config["gateway_url"],
    "COGNITO_CLIENT_ID": cognito_config["client_id"],
    "COGNITO_CLIENT_SECRET": cognito_config["client_secret"],
    "COGNITO_DISCOVERY_URL": cognito_config["discovery_url"],
    "OAUTH_SCOPES": "returns-gateway-api/read returns-gateway-api/write returns-gateway-api/invoke"
}

print("\nEnvironment variables configured:")
for key in env_vars:
    if "SECRET" in key:
        print(f"  {key}: ***")
    else:
        print(f"  {key}: {env_vars[key]}")

# Launch agent
print("\n" + "=" * 80)
print("LAUNCHING AGENT TO AGENTCORE RUNTIME")
print("=" * 80)
print("\nThis process will:")
print("  1. Create CodeBuild project")
print("  2. Build Docker container from your agent code")
print("  3. Push container to Amazon ECR")
print("  4. Deploy to AgentCore Runtime")
print("\n⏱️  Expected time: 5-10 minutes")
print("\n☕ Grab a coffee while the deployment runs...")
print("=" * 80)

launch_result = runtime.launch(
    env_vars=env_vars,
    auto_update_on_conflict=True
)

agent_arn = launch_result.agent_arn

# Save agent ARN to config
runtime_output_config = {
    "agent_arn": agent_arn,
    "agent_name": "returns_refunds_agent",
    "region": "us-west-2",
    "memory_id": memory_config["memory_id"],
    "gateway_url": gateway_config["gateway_url"]
}

with open('runtime_config.json', 'w') as f:
    json.dump(runtime_output_config, f, indent=2)

print(f"\n✓ Agent deployment initiated!")
print(f"  Agent ARN: {agent_arn}")
print(f"✓ Configuration saved to runtime_config.json")
print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("\n1. Monitor deployment status:")
print("   Run: python 20_check_status.py")
print("\n2. Wait for status to show 'READY' (may take 5-10 minutes)")
print("\n3. Once READY, test your agent:")
print("   Run: python 21_invoke_agent.py")
print("\n" + "=" * 80)
