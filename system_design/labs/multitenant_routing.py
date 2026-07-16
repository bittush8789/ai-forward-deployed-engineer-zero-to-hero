#!/usr/bin/env python3
"""
Multi-Tenant API Gateway headers validation and routing script.
"""

import sys

def validate_tenant_routing(request_headers: dict):
    print("=== Ingress Gateway Header Validation ===")
    
    tenant_header = request_headers.get("X-Tenant-ID")
    if not tenant_header:
        print("Error: Missing required X-Tenant-ID header. Rejecting request.")
        return False
        
    valid_tenants = ["bank-a", "bank-b", "bank-c"]
    if tenant_header not in valid_tenants:
        print(f"Error: Unauthorized Tenant ID: '{tenant_header}'. Rejecting request.")
        return False
        
    print(f"Success: Tenant '{tenant_header}' authorized.")
    print(f"Routing rule: Namespace = '{tenant_header}' | DB Schema = '{tenant_header}_db'")
    print("=========================================")
    return True

def main():
    # 1. Check unauthorized header
    validate_tenant_routing({"X-Tenant-ID": "invalid-bank"})
    print("---")
    # 2. Check authorized header
    validate_tenant_routing({"X-Tenant-ID": "bank-c"})

if __name__ == "__main__":
    main()
