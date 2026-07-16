#!/usr/bin/env python3
"""
Automated FDE discovery workshop agenda template generator.
"""

import sys

def generate_agenda(client_name: str, use_case: str):
    print(f"=== Discovery Workshop Agenda for {client_name} ===")
    print(f"Target Use Case: {use_case}\n")
    
    agenda = [
        ("09:00 - 09:30", "Executive Alignment Meeting (Sponsor sync & KPIs alignment)"),
        ("09:30 - 11:30", "As-Is Process Mapping Session (Audit manual workflows & pain points)"),
        ("11:30 - 12:30", "To-Be Design Scoping Session (Brainstorming AI solution design flows)"),
        ("13:30 - 15:00", "Technical Architecture Discovery Session (Identify data access & APIs)"),
        ("15:00 - 16:30", "Use Case Prioritization Mapping & Implementation Roadmap Setup")
    ]
    
    for time_slot, activity in agenda:
        print(f"[{time_slot}] - {activity}")
    print("====================================================")

def main():
    generate_agenda("MetLife Insurance", "Claims Ingestion AI Copilot")
    sys.exit(0)

if __name__ == "__main__":
    main()
