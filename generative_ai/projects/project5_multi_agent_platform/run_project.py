#!/usr/bin/env python3
"""
Project 5: Enterprise Multi-Agent Platform (Multi-Agent Systems)
Skills Focus: State Orchestration, Routing Nodes, Multi-Agent Collaboration.

This script demonstrates a multi-agent state graph orchestrator.
A Router Agent coordinates tasks between an IT Diagnostic Agent 
and a DB Audit Agent, sharing states to resolve complex system queries.
"""

import json

class MultiAgentPlatform:
    def __init__(self):
        # Master state variables passed between routing nodes
        self.shared_state = {
            "current_node": "ROUTER",
            "user_query": "",
            "diagnostic_notes": "",
            "database_records": "",
            "final_response": ""
        }

    # Agent Node 1: Coordinator Router
    def router_node(self, query):
        self.shared_state["user_query"] = query
        print(f"[ROUTER] Analyzing user query: '{query}'")
        
        # Simple routing rule checks
        if "server" in query.lower() or "disk" in query.lower():
            self.shared_state["current_node"] = "IT_DIAGNOSTIC_AGENT"
            print(" -> Routing to: IT_DIAGNOSTIC_AGENT")
        elif "user" in query.lower() or "audit" in query.lower():
            self.shared_state["current_node"] = "DB_AUDIT_AGENT"
            print(" -> Routing to: DB_AUDIT_AGENT")
        else:
            self.shared_state["current_node"] = "COMPLETED"
            self.shared_state["final_response"] = "I cannot determine the destination team for your query."

    # Agent Node 2: IT Diagnostic specialist
    def it_diagnostic_node(self):
        print("[IT_DIAGNOSTIC_AGENT] Running hardware resource checks...")
        # Simulate local tool action
        self.shared_state["diagnostic_notes"] = "Server check: CPU usage 45%, Storage usage 94% (CRITICAL)."
        
        # Decide next route (escalate to DB or complete)
        print(" -> Task complete. Routing back to: ROUTER")
        self.shared_state["current_node"] = "COMPLETED"

    # Agent Node 3: Database Audit specialist
    def db_audit_node(self):
        print("[DB_AUDIT_AGENT] Running query checks over account logs...")
        # Simulate local tool action
        self.shared_state["database_records"] = "Found 3 failed logins for account admin-01 today."
        
        print(" -> Task complete. Routing back to: ROUTER")
        self.shared_state["current_node"] = "COMPLETED"

    # Orchestrator Loop
    def run_platform(self, query):
        self.router_node(query)
        
        # Graph execution loop
        while self.shared_state["current_node"] != "COMPLETED":
            node = self.shared_state["current_node"]
            
            if node == "IT_DIAGNOSTIC_AGENT":
                self.it_diagnostic_node()
                self.shared_state["current_node"] = "ROUTER"
            elif node == "DB_AUDIT_AGENT":
                self.db_audit_node()
                self.shared_state["current_node"] = "ROUTER"
            
            # Simple manual routing check to prevent infinite loops in mock
            if self.shared_state["diagnostic_notes"] or self.shared_state["database_records"]:
                self.shared_state["current_node"] = "COMPLETED"

        # Final response compiling
        if self.shared_state["diagnostic_notes"]:
            self.shared_state["final_response"] = f"IT Diagnostic report complete. {self.shared_state['diagnostic_notes']}"
        elif self.shared_state["database_records"]:
            self.shared_state["final_response"] = f"DB Audit query complete. {self.shared_state['database_records']}"
            
        print("\n" + "="*50)
        print(f"Final Compiled Answer:\n{self.shared_state['final_response']}")
        print("="*50)
        
        return self.shared_state

def main():
    print("Project 5: Enterprise Multi-Agent Platform (State Orchestration)")
    print("="*60)
    
    platform = MultiAgentPlatform()
    final_state = platform.run_platform("Run diagnostic scans on the production server.")
    
    print("\nShared Graph State Logs:")
    print(json.dumps(final_state, indent=2))
    print("="*60)

if __name__ == "__main__":
    main()
