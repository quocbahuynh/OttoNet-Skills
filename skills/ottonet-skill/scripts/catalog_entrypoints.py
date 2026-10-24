#!/usr/bin/env python3
"""
catalog_entrypoints.py - Targeted Entrypoint Cataloger for Ottonet Skill.
Hardened for real-world enterprise repositories:
1. Resolves IEndpointGroup & RouteGroupBuilder (Jason Taylor CleanArchitecture & Microsoft eShop patterns)
2. FastEndpoints route constants resolution (e.g. Post(CreateRequest.Route))
3. Eliminates gRPC false positives (filters EntityBase, ViewModelBase, TestFixtureBase; requires ServerCallContext / Grpc namespace)
4. Inheritance & Partial class resolution
"""

import os
import sys
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional

INTEL_DIR_NAME = ".codebase-intel"

HTTP_ATTR_REGEX = re.compile(r'\[Http(Get|Post|Put|Delete|Patch|Options|Head)(?:\((?:(?:template:\s*)?["\']([^"\']*)["\'])?[^)]*\))?\]', re.IGNORECASE)
ROUTE_ATTR_REGEX = re.compile(r'\[(?:Route|CustomRoute)\(\s*(?:template:\s*)?["\']([^"\']*)["\']', re.IGNORECASE)
CONTROLLER_CLASS_REGEX = re.compile(r'public\s+(?:[a-z]+\s+)*class\s+(\w+)[^{:]*(?::\s*([^{]+))?', re.IGNORECASE)
FAST_ENDPOINT_CLASS_REGEX = re.compile(r'public\s+class\s+(\w+)[^{:]*:\s*Endpoint<', re.IGNORECASE)
CARTER_MODULE_REGEX = re.compile(r'public\s+class\s+(\w+)[^{:]*:\s*ICarterModule', re.IGNORECASE)
RAZOR_PAGEMODEL_REGEX = re.compile(r'public\s+(?:partial\s+)?class\s+(\w+)[^{:]*:\s*PageModel', re.IGNORECASE)
CONSUMER_REGEX = re.compile(r'public\s+class\s+(\w+)[^{:]*:\s*[^{:]*(?:IConsumer<([^>]+)>|INotificationHandler<([^>]+)>|IHandleMessages<([^>]+)>)', re.IGNORECASE)

# gRPC filter list
NON_GRPC_BASES = {
    "entitybase", "viewmodelbase", "animationbase", "basetestfixture",
    "testbase", "controllerbase", "pagemodelbase", "seedwork", "domainobject",
    "baseentity", "aggregatebase", "valueobjectbase"
}

def parse_class_symbols(root: Path) -> Dict[str, Dict[str, Any]]:
    symbol_table = {}
    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git"]):
            continue
        try:
            content = cs_file.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue

        rel = str(cs_file.relative_to(root))
        for m in CONTROLLER_CLASS_REGEX.finditer(content):
            cname = m.group(1)
            raw_base = m.group(2) or ""
            base_decl = raw_base.split("where")[0].strip()
            base_name = base_decl.split("<")[0].split(",")[0].strip()

            if not (cname.endswith("Controller") or "Controller" in base_name or "[ApiController]" in content):
                continue

            if cname not in symbol_table:
                symbol_table[cname] = {
                    "base_class": base_name,
                    "files": [rel],
                    "raw_content": [content]
                }
            else:
                symbol_table[cname]["files"].append(rel)
                symbol_table[cname]["raw_content"].append(content)
    return symbol_table

def scan_controller_actions(content: str, controller_name: str, rel_path: str, base_route_override: str = "") -> List[Dict[str, Any]]:
    actions = []
    lines = content.splitlines()

    base_route = base_route_override
    if not base_route:
        route_match = ROUTE_ATTR_REGEX.search(content)
        if route_match:
            base_route = route_match.group(1).replace("[controller]", controller_name.replace("Controller", ""))

    for i, line in enumerate(lines):
        http_match = HTTP_ATTR_REGEX.search(line)
        if http_match:
            verb = http_match.group(1).upper()
            sub_route = http_match.group(2) or ""
            method_name = "Action"
            for j in range(i + 1, min(i + 12, len(lines))):
                method_decl = re.search(r'public\s+(?:async\s+)?(?:Task<[A-Za-z0-9_<>,\s]+>|Task|IActionResult|ActionResult<[A-Za-z0-9_<>,\s]+>|[A-Za-z0-9_<>]+)\s+(\w+)\s*\(', lines[j])
                if method_decl:
                    method_name = method_decl.group(1)
                    break
            
            curr_route = base_route.replace("[action]", method_name) if base_route else ""
            if sub_route:
                full_route = f"{curr_route}/{sub_route}".strip("/").replace("//", "/")
            else:
                full_route = curr_route.strip("/")

            actions.append({
                "category": "Controller API",
                "trigger": verb,
                "pattern": f"/{full_route}",
                "handler": f"{controller_name}.{method_name}",
                "file": rel_path,
                "line": i + 1
            })
    return actions

