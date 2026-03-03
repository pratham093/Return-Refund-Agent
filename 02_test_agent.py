"""
Test script for returns_refunds_agent
Tests all 5 tools with realistic customer queries
"""

import importlib.util
import sys
from pathlib import Path

# Import run_agent from 01_returns_refunds_agent.py using importlib
agent_file = Path("01_returns_refunds_agent.py")
spec = importlib.util.spec_from_file_location("returns_refunds_agent", agent_file)
agent_module = importlib.util.module_from_spec(spec)
sys.modules["returns_refunds_agent"] = agent_module
spec.loader.exec_module(agent_module)

# Import the run_agent function
run_agent = agent_module.run_agent

def test_agent():
    """Run test queries against the returns agent"""
    
    test_queries = [
        {
            "name": "Test 1: Current Time",
            "query": "What time is it?"
        },
        {
            "name": "Test 2: Return Eligibility",
            "query": "Can I return a laptop I purchased 25 days ago?"
        },
        {
            "name": "Test 3: Refund Calculation",
            "query": "Calculate my refund for a $500 item returned due to defect in like-new condition"
        },
        {
            "name": "Test 4: Policy Explanation",
            "query": "Explain the return policy for electronics in a simple way"
        },
        {
            "name": "Test 5: Knowledge Base Retrieval",
            "query": "Use the retrieve tool to search the knowledge base for 'Amazon return policy for electronics'"
        }
    ]
    
    print("=" * 80)
    print("TESTING RETURNS & REFUNDS AGENT")
    print("=" * 80)
    print()
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'=' * 80}")
        print(f"{test['name']}")
        print(f"{'=' * 80}")
        print(f"Query: {test['query']}")
        print(f"\n{'-' * 80}")
        print("Agent Response:")
        print(f"{'-' * 80}\n")
        
        try:
            response = run_agent(test['query'])
            print(response)
            print(f"\n✓ Test {i} completed successfully")
        except Exception as e:
            print(f"✗ Test {i} failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print("=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_agent()
