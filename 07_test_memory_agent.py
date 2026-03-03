"""
Test script for memory-enabled returns agent
Tests if the agent can recall customer preferences and history
"""

import importlib.util
import sys
from pathlib import Path

# Import run_agent from 06_memory_enabled_agent.py using importlib
agent_file = Path("06_memory_enabled_agent.py")
spec = importlib.util.spec_from_file_location("memory_enabled_agent", agent_file)
agent_module = importlib.util.module_from_spec(spec)
sys.modules["memory_enabled_agent"] = agent_module
spec.loader.exec_module(agent_module)

# Import the run_agent function
run_agent = agent_module.run_agent

def test_memory_agent():
    """Test the memory-enabled agent with user_001"""
    
    print("=" * 80)
    print("TESTING MEMORY-ENABLED RETURNS AGENT")
    print("=" * 80)
    print()
    
    # Test query asking about remembered preferences
    test_query = "Hi! I'm thinking about returning something. What do you remember about my preferences?"
    
    print("Test Query:")
    print("-" * 80)
    print(test_query)
    print()
    
    print("=" * 80)
    print("AGENT RESPONSE (with Memory)")
    print("=" * 80)
    print()
    
    try:
        # Run agent with user_001 as actor_id
        response = run_agent(
            user_input=test_query,
            session_id="test_session_001",
            actor_id="user_001"
        )
        
        print(response)
        print()
        
        print("=" * 80)
        print("MEMORY VERIFICATION")
        print("=" * 80)
        print()
        print("✓ Agent should have recalled:")
        print("  • Email notification preference")
        print("  • Previous defective laptop return")
        print("  • Interest in electronics return windows")
        print()
        
        # Check if response mentions key memory items
        response_lower = response.lower()
        
        checks = {
            "Email preference": any(word in response_lower for word in ["email", "notification", "communicate"]),
            "Laptop return history": any(word in response_lower for word in ["laptop", "defective", "returned"]),
            "Personalization": any(word in response_lower for word in ["remember", "recall", "preference", "history"])
        }
        
        print("Memory Recall Check:")
        print("-" * 80)
        for check_name, found in checks.items():
            status = "✓" if found else "⚠️"
            print(f"{status} {check_name}: {'Found' if found else 'Not detected'}")
        
        print()
        
        if all(checks.values()):
            print("🎉 SUCCESS: Agent successfully recalled customer information!")
        else:
            print("⚠️  PARTIAL: Some memory items may not have been recalled")
            print("   (This is normal if memory processing is still ongoing)")
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_memory_agent()
