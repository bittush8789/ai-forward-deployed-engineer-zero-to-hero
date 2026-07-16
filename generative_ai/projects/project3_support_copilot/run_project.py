#!/usr/bin/env python3
"""
Project 3: Customer Support Copilot (AI Agents & Workflows)
Skills Focus: Agentic Architectures, Tool Execution, Short-Term State Memory.

This script simulates a Customer Support Agent with short-term state memory.
The agent receives inquiries, selects matching tools, executes them, and logs 
results to its memory graph to resolve customer issues.
"""

import json

class CustomerSupportAgent:
    def __init__(self):
        # Initial memory store state
        self.state = {
            "customer_id": None,
            "order_number": None,
            "resolved": False,
            "execution_log": []
        }
        
        # Mock database registries
        self.orders_db = {
            "ORD-998": {"status": "DELIVERED", "date": "2026-07-02", "item": "Ergonomic Office Chair"},
            "ORD-104": {"status": "IN_TRANSIT", "date": "2026-07-15", "item": "Mechanical Keyboard"}
        }

    # Agent Tools
    def identify_customer(self, customer_name):
        self.state["customer_id"] = "CUST-402"
        log_entry = f"Tool Call: identify_customer({customer_name}) -> Verified Customer ID: CUST-402"
        self.state["execution_log"].append(log_entry)
        return {"customer_id": "CUST-402", "status": "VERIFIED"}

    def fetch_order_details(self, order_id):
        self.state["order_number"] = order_id
        if order_id in self.orders_db:
            res = self.orders_db[order_id]
            log_entry = f"Tool Call: fetch_order_details({order_id}) -> Found Item: {res['item']}, Status: {res['status']}"
            self.state["execution_log"].append(log_entry)
            return {"order": order_id, "details": res, "status": "SUCCESS"}
        else:
            log_entry = f"Tool Call: fetch_order_details({order_id}) -> Order not found"
            self.state["execution_log"].append(log_entry)
            return {"order": order_id, "status": "NOT_FOUND"}

    def run_agentic_workflow(self, customer_name, query_text):
        print(f"Customer Name: {customer_name}")
        print(f"User Query: '{query_text}'\n")
        
        # Step 1: Agent decides to verify customer identity
        print("Thought: Before accessing order databases, I must verify the customer's account identity.")
        identity_res = self.identify_customer(customer_name)
        print(f"Observation: {json.dumps(identity_res)}")
        
        # Step 2: Agent checks query for order numbers and calls database tool
        print("\nThought: Now that identity is verified, I need to check the query for order details. The customer mentioned 'ORD-104'. I will run fetch_order_details.")
        order_res = self.fetch_order_details("ORD-104")
        print(f"Observation: {json.dumps(order_res)}")
        
        # Step 3: Agent checks status and compiles resolution response
        print("\nThought: Order status is IN_TRANSIT. I can now inform the customer of their package delivery status.")
        self.state["resolved"] = True
        
        final_response = f"Hello {customer_name}, I've verified your account. Your order ORD-104 ({order_res['details']['item']}) is currently in transit. It departed our warehouse on {order_res['details']['date']}."
        
        print("\n" + "="*50)
        print(f"Agent Final Response:\n{final_response}")
        print("="*50)
        
        return self.state

def main():
    print("Project 3: Customer Support Copilot (AI Agent Platform Simulator)")
    print("="*60)
    
    agent = CustomerSupportAgent()
    history_state = agent.run_agentic_workflow(
        customer_name="Fenchurch Kent",
        query_text="Where is my keyboard order ORD-104? It hasn't arrived yet."
    )
    
    print("\nAgent Short-Term Memory State Logs:")
    print(json.dumps(history_state, indent=2))
    print("="*60)

if __name__ == "__main__":
    main()
