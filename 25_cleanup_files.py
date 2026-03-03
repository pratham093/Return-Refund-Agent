#!/usr/bin/env python3
"""
Script to clean up all local workshop files.

WARNING: This deletes all Python scripts and config files created during the workshop!
"""

import os
import time

print("=" * 80)
print("LOCAL FILE CLEANUP")
print("=" * 80)
print("\n⚠️  WARNING: This will delete all local workshop files:")
print("  - All Python scripts (01-25)")
print("  - All config JSON files")
print("  - Runtime configuration files")
print("  - Docker files")
print("  - Requirements file")
print("\nThis action CANNOT be undone!")
print("\n⏱️  Countdown: 5 seconds to cancel (Ctrl+C)...")

for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("\nStarting cleanup...\n")

deleted_count = 0

# Step 1: Delete Python scripts
print("Step 1: Deleting Python scripts...")
print("-" * 80)
python_files = [
    '01_returns_refunds_agent.py',
    '02_test_agent.py',
    '03_create_memory.py',
    '04_seed_memory.py',
    '05_test_memory.py',
    '06_memory_enabled_agent.py',
    '07_test_memory_agent.py',
    '08_create_cognito.py',
    '09_create_gateway_role.py',
    '10_create_lambda.py',
    '11_create_gateway.py',
    '12_add_lambda_to_gateway.py',
    '13_list_gateway_targets.py',
    '14_full_agent.py',
    '15_test_full_agent.py',
    '16_create_runtime_role.py',
    '17_runtime_agent.py',
    '19_deploy_agent.py',
    '20_check_status.py',
    '21_invoke_agent.py',
    '22_get_dashboard.py',
    '23_get_logs_info.py',
    '24_cleanup_aws.py',
    '25_cleanup_files.py'
]

for file in python_files:
    try:
        if os.path.exists(file):
            os.remove(file)
            deleted_count += 1
            print(f"✓ Deleted: {file}")
    except Exception as e:
        print(f"⚠️  Error deleting {file}: {e}")

print(f"\n✓ Deleted {deleted_count} Python files")
print()

# Step 2: Delete config JSON files
print("Step 2: Deleting config files...")
print("-" * 80)
config_files = [
    'memory_config.json',
    'cognito_config.json',
    'gateway_role_config.json',
    'lambda_config.json',
    'gateway_config.json',
    'kb_config.json',
    'runtime_execution_role_config.json',
    'runtime_config.json'
]

config_count = 0
for file in config_files:
    try:
        if os.path.exists(file):
            os.remove(file)
            config_count += 1
            print(f"✓ Deleted: {file}")
    except Exception as e:
        print(f"⚠️  Error deleting {file}: {e}")

print(f"\n✓ Deleted {config_count} config files")
print()

# Step 3: Delete runtime files
print("Step 3: Deleting runtime files...")
print("-" * 80)
runtime_files = [
    '.bedrock_agentcore.yaml',
    'Dockerfile',
    '.dockerignore',
    'requirements.txt'
]

runtime_count = 0
for file in runtime_files:
    try:
        if os.path.exists(file):
            os.remove(file)
            runtime_count += 1
            print(f"✓ Deleted: {file}")
    except Exception as e:
        print(f"⚠️  Error deleting {file}: {e}")

print(f"\n✓ Deleted {runtime_count} runtime files")
print()

# Summary
print("=" * 80)
print("LOCAL CLEANUP COMPLETE")
print("=" * 80)
print(f"\n✓ Total files deleted: {deleted_count + config_count + runtime_count}")
print("\nYour workspace is now clean and ready for the next workshop!")
print("\nNote: The following were preserved:")
print("  - agentcore-mcp-server/ (MCP server code)")
print("  - agentcore-workflow/ (workshop guide)")
