#!/usr/bin/env python3
"""
LLM Observability and metrics exporter mock script.
Logs tokens consumption, latency, and costs.
"""

import sys

class ObservabilityExporter:
    def __init__(self, cost_per_k_input=0.0015, cost_per_k_output=0.0020):
        self.cost_per_k_input = cost_per_k_input
        self.cost_per_k_output = cost_per_k_output

    def log_inference_metrics(self, input_tokens: int, output_tokens: int, latency: float):
        print("=== Exporting LLM Observability Metrics ===")
        
        # Calculate cost
        input_cost = (input_tokens / 1000.0) * self.cost_per_k_input
        output_cost = (output_tokens / 1000.0) * self.cost_per_k_output
        total_cost = input_cost + output_cost
        
        print(f"Input/Output Tokens: {input_tokens} / {output_tokens}")
        print(f"Inference Latency: {latency:.2f} seconds")
        print(f"Calculated cost: ${total_cost:.5f}")
        print("Telemetry status: EXPORTED SUCCESS")
        print("==========================================")

def main():
    exporter = ObservabilityExporter()
    exporter.log_inference_metrics(1200, 800, 1.45)
    sys.exit(0)

if __name__ == "__main__":
    main()
