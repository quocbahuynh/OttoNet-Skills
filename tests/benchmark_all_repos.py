#!/usr/bin/env python3
"""
benchmark_all_repos.py - Automated Benchmark & Comparison Suite for Ottonet Skill.
Runs full scans, route extraction, entity & raw SQL table discovery, invariant mining,
and Roslyn AST skeletonization across all 13 real-world GitHub repositories + mock fixtures.
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any

# Insert scripts path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "skills" / "ottonet-skill" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from intel_init import init_intel_directory
from resolve_master_keys import resolve_master_keys
from detect_architecture import detect_architecture
from catalog_entrypoints import catalog_entrypoints, filter_routes
from distill_entity_schema import scan_entities, scan_raw_sql_tables, build_schema_documentation
from extract_business_rules import build_module_rule_card, extract_rules_from_file
from trace_di_decorators import trace_di_wiring
from csharp_skeleton import get_skeleton

REPOS_DIR = Path(__file__).resolve().parent / "real_world_repos"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

def count_raw_codebase_tokens(repo_path: Path) -> int:
    total_bytes = 0
    for cs in repo_path.rglob("*.cs"):
        parts = cs.parts
        if any(x in parts for x in [".codebase-intel", "bin", "obj", "node_modules", ".git", "TestResults"]):
            continue
        try:
            total_bytes += cs.stat().st_size
        except Exception:
            pass
    return total_bytes // 4

def count_intel_tokens(repo_path: Path) -> int:
    intel_dir = repo_path / ".codebase-intel"
    if not intel_dir.exists():
        return 0
    total_bytes = 0
    for f in intel_dir.rglob("*"):
        if f.is_file() and not f.name.endswith(".gitignore"):
            try:
                total_bytes += f.stat().st_size
            except Exception:
                pass
    return total_bytes // 4

def benchmark_repo(name: str, repo_path: Path) -> Dict[str, Any]:
    print(f"\n=======================================================")
    print(f"BENCHMARKING: {name}")
    print(f"Path: {repo_path}")
    print(f"=======================================================")

    t0 = time.perf_counter()

    # 1. Init
    init_intel_directory(str(repo_path))

    # 2. Master Keys
    keys = resolve_master_keys(str(repo_path))

    # 3. Architecture
    arch = detect_architecture(str(repo_path))

    # 4. Entrypoints
    routes = catalog_entrypoints(str(repo_path), force=True)

    # 5. Entities (EF Core & Sealed/Record)
    entities = scan_entities(repo_path)

    # 6. Raw SQL / Dapper Tables
    sql_tables = scan_raw_sql_tables(repo_path)
    build_schema_documentation(entities, str(repo_path), sql_tables)

    # 7. Wiring / Decorators
    wiring = trace_di_wiring(str(repo_path))

    # 8. Business Rules Sample Scan
    sample_rules_count = 0
    procedural_guards_count = 0
    calculations_count = 0
    for cs in repo_path.rglob("*.cs"):
        parts = cs.parts
        if any(x in parts for x in [".codebase-intel", "bin", "obj", "node_modules", ".git", "TestResults"]):
            continue
        res = extract_rules_from_file(cs)
        if res:
            sample_rules_count += len(res.get("guard_invariants", [])) + len(res.get("validators", []))
            procedural_guards_count += len(res.get("procedural_guards", []))
            calculations_count += len(res.get("calculations", []))

    scan_duration = time.perf_counter() - t0

    # 9. Token Footprints
    raw_tokens = count_raw_codebase_tokens(repo_path)
    intel_tokens = count_intel_tokens(repo_path)
    reduction = ((raw_tokens - intel_tokens) / raw_tokens * 100) if raw_tokens > 0 else 0

    # 10. Sample Zoom Test
    zoom_verified = False
    sample_cs = next(
        (f for f in repo_path.rglob("*.cs")
         if not any(x in f.parts for x in [".codebase-intel", "bin", "obj", "node_modules", ".git"])
         and ("Controller" in f.name or "Service" in f.name or "Handler" in f.name)),
        None
    )
    if sample_cs:
        skel = get_skeleton(sample_cs, repo_path, prefer_roslyn=True)
        zoom_verified = bool(skel and len(skel) > 50)

    result = {
        "name": name,
        "path": str(repo_path),
        "duration_sec": round(scan_duration, 3),
        "bootstrap": keys.get("bootstrap", ""),
        "api_key": keys.get("api", ""),
        "domain_key": keys.get("domain", ""),
        "persistence_key": keys.get("persistence", ""),
        "routes_count": len(routes),
        "entities_count": len(entities),
        "sql_tables_count": len(sql_tables),
        "decorators_count": len(wiring.get("decorators", [])),
        "domain_invariants": sample_rules_count,
        "procedural_guards": procedural_guards_count,
        "calculations": calculations_count,
        "raw_tokens": raw_tokens,
        "intel_tokens": intel_tokens,
        "token_reduction_pct": round(reduction, 1),
        "zoom_verified": zoom_verified
    }

    print(f"  ✓ Master Keys: {keys['bootstrap']} | {keys['api']} | {keys['domain']} | {keys['persistence']}")
    print(f"  ✓ Routes: {len(routes)} routes cataloged")
    print(f"  ✓ Schemas: {len(entities)} Entities | {len(sql_tables)} Raw SQL/Dapper Tables")
    print(f"  ✓ Invariants: {sample_rules_count} Domain Rules | {procedural_guards_count} Procedural HTTP Guards")
    print(f"  ✓ Time: {round(scan_duration, 3)}s | Raw: {raw_tokens:,} tokens | Intel: {intel_tokens:,} tokens ({round(reduction, 1)}% reduction)")

    return result

def main():
    print("=================================================================")
    print("      RUNNING FULL BENCHMARK & COMPARISON ON ALL REPOSITORIES     ")
    print("=================================================================")

    target_repos = [
        ("EduardoPires_EquinoxProject", REPOS_DIR / "EduardoPires_EquinoxProject"),
        ("Pentatomic_BillingSystem", REPOS_DIR / "Pentatomic_BillingSystem"),
        ("Tayara_AccountingSystem", REPOS_DIR / "Tayara_AccountingSystem"),
        ("amantinband_clean_architecture", REPOS_DIR / "amantinband_clean_architecture"),
        ("ardalis_CleanArchitecture", REPOS_DIR / "ardalis_CleanArchitecture"),
        ("dotnet_eShop", REPOS_DIR / "dotnet_eShop"),
        ("gothinkster_realworld", REPOS_DIR / "gothinkster_realworld"),
        ("ivanpaulovich_clean_architecture", REPOS_DIR / "ivanpaulovich_clean_architecture"),
        ("jasontaylordev_CleanArchitecture", REPOS_DIR / "jasontaylordev_CleanArchitecture"),
        ("jasontaylordev_NorthwindTraders", REPOS_DIR / "jasontaylordev_NorthwindTraders"),
        ("kgrzybek_modular_monolith", REPOS_DIR / "kgrzybek_modular_monolith"),
        ("nikiforovall_minimal_api_example", REPOS_DIR / "nikiforovall_minimal_api_example"),
        ("simplcommerce_SimplCommerce", REPOS_DIR / "simplcommerce_SimplCommerce"),
    ]

    # Add mock fixtures
    mock_fixtures = [
        ("mock_legacy_net48", FIXTURES_DIR / "mock_legacy_net48"),
        ("mock_modern_clean_net8", FIXTURES_DIR / "mock_modern_clean_net8"),
        ("mock_fastendpoints_anemic", FIXTURES_DIR / "mock_fastendpoints_anemic"),
    ]

    results = []

    # Run real-world repos
    for name, path in target_repos:
        if path.exists():
            res = benchmark_repo(name, path)
            results.append(res)
        else:
            print(f"[WARN] Repository {path} does not exist. Skipping.")

    # Run mock fixtures
    print("\n-------------------------------------------------------")
    print("RUNNING BENCHMARKS ON MOCK TEST FIXTURES")
    print("-------------------------------------------------------")
    for name, path in mock_fixtures:
        if path.exists():
            res = benchmark_repo(name, path)
            results.append(res)

    # Save results as JSON
    out_json = Path(__file__).resolve().parent / "benchmark_results.json"
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n[OK] Benchmark results written to: {out_json}")

if __name__ == "__main__":
    main()