def scan_minimal_api_groups(content: str, cs_file: Path, rel_path: str) -> List[Dict[str, Any]]:
    """Scans RouteGroupBuilder, IEndpointGroup, and app.MapGroup patterns."""
    entries = []
    lines = content.splitlines()
    stem = cs_file.stem

    # Detect base route prefix
    base_group_route = ""
    group_match = re.search(r'MapGroup\s*\(\s*["\']([^"\']+)["\']', content)
    if group_match:
        base_group_route = group_match.group(1).strip("/")
    elif "IEndpointGroup" in content or "Endpoints" in cs_file.parts:
        base_group_route = f"api/{stem}"

    # Scan for MapGet, MapPost, MapPut, MapDelete, MapPatch
    # Handles:
    # 1. api.MapGet("/items", GetAllItems)
    # 2. groupBuilder.MapPost(CreateTodoItem)
    # 3. groupBuilder.MapPut(UpdateTodoItem, "{id}")
    map_call_regex = re.compile(r'(?:\w+)\.Map(Get|Post|Put|Delete|Patch)\s*\(\s*([^)]+)\)', re.IGNORECASE)

    for i, line in enumerate(lines):
        for m in map_call_regex.finditer(line):
            verb = m.group(1).upper()
            args_str = m.group(2).strip()
            args = [a.strip() for a in args_str.split(",")]

            sub_route = ""
            handler_name = f"Endpoint ({stem})"

            if len(args) == 1:
                arg0 = args[0]
                if (arg0.startswith('"') or arg0.startswith("'")) and (arg0.endswith('"') or arg0.endswith("'")):
                    sub_route = arg0.strip('"\'')
                else:
                    # Delegate argument: MapPost(CreateTodoItem)
                    handler_name = f"{stem}.{arg0}"
            elif len(args) >= 2:
                arg0, arg1 = args[0], args[1]
                if (arg0.startswith('"') or arg0.startswith("'")):
                    sub_route = arg0.strip('"\'')
                    handler_name = f"{stem}.{arg1}"
                else:
                    # Delegate first, route second: MapPut(UpdateTodoItem, "{id}")
                    handler_name = f"{stem}.{arg0}"
                    sub_route = arg1.strip('"\'')

            full_route = f"{base_group_route}/{sub_route}".strip("/").replace("//", "/")
            entries.append({
                "category": "Minimal API",
                "trigger": verb,
                "pattern": f"/{full_route}",
                "handler": handler_name,
                "file": rel_path,
                "line": i + 1
            })

    return entries

def scan_fastendpoint(content: str, cs_file: Path, rel_path: str) -> Optional[Dict[str, Any]]:
    fe_match = FAST_ENDPOINT_CLASS_REGEX.search(content)
    if not fe_match:
        return None

    ep_name = fe_match.group(1)
    
    # Verb
    verb = "POST"
    verb_m = re.search(r'\b(Post|Get|Put|Delete|Patch)\s*\(', content)
    if verb_m:
        verb = verb_m.group(1).upper()

    # Route
    route_val = ""
    # Try literal string: Post("/api/users")
    route_str_m = re.search(r'\b(?:Post|Get|Put|Delete|Patch)\s*\(\s*["\']([^"\']+)["\']', content)
    if route_str_m:
        route_val = route_str_m.group(1)
    else:
        # Try constant Route: public const string Route = "/..."
        const_route_m = re.search(r'public\s+const\s+string\s+Route\s*=\s*["\']([^"\']+)["\']', content)
        if const_route_m:
            route_val = const_route_m.group(1)
        else:
            # Fallback to parent directory as resource name
            parent_dir = cs_file.parent.name
            route_val = f"/{parent_dir}/{ep_name}" if parent_dir != "Endpoints" else f"/{ep_name}"

    return {
        "category": "FastEndpoint",
        "trigger": verb,
        "pattern": route_val,
        "handler": ep_name,
        "file": rel_path,
        "line": 1
    }

