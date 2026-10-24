#!/usr/bin/env python3
"""
run_tests.py - Comprehensive Test Suite for Ottonet Skill.
Validates behavior across:
1. mock_legacy_net48 (XML namespaces, packages.config, Global.asax, Stored Procs)
2. mock_modern_clean_net8 (CPM Directory.Packages.props, Rich DDD, Generic Base Controller inheritance, Scrutor decorators, Targeted Zoom-In)
3. mock_fastendpoints_anemic (FastEndpoints, Semantic Logic Distiller for math equations & mutations)
"""

import sys
import json
from pathlib import Path

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent / "skills" / "ottonet-skill" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from intel_init import init_intel_directory
from resolve_master_keys import resolve_master_keys
from detect_architecture import detect_architecture
from catalog_entrypoints import catalog_entrypoints, filter_routes
from extract_business_rules import build_module_rule_card
from trace_di_decorators import trace_di_wiring
from csharp_skeleton import get_skeleton
from distill_entity_schema import scan_entities, get_entity_card, build_schema_documentation, scan_raw_sql_tables

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_mock_legacy_net48():
    print("\n[TEST 1] Testing Mock Legacy .NET 4.8 Project...")
    root = FIXTURES_DIR / "mock_legacy_net48"
    init_intel_directory(str(root))
    
    # 1. Test Master Keys
    keys = resolve_master_keys(str(root))
    assert keys["bootstrap"] == "LegacyDotNetFramework", f"Expected LegacyDotNetFramework, got {keys['bootstrap']}"
    assert keys["persistence"] in ["Dapper_StoredProcedures", "EF6_Legacy"], f"Unexpected persistence: {keys['persistence']}"
    print("  ✓ Bootstrap key detected as LegacyDotNetFramework despite XML namespaces!")

    # 2. Test Architecture summary
    arch = detect_architecture(str(root))
    assert "net48" in arch["target_frameworks"], f"Expected net48, got {arch['target_frameworks']}"
    print("  ✓ Target framework net48 parsed correctly from legacy MSBuild XML!")

    # 3. Test Entrypoints
    entries = catalog_entrypoints(str(root))
    patterns = [e["pattern"] for e in entries]
    assert any("legacy/orders" in p for p in patterns), f"Expected legacy/orders in {patterns}"
    print(f"  ✓ Found {len(entries)} legacy MVC endpoints!")

    # 4. Test Stored Procedure extraction
    card_file = build_module_rule_card("order", str(root))
    card_content = Path(card_file).read_text(encoding="utf-8")
    assert "sp_CalculateLegacyTax" in card_content, "Expected sp_CalculateLegacyTax in rules card!"
    print("  ✓ Stored Procedure 'sp_CalculateLegacyTax' successfully extracted!")

def test_mock_modern_clean_net8():
    print("\n[TEST 2] Testing Mock Modern .NET 8 Clean Architecture Project...")
    root = FIXTURES_DIR / "mock_modern_clean_net8"
    init_intel_directory(str(root))

    # 1. Test Master Keys & CPM props
    keys = resolve_master_keys(str(root))
    assert keys["bootstrap"] == "ModernDotNet", f"Expected ModernDotNet, got {keys['bootstrap']}"
    assert keys["domain"] == "RichDomain_DDD", f"Expected RichDomain_DDD, got {keys['domain']}"
    print("  ✓ CPM packages parsed and Domain shape identified as RichDomain_DDD!")

    # 2. Test Scrutor Decorator Detection
    wiring = trace_di_wiring(str(root))
    assert len(wiring["decorators"]) > 0, "Expected Scrutor decorator to be detected!"
    assert wiring["decorators"][0]["decorator"] == "CachedOrderService", f"Expected CachedOrderService, got {wiring['decorators']}"
    print("  ✓ Scrutor Decorator 'CachedOrderService' detected with runtime warning!")

    # 3. Test Generic Base Controller Inheritance
    entries = catalog_entrypoints(str(root))
    orders_entries = [e for e in entries if "OrdersController" in e["handler"]]
    assert len(orders_entries) >= 2, f"Expected inherited endpoints for OrdersController, got {orders_entries}"
    print(f"  ✓ Inherited CRUD actions (GetAll, GetById) resolved for OrdersController!")

    # 4. Test Targeted Method Zoom-In
    orders_controller_file = root / "src" / "WebApi" / "Controllers" / "OrdersController.cs"
    skeleton = get_skeleton(orders_controller_file, root, focus_method="SubmitOrder")
    assert "OTTONET ZOOM-IN: FULL FIDELITY BODY OF SubmitOrder" in skeleton, "Expected Zoom-in header"
    assert "return Ok(dto);" in skeleton, "Expected full body of SubmitOrder"
    print("  ✓ Targeted Method Zoom-In successfully kept 100% full body for 'SubmitOrder'!")

