#!/usr/bin/env python3
"""
Project 5: Enterprise AI Agent
Skills Focus: Agent Instructions, Tool Usage (ReAct Loop), Multi-Step Workflows.

This script demonstrates a ReAct (Reasoning and Acting) prompt loop for an 
autonomous IT Operations Agent. The agent plans, runs terminal diagnostic tools, 
inspects outputs, and resolves server alerts.
"""

import json

AGENT_SYSTEM_PROMPT = """You are the Apex Ops Agent. Your objective is to resolve server alerts.
You have access to the following tools:

- `check_disk_space(server_name)`: Returns CPU and disk space allocation percentages.
- `clear_tmp_directory(server_name)`: Deletes logs in the /tmp directory and returns recovered space.
- `restart_service(server_name, service_name)`: Restarts a system service and returns success status.

You must work in a loop of steps using this exact format:

Thought: [Explain your reasoning about what to do next]
Action: [tool_name]([arguments])
Observation: [Tool result will be printed here]

When you have resolved the alert, output:
Final Answer: [Detailed status of how the alert was resolved]

Let's begin.
"""

class ITServiceAgent:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.step_history = []

    # Mock tool functions
    def check_disk_space(self, server):
        self.step_history.append(f"Tool Call: check_disk_space({server})")
        return {"disk_used_pct": 94, "cpu_used_pct": 45, "status": "WARN: Disk Space Critical"}

    def clear_tmp_directory(self, server):
        self.step_history.append(f"Tool Call: clear_tmp_directory({server})")
        return {"freed_bytes": "42GB", "new_disk_used_pct": 65, "status": "OK: Operations complete"}

    def restart_service(self, server, service):
        self.step_history.append(f"Tool Call: restart_service({server}, {service})")
        return {"service": service, "status": "ACTIVE", "code": 200}

    def run_agent_loop(self, alert_description):
        print(f"Inbound Server Alert: '{alert_description}'\n")
        print("System Instructions Loaded.")
        print(self.system_prompt)
        print("="*60)

        # Step 1: Agent decides to check disk space
        thought_1 = "Thought: The alert indicates server-01 has a storage threshold issue. I should run the disk diagnostic tool first to verify space statistics."
        print(thought_1)
        action_1 = "Action: check_disk_space('server-01')"
        print(action_1)
        observation_1 = self.check_disk_space('server-01')
        print(f"Observation: {json.dumps(observation_1)}")
        print("-" * 40)

        # Step 2: Agent decides to clear temp directory
        thought_2 = "Thought: Disk usage is indeed critical at 94%. I need to clear the log files stored in the /tmp directory to free up space."
        print(thought_2)
        action_2 = "Action: clear_tmp_directory('server-01')"
        print(action_2)
        observation_2 = self.clear_tmp_directory('server-01')
        print(f"Observation: {json.dumps(observation_2)}")
        print("-" * 40)

        # Step 3: Agent verifies and finishes
        thought_3 = "Thought: The clean operation succeeded and reduced disk usage to 65%. The disk space alert is resolved. I can report the status."
        print(thought_3)
        final_answer = "Final Answer: Successfully resolved disk space warning on server-01. Ran `clear_tmp_directory` which cleared 42GB of files, bringing total usage down from 94% to 65%."
        print(final_answer)
        print("="*60)
        
        return self.step_history

def main():
    agent = ITServiceAgent(AGENT_SYSTEM_PROMPT)
    print("Enterprise ReAct Agent Simulation")
    print("="*60)
    
    alert = "CRITICAL_ALERT: Disk space on production server-01 exceeds 90% threshold."
    history = agent.run_agent_loop(alert)
    
    print("\nExecution History Logs:")
    for step in history:
        print(f" - {step}")

if __name__ == "__main__":
    main()
