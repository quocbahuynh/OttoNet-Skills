#!/usr/bin/env python3
"""
detect_conventions.py - Team Coding Style Learner for Ottonet Skill.
Detects:
1. Error handling idiom: Result Pattern (Result<T>, ErrorOr, OneOf) vs Exceptions
2. Namespace style: File-scoped (namespace Foo;) vs Block-scoped (namespace Foo {)
3. Constructor style: C# 12 Primary Constructors vs Classic Constructor Injection
4. Object Mapping: AutoMapper vs Mapster vs Manual Mappers

Outputs:
- .codebase-intel/conventions/team-style.json
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, Any

INTEL_DIR_NAME = ".codebase-intel"

FILE_SCOPED_NS_REGEX = re.compile(r'^\s*namespace\s+[A-Za-z0-9_.]+\s*;', re.MULTILINE)
BLOCK_SCOPED_NS_REGEX = re.compile(r'^\s*namespace\s+[A-Za-z0-9_.]+\s*\{', re.MULTILINE)
PRIMARY_CTOR_REGEX = re.compile(r'public\s+class\s+\w+\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{', re.MULTILINE)
RESULT_PATTERN_REGEX = re.compile(r'\b(?:Result<|ErrorOr<|OneOf<|IResult<)', re.IGNORECASE)
MAPPER_REGEX = re.compile(r'\b(?:IMapper|CreateMap|Mapster|\.Adapt<)', re.IGNORECASE)

def detect_conventions(target_root: str = ".") -> Dict[str, Any]:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    conv_dir = intel_dir / "conventions"
    conv_dir.mkdir(parents=True, exist_ok=True)
    output_file = conv_dir / "team-style.json"

    file_scoped_count = 0
    block_scoped_count = 0
    primary_ctor_count = 0
    result_pattern_count = 0
    automapper_count = 0
    mapster_count = 0

    scanned_files = 0
    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git"]):
            continue
        try:
            content = cs_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        scanned_files += 1
        if FILE_SCOPED_NS_REGEX.search(content):
            file_scoped_count += 1
        if BLOCK_SCOPED_NS_REGEX.search(content):
            block_scoped_count += 1
        if PRIMARY_CTOR_REGEX.search(content):
            primary_ctor_count += 1
        if RESULT_PATTERN_REGEX.search(content):
            result_pattern_count += 1
        if "IMapper" in content or "CreateMap" in content:
            automapper_count += 1
        if "Mapster" in content or ".Adapt<" in content:
            mapster_count += 1

    # Determine preferences
    ns_style = "File-scoped (namespace Foo;)" if file_scoped_count >= block_scoped_count else "Block-scoped (namespace Foo { })"
    error_handling = "Result Pattern (Result<T> / ErrorOr - Avoid throwing exceptions)" if result_pattern_count > 3 else "Standard Exceptions / ValidationException"
    ctor_style = "Prefer C# 12 Primary Constructors" if primary_ctor_count > 5 else "Classic Constructor Injection"
    
    mapping_tool = "Manual / Extension Methods"
    if mapster_count > automapper_count and mapster_count > 0:
        mapping_tool = "Mapster (.Adapt<T>())"
    elif automapper_count > 0:
        mapping_tool = "AutoMapper (IMapper)"

    conventions = {
        "namespace_style": ns_style,
        "error_handling_idiom": error_handling,
        "constructor_preference": ctor_style,
        "object_mapping_tool": mapping_tool,
        "rules_of_engagement": [
            f"Always use {ns_style} when creating new C# files.",
            f"Follow {error_handling} when handling business failures.",
            f"Use {mapping_tool} for mapping DTOs to entities."
        ],
        "metrics": {
            "scanned_files": scanned_files,
            "file_scoped_namespaces": file_scoped_count,
            "block_scoped_namespaces": block_scoped_count,
            "result_pattern_occurrences": result_pattern_count
        }
    }

    output_file.write_text(json.dumps(conventions, indent=2), encoding="utf-8")
    return conventions

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    conv = detect_conventions(target)
    print("================ OTTONET SKILL: TEAM CODING STYLE ================")
    print(f"Namespace Style:   {conv['namespace_style']}")
    print(f"Error Handling:    {conv['error_handling_idiom']}")
    print(f"Constructors:      {conv['constructor_preference']}")
    print(f"Mapping Approach:  {conv['object_mapping_tool']}")
    print("==================================================================")