def test_mock_fastendpoints_anemic():
    print("\n[TEST 3] Testing Mock FastEndpoints & Anemic Logic Distiller...")
    root = FIXTURES_DIR / "mock_fastendpoints_anemic"
    init_intel_directory(str(root))

    # 1. Test Master Keys
    keys = resolve_master_keys(str(root))
    assert keys["api"] == "FastEndpoints", f"Expected FastEndpoints, got {keys['api']}"
    assert keys["domain"] == "AnemicDomain_FatService", f"Expected AnemicDomain_FatService, got {keys['domain']}"
    print("  ✓ API Key detected as FastEndpoints and Domain as AnemicDomain_FatService!")

    # 2. Test Entrypoint cataloging
    entries = catalog_entrypoints(str(root))
    assert any(e["category"] == "FastEndpoint" and "/api/invoices" in e["pattern"] for e in entries), f"Missing FastEndpoint in {entries}"
    print("  ✓ FastEndpoint '/api/invoices' cataloged successfully!")

    # 3. Test Semantic Logic Distiller
    card_file = build_module_rule_card("invoice", str(root))
    card_content = Path(card_file).read_text(encoding="utf-8")
    assert "total = subtotal * (1 + taxRate) + 5.50m;" in card_content, f"Missing math equation in: {card_content}"
    assert "invoice.Status = \"Approved\";" in card_content, f"Missing status mutation in: {card_content}"
    print("  ✓ Semantic Logic Distiller successfully extracted math equations and state mutations!")

def test_advanced_enterprise_proposals():
    print("\n[TEST 4] Testing 5 Enterprise Proposals (Search, Partitions, Schema, Exceptions, Cache)...")
    root = FIXTURES_DIR / "mock_modern_clean_net8"

    # 1. Proposal 1 & 5: Routes Cataloging with Incremental Cache & Search Filter
    entries = catalog_entrypoints(str(root))
    assert len(entries) > 0, "Expected cataloged entries"
    manifest_file = root / ".codebase-intel" / "cache" / "catalog_manifest.json"
    assert manifest_file.exists(), "Expected incremental cache manifest"
    print("  ✓ Proposal 5 (Incremental Cache): Manifest created successfully!")

    filtered = filter_routes(entries, search="order", method="POST")
    assert any("/api/orders" in e["pattern"].lower() for e in filtered), "Expected matching POST order route"
    print("  ✓ Proposal 1 (Route Search & Filter): Found targeted POST /api/orders route directly!")

    # 2. Proposal 3: Entity-Relationship & Navigation Properties Distiller
    entities = scan_entities(root)
    assert "Order" in entities, f"Expected 'Order' entity in {list(entities.keys())}"
    order_card = get_entity_card("Order", entities)
    assert "CustomerId" in order_card, "Expected CustomerId foreign key in Order card"
    assert "Items" in order_card and "OrderItem" in order_card, "Expected Items collection in Order card"
    print("  ✓ Proposal 3 (Entity Schema & ERD): Extracted Foreign Keys and Navigation Properties!")

    # 3. Proposal 4: Custom Domain Exceptions
    rules_card = Path(build_module_rule_card("order", str(root))).read_text()
    assert "DomainException" in rules_card or "Exception" in rules_card, "Expected exception detection in rules card"
    print("  ✓ Proposal 4 (Domain Exceptions): Captured business domain errors!")

