#!/usr/bin/env python3
"""
Script to create Lambda function for order lookup.

This script creates a Lambda function that looks up order details.
"""

import boto3
import json
import zipfile
import io
import time
from datetime import datetime, timedelta

# Configuration
REGION = 'us-west-2'
FUNCTION_NAME = 'OrderLookupFunction'

print("=" * 80)
print("CREATING LAMBDA FUNCTION FOR ORDER LOOKUP")
print("=" * 80)
print()

# Create clients
lambda_client = boto3.client('lambda', region_name=REGION)
iam_client = boto3.client('iam', region_name=REGION)
sts_client = boto3.client('sts', region_name=REGION)

# Get account ID
account_id = sts_client.get_caller_identity()['Account']

# Step 1: Create Lambda execution role
print("Step 1: Creating Lambda execution role...")
print("-" * 80)

lambda_role_name = 'OrderLookupLambdaRole'

# Trust policy for Lambda
lambda_trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    role_response = iam_client.create_role(
        RoleName=lambda_role_name,
        AssumeRolePolicyDocument=json.dumps(lambda_trust_policy),
        Description='Execution role for OrderLookupFunction'
    )
    lambda_role_arn = role_response['Role']['Arn']
    print(f"✓ Lambda role created: {lambda_role_name}")
    print(f"  ARN: {lambda_role_arn}")
    
    # Attach basic Lambda execution policy
    iam_client.attach_role_policy(
        RoleName=lambda_role_name,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    )
    print(f"✓ Attached AWSLambdaBasicExecutionRole policy")
    
    # Wait for role propagation
    print("  Waiting for IAM role propagation (10 seconds)...")
    time.sleep(10)
    
except iam_client.exceptions.EntityAlreadyExistsException:
    print(f"⚠️  Role {lambda_role_name} already exists, retrieving ARN...")
    role_response = iam_client.get_role(RoleName=lambda_role_name)
    lambda_role_arn = role_response['Role']['Arn']
    print(f"  ARN: {lambda_role_arn}")

print()

# Step 2: Create Lambda function code
print("Step 2: Creating Lambda function code...")
print("-" * 80)

# Calculate dates for mock data
today = datetime.now()
recent_date = (today - timedelta(days=15)).strftime('%Y-%m-%d')
old_date = (today - timedelta(days=45)).strftime('%Y-%m-%d')
defective_date = (today - timedelta(days=10)).strftime('%Y-%m-%d')

lambda_code = f'''
import json
from datetime import datetime

# Mock order database
ORDERS = {{
    "ORD-001": {{
        "order_id": "ORD-001",
        "product_name": "Dell XPS 15 Laptop",
        "category": "electronics",
        "purchase_date": "{recent_date}",
        "amount": 1299.99,
        "condition": "new",
        "status": "delivered",
        "eligible_for_return": True,
        "return_window_days": 30
    }},
    "ORD-002": {{
        "order_id": "ORD-002",
        "product_name": "iPhone 13",
        "category": "electronics",
        "purchase_date": "{old_date}",
        "amount": 799.99,
        "condition": "new",
        "status": "delivered",
        "eligible_for_return": False,
        "return_window_days": 30
    }},
    "ORD-003": {{
        "order_id": "ORD-003",
        "product_name": "Samsung Galaxy Tab",
        "category": "electronics",
        "purchase_date": "{defective_date}",
        "amount": 449.99,
        "condition": "defective",
        "status": "delivered",
        "eligible_for_return": True,
        "return_window_days": 30,
        "notes": "Customer reported screen defect"
    }}
}}

def lambda_handler(event, context):
    """
    Look up order details by order ID.
    
    Expected input format (from MCP Gateway):
    {{
        "order_id": "ORD-001"
    }}
    """
    try:
        # Extract order_id from event
        if isinstance(event, str):
            event = json.loads(event)
        
        order_id = event.get('order_id', '').upper()
        
        if not order_id:
            return {{
                'statusCode': 400,
                'body': json.dumps({{
                    'error': 'Missing order_id parameter'
                }})
            }}
        
        # Look up order
        order = ORDERS.get(order_id)
        
        if not order:
            return {{
                'statusCode': 404,
                'body': json.dumps({{
                    'error': f'Order {{order_id}} not found',
                    'available_orders': list(ORDERS.keys())
                }})
            }}
        
        # Calculate days since purchase
        purchase_date = datetime.strptime(order['purchase_date'], '%Y-%m-%d')
        days_since_purchase = (datetime.now() - purchase_date).days
        
        # Add calculated fields
        order['days_since_purchase'] = days_since_purchase
        order['days_remaining'] = max(0, order['return_window_days'] - days_since_purchase)
        
        return {{
            'statusCode': 200,
            'body': json.dumps(order)
        }}
        
    except Exception as e:
        return {{
            'statusCode': 500,
            'body': json.dumps({{
                'error': f'Internal error: {{str(e)}}'
            }})
        }}
'''

