#!/usr/bin/env python3
"""
Project 1: Enterprise Knowledge Assistant (RAG Prompting)
Skills Focus: Context Injection, Citation Strategies, Hallucination Reduction.

This script demonstrates how an FDE builds a Retrieval-Augmented Generation (RAG)
prompt template, parses document context blocks, manages citations, and prevents 
hallucinations when query information is missing.
"""

import json

# Define the production RAG System Prompt
RAG_SYSTEM_PROMPT = """You are the Apex Corporate Knowledge Assistant.
Your core objective is to answer user queries using ONLY the retrieved documents provided in the context section of the user message.

Operational Grounding Rules:
1. Grounding: Answer the question using only the facts stated in the documents. Do not assume or extrapolate.
2. Citation: Every claim or fact you mention must be followed by a citation pointing to the document ID (e.g., "[Doc-1]").
3. Strict Out-of-Bounds: If the retrieved documents do not contain the answer, or if the context is insufficient, respond verbatim: "I am sorry, but the provided documentation does not contain the information required to answer your question." Do not attempt to use pre-trained general knowledge.
4. Formatting: Keep your answers professional, concise, and structured.
"""

# Define the User Prompt Template
RAG_USER_TEMPLATE = """Please answer my query based on the following documents.

<documents>
{context_documents}
</documents>

User Query: "{query}"
Answer:"""

# Mock retrieved document corpus
MOCK_KNOWLEDGE_BASE = [
    {
        "id": "Doc-1",
        "title": "Corporate Work From Home Policy 2026",
        "content": "All employees are eligible for up to 2 days of remote work per week, subject to manager approval. Hybrid days must be logged in the HR portal."
    },
    {
        "id": "Doc-2",
        "title": "Expense Reimbursement Guide",
        "content": "Work-related travel expenses must be submitted within 30 days of return. Meal allowance is capped at $75 per day."
    },
    {
        "id": "Doc-3",
        "title": "IT Equipment Allocation Standard",
        "content": "New hires receive a standard laptop, a 27-inch monitor, and a keyboard. Upgrades require a department head business justification."
    }
]

class EnterpriseKnowledgeAssistant:
    def __init__(self, system_prompt, user_template):
        self.system_prompt = system_prompt
        self.user_template = user_template

    def assemble_prompt(self, query, retrieved_docs):
        # Format the retrieved documents into structured XML tags
        context_str = ""
        for doc in retrieved_docs:
            context_str += f'<document id="{doc["id"]}">\n'
            context_str += f'  <title>{doc["title"]}</title>\n'
            context_str += f'  <content>{doc["content"]}</content>\n'
            context_str += '</document>\n'
        
        # Interpolate variables into the user template
        user_prompt = self.user_template.format(
            context_documents=context_str.strip(),
            query=query
        )
        return user_prompt

    def mock_inference(self, assembled_prompt, query):
        """Simulates LLM inference based on prompt rules and grounding check."""
        print("\n--- [SYSTEM ROLE SYSTEM PROMPT] ---")
        print(self.system_prompt)
        print("\n--- [INJECTED USER PROMPT] ---")
        print(assembled_prompt)
        
        # Simple rule-based mock logic matching our prompt constraints
        query_lower = query.lower()
        print("\n--- [LLM GENERATED RESPONSE] ---")
        
        if "remote" in query_lower or "wfh" in query_lower or "work from home" in query_lower:
            response = "Under the Corporate Work From Home Policy 2026, employees can work remotely for up to 2 days per week, provided they obtain manager approval and log their hybrid schedule in the HR portal [Doc-1]."
        elif "meal" in query_lower or "expense" in query_lower:
            response = "According to the Expense Reimbursement Guide, travel expenses must be filed within 30 days of returning, and the daily meal allowance is capped at $75 [Doc-2]."
        elif "monitor" in query_lower or "laptop" in query_lower or "equipment" in query_lower:
            response = "New hires are allocated a standard laptop, a 27-inch monitor, and a keyboard. Any equipment upgrades require a formal business justification from the department head [Doc-3]."
        else:
            # Trigger strict hallucination fallback
            response = "I am sorry, but the provided documentation does not contain the information required to answer your question."
            
        print(response)
        print("="*60)
        return response

def main():
    assistant = EnterpriseKnowledgeAssistant(RAG_SYSTEM_PROMPT, RAG_USER_TEMPLATE)
    
    print("Enterprise RAG Prompting Simulation")
    print("="*60)
    
    # Scenario A: Query covered by retrieved documents
    query_a = "What is the daily meal limit for business trips?"
    prompt_a = assistant.assemble_prompt(query_a, MOCK_KNOWLEDGE_BASE)
    assistant.mock_inference(prompt_a, query_a)
    
    # Scenario B: Query NOT covered (testing hallucination block)
    query_b = "How do I request maternity leave?"
    prompt_b = assistant.assemble_prompt(query_b, MOCK_KNOWLEDGE_BASE)
    assistant.mock_inference(prompt_b, query_b)

if __name__ == "__main__":
    main()