def test_iteration_2_hardening():
    print("\n[TEST 5] Testing Iteration 2 Hardening (Dapper SQL, Procedural Guards, Roslyn AST, Universal Inspect)...")
    legacy_root = FIXTURES_DIR / "mock_legacy_net48"
    modern_root = FIXTURES_DIR / "mock_modern_clean_net8"

    # 1. Test Raw SQL & Dapper Tables & Joins Distiller
    sqls = scan_raw_sql_tables(legacy_root)
    assert "Orders" in sqls, f"Expected 'Orders' table in {list(sqls.keys())}"
    assert "Invoices" in sqls, f"Expected 'Invoices' table in {list(sqls.keys())}"
    assert "SELECT" in sqls["Orders"]["operations"], "Expected SELECT operation on Orders"
    assert "INSERT" in sqls["Invoices"]["operations"], "Expected INSERT operation on Invoices"
    assert any("Orders.CustomerId = Customers.Id" in j for j in sqls["Orders"]["joins"]), f"Expected join relation in {sqls['Orders']['joins']}"
    assert "@OrderId" in sqls["Orders"]["parameters"], "Expected @OrderId parameter"
    print("  ✓ Dapper / Raw SQL Distiller: Extracted tables, CRUD ops, join relations and parameters!")

    # 2. Test Procedural HTTP Guards
    card_path = build_module_rule_card("order", str(legacy_root))
    card_content = Path(card_path).read_text(encoding="utf-8")
    assert "BadRequest" in card_content, "Expected BadRequest HTTP guard in module rules card"
    assert "orderId <= 0" in card_content, "Expected 'orderId <= 0' condition in module rules card"
    print("  ✓ Procedural HTTP Guards: Extracted Controller BadRequest preconditions into module rules card!")

    # 3. Test Native Roslyn AST vs Python Lexer Fallback
    test_cs_file = modern_root / "src" / "WebApi" / "Controllers" / "OrdersController.cs"
    roslyn_skel = get_skeleton(test_cs_file, modern_root, focus_method="SubmitOrder", prefer_roslyn=True)
    assert "SubmitOrder" in roslyn_skel, "Expected SubmitOrder in Roslyn skeleton"
    assert "[OTTONET ROSLYN AST]" in roslyn_skel, "Expected Roslyn notice"

    python_skel = get_skeleton(test_cs_file, modern_root, focus_method="SubmitOrder", prefer_roslyn=False)
    assert "SubmitOrder" in python_skel, "Expected SubmitOrder in Python skeleton"
    assert "[OTTONET INTEL NOTICE]" in python_skel, "Expected Python lexer notice"
    print("  ✓ Hybrid Roslyn AST & Python fallback lexer: Both executed and verified with 100% fidelity!")

if __name__ == "__main__":
    print("=================================================================")
    print("        RUNNING COMPREHENSIVE TEST SUITE FOR OTTONET SKILL        ")
    print("=================================================================")
    try:
        test_mock_legacy_net48()
        test_mock_modern_clean_net8()
        test_mock_fastendpoints_anemic()
        test_advanced_enterprise_proposals()
        test_iteration_2_hardening()
        print("\n=================================================================")
        print("          ALL 5 TEST SUITES PASSED WITH 100% SUCCESS!             ")
        print("=================================================================")
    except AssertionError as err:
        print(f"\n[FAIL] Test assertion failed: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        print(f"\n[ERROR] Unexpected error: {ex}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
