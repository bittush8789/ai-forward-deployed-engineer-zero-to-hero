#!/usr/bin/env python3
"""
Lab 4: Milvus cluster connection status checker and collection health validator.
Simulates node health checks and collection schema validation.
"""
import sys
import socket
import time


def check_port(host: str, port: int, timeout: float = 1.5) -> bool:
    """Test TCP connectivity to a host:port."""
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.close()
        return True
    except (ConnectionRefusedError, OSError, TimeoutError):
        return False


def simulate_cluster_status() -> dict:
    """Simulate Milvus cluster component health status."""
    return {
        "root_coord":  {"status": "HEALTHY", "uptime_sec": 14400},
        "query_node":  {"status": "HEALTHY", "uptime_sec": 14400, "loaded_segments": 12},
        "data_node":   {"status": "HEALTHY", "uptime_sec": 14200, "pending_flushes": 0},
        "index_node":  {"status": "HEALTHY", "uptime_sec": 14000, "building_tasks": 1},
        "proxy":       {"status": "HEALTHY", "uptime_sec": 14400, "qps": 42.5},
    }


def simulate_collections() -> list:
    """Simulate Milvus collection metadata."""
    return [
        {
            "name": "enterprise_knowledge",
            "row_count": 1_240_000,
            "dim": 1536,
            "index_type": "HNSW",
            "index_built": True,
            "shards": 2
        },
        {
            "name": "agent_memory",
            "row_count": 88_000,
            "dim": 768,
            "index_type": "IVF_FLAT",
            "index_built": True,
            "shards": 1
        }
    ]


def main():
    print("=" * 60)
    print(" Milvus Cluster Health Check")
    print("=" * 60)

    milvus_host = "localhost"
    milvus_port = 19530

    # --- Check TCP connectivity ---
    print(f"\n[1] Checking TCP connection to {milvus_host}:{milvus_port}...")
    connected = check_port(milvus_host, milvus_port)
    if connected:
        print("    Status: CONNECTED")
    else:
        print("    Status: OFFLINE (simulated — running in mock mode)")

    # --- Node health status ---
    print("\n[2] Cluster Node Health:")
    status = simulate_cluster_status()
    all_healthy = True
    for component, info in status.items():
        health = info["status"]
        uptime_h = info["uptime_sec"] // 3600
        extra = ""
        if "loaded_segments" in info:
            extra = f"| loaded_segments={info['loaded_segments']}"
        elif "qps" in info:
            extra = f"| qps={info['qps']}"
        status_symbol = "OK" if health == "HEALTHY" else "WARN"
        print(f"    [{status_symbol}] {component:<15} uptime={uptime_h}h {extra}")
        if health != "HEALTHY":
            all_healthy = False

    # --- Collection validation ---
    print("\n[3] Collection Schema Validation:")
    collections = simulate_collections()
    for col in collections:
        index_ok = "BUILT" if col["index_built"] else "NOT BUILT"
        row_fmt = f"{col['row_count']:,}"
        print(f"    Collection  : {col['name']}")
        print(f"    Row Count   : {row_fmt}")
        print(f"    Dimensions  : {col['dim']}")
        print(f"    Index Type  : {col['index_type']} ({index_ok})")
        print(f"    Shards      : {col['shards']}")
        print()

    # --- Summary ---
    print("=" * 60)
    if all_healthy:
        print("RESULT: All cluster components are HEALTHY.")
    else:
        print("RESULT: One or more components require attention.")
    print("Milvus cluster check completed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
