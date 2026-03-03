# AgentCore Workshop: Returns & Refunds Agent

This repository contains all the code and configurations from the AgentCore workshop where we built a production-ready returns and refunds AI agent using **vibe coding** - generating all code through natural language prompts with Kiro.

## 🎯 What Was Built

A complete, production-ready returns and refunds assistant with:
- ✅ Custom tools for returns processing (eligibility checks, refund calculations, policy formatting)
- ✅ Memory to remember customer preferences and history
- ✅ External order lookup via Lambda through AgentCore Gateway
- ✅ Knowledge Base integration for Amazon return policy documents
- ✅ Production deployment on AgentCore Runtime
- ✅ Full observability with CloudWatch monitoring

## 📁 Repository Structure

```
.
├── 01_returns_refunds_agent.py          # Initial agent with custom tools + KB
├── 02_test_agent.py                     # Test script for initial agent
├── 03_create_memory.py                  # Create AgentCore Memory
├── 04_seed_memory.py                    # Seed memory with sample data
├── 05_test_memory.py                    # Test memory retrieval
├── 06_memory_enabled_agent.py           # Agent with memory integration
├── 07_test_memory_agent.py              # Test memory-enabled agent
├── 08_create_cognito.py                 # Create Cognito for authentication
├── 09_create_gateway_role.py            # Create IAM role for gateway
├── 10_create_lambda.py                  # Create Lambda for order lookup
├── 11_create_gateway.py                 # Create AgentCore Gateway
├── 12_add_lambda_to_gateway.py          # Register Lambda with gateway
├── 13_list_gateway_targets.py           # Verify gateway targets
├── 14_full_agent.py                     # Complete agent (all features)
├── 15_test_full_agent.py                # Test complete agent
├── 16_create_runtime_role.py            # Create IAM role for runtime
├── 17_runtime_agent.py                  # Runtime-ready agent
├── 19_deploy_agent.py                   # Deploy to AgentCore Runtime
├── 20_check_status.py                   # Check deployment status
├── 21_invoke_agent.py                   # Invoke production agent
├── 22_get_dashboard.py                  # Get observability dashboard URL
├── 23_get_logs_info.py                  # Get CloudWatch logs info
├── 24_cleanup_aws.py                    # Delete all AWS resources
├── 25_cleanup_files.py                  # Delete all local files
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Docker configuration for runtime
├── .bedrock_agentcore.yaml              # AgentCore runtime configuration
├── agentcore-mcp-server/                # MCP server implementation
├── agentcore-workflow/                  # Workshop guide and prompts
└── *.json                               # Configuration files
```

## 🔧 Configuration Files

All AWS resource IDs and configurations are stored in JSON files:

- `memory_config.json` - Memory ID
- `cognito_config.json` - Cognito User Pool, Client ID, secrets
- `gateway_config.json` - Gateway ID and URL
- `gateway_role_config.json` - Gateway IAM role ARN
- `lambda_config.json` - Lambda function ARN and tool schema
- `kb_config.json` - Knowledge Base ID
- `runtime_execution_role_config.json` - Runtime IAM role ARN
- `runtime_config.json` - Deployed agent ARN

## 🚀 Current Deployment

**Agent Status:** READY ✅

**Deployed Resources:**
- **Agent ARN:** `arn:aws:bedrock-agentcore:us-west-2:571806540395:runtime/returns_refunds_agent-2nwntDCSqF`
- **Memory ID:** `returns_refunds_memory-uOuluz6smV`
- **Gateway ID:** `returnsrefundsgateway-uxgokboiyh`
- **Gateway URL:** `https://returnsrefundsgateway-uxgokboiyh.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp`
- **Knowledge Base ID:** `ZR9PWNFZPW`
- **Region:** `us-west-2`

## 📊 Monitoring & Observability

**CloudWatch Dashboard:**
```
https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core
```

