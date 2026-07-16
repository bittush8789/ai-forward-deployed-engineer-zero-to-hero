#!/usr/bin/env python3
"""
Project 3: Autonomous IT Operations Agent (AutoGen Loops)
Skills Focus: AutoGen Conversational Agents, Sandboxed Code Execution, Fail-safe Recovery.

This script simulates a conversation between a CoderAgent and an ExecutorAgent 
to resolve a disk storage alert. The CoderAgent drafts script fixes, and 
the ExecutorAgent simulates running them in an isolated console environment.
"""

import json

class CoderAgent:
    def generate_disk_cleanup_script(self, error_message=None):
        """Simulates LLM writing a python script, updating logic based on console errors."""
        if error_message:
            print(f"\n[CODER] Received error feedback from console: '{error_message}'")
            print("[CODER] Refining cleanup script to fix directory check permissions...")
            script = """
# Refined clean script
import os
import shutil

target_dir = "/tmp/system_logs"
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
    print("Disk cleanup successful. 42GB log files deleted.")
else:
    print("Target directory not found.")
"""
        else:
            print("\n[CODER] Drafting disk cleanup script...")
            # First draft has a simulated typo or error (e.g. missing import)
            script = """
# Initial clean script
target_dir = "/tmp/system_logs"
shutil.rmtree(target_dir) # Typo: shutil is not imported
print("Cleanup successful.")
"""
        return script

class ExecutorAgent:
    def execute_in_sandbox(self, script_code):
        """Simulates running the model-generated python script in a secure sandbox."""
        print("\n[EXECUTOR] Received script payload for execution in isolated container...")
        print("-" * 40)
        print(script_code.strip())
        print("-" * 40)
        
        # Simulate console checks
        if "import shutil" not in script_code:
            error = "NameError: name 'shutil' is not defined"
            print(f"[EXECUTOR] Console output: {error}")
            return {"exit_code": 1, "error": error}
        else:
            success_msg = "Disk cleanup successful. 42GB log files deleted."
            print(f"[EXECUTOR] Console output: {success_msg}")
            return {"exit_code": 0, "output": success_msg}

class AutoGenITManager:
    def __init__(self):
        self.coder = CoderAgent()
        self.executor = ExecutorAgent()

    def resolve_alert(self):
        print("Starting AutoGen IT Operations Agent Loop...")
        print("Alert: production server disk space exceeding 90% threshold.")
        print("="*60)
        
        # Step 1: Coder generates initial script
        script = self.coder.generate_disk_cleanup_script()
        
        # Step 2: Executor runs script in sandbox (and encounters NameError)
        result = self.executor.execute_in_sandbox(script)
        
        # Step 3: Check status and run correction loop if needed
        if result["exit_code"] != 0:
            # Code failed, route error back to Coder
            refined_script = self.coder.generate_disk_cleanup_script(error_message=result["error"])
            
            # Re-run corrected script in sandbox
            final_result = self.executor.execute_in_sandbox(refined_script)
            
            if final_result["exit_code"] == 0:
                status = "RESOLVED"
                log = final_result["output"]
            else:
                status = "FAILED"
                log = "Refined script execution failed."
        else:
            status = "RESOLVED"
            log = result["output"]
            
        print("\n" + "="*50)
        print(f"IT Agent Execution Finished. Status: {status}")
        print(f"Final Console Log:\n{log}")
        print("="*50)

def main():
    manager = AutoGenITManager()
    manager.resolve_alert()

if __name__ == "__main__":
    main()
