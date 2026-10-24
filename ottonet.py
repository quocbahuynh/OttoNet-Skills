#!/usr/bin/env python3
"""
ottonet.py - Universal Single-Entrypoint CLI for Ottonet Skill.
Works seamlessly across all AI Coding Agents (Google Antigravity, Cursor, Claude Code, GitHub Copilot, Windsurf, Cline).

Usage:
  python ottonet.py init [target_root]
  python ottonet.py scan [target_root]
  python ottonet.py keys [target_root]
  python ottonet.py routes [target_root]
  python ottonet.py zoom <file_path> --method <method_name>
  python ottonet.py rules <module_name> [target_root]
  python ottonet.py wiring [target_root]
  python ottonet.py switch --task <id> --domain <module_name> [target_root]
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent / "skills" / "ottonet-skill" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from intel_init import init_intel_directory
from resolve_master_keys import resolve_master_keys
from detect_architecture import detect_architecture
from catalog_entrypoints import catalog_entrypoints, filter_routes
from extract_business_rules import build_module_rule_card
from trace_di_decorators import trace_di_wiring
from scan_invariants import scan_invariants
from detect_conventions import detect_conventions
from csharp_skeleton import get_skeleton
from domain_manager import switch_domain
from distill_entity_schema import scan_entities, build_schema_documentation, get_entity_card, scan_raw_sql_tables

def main():
    parser = argparse.ArgumentParser(
        prog="ottonet",
        description="Ottonet Skill: Universal Enterprise ASP.NET Intelligence CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    # init
    init_p = subparsers.add_parser("init", help="Initialize .codebase-intel with strict Git isolation")
    init_p.add_argument("root", nargs="?", default=".", help="Root directory")

    # scan (full discovery)
    scan_p = subparsers.add_parser("scan", help="Run full discovery (keys, routes, wiring, invariants, conventions, schema)")
    scan_p.add_argument("root", nargs="?", default=".", help="Root directory")
    scan_p.add_argument("--force", action="store_true", help="Bypass incremental cache and force re-scan")

    # keys
    keys_p = subparsers.add_parser("keys", help="Resolve 4 Master Keys Discriminator in 0.05s")
    keys_p.add_argument("root", nargs="?", default=".", help="Root directory")

    # routes
    routes_p = subparsers.add_parser("routes", help="Catalog and query entry points with search and method filters")
    routes_p.add_argument("root", nargs="?", default=".", help="Root directory")
    routes_p.add_argument("--search", "-s", help="Filter routes by keyword")
    routes_p.add_argument("--method", "-m", help="Filter routes by HTTP method")
    routes_p.add_argument("--force", action="store_true", help="Bypass incremental cache")

    # schema (Entity-Relationship & Navigation Properties Distiller)
    schema_p = subparsers.add_parser("schema", help="Distill entity schema, foreign keys, navigation properties & Mermaid ERD")
    schema_p.add_argument("entity", nargs="?", default="", help="Optional entity name to inspect (e.g. Order, Invoice)")
    schema_p.add_argument("root", nargs="?", default=".", help="Root directory")

    # zoom
    zoom_p = subparsers.add_parser("zoom", help="Targeted Method Zoom-In (full body for target method, skeleton for others)")
    zoom_p.add_argument("file", help="Path to C# file")
    zoom_p.add_argument("--method", "-m", default=None, help="Method name to Zoom-In with 100%% full body fidelity")
    zoom_p.add_argument("--distill", action="store_true", help="Enable Semantic Logic Distiller")
    zoom_p.add_argument("--full", action="store_true", help="Display full unabridged source code")
    zoom_p.add_argument("--root", default=".", help="Root directory")

    # rules
    rules_p = subparsers.add_parser("rules", help="Extract distilled business rules & algorithms for a module")
    rules_p.add_argument("module", help="Module or domain name")
    rules_p.add_argument("root", nargs="?", default=".", help="Root directory")

    # inspect (Universal Single-Target Intelligence Investigator)
    inspect_p = subparsers.add_parser("inspect", help="Universal investigator: inspect file, route, entity, or module in 1 shot")
    inspect_p.add_argument("target", help="File path, route path (/api/...), entity name (Order), or module name (Billing)")
    inspect_p.add_argument("--method", "-m", help="Method name to focus if target is a C# file")
    inspect_p.add_argument("--full", action="store_true", help="Display full unabridged source if target is a file")
    inspect_p.add_argument("--root", default=".", help="Root directory")

    # wiring
    wiring_p = subparsers.add_parser("wiring", help="Trace runtime DI and Scrutor decorators")
    wiring_p.add_argument("root", nargs="?", default=".", help="Root directory")

    # switch
    switch_p = subparsers.add_parser("switch", help="Switch task/domain context card")
    switch_p.add_argument("--task", required=True, help="Task ID (e.g. 103)")
    switch_p.add_argument("--domain", required=True, help="Domain/Module name (e.g. project-schedule)")
    switch_p.add_argument("root", nargs="?", default=".", help="Root directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        p = init_intel_directory(args.root)
        print(f"[OK] Ottonet initialized at: {p}")
    elif args.command == "keys":
        k = resolve_master_keys(args.root)
        print(f"[OK] 4 Master Keys: Bootstrap={k['bootstrap']} | API={k['api']} | Domain={k['domain']} | Persistence={k['persistence']}")
    elif args.command == "scan":
        init_intel_directory(args.root)
        k = resolve_master_keys(args.root)
        arch = detect_architecture(args.root)
        wiring = trace_di_wiring(args.root)
        inv = scan_invariants(args.root)
        conv = detect_conventions(args.root)
        routes = catalog_entrypoints(args.root, force=args.force)
        ents = scan_entities(Path(args.root).resolve())
        sqls = scan_raw_sql_tables(Path(args.root).resolve())
        build_schema_documentation(ents, args.root, sqls)
        print(f"[OK] Full Scan Complete: {len(routes)} routes | {len(ents)} entities | {len(sqls)} raw SQL tables | {len(wiring['decorators'])} decorators | Mode {k['api']}")
    elif args.command == "routes":
        routes = catalog_entrypoints(args.root, force=args.force)
        if args.search or args.method:
            matches = filter_routes(routes, search=args.search or "", method=args.method or "")
            print(f"[OK] Found {len(matches)} matching entry points:")
            print("| Category | Verb | Route / Pattern | Handler / Class | Source File |")
            print("| :--- | :--- | :--- | :--- | :--- |")
            for m in matches:
                print(f"| `{m['category']}` | **{m['trigger']}** | `{m['pattern']}` | `{m['handler']}` | [{m['file']}#L{m['line']}]({m['file']}) |")
        else:
            print(f"[OK] Cataloged {len(routes)} entrypoints in .codebase-intel/entrypoints/catalog.md")
    elif args.command == "schema":
        root = args.root
        ent = args.entity
        if ent and Path(ent).is_dir():
            root, ent = ent, ""
        all_ents = scan_entities(Path(root).resolve())
        all_sqls = scan_raw_sql_tables(Path(root).resolve())
        if ent:
            card = get_entity_card(ent, all_ents, all_sqls)
            print(card)
        else:
            doc = build_schema_documentation(all_ents, root, all_sqls)
            print(f"[OK] Discovered {len(all_ents)} entities and {len(all_sqls)} raw SQL tables. Schema written to: {doc}")
    elif args.command == "zoom":
        target = Path(args.file).resolve()
        skel = get_skeleton(target, Path(args.root).resolve(), focus_method=args.method, distill=args.distill, full=args.full)
        print(skel)
    elif args.command == "rules":
        root = args.root
        module = args.module
        # Ergonomic safeguard: allow both 'rules <module> [root]' and 'rules <root> <module>'
        if Path(module).is_dir() and not Path(root).is_dir():
            module, root = root, module
        card = build_module_rule_card(module, root)
        print(f"[OK] Rules card generated: {card}")
    elif args.command == "inspect":
        root = Path(args.root).resolve()
        target = args.target.strip()

        # Case 1: Target is an existing file
        target_path = Path(target)
        if not target_path.is_absolute():
            target_path = root / target
        if target_path.is_file():
            skel = get_skeleton(target_path, root, focus_method=args.method, full=args.full)
            print(skel)
        # Case 2: Target is a Route (/api/... or GET /...)
        elif target.startswith("/") or any(target.upper().startswith(v + " ") for v in ["GET", "POST", "PUT", "DELETE", "PATCH"]):
            verb = ""
            route_part = target
            for v in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                if target.upper().startswith(v + " "):
                    verb = v
                    route_part = target[len(v):].strip()
                    break
            routes = catalog_entrypoints(str(root))
            matches = filter_routes(routes, search=route_part, method=verb)
            if matches:
                print(f"[OK] Found {len(matches)} matching entry point(s) for '{target}':")
                print("| Category | Verb | Route / Pattern | Handler / Class | Source File |")
                print("| :--- | :--- | :--- | :--- | :--- |")
                for m in matches:
                    print(f"| `{m['category']}` | **{m['trigger']}** | `{m['pattern']}` | `{m['handler']}` | [{m['file']}#L{m['line']}]({m['file']}) |")
            else:
                print(f"[WARN] No routes matching '{target}' found in catalog.")
        # Case 3: Target matches an Entity or Raw SQL Table
        else:
            ents = scan_entities(root)
            sqls = scan_raw_sql_tables(root)
            matched_ent = any(e.lower() == target.lower() for e in ents)
            matched_sql = any(t.lower() == target.lower() or t.lower() == f"{target}s".lower() or f"{t}s".lower() == target.lower() for t in sqls)
            if matched_ent or matched_sql:
                card = get_entity_card(target, ents, sqls)
                print(card)
            else:
                # Case 4: Target matches a Module or Domain
                card_file = build_module_rule_card(target, str(root))
                if Path(card_file).exists():
                    card_content = Path(card_file).read_text(encoding="utf-8")
                    print(card_content)
                else:
                    print(f"[WARN] Could not identify target '{target}'. Available entities: {', '.join(sorted(ents.keys())[:10])}")
    elif args.command == "wiring":
        w = trace_di_wiring(args.root)
        print(f"[OK] Wiring complete: {len(w['decorators'])} decorators detected")
    elif args.command == "switch":
        res = switch_domain(args.task, args.domain, args.root)
        print(f"[OK] Switched to Task #{args.task} (Domain: {args.domain})")

if __name__ == "__main__":
    main()