def scan_grpc_service(content: str, cs_file: Path, rel_path: str) -> Optional[Dict[str, Any]]:
    # Strict gRPC validation
    is_test = any(t in cs_file.parts for t in ["test", "tests", "Test", "Tests", "FunctionalTests", "UnitTests"])
    if is_test:
        return None

    grpc_decl = re.search(r'public\s+class\s+(\w+)[^{:]*:\s*([A-Za-z0-9_.]+(?:Base|Impl))', content)
    if not grpc_decl:
        return None

    svc_name = grpc_decl.group(1)
    base_name = grpc_decl.group(2).split(".")[-1].strip()

    if base_name.lower() in NON_GRPC_BASES or svc_name.endswith("Tests") or svc_name.endswith("Fixture"):
        return None

    # Must have gRPC markers (ServerCallContext or Grpc.Core or Proto)
    has_grpc_marker = ("ServerCallContext" in content or "using Grpc" in content or "Grpc." in content or "Proto" in cs_file.parts)
    if not has_grpc_marker:
        return None

    return {
        "category": "gRPC Service",
        "trigger": "RPC",
        "pattern": f"gRPC: {base_name.replace('Base', '')}",
        "handler": svc_name,
        "file": rel_path,
        "line": 1
    }

def detect_entry_module(file_path: str) -> str:
    """Detects module or bounded context from file path."""
    parts = Path(file_path).parts
    for idx, p in enumerate(parts):
        if p.lower() in ["modules", "features", "areas", "components"]:
            if idx + 1 < len(parts):
                mod = parts[idx + 1]
                return mod.split(".")[-1]
        if ".module." in p.lower():
            return p.split(".module.")[-1].split(".")[0]
    return ""

def get_git_head(root: Path) -> str:
    """Reads Git HEAD state to detect branch switches and commit changes."""
    git_head_file = root / ".git" / "HEAD"
    if not git_head_file.exists():
        return ""
    try:
        content = git_head_file.read_text(encoding="utf-8", errors="ignore").strip()
        if content.startswith("ref:"):
            ref_path = root / ".git" / content[4:].strip()
            if ref_path.exists():
                return f"{content}:{ref_path.read_text(encoding='utf-8', errors='ignore').strip()}"
        return content
    except Exception:
        return ""

def filter_routes(entries: List[Dict[str, Any]], search: str = "", method: str = "") -> List[Dict[str, Any]]:
    """Filters routes by search query and/or HTTP method."""
    filtered = []
    s_low = search.lower().strip()
    m_low = method.upper().strip()
    for e in entries:
        if m_low and e.get("trigger", "").upper() != m_low:
            continue
        if s_low:
            text_blob = f"{e.get('pattern', '')} {e.get('handler', '')} {e.get('category', '')} {e.get('file', '')}".lower()
            if s_low not in text_blob:
                continue
        filtered.append(e)
    return filtered

