#!/usr/bin/env python3
"""
trace_di_decorators.py - Runtime Wiring & Decorator Tracer for Ottonet Skill.
Detects:
1. Scrutor Decorators (services.Decorate<IInterface, DecoratorClass>())
2. Dynamic Assembly Scanning (services.Scan(...))
3. Direct Service Lifetimes (AddScoped, AddSingleton, AddTransient)
4. Key Middleware Pipeline Order (Authentication, Authorization, RateLimiting)

Outputs:
- .codebase-intel/architecture/runtime-wiring.json
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Any

INTEL_DIR_NAME = ".codebase-intel"

SCRUTOR_DECORATE_REGEX = re.compile(r'services\.Decorate\s*<\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*>', re.IGNORECASE)
ASSEMBLY_SCAN_REGEX = re.compile(r'services\.Scan\s*\(', re.IGNORECASE)
DI_REGISTRATION_REGEX = re.compile(r'services\.Add(Scoped|Singleton|Transient)\s*<\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*>', re.IGNORECASE)
MIDDLEWARE_REGEX = re.compile(r'app\.Use([A-Za-z0-9_]+)\s*\(', re.IGNORECASE)

def trace_di_wiring(target_root: str = ".") -> Dict[str, Any]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    arch_dir = intel_dir / "architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    output_file = arch_dir / "runtime-wiring.json"

    decorators = []
    has_assembly_scan = False
    di_registrations = {}
    middleware_pipeline = []

    # Target composition root files
    candidate_files = []
    for cs in root.rglob("*.cs"):
        parts = cs.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", ".git"]):
            continue
        stem = cs.stem
        if any(k in stem for k in ["Program", "Startup", "ServiceCollection", "Module", "DependencyInjection", "Installer"]):
            candidate_files.append(cs)

    for cf in candidate_files:
        try:
            content = cf.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        rel = str(cf.relative_to(root))

        # Check Scrutor Decorators
        for dec in SCRUTOR_DECORATE_REGEX.finditer(content):
            decorators.append({
                "interface": dec.group(1),
                "decorator": dec.group(2),
                "source_file": rel,
                "warning": f"CRITICAL: Calls to {dec.group(1)} are wrapped by decorator {dec.group(2)} at runtime!"
            })

        if ASSEMBLY_SCAN_REGEX.search(content):
            has_assembly_scan = True

        # Check explicit DI registrations
        for reg in DI_REGISTRATION_REGEX.finditer(content):
            lifetime = reg.group(1)
            interface_name = reg.group(2)
            impl_name = reg.group(3)
            di_registrations[interface_name] = {
                "lifetime": lifetime,
                "implementation": impl_name,
                "file": rel
            }

        # Check Middlewares (in Program/Startup)
        if "Program" in cf.stem or "Startup" in cf.stem:
            for mw in MIDDLEWARE_REGEX.finditer(content):
                mw_name = mw.group(1)
                if mw_name not in ["Routing", "Endpoints"] and mw_name not in middleware_pipeline:
                    middleware_pipeline.append(mw_name)

    result = {
        "decorators": decorators,
        "has_assembly_scanning": has_assembly_scan,
        "registered_services_sample": dict(list(di_registrations.items())[:30]),
        "middleware_pipeline": middleware_pipeline,
        "architectural_alert": "Scrutor decorators active! Inspect decorator classes before modifying service implementations." if decorators else "No decorators detected."
    }

    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    wiring = trace_di_wiring(target)
    print("================ OTTONET SKILL: RUNTIME DI & DECORATORS ================")
    print(f"Decorators Detected:   {len(wiring['decorators'])}")
    for d in wiring['decorators']:
        print(f"  * {d['interface']} -> Decorated by {d['decorator']}")
    print(f"Assembly Scanning:     {wiring['has_assembly_scanning']}")
    print(f"Sample DI Map Size:    {len(wiring['registered_services_sample'])} services mapped")
    print(f"Middleware Pipeline:   {' -> '.join(wiring['middleware_pipeline']) or 'Standard'}")
    print("=======================================================================")
