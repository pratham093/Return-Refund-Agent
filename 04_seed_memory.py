#!/usr/bin/env python3
"""
Script to seed AgentCore Memory with sample customer conversations.

This script adds sample conversations to test memory functionality.
"""

import json
import time

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

print(f"Using Memory ID: {memory_id}")
print("=" * 80)

# Create memory client
memory_client = MemoryClient(region_name='us-west-2')

# Conversation 1: Customer mentions email preference and previous laptop return
print("\n📝 Storing Conversation 1: Email preferences and laptop return history")
print("-" * 80)

messages_1 = [
    (
        "Hi, I prefer to receive email notifications for all my orders and returns. By the way, I previously returned a defective laptop last month and the process was smooth.",
        "USER"
    ),
    (
        "Thank you for letting me know! I've noted that you prefer email notifications. I'm glad your previous laptop return went smoothly. Is there anything I can help you with today regarding returns or refunds?",
        "ASSISTANT"
    )
]

memory_client.create_event(
    memory_id=memory_id,
    actor_id="user_001",
    session_id="session_001",
    messages=messages_1
)

print(f"✓ Stored {len(messages_1)} messages from conversation 1")

# Conversation 2: Customer asks about return windows for electronics
print("\n📝 Storing Conversation 2: Return window inquiry")
print("-" * 80)

messages_2 = [
    (
        "I'm thinking about buying a new tablet. What's the return window for electronics if I change my mind?",
        "USER"
    ),
    (
        "Great question! For electronics like tablets, you typically have a 30-day return window from the delivery date. The item must be in its original condition with all accessories and packaging. Would you like more details about the return process?",
        "ASSISTANT"
    )
]

memory_client.create_event(
    memory_id=memory_id,
    actor_id="user_001",
    session_id="session_002",
    messages=messages_2
)

print(f"✓ Stored {len(messages_2)} messages from conversation 2")

# Summary
print("\n" + "=" * 80)
print(f"✓ Successfully stored {len(messages_1) + len(messages_2)} total messages for user_001")
print("=" * 80)

# Wait for memory processing
print("\n⏳ Waiting 30 seconds for memory processing...")
print("   (Memory system extracts preferences, facts, and summaries)")
for i in range(30, 0, -5):
    print(f"   {i} seconds remaining...")
    time.sleep(5)

print("\n✓ Memory processing complete!")
print("\nMemory should now contain:")
print("  • Preference: User prefers email notifications")
print("  • Fact: Previously returned a defective laptop")
print("  • Fact: Interested in electronics return windows")
print("  • Summary: Conversation context about returns and preferences")
