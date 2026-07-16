#!/usr/bin/env python3
"""
Hospital Care Guidelines Knowledge Query simulator.
Query internal documents and return references.
"""

import sys

def search_care_guidelines(query_str: str):
    print(f"Clinician Query: '{query_str}'")
    
    # Mock RAG matching logic
    mock_db = {
        "heart attack": {
            "action": "Administer aspirin immediately and prepare for EKG.",
            "source": "American Heart Association Guidelines 2024, Page 12"
        },
        "burns": {
            "action": "Cool the burn with running water for 10 minutes.",
            "source": "First Aid Medical Manual, Page 45"
        }
    }
    
    # Search DB
    match = None
    for key in mock_db:
        if key in query_str.lower():
            match = mock_db[key]
            break
            
    print("=== Search Results ===")
    if match:
        print(f"Care Protocol: {match['action']}")
        print(f"Citation: {match['source']}")
    else:
        print("No matching care guidelines found. Refer to duty physician.")
    print("======================\n")

def main():
    search_care_guidelines("Protocol for patient with chest pain and suspected heart attack")
    sys.exit(0)

if __name__ == "__main__":
    main()
