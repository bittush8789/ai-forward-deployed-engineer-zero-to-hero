#!/usr/bin/env python3
"""
AI Copilot tool call dispatcher simulator.
Parses query parameters and maps functions.
"""

import sys

class CopilotDispatcher:
    def __init__(self):
        self.tools = {
            "fetch_user": self.fetch_user_record,
            "send_email": self.send_email_notification
        }

    def fetch_user_record(self, params):
        return f"User details: {params.get('user_id')} | Account Status: ACTIVE"

    def send_email_notification(self, params):
        return f"Email sent successfully to {params.get('email')}."

    def dispatch(self, tool_name: str, params: dict) -> str:
        tool_func = self.tools.get(tool_name)
        if tool_func:
            print(f"Dispatcher - Executing Tool: '{tool_name}' with parameters: {params}")
            return tool_func(params)
        else:
            return f"Error: Tool '{tool_name}' not registered."

def main():
    print("=== Initializing Copilot Tool Dispatcher ===")
    dispatcher = CopilotDispatcher()
    
    # Test fetch user tool execution
    result_1 = dispatcher.dispatch("fetch_user", {"user_id": "usr_7720"})
    print(f"Tool Output: {result_1}\n---")
    
    # Test send email tool execution
    result_2 = dispatcher.dispatch("send_email", {"email": "alice@corp.local"})
    print(f"Tool Output: {result_2}")
    print("===========================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
