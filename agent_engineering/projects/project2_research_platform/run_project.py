#!/usr/bin/env python3
"""
Project 2: Multi-Agent Research Platform (CrewAI Collaboration)
Skills Focus: CrewAI Agent Roles, Backstory Tuning, Task Delegation.

This script simulates a collaborative CrewAI research crew consisting of 
a Research Specialist and a Technical Writer. The agents work sequentially 
to fetch data, compile reports, and review deliverables.
"""

import json

class ResearchAgent:
    def __init__(self):
        self.role = "Research Specialist"
        self.goal = "Extract technical specifications and model accuracy benchmarks for target models."
        self.backstory = "Expert research auditor. Focuses strictly on data facts, benchmarks, and details. Does not summarize."

    def execute_research(self, topic):
        print(f"[{self.role}] Running deep web queries on topic: '{topic}'...")
        print(f"[{self.role}] Analyzing parameters...")
        
        # Simulate data retrieval
        data = {
            "model_name": "Llama-3-70B",
            "mmlu_score": 82.0,
            "context_window": "128k tokens",
            "licensing": "Commercial Llama 3 Community License"
        }
        return data

class WriterAgent:
    def __init__(self):
        self.role = "Technical Writer"
        self.goal = "Compile raw research facts into executive-ready comparison briefs."
        self.backstory = "Professional editor. Translates technical data logs into clear summaries under 4 sentences."

    def compile_brief(self, raw_data):
        print(f"\n[{self.role}] Received raw research logs: {json.dumps(raw_data)}")
        print(f"[{self.role}] Structuring comparison brief...")
        
        brief = f"Executive Brief: Technical review of {raw_data['model_name']}.\n" \
                f"- Evaluated performance reveals a MMLU accuracy score of {raw_data['mmlu_score']}%.\n" \
                f"- Model includes a large context window of {raw_data['context_window']} tokens.\n" \
                f"- Released under a {raw_data['licensing']}."
        return brief

class ResearchCrew:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()

    def run_research_crew(self, topic):
        print("Initializing CrewAI Collaborative Session...")
        print(f" - Crew Member 1: {self.researcher.role}")
        print(f" - Crew Member 2: {self.writer.role}")
        print("="*60)
        
        # Step 1: Researcher extracts details
        raw_facts = self.researcher.execute_research(topic)
        print(f"[SYSTEM] Task output from Researcher: {json.dumps(raw_facts)}")
        
        # Step 2: Task gets delegated to Writer
        final_brief = self.writer.compile_brief(raw_facts)
        
        print("\n" + "="*50)
        print(f"Crew Final Deliverable:\n{final_brief}")
        print("="*50)
        
        return final_brief

def main():
    print("Project 2: Multi-Agent Research Platform (CrewAI Collaboration)")
    print("="*60)
    
    crew = ResearchCrew()
    crew.run_research_crew("Llama-3-70B Specifications")

if __name__ == "__main__":
    main()
