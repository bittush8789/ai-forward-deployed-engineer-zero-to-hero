#!/usr/bin/env python3
"""
Project 4: Customer Support Multi-Agent System (LangGraph State Graphs)
Skills Focus: LangGraph Graph States, Node Transitions, State Checkpoints.

This script implements a simulated state graph orchestrator for a multi-agent
customer support platform. It manages state transitions, updates customer details,
and runs conditional routing logic.
"""

import json

class LangGraphSupportOrchestrator:
    def __init__(self):
        # Initial graph state schema
        self.state = {
            "customer_name": "",
            "active_node": "START",
            "messages": [],
            "checkpoint_db": []
        }
        
        # Simulated database
        self.customer_accounts = {
            "Arthur Dent": {"tier": "PREMIUM", "preferred_language": "English"},
            "Trillian McMillan": {"tier": "STANDARD", "preferred_language": "French"}
        }

    def save_checkpoint(self):
        """Saves a serialized copy of the current state to the checkpoint DB."""
        checkpoint = json.loads(json.dumps(self.state))
        self.state["checkpoint_db"].append(checkpoint)
        print(f" -> Checkpoint saved. Total checkpoints: {len(self.state['checkpoint_db'])}")

    # Graph Nodes
    def start_node(self, customer_name, message):
        self.state["customer_name"] = customer_name
        self.state["active_node"] = "START"
        self.state["messages"].append(message)
        print(f"\n[NODE: START] Processing message from customer: {customer_name}")
        self.save_checkpoint()

    def route_edge(self):
        """Conditional routing edge deciding which specialist agent node to invoke."""
        name = self.state["customer_name"]
        print(f"[EDGE: ROUTER] Evaluating user metadata for customer: '{name}'")
        
        # Route based on customer tier
        if name in self.customer_accounts:
            tier = self.customer_accounts[name]["tier"]
            if tier == "PREMIUM":
                print(" -> Conditional Match: Premium Tier. Routing to VIP_SUPPORT_AGENT.")
                self.state["active_node"] = "VIP_SUPPORT_AGENT"
            else:
                print(" -> Conditional Match: Standard Tier. Routing to STANDARD_SUPPORT_AGENT.")
                self.state["active_node"] = "STANDARD_SUPPORT_AGENT"
        else:
            print(" -> Conditional Match: Unregistered Account. Routing to STANDARD_SUPPORT_AGENT.")
            self.state["active_node"] = "STANDARD_SUPPORT_AGENT"

    def vip_agent_node(self):
        print("[NODE: VIP_SUPPORT_AGENT] Executing high-priority support workflow...")
        reply = f"Hello {self.state['customer_name']}, welcome to our Priority Desk. How can I help you today?"
        self.state["messages"].append(reply)
        self.save_checkpoint()
        self.state["active_node"] = "COMPLETED"

    def standard_agent_node(self):
        print("[NODE: STANDARD_SUPPORT_AGENT] Executing standard support workflow...")
        reply = f"Hello {self.state['customer_name']}, thank you for reaching out. How can I help you today?"
        self.state["messages"].append(reply)
        self.save_checkpoint()
        self.state["active_node"] = "COMPLETED"

    # Orchestrator Loop
    def run_graph(self, customer_name, query_text):
        print(f"Inbound query: '{query_text}' from {customer_name}")
        print("Initializing LangGraph state schema...")
        print("="*60)
        
        # 1. Run start node
        self.start_node(customer_name, query_text)
        
        # 2. Evaluate routing edge
        self.route_edge()
        
        # 3. Transition to target specialist node
        if self.state["active_node"] == "VIP_SUPPORT_AGENT":
            self.vip_agent_node()
        elif self.state["active_node"] == "STANDARD_SUPPORT_AGENT":
            self.standard_agent_node()
            
        print("\n" + "="*50)
        print(f"Support Flow Completed. Active Node: {self.state['active_node']}")
        print(f"Chat Messages History: {self.state['messages']}")
        print("="*50)
        
        return self.state

def main():
    print("Project 4: Customer Support Multi-Agent System (LangGraph State Simulator)")
    print("="*60)
    
    orchestrator = LangGraphSupportOrchestrator()
    orchestrator.run_graph(
        customer_name="Arthur Dent",
        query_text="Hi, I have a question regarding my corporate invoice billing."
    )

if __name__ == "__main__":
    main()
