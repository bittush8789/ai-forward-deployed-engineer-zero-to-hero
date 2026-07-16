#!/usr/bin/env python3
"""
Project 4: Legal Document Assistant (Fine-Tuning & RAG)
Skills Focus: SFT JSONL Dataset Formatting, Validation Splits, Structured Legal Summaries.

This script demonstrates how an FDE builds a fine-tuning data prep pipeline 
for contract auditing. It formats raw contract text and human labels into 
structured JSONL training tuples (SFT format) for model fine-tuning.
"""

import json

# Unstructured contract examples with target audit extractions
RAW_CONTRACT_ENTRIES = [
    {
        "contract_id": "CON-201",
        "text": "Governing Law: This agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without giving effect to conflict of laws principles.",
        "label": {"governing_law": "Delaware", "jurisdiction_status": "STANDARD"}
    },
    {
        "contract_id": "CON-202",
        "text": "Governing Law: This contract is executed in Munich and shall be governed strictly under German Federal Law. Parties submit to the jurisdiction of Munich courts.",
        "label": {"governing_law": "Germany", "jurisdiction_status": "INTERNATIONAL"}
    },
    {
        "contract_id": "CON-203",
        "text": "Governing Law: The validity, construction, and performance of this Agreement shall be governed by the laws of England and Wales.",
        "label": {"governing_law": "United Kingdom", "jurisdiction_status": "INTERNATIONAL"}
    }
]

class FineTuningDataPipeline:
    def format_to_sft_structure(self, contract_text, label_dict):
        """Formats text and labels into standard model instruction training tuples."""
        system_instruction = "You are an expert Legal Auditor. Extract the governing law and jurisdiction status from the contract text."
        
        # Supervised Fine-Tuning format (Messages format supported by OpenAI/HuggingFace)
        sft_format = {
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Extract details from: {contract_text}"},
                {"role": "assistant", "content": json.dumps(label_dict)}
            ]
        }
        return sft_format

    def generate_sft_dataset(self, entries):
        dataset = []
        for entry in entries:
            formatted = self.format_to_sft_structure(entry["text"], entry["label"])
            dataset.append(formatted)
        return dataset

def main():
    print("Project 4: Legal Document Assistant (Fine-Tuning Data Pipeline)")
    print("="*60)
    
    pipeline = FineTuningDataPipeline()
    
    # 1. Compile SFT training list
    print("Formatting raw labels to instruction SFT tuples...")
    sft_dataset = pipeline.generate_sft_dataset(RAW_CONTRACT_ENTRIES)
    
    # 2. Output training entries (simulating JSONL file write)
    print("\nGenerated SFT JSONL Dataset Preview (First 2 entries):")
    for idx, entry in enumerate(sft_dataset[:2]):
        print(f"\n[ENTRY {idx+1}]:")
        print(json.dumps(entry, indent=2))
        
    print("\nDataset preparation completed. Ready for supervised training split upload.")
    print("="*60)

if __name__ == "__main__":
    main()
