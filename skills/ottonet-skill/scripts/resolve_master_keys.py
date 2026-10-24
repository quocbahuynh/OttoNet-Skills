#!/usr/bin/env python3
"""
resolve_master_keys.py - 4 Master Keys Discriminator Router for Ottonet Skill.
Hardened against:
1. XML Namespaces in legacy .csproj (xmlns="http://schemas.microsoft.com/developer/msbuild/2003")
2. UTF-8 with BOM (utf-8-sig) & Windows-1252 encodings
3. Central Package Management (Directory.Packages.props)
4. packages.config & Global.asax in legacy .NET Framework
"""

import os
import sys
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List

INTEL_DIR_NAME = ".codebase-intel"

def get_tag_name(elem: ET.Element) -> str:
    """Namespace-agnostic tag name extraction."""
    return elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag

def read_file_safely(file_path: Path) -> str:
    """Reads file with BOM stripping and fallback encoding."""
    try:
        return file_path.read_text(encoding="utf-8-sig", errors="ignore")
    except Exception:
        try:
            return file_path.read_text(encoding="latin-1", errors="ignore")
        except Exception:
            return ""

def resolve_bootstrap_key(root: Path) -> str:
    if any(root.rglob("Global.asax*")) or any(root.rglob("packages.config")):
        return "LegacyDotNetFramework"
    if any(root.rglob("Startup.cs")):
        return "ClassicDotNetCore"
    return "ModernDotNet"

def extract_all_package_names(root: Path) -> List[str]:
    packages = set()

    # 1. Check Directory.Packages.props (Central Package Management)
    cpm_file = root / "Directory.Packages.props"
    if cpm_file.exists():
        try:
            tree = ET.parse(cpm_file)
            for elem in tree.getroot().iter():
                if get_tag_name(elem) in ["PackageVersion", "PackageReference"]:
                    inc = elem.get("Include") or elem.get("Update")
                    if inc:
                        packages.add(inc.lower())
        except Exception:
            pass

    # 2. Check packages.config (Legacy .NET Framework)
    for pkg_config in root.rglob("packages.config"):
        if any(x in pkg_config.parts for x in [INTEL_DIR_NAME, "bin", "obj", ".git"]):
            continue
        try:
            tree = ET.parse(pkg_config)
            for elem in tree.getroot().iter():
                if get_tag_name(elem) == "package":
                    pid = elem.get("id")
                    if pid:
                        packages.add(pid.lower())
        except Exception:
            pass

    # 3. Check .csproj files (Namespace-agnostic traversal)
    for csproj in root.rglob("*.csproj"):
        if any(x in csproj.parts for x in [INTEL_DIR_NAME, "bin", "obj", ".git"]):
            continue
        try:
            tree = ET.parse(csproj)
            for elem in tree.getroot().iter():
                tag = get_tag_name(elem)
                if tag in ["PackageReference", "Reference"]:
                    inc = elem.get("Include") or elem.get("Update")
                    if inc:
                        packages.add(inc.split(",")[0].strip().lower())
        except Exception:
            pass

    return list(packages)

def resolve_api_key(packages: List[str], root: Path) -> str:
    if any("fastendpoints" in p for p in packages):
        return "FastEndpoints"
    if any("carter" in p for p in packages):
        return "Carter"
    if any("grpc.aspnetcore" in p for p in packages):
        return "GrpcService"
    if any("microsoft.aspnetcore.mvc.razorpages" in p for p in packages):
        return "RazorPages"
    if any("system.web.mvc" in p for p in packages) or any("system.web.http" in p for p in packages):
        return "LegacyMvc"
    
    # Check if controllers exist
    for cs in root.rglob("*Controller*.cs"):
        if any(x in cs.parts for x in [INTEL_DIR_NAME, "bin", "obj", ".git"]):
            continue
        return "ControllerApi"

    return "MinimalApi"

def resolve_domain_key(root: Path) -> str:
    # Check for Vertical Slice
    for p in root.rglob("Features"):
        if p.is_dir() and not any(x in p.parts for x in [INTEL_DIR_NAME, "bin", "obj", ".git"]):
            return "VerticalSlice"

    # Sample up to 5 entity/model files
    entity_files = []
    for cs in root.rglob("*.cs"):
        parts = cs.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", ".git", "Test", "Tests"]):
            continue
        if any(d in parts for d in ["Entities", "Entity", "Domain", "Models"]):
            entity_files.append(cs)
            if len(entity_files) >= 5:
                break

    has_domain_methods = False
    for ef in entity_files:
        content = read_file_safely(ef)
        methods = re.findall(r'public\s+(?:async\s+)?(?:void|Task|Result|[A-Za-z0-9_<>]+)\s+([A-Z]\w+)\s*\([^)]*\)\s*\{', content)
        meaningful_methods = [m for m in methods if not m.startswith("get_") and not m.startswith("set_") and m != ef.stem]
        if len(meaningful_methods) > 0 and ("throw " in content or "Result." in content):
            has_domain_methods = True
            break

    if has_domain_methods:
        return "RichDomain_DDD"
    return "AnemicDomain_FatService"

def resolve_persistence_key(packages: List[str], root: Path) -> str:
    if any("entityframeworkcore" in p for p in packages):
        return "EFCore"
    if any("entityframework" in p for p in packages):
        return "EF6_Legacy"
    if any("dapper" in p for p in packages):
        return "Dapper_StoredProcedures"
    if any("mongodb.driver" in p for p in packages):
        return "DocumentDb"
    if any("system.data.sqlclient" in p for p in packages) or any("microsoft.data.sqlclient" in p for p in packages):
        return "RawAdoNet"
    return "EFCore"

def resolve_master_keys(target_root: str = ".") -> Dict[str, Any]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    arch_dir = intel_dir / "architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    output_file = arch_dir / "master-keys.json"

    packages = extract_all_package_names(root)
    bootstrap_key = resolve_bootstrap_key(root)
    api_key = resolve_api_key(packages, root)
    domain_key = resolve_domain_key(root)
    persistence_key = resolve_persistence_key(packages, root)

    directives = {
        "bootstrap": bootstrap_key,
        "api": api_key,
        "domain": domain_key,
        "persistence": persistence_key,
        "execution_strategy": {
            "api_scanner_mode": api_key,
            "business_rule_target": "Services/Handlers" if domain_key == "AnemicDomain_FatService" else ("Features" if domain_key == "VerticalSlice" else "AggregateRoots"),
            "persistence_scanner_mode": persistence_key,
            "skip_irrelevant_scanners": True
        }
    }

    output_file.write_text(json.dumps(directives, indent=2), encoding="utf-8")
    return directives

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    keys = resolve_master_keys(target)
    print("================ OTTONET SKILL: 4 MASTER KEYS RESOLVED ================")
    print(f"1. Bootstrap Key:   {keys['bootstrap']}")
    print(f"2. API Key:         {keys['api']}")
    print(f"3. Domain Key:      {keys['domain']}")
    print(f"4. Persistence Key: {keys['persistence']}")
    print("-----------------------------------------------------------------------")
    print(f"Target Strategy:    Scan {keys['execution_strategy']['business_rule_target']} | Mode {keys['execution_strategy']['api_scanner_mode']}")
    print("=======================================================================")
