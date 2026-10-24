#!/usr/bin/env python3
"""
detect_architecture.py - Adaptive Architecture Fingerprinting for Ottonet Skill.
Namespace-agnostic XML parsing for legacy and modern .csproj.
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any

try:
    from resolve_master_keys import resolve_master_keys, get_tag_name, read_file_safely
except ImportError:
    from .resolve_master_keys import resolve_master_keys, get_tag_name, read_file_safely

INTEL_DIR_NAME = ".codebase-intel"

def get_file_mtimes(root: Path, extensions: tuple) -> Dict[str, float]:
    mtimes = {}
    for ext in extensions:
        for p in root.rglob(f"*{ext}"):
            parts = p.parts
            if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git"]):
                continue
            mtimes[str(p.relative_to(root))] = p.stat().st_mtime
    return mtimes

def parse_csproj(file_path: Path) -> Dict[str, Any]:
    info = {
        "name": file_path.stem,
        "path": str(file_path),
        "target_frameworks": [],
        "package_references": [],
        "project_references": []
    }
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for elem in root.iter():
            tag = get_tag_name(elem)
            if tag == "TargetFramework" and elem.text:
                info["target_frameworks"].append(elem.text.strip())
            elif tag == "TargetFrameworks" and elem.text:
                info["target_frameworks"].extend([x.strip() for x in elem.text.split(";") if x.strip()])
            elif tag == "TargetFrameworkVersion" and elem.text:
                info["target_frameworks"].append(f"net{elem.text.replace('v', '').replace('.', '')}")
            elif tag in ["PackageReference", "Reference"]:
                name = elem.get("Include") or elem.get("Update")
                version = elem.get("Version") or ""
                if name:
                    clean_name = name.split(",")[0].strip()
                    info["package_references"].append({"name": clean_name, "version": version})
            elif tag == "ProjectReference":
                include = elem.get("Include")
                if include:
                    proj_name = Path(include).stem
                    info["project_references"].append(proj_name)
    except Exception as e:
        info["parse_error"] = str(e)
    return info

def detect_architecture(target_root: str = ".") -> Dict[str, Any]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    arch_dir = intel_dir / "architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    summary_file = arch_dir / "summary.json"
    graph_file = arch_dir / "project-graph.json"

    # 1. Resolve Master Keys
    master_keys = resolve_master_keys(str(root))

    # Fast hash / timestamp check for cache validity
    current_mtimes = get_file_mtimes(root, (".sln", ".csproj", ".props", ".config"))
    cache_meta_file = arch_dir / ".cache_meta.json"
    
    if summary_file.exists() and graph_file.exists() and cache_meta_file.exists():
        try:
            cached_meta = json.loads(cache_meta_file.read_text(encoding="utf-8"))
            if cached_meta.get("mtimes") == current_mtimes:
                return json.loads(summary_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    csproj_files = []
    for p in root.rglob("*.csproj"):
        if any(x in p.parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git"]):
            continue
        csproj_files.append(p)

    parsed_projects = [parse_csproj(p) for p in csproj_files]

    all_frameworks = set()
    for p in parsed_projects:
        all_frameworks.update(p.get("target_frameworks", []))

    project_graph = {
        p["name"]: {
            "path": str(Path(p["path"]).relative_to(root)),
            "frameworks": p["target_frameworks"],
            "dependencies": p["project_references"]
        } for p in parsed_projects
    }

    summary = {
        "root_directory": str(root),
        "master_keys": master_keys,
        "target_frameworks": sorted(list(all_frameworks)),
        "project_count": len(parsed_projects),
        "projects": [p["name"] for p in parsed_projects]
    }

    summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    graph_file.write_text(json.dumps(project_graph, indent=2), encoding="utf-8")
    cache_meta_file.write_text(json.dumps({"mtimes": current_mtimes}, indent=2), encoding="utf-8")

    return summary

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    result = detect_architecture(target)
    mk = result.get("master_keys", {})
    print("================ OTTONET SKILL: ARCHITECTURE SUMMARY ================")
    print(f"Bootstrap:       {mk.get('bootstrap')}")
    print(f"API Mode:        {mk.get('api')}")
    print(f"Domain Shape:    {mk.get('domain')}")
    print(f"Persistence:     {mk.get('persistence')}")
    print(f"Frameworks:      {', '.join(result.get('target_frameworks', [])) or 'Detected from Master Keys'}")
    print(f"Project Count:   {result.get('project_count')}")
    print("======================================================================")
