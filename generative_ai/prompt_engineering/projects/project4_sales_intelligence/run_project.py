#!/usr/bin/env python3
"""
Project 4: Sales Intelligence Copilot
Skills Focus: Prompt Templates, Dynamic Personas, AI Response Evaluation.

This project implements a Sales Intelligence Copilot that adjusts email replies based on 
a dynamically calculated prospect persona, followed by a programmatic LLM-as-a-Judge 
evaluation scorecard to check reply quality before delivery.
"""

import json

# Master system instruction
SALES_SYSTEM_PROMPT = """You are an Enterprise Sales Advisor.
Your job is to draft sales response emails tailored to the prospect's personality profile (e.g., Assertive, Analytical, Amiable).
"""

# Template for dynamic persona email drafting
SALES_DRAFT_TEMPLATE = """You are drafting an email reply to a prospect.

Prospect Profile:
- Name: {prospect_name}
- Job Title: {job_title}
- Persona Style: {persona_style} (Assertive = direct, Amiable = friendly, Analytical = data-driven)
- Concern: {primary_concern}

Operational Instructions:
1. Tailor the tone of your message to match the Persona Style.
2. Address the primary concern directly.
3. Keep the email under 4 sentences.
4. Conclude with a clear call-to-action (CTA).

Draft email response:"""

# LLM-as-a-Judge Evaluation Template
JUDGE_SCORECARD_TEMPLATE = """You are an independent Sales Quality Auditor.
Evaluate the drafted sales email against these criteria:
1. Does the tone match the target persona ({persona_style})? (Score 0-3)
2. Does it directly address the primary concern ({primary_concern})? (Score 0-3)
3. Is it under 4 sentences? (Score 0-1)

Return your audit as a JSON object:
{{
  "tone_score": int,
  "concern_score": int,
  "length_compliance": boolean,
  "audit_notes": string
}}

Drafted Email:
"{drafted_email}"

Audit Report JSON:"""

class SalesIntelligenceCopilot:
    def __init__(self):
        self.draft_template = SALES_DRAFT_TEMPLATE
        self.judge_template = JUDGE_SCORECARD_TEMPLATE

    def draft_reply(self, prospect_name, job_title, persona_style, primary_concern):
        # Dynamically compile the prompt template
        compiled_prompt = self.draft_template.format(
            prospect_name=prospect_name,
            job_title=job_title,
            persona_style=persona_style,
            primary_concern=primary_concern
        )
        
        # Simulating LLM response based on the persona
        if persona_style == "Assertive":
            draft = f"Hello {prospect_name}, I understand you're looking to cut server overhead immediately. Our software automates optimization, slashing cloud expenditures by 30% without downtime. Let's schedule a brief 10-minute demo this Thursday at 2 PM."
        elif persona_style == "Analytical":
            draft = f"Hi {prospect_name}, our benchmark reports indicate that implementing our automation cuts cloud costs by 28.4% on average (based on 120 case studies). I can share our complete performance PDF. Are you available for a technical review next Tuesday?"
        else: # Amiable
            draft = f"Dear {prospect_name}, thanks for reaching out. We would love to partner with you to help make your engineering team's cloud journey easier. I can walk you through the details whenever suits you. Would next Wednesday work for a quick chat?"
            
        return compiled_prompt, draft

    def evaluate_draft(self, draft, persona_style, primary_concern):
        compiled_judge_prompt = self.judge_template.format(
            persona_style=persona_style,
            primary_concern=primary_concern,
            drafted_email=draft
        )
        
        # Simulating Judge output
        sentence_count = len(draft.split(". "))
        compliant = sentence_count <= 4
        
        mock_judge_json = {
            "tone_score": 3,
            "concern_score": 3,
            "length_compliance": compliant,
            "audit_notes": f"The email successfully addresses '{primary_concern}' in a style matching the {persona_style} persona. Length check passed."
        }
        return compiled_judge_prompt, json.dumps(mock_judge_json)

def main():
    copilot = SalesIntelligenceCopilot()
    
    print("Sales Intelligence Copilot and Evaluation Simulator")
    print("="*60)
    
    prospects = [
        {
            "name": "Douglas Adams",
            "title": "VP of Operations",
            "persona": "Assertive",
            "concern": "Reducing cloud costs immediately"
        },
        {
            "name": "Fenchurch Kent",
            "title": "Data Science Lead",
            "persona": "Analytical",
            "concern": "Checking model accuracy benchmarks"
        }
    ]
    
    for prospect in prospects:
        print(f"\nProspect: {prospect['name']} ({prospect['title']})")
        print(f"Target Persona: {prospect['persona']}")
        
        # Step 1: Draft Email
        compiled_draft_p, draft = copilot.draft_reply(
            prospect['name'], prospect['title'], prospect['persona'], prospect['concern']
        )
        print(f"Compiled Draft Prompt:\n{compiled_draft_p}\n")
        print(f"Drafted Email Output:\n'{draft}'\n")
        
        # Step 2: Run Evaluation
        compiled_eval_p, scorecard = copilot.evaluate_draft(draft, prospect['persona'], prospect['concern'])
        print(f"Compiled Evaluator Prompt:\n{compiled_eval_p}\n")
        print(f"Evaluator Scorecard:\n{scorecard}")
        print("="*60)

if __name__ == "__main__":
    main()
