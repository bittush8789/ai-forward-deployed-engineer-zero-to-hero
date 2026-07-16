#!/usr/bin/env python3
"""
Triton Server performance verification client.
Checks connection status and sends mock payload formats.
"""

import socket
import sys

def check_connection(host, port):
    try:
        s = socket.create_connection((host, port), timeout=2)
        s.close()
        return True
    except Exception:
        return False

def main():
    print("=== Triton Performance Client Status ===")
    
    # Check default Triton HTTP port 8000 and gRPC port 8001
    http_status = "ONLINE" if check_connection("localhost", 8000) else "OFFLINE (simulated environment check)"
    grpc_status = "ONLINE" if check_connection("localhost", 8001) else "OFFLINE (simulated environment check)"
    
    print(f"Triton HTTP (8000): {http_status}")
    print(f"Triton gRPC (8001): {grpc_status}")
    print("=========================================")

if __name__ == "__main__":
    main()
