#!/usr/bin/env python3
"""
Project 1: Enterprise Knowledge Copilot (LangChain & RAG)
Skills Focus: LangChain Tool Binding, RAG Integrations, Query Execution.

This script demonstrates how an FDE builds a RAG-enabled agent using LangChain
abstractions. It defines tools, binds them to a mock chat model, and runs a
retrieval chain to answer user questions using verified documents.
"""

import json

class MockChatModel:
    def __init__(self, system_instruction):
        self.system = system_instruction

    def generate_tool_call(self, query):
        """Simulates LLM deciding to invoke the RAG search tool."""
        print(f"[MODEL] Received query: '{query}'")
        print(f"[MODEL] System Guidelines: {self.system}")
        
        # Decide if the query requires document search
        query_lower = query.lower()
        if "policy" in query_lower or "allowance" in query_lower or "wfh" in query_lower:
            tool_call = {
                "name": "retrieve_company_documents",
                "arguments": {"search_term": query}
            }
            print(f"[MODEL] Decision: Invoke tool '{tool_call['name']}' with args: {tool_call['arguments']}")
            return tool_call
        else:
            print("[MODEL] Decision: Answer directly without calling tools.")
            return None

class EnterpriseKnowledgeCopilot:
    def __init__(self):
        # Initializing the model wrapper
        self.model = MockChatModel(
            system_instruction="Analyze queries. Use retrieve_company_documents ONLY if policy facts are requested. Cite sources."
        )
        
        # In-memory document index
        self.document_database = {
            "remote": "WFH Policy 2026: Employees can work remotely up to 2 days per week [Doc-1].",
            "meal": "Reimbursement Policy: Daily travel meal allowance is capped at $75 [Doc-2].",
            "allowance": "Reimbursement Policy: Daily travel meal allowance is capped at $75 [Doc-2]."
        }

    # Tool declaration
    def retrieve_company_documents(self, search_term):
        """Standard tool function to fetch company documents."""
        print(f"[TOOL] Executing retrieve_company_documents with search term: '{search_term}'")
        
        # Search documents
        search_lower = search_term.lower()
        found_docs = []
        for key, text in self.document_database.items():
            if key in search_lower:
                found_docs.append(text)
                
        if found_docs:
            return {"results": found_docs, "status": "SUCCESS"}
        else:
            return {"results": [], "status": "NOT_FOUND"}

    def run_copilot(self, query):
        # 1. Model evaluates query and decides to call tool
        tool_call = self.model.generate_tool_call(query)
        
        if tool_call and tool_call["name"] == "retrieve_company_documents":
            # 2. Application executes the requested tool
            observation = self.retrieve_company_documents(tool_call["arguments"]["search_term"])
            print(f"[SYSTEM] Tool Observation: {json.dumps(observation)}")
            
            # 3. Model compiles final response using the retrieved context
            if observation["status"] == "SUCCESS":
                final_answer = f"Based on retrieved documentation: {observation['results'][0]}"
            else:
                final_answer = "I am sorry, but I cannot find any company policy documents matching your query."
        else:
            final_answer = "How can I assist you with general tasks today?"
            
        print("\n" + "="*50)
        print(f"Copilot Response:\n{final_answer}")
        print("="*50)
        
        return final_answer

def main():
    print("Project 1: Enterprise Knowledge Copilot (LangChain & Tool Call Ingest)")
    print("="*60)
    
    copilot = EnterpriseKnowledgeCopilot()
    copilot.run_copilot("What is the maximum daily meal allowance for business trips?")
    
if __name__ == "__main__":
    main()
