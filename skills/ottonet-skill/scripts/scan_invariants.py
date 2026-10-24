#!/usr/bin/env python3
"""
scan_invariants.py - Cross-Cutting Invariants Scanner for Ottonet Skill.
Detects:
1. Multi-Tenancy (TenantId, ITenantScoped, IMultiTenant)
2. Soft-Delete (ISoftDelete, IsDeleted, DeletedAt)
3. Auditing (IAuditableEntity, CreatedAt, CreatedBy, LastModifiedAt)
4. EF Core Global Query Filters (HasQueryFilter)

Outputs:
- .codebase-intel/invariants/cross-cutting.json
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Any

INTEL_DIR_NAME = ".codebase-intel"

MULTI_TENANT_PATTERNS = [r'ITenant', r'IMultiTenant', r'TenantId', r'CompanyId', r'OrganizationId']
SOFT_DELETE_PATTERNS = [r'ISoftDelete', r'ISoftDeletable', r'IsDeleted', r'DeletedAt']
AUDIT_PATTERNS = [r'IAuditable', r'IAuditedEntity', r'CreatedAt', r'CreatedBy', r'LastModifiedAt']
QUERY_FILTER_REGEX = re.compile(r'HasQueryFilter\s*\(\s*([^)]+)\)', re.IGNORECASE)

def scan_invariants(target_root: str = ".") -> Dict[str, Any]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    inv_dir = intel_dir / "invariants"
    inv_dir.mkdir(parents=True, exist_ok=True)
    output_file = inv_dir / "cross-cutting.json"

    detected_multi_tenant = set()
    detected_soft_delete = set()
    detected_auditing = set()
    detected_query_filters = []

    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git"]):
            continue
        try:
            content = cs_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        rel = str(cs_file.relative_to(root))

        for pat in MULTI_TENANT_PATTERNS:
            if re.search(r'\b' + pat + r'\b', content):
                detected_multi_tenant.add(pat)

        for pat in SOFT_DELETE_PATTERNS:
            if re.search(r'\b' + pat + r'\b', content):
                detected_soft_delete.add(pat)

        for pat in AUDIT_PATTERNS:
            if re.search(r'\b' + pat + r'\b', content):
                detected_auditing.add(pat)

        for qf in QUERY_FILTER_REGEX.finditer(content):
            detected_query_filters.append({
                "filter": qf.group(1).strip(),
                "file": rel
            })

    result = {
        "multi_tenancy": {
            "enabled": len(detected_multi_tenant) > 0,
            "indicators": sorted(list(detected_multi_tenant)),
            "warning": "CRITICAL: Ensure all entity queries and insertions include/respect TenantId!" if detected_multi_tenant else "None"
        },
        "soft_delete": {
            "enabled": len(detected_soft_delete) > 0,
            "indicators": sorted(list(detected_soft_delete)),
            "warning": "CRITICAL: Do NOT execute hard deletes (context.Remove). Set IsDeleted = true!" if detected_soft_delete else "None"
        },
        "auditing": {
            "enabled": len(detected_auditing) > 0,
            "indicators": sorted(list(detected_auditing)),
            "note": "Audited entities: populate or allow interceptors to fill CreatedAt/CreatedBy/ModifiedAt."
        },
        "ef_query_filters": detected_query_filters[:10]
    }

    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    res = scan_invariants(target)
    print("============== OTTONET SKILL: CROSS-CUTTING INVARIANTS ==============")
    print(f"Multi-Tenancy Active: {res['multi_tenancy']['enabled']} ({', '.join(res['multi_tenancy']['indicators']) or 'None'})")
    print(f"Soft-Delete Active:   {res['soft_delete']['enabled']} ({', '.join(res['soft_delete']['indicators']) or 'None'})")
    print(f"Auditing Active:      {res['auditing']['enabled']} ({', '.join(res['auditing']['indicators']) or 'None'})")
    print(f"EF Query Filters:     {len(res['ef_query_filters'])} detected")
    print("=====================================================================")
