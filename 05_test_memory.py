#!/usr/bin/env python3
"""
Script to test memory retrieval from AgentCore Memory.

This script retrieves and displays what the agent remembers about user_001.
"""

import json

try:
    from bedrock_agentcore.memory import MemoryClient
except ImportError:
    print("✗ Error: bedrock_agentcore package not found")
    print("  Install with: pip install bedrock-agentcore")
    exit(1)

# Load memory_id from config
with open('memory_config.json') as f:
    config = json.load(f)
    memory_id = config['memory_id']

print("=" * 80)
print("TESTING MEMORY RETRIEVAL FOR USER_001")
print("=" * 80)
print(f"\nUsing Memory ID: {memory_id}")
print()

# Create memory client
memory_client = MemoryClient(region_name='us-west-2')

# Test 1: Retrieve from preferences namespace
print("=" * 80)
print("TEST 1: Retrieving from PREFERENCES namespace")
print("=" * 80)
print(f"Namespace: app/user_001/preferences")
print(f"Search query: 'customer preferences and communication'")
print(f"Top K: 3")
print()

try:
    preferences = memory_client.retrieve_memories(
        memory_id=memory_id,
        namespace="app/user_001/preferences",
        query="customer preferences and communication",
        top_k=3
    )
    
    if preferences:
        print(f"✓ Retrieved {len(preferences)} preference memories")
        print()
        
        for i, memory in enumerate(preferences, 1):
            print(f"Preference Memory {i}:")
            print("─" * 80)
            content = memory.get('content', {})
            if isinstance(content, dict):
                text = content.get('text', 'N/A')
            else:
                text = str(content)
            print(f"Content: {text}")
            
            relevance = memory.get('relevanceScore', 'N/A')
            if isinstance(relevance, (int, float)):
                print(f"Relevance Score: {relevance:.3f}")
            else:
                print(f"Relevance Score: {relevance}")
            print()
    else:
        print("⚠️  No preference memories found yet")
        print("   (Memory extraction may still be processing)")
        print()
        
except Exception as e:
    print(f"❌ Error retrieving preferences: {e}")
    print()

# Test 2: Retrieve from semantic namespace
print("=" * 80)
print("TEST 2: Retrieving from SEMANTIC namespace")
print("=" * 80)
print(f"Namespace: app/user_001/semantic")
print(f"Search query: 'return history and laptop'")
print(f"Top K: 3")
print()

try:
    semantic = memory_client.retrieve_memories(
        memory_id=memory_id,
        namespace="app/user_001/semantic",
        query="return history and laptop",
        top_k=3
    )
    
    if semantic:
        print(f"✓ Retrieved {len(semantic)} semantic memories")
        print()
        
        for i, memory in enumerate(semantic, 1):
            print(f"Semantic Memory {i}:")
            print("─" * 80)
            content = memory.get('content', {})
            if isinstance(content, dict):
                text = content.get('text', 'N/A')
            else:
                text = str(content)
            print(f"Content: {text}")
            
            relevance = memory.get('relevanceScore', 'N/A')
            if isinstance(relevance, (int, float)):
                print(f"Relevance Score: {relevance:.3f}")
            else:
                print(f"Relevance Score: {relevance}")
            print()
    else:
        print("⚠️  No semantic memories found yet")
        print("   (Memory extraction may still be processing)")
        print()
        
except Exception as e:
    print(f"❌ Error retrieving semantic memories: {e}")
    print()

# Summary
print("=" * 80)
print("MEMORY RETRIEVAL TEST COMPLETE")
print("=" * 80)
print("\nWhat the agent remembers about user_001:")
print("  • Check preferences namespace for: email notification preferences")
print("  • Check semantic namespace for: defective laptop return history")
print("  • Check semantic namespace for: interest in electronics return windows")
