import streamlit as st
import json
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="Returns & Refunds Agent", page_icon="🛒", layout="centered")

st.title("🛒 Returns & Refunds Agent")
st.caption("Powered by Llama 3.2 via Groq")

MODEL = "llama-3.3-70b-versatile"

# ============================================================================
# TOOLS
# ============================================================================

def check_return_eligibility(purchase_date: str, category: str) -> str:
    try:
        purchase = datetime.strptime(purchase_date, "%Y-%m-%d")
        days = (datetime.now() - purchase).days
        windows = {"electronics": 30, "clothing": 60, "books": 30, "home": 90, "toys": 90}
        window = windows.get(category.lower(), 30)
        if days <= window:
            return f"Eligible for return. Purchased {days} days ago. {category.title()} have a {window}-day window. {window - days} days remaining."
        return f"Not eligible. Purchased {days} days ago, exceeds the {window}-day window for {category}."
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD."


def calculate_refund_amount(price: float, condition: str, return_reason: str) -> str:
    cond = {"new": 1.0, "like-new": 1.0, "used": 0.8, "damaged": 0.5}.get(condition.lower(), 0.8)
    reason = {"defect": 1.0, "wrong-item": 1.0, "damaged-shipping": 1.0, "changed-mind": 0.9}.get(return_reason.lower(), 0.9)
    refund = price * cond * reason
    result = f"Refund amount: ${refund:.2f} (Original: ${price:.2f})"
    if cond < 1.0:
        result += f"\nCondition adjustment: {cond * 100:.0f}%"
    if reason < 1.0:
        result += f"\nRestocking fee: {(1 - reason) * 100:.0f}%"
    return result


def lookup_order(order_id: str) -> str:
    orders = {
        "ORD-001": {"order_id": "ORD-001", "customer": "John Doe", "item": "Wireless Headphones", "category": "electronics", "price": 79.99, "date": "2026-03-15", "status": "delivered"},
        "ORD-002": {"order_id": "ORD-002", "customer": "Jane Smith", "item": "Running Shoes", "category": "clothing", "price": 129.99, "date": "2026-02-20", "status": "delivered"},
        "ORD-003": {"order_id": "ORD-003", "customer": "Bob Wilson", "item": "Python Programming Book", "category": "books", "price": 45.99, "date": "2026-01-10", "status": "delivered"},
    }
    order = orders.get(order_id.upper())
    if order:
        return json.dumps(order, indent=2)
    return f"Order {order_id} not found. Available: ORD-001, ORD-002, ORD-003."


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_return_eligibility",
            "description": "Check if an item can be returned based on purchase date and category",
            "parameters": {
                "type": "object",
                "properties": {
                    "purchase_date": {"type": "string", "description": "Purchase date in YYYY-MM-DD format"},
                    "category": {"type": "string", "description": "Product category (electronics, clothing, books, home, toys)"},
                },
                "required": ["purchase_date", "category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_refund_amount",
            "description": "Calculate refund amount based on price, condition, and return reason",
            "parameters": {
                "type": "object",
                "properties": {
                    "price": {"type": "number", "description": "Original purchase price"},
                    "condition": {"type": "string", "description": "Item condition: new, like-new, used, damaged"},
                    "return_reason": {"type": "string", "description": "Reason: defect, wrong-item, changed-mind, damaged-shipping"},
                },
                "required": ["price", "condition", "return_reason"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up order details by order ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order ID (e.g. ORD-001, ORD-002, ORD-003)"},
                },
                "required": ["order_id"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "check_return_eligibility": check_return_eligibility,
    "calculate_refund_amount": calculate_refund_amount,
    "lookup_order": lookup_order,
}

SYSTEM_PROMPT = """You are a helpful returns and refunds assistant. Help customers check return eligibility, calculate refunds, and look up orders. Be friendly, accurate, and concise.

You have access to these tools:
- check_return_eligibility: Check if an item can be returned
- calculate_refund_amount: Calculate the refund amount
- lookup_order: Look up order details (ORD-001, ORD-002, ORD-003)

Return policy summary:
- Electronics: 30-day return window
- Clothing: 60-day return window
- Books: 30-day return window
- Home & Toys: 90-day return window
- Defective/wrong items: full refund
- Changed mind: 10% restocking fee
- Used items: 80% refund, Damaged: 50% refund"""


def run_agent(client, user_input, chat_history):
    """Run the agent with tool-call loop."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        msg = response.choices[0].message
        tool_calls = msg.tool_calls

        if not tool_calls:
            return msg.content or "I'm not sure how to help with that."

        messages.append(msg)

        for tc in tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)
            fn = TOOL_FUNCTIONS.get(fn_name)
            if fn:
                tool_result = fn(**fn_args)
            else:
                tool_result = f"Unknown tool: {fn_name}"

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": tool_result,
            })

    return msg.content or "I ran into an issue processing your request."


# Sidebar
with st.sidebar:
    st.header("Agent Info")
    st.markdown(f"**Model:** `{MODEL}`")
    st.markdown("**Hosted on:** Groq (free)")
    st.divider()
    st.markdown("**Capabilities:**")
    st.markdown("- Return eligibility checks")
    st.markdown("- Refund calculations")
    st.markdown("- Order lookup (ORD-001 to 003)")
    st.divider()
    st.markdown("**Sample queries:**")
    st.code("Look up order ORD-001", language=None)
    st.code("Can I return headphones bought on 2026-03-15?", language=None)
    st.code("Calculate refund for $79.99 used item, changed mind", language=None)
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Get API key
groq_key = st.secrets.get("GROQ_API_KEY", "")
if not groq_key:
    st.warning("Please add your Groq API key to `.streamlit/secrets.toml` or Streamlit Cloud secrets.")
    st.code('GROQ_API_KEY = "gsk_your_key_here"', language="toml")
    st.stop()

client = Groq(api_key=groq_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about returns, refunds, or orders..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
                response = run_agent(client, prompt, history)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