# Create ZIP file in memory
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.writestr('lambda_function.py', lambda_code)

zip_buffer.seek(0)
lambda_zip = zip_buffer.read()

print(f"✓ Lambda code created ({len(lambda_zip)} bytes)")
print(f"  Mock orders: ORD-001 (recent laptop), ORD-002 (old phone), ORD-003 (defective tablet)")
print()

# Step 3: Create Lambda function
print("Step 3: Creating Lambda function...")
print("-" * 80)

try:
    function_response = lambda_client.create_function(
        FunctionName=FUNCTION_NAME,
        Runtime='python3.12',
        Role=lambda_role_arn,
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': lambda_zip},
        Description='Look up order details by order ID',
        Timeout=30,
        MemorySize=128
    )
    
    function_arn = function_response['FunctionArn']
    print(f"✓ Lambda function created: {FUNCTION_NAME}")
    print(f"  ARN: {function_arn}")
    print(f"  Runtime: python3.12")
    print(f"  Handler: lambda_function.lambda_handler")
    
except lambda_client.exceptions.ResourceConflictException:
    print(f"⚠️  Function {FUNCTION_NAME} already exists, updating code...")
    
    # Update function code
    lambda_client.update_function_code(
        FunctionName=FUNCTION_NAME,
        ZipFile=lambda_zip
    )
    
    # Get function ARN
    function_response = lambda_client.get_function(FunctionName=FUNCTION_NAME)
    function_arn = function_response['Configuration']['FunctionArn']
    print(f"✓ Function code updated: {FUNCTION_NAME}")
    print(f"  ARN: {function_arn}")

print()

# Step 4: Create tool schema for MCP Gateway
print("Step 4: Creating tool schema...")
print("-" * 80)

tool_schema = {
    "name": "lookup_order",
    "description": "Look up order details by order ID. Returns order information including product name, purchase date, amount, and return eligibility.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order ID to look up (e.g., ORD-001, ORD-002, ORD-003)"
            }
        },
        "required": ["order_id"]
    }
}

print(f"✓ Tool schema created: lookup_order")
print(f"  Input: order_id (string)")
print(f"  Returns: order details with return eligibility")
print()

# Step 5: Save configuration
print("Step 5: Saving configuration...")
print("-" * 80)

config = {
    "function_name": FUNCTION_NAME,
    "function_arn": function_arn,
    "lambda_role_arn": lambda_role_arn,
    "region": REGION,
    "tool_schema": tool_schema,
    "sample_orders": ["ORD-001", "ORD-002", "ORD-003"]
}

with open('lambda_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"✓ Configuration saved to lambda_config.json")
print()

# Summary
print("=" * 80)
print("LAMBDA FUNCTION SETUP COMPLETE")
print("=" * 80)
print()
print("Configuration Summary:")
print(f"  Function Name: {FUNCTION_NAME}")
print(f"  Function ARN: {function_arn}")
print(f"  Tool Name: lookup_order")
print(f"  Sample Orders: ORD-001, ORD-002, ORD-003")
print()
print("✓ Lambda function is ready to be connected to gateway!")
print("✓ Test with order IDs: ORD-001, ORD-002, or ORD-003")