**View Logs:**
```bash
# Tail logs in real-time
aws logs tail /aws/bedrock-agentcore/runtimes/returns_refunds_agent-2nwntDCSqF-DEFAULT \
  --log-stream-name-prefix "2026/03/03/[runtime-logs]" --follow

# View recent logs (last hour)
aws logs tail /aws/bedrock-agentcore/runtimes/returns_refunds_agent-2nwntDCSqF-DEFAULT \
  --log-stream-name-prefix "2026/03/03/[runtime-logs]" --since 1h
```

## 🧪 Testing the Agent

**Test locally (before deployment):**
```bash
python3 15_test_full_agent.py
```

**Test production agent:**
```bash
python3 21_invoke_agent.py
```

**Check deployment status:**
```bash
python3 20_check_status.py
```

## 🛠️ Agent Capabilities

### Custom Tools
1. **check_return_eligibility** - Checks if items can be returned based on purchase date and category
2. **calculate_refund_amount** - Calculates refund based on price, condition, and return reason
3. **format_policy_response** - Formats policy info in a customer-friendly way
4. **current_time** - Gets current date/time
5. **retrieve** - Searches Knowledge Base for Amazon return policy documents

### Gateway Tools
- **lookup_order** - Looks up order details from Lambda (ORD-001, ORD-002, ORD-003)

### Memory Integration
- **Semantic Memory** - Stores factual details about customer interactions
- **Preferences Memory** - Captures customer preferences (e.g., "prefers email")
- **Summary Memory** - Maintains conversation context and summaries

### Knowledge Base
- Access to Amazon return policy documents
- Semantic search for accurate policy information

## 📦 Dependencies

```
strands-agents
strands-agents-tools
bedrock-agentcore
boto3
requests
```

## 🔐 AWS Permissions Required

The agent has the following permissions:
- Bedrock model invocation (Claude Sonnet 4.5)
- AgentCore Memory access (GetMemory, CreateEvent, RetrieveMemory)
- Knowledge Base access (Retrieve)
- Gateway access (InvokeGateway, GetGateway, ListGatewayTargets)
- CloudWatch Logs (CreateLogGroup, PutLogEvents)
- X-Ray tracing (PutTraceSegments, PutTelemetryRecords)
- ECR access (GetAuthorizationToken, BatchGetImage)

## 🧹 Cleanup

**Delete all AWS resources:**
```bash
python3 24_cleanup_aws.py
```
⚠️ This permanently deletes: Runtime agent, Gateway, Memory, Lambda, Cognito, IAM roles, ECR repository

**Delete all local files:**
```bash
python3 25_cleanup_files.py
```
⚠️ This permanently deletes all Python scripts and config files

## 📚 Workshop Guide

The complete workshop guide with all prompts is available in:
```
agentcore-workflow/prompts.md
```

This guide contains all 25 prompts used to build the agent through vibe coding.

## 🎓 What You Learned

1. **Strands Agents** - Building AI agents with custom tools
2. **AgentCore Memory** - Persistent customer memory across sessions
3. **AgentCore Gateway** - Secure integration with external services
4. **Knowledge Base** - Semantic search for policy documents
5. **AgentCore Runtime** - Serverless production deployment
6. **Observability** - CloudWatch monitoring and tracing
7. **Vibe Coding** - Building production code through natural language

## 🔗 Useful Links

- [Strands Agents Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/strands-agents.html)
- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [AgentCore Runtime Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html)

## 💡 Key Takeaways

- **Zero Manual Coding** - All code generated through natural language prompts
- **Production Ready** - Deployed agent handles real customer queries
- **Full Stack** - Memory, external tools, knowledge base, monitoring
- **Scalable** - Serverless runtime auto-scales with demand
- **Observable** - Complete visibility into agent behavior

## 📝 Notes

- All resources are deployed in `us-west-2` region
- Agent uses Claude Sonnet 4.5 model
- Memory processing takes ~30 seconds after storing conversations
- Gateway targets may take a few seconds to show due to AWS eventual consistency

---

**Built with:** Amazon Bedrock AgentCore, Strands Agents, AWS Lambda, Cognito, CloudWatch

**Workshop Date:** March 3, 2026

**Status:** ✅ Production Deployed & Tested