def catalog_entrypoints(target_root: str = ".", force: bool = False) -> List[Dict[str, Any]]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    entry_dir = intel_dir / "entrypoints"
    entry_dir.mkdir(parents=True, exist_ok=True)
    json_output = entry_dir / "catalog.json"
    md_output = entry_dir / "catalog.md"

    # Incremental Hash-based Cache
    cache_dir = intel_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = cache_dir / "catalog_manifest.json"

    cs_files = [f for f in root.rglob("*.cs") if not any(x in f.parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git", "TestResults"])]
    current_manifest = {str(f.relative_to(root)): f.stat().st_mtime_ns for f in cs_files}
    current_manifest["__git_head__"] = get_git_head(root)

    if not force and json_output.exists() and manifest_file.exists():
        try:
            saved_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
            if saved_manifest == current_manifest:
                cached_data = json.loads(json_output.read_text(encoding="utf-8"))
                return cached_data
        except Exception:
            pass

    symbol_table = parse_class_symbols(root)
    all_entries = []

    # Map of base controller actions
    base_controller_actions = {}
    base_controller_routes = {}
    for cname, cinfo in symbol_table.items():
        if "Base" in cname or "Crud" in cname:
            for idx, content in enumerate(cinfo["raw_content"]):
                route_m = ROUTE_ATTR_REGEX.search(content)
                if route_m:
                    base_controller_routes[cname] = route_m.group(1)
                actions = scan_controller_actions(content, cname, cinfo["files"][idx])
                if actions:
                    base_controller_actions[cname] = actions

    # Process all controllers with partial and inheritance resolution
    for cname, cinfo in symbol_table.items():
        if "Base" in cname or "Crud" in cname:
            continue
        
        base_name = cinfo.get("base_class", "")
        derived_base_route = ""
        for content in cinfo["raw_content"]:
            route_m = ROUTE_ATTR_REGEX.search(content)
            if route_m:
                derived_base_route = route_m.group(1).replace("[controller]", cname.replace("Controller", "")).strip("/")
                break

        if not derived_base_route and base_name in base_controller_routes:
            derived_base_route = base_controller_routes[base_name].replace("[controller]", cname.replace("Controller", "")).strip("/")

        controller_actions = []
        for idx, content in enumerate(cinfo["raw_content"]):
            actions = scan_controller_actions(content, cname, cinfo["files"][idx], base_route_override=derived_base_route)
            controller_actions.extend(actions)

        if base_name in base_controller_actions:
            existing_action_names = {a["handler"].split(".")[-1].split(" ")[0] for a in controller_actions}
            for base_act in base_controller_actions[base_name]:
                base_act_name = base_act["handler"].split(".")[-1]
                if base_act_name not in existing_action_names:
                    inherited_act = dict(base_act)
                    inherited_act["handler"] = f"{cname}.{base_act_name} (Inherited from {base_name})"
                    inherited_act["file"] = cinfo["files"][0]
                    if derived_base_route:
                        sub_route = base_act["pattern"].lstrip("/").replace("Base", "")
                        if "{" in sub_route:
                            sub_param = sub_route[sub_route.find("{"):]
                            inherited_act["pattern"] = f"/{derived_base_route}/{sub_param}".replace("//", "/")
                        else:
                            inherited_act["pattern"] = f"/{derived_base_route}"
                    controller_actions.append(inherited_act)

        all_entries.extend(controller_actions)

    # Process files for FastEndpoints, Minimal APIs, Razor, gRPC, Consumers
    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git", "TestResults"]):
            continue
        try:
            content = cs_file.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue

        rel = str(cs_file.relative_to(root))

        # FastEndpoints
        fe_entry = scan_fastendpoint(content, cs_file, rel)
        if fe_entry:
            all_entries.append(fe_entry)
            continue

        # Minimal APIs / Endpoint Groups
        if any(k in cs_file.stem for k in ["Api", "Apis", "Endpoint", "Endpoints", "Program", "Startup"]) or "IEndpointGroup" in content or "MapGroup" in content:
            min_entries = scan_minimal_api_groups(content, cs_file, rel)
            all_entries.extend(min_entries)

        # Carter
        if CARTER_MODULE_REGEX.search(content):
            c_entries = scan_minimal_api_groups(content, cs_file, rel)
            for ce in c_entries:
                ce["category"] = "Carter Module"
            all_entries.extend(c_entries)

        # Razor
        razor_m = RAZOR_PAGEMODEL_REGEX.search(content)
        if razor_m:
            page_name = razor_m.group(1)
            for i, line in enumerate(content.splitlines()):
                h_match = re.search(r'public\s+(?:async\s+)?(?:Task<[A-Za-z0-9_<>,\s]+>|Task|IActionResult|[A-Za-z0-9_<>]+)\s+(On(Get|Post)\w*)\s*\(', line)
                if h_match:
                    all_entries.append({
                        "category": "Razor Page",
                        "trigger": h_match.group(2).upper(),
                        "pattern": f"/{page_name.replace('Model', '')}",
                        "handler": f"{page_name}.{h_match.group(1)}",
                        "file": rel,
                        "line": i + 1
                    })

        # gRPC
        grpc_entry = scan_grpc_service(content, cs_file, rel)
        if grpc_entry:
            all_entries.append(grpc_entry)

        # Consumers
        for cm in CONSUMER_REGEX.finditer(content):
            c_name = cm.group(1)
            ev_type = cm.group(2) or cm.group(3) or cm.group(4)
            all_entries.append({
                "category": "Message Consumer",
                "trigger": "EVENT",
                "pattern": f"Event: {ev_type}",
                "handler": c_name,
                "file": rel,
                "line": 1
            })

    # Deduplicate entries by (category, trigger, pattern, handler)
    seen = set()
    deduped = []
    for e in all_entries:
        key = (e["category"], e["trigger"], e["pattern"], e["handler"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)

    deduped.sort(key=lambda x: (x["category"], x["pattern"]))

    # Update incremental cache manifest
    json_output.write_text(json.dumps(deduped, indent=2), encoding="utf-8")
    try:
        manifest_file.write_text(json.dumps(current_manifest, indent=2), encoding="utf-8")
    except Exception:
        pass

    # Partition by module/bounded context
    module_groups: Dict[str, List[Dict[str, Any]]] = {}
    for e in deduped:
        mod = detect_entry_module(e["file"])
        e["module"] = mod
        if mod:
            module_groups.setdefault(mod, []).append(e)

    modules_dir = entry_dir / "modules"
    if module_groups:
        modules_dir.mkdir(parents=True, exist_ok=True)
        for mname, m_entries in sorted(module_groups.items()):
            mod_md = [
                f"# Modular Entrypoints: {mname}",
                f"*Discovered: {len(m_entries)} entry points*",
                "",
                "| Category | Verb / Trigger | Route / Pattern | Handler / Class | Source File |",
                "| :--- | :--- | :--- | :--- | :--- |"
            ]
            for me in m_entries:
                mod_md.append(f"| `{me['category']}` | **{me['trigger']}** | `{me['pattern']}` | `{me['handler']}` | [{me['file']}#L{me['line']}](../{me['file']}) |")
            (modules_dir / f"{mname}.md").write_text("\n".join(mod_md), encoding="utf-8")

    md_lines = [
        "# Universal Entrypoint Catalog",
        f"*Discovered: {len(deduped)} entry points (Enterprise Grade)*",
        ""
    ]

    if module_groups:
        md_lines.extend([
            "## Modular Subsystems",
            "| Module | Routes | Specialized Catalog |",
            "| :--- | :---: | :--- |"
        ])
        for mname, m_entries in sorted(module_groups.items()):
            md_lines.append(f"| `{mname}` | {len(m_entries)} routes | [modules/{mname}.md](modules/{mname}.md) |")
        md_lines.append("")

    md_lines.extend([
        "## Master Entrypoint Catalog",
        "| Category | Verb / Trigger | Route / Pattern | Handler / Class | Source File |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])
    for e in deduped:
        md_lines.append(f"| `{e['category']}` | **{e['trigger']}** | `{e['pattern']}` | `{e['handler']}` | [{e['file']}#L{e['line']}]({e['file']}) |")

    md_output.write_text("\n".join(md_lines), encoding="utf-8")
    return deduped

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ottonet Skill Universal Entrypoint Cataloger")
    parser.add_argument("root", nargs="?", default=".", help="Root directory")
    parser.add_argument("--search", "-s", help="Filter routes by keyword")
    parser.add_argument("--method", "-m", help="Filter routes by HTTP method")
    parser.add_argument("--force", action="store_true", help="Bypass incremental cache")
    args = parser.parse_args()

    entries = catalog_entrypoints(args.root, force=args.force)
    if args.search or args.method:
        matches = filter_routes(entries, search=args.search or "", method=args.method or "")
        print(f"[OK] Found {len(matches)} matching entry points:")
        print("| Category | Verb | Route / Pattern | Handler / Class | Source File |")
        print("| :--- | :--- | :--- | :--- | :--- |")
        for m in matches:
            print(f"| `{m['category']}` | **{m['trigger']}** | `{m['pattern']}` | `{m['handler']}` | [{m['file']}#L{m['line']}]({m['file']}) |")
    else:
        print(f"[OK] Ottonet Skill cataloged {len(entries)} entry points.")
        print(f"[OK] Output: .codebase-intel/entrypoints/catalog.md")
