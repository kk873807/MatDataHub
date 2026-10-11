"""
Tenant Isolation Test Runner.

Executes hermetic cross-tenant verification covering:
  - Multi-tenant BOM history isolation
  - Direct detail query isolation (404 on cross-tenant access)
  - Cross-tenant delete protection (cannot delete another tenant's rows)
  - Unauthenticated access rejection (401)
  - Tier gating on CBAM modeling (403 for free tier)
  - Custom material isolation
  - Transaction ledger isolation
"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from tests.test_tenant_isolation import test_tenant_isolation

if __name__ == "__main__":
    print("Running Tenant Isolation Tests...")
    test_tenant_isolation()
    print("ALL TENANT ISOLATION TESTS PASSED (8/8)")
