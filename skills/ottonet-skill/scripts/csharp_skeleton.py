#!/usr/bin/env python3
"""
csharp_skeleton.py - Advanced C# Skeleton & Targeted Method Zoom-In for Ottonet Skill.
Hardened against:
1. Multiline method declarations where parameters span multiple lines
2. UTF-8 with BOM (utf-8-sig) & Windows-1252 encodings
3. Targeted Method Zoom-In (--focus-method <name>): Keeps 100% full body for target method!
4. Semantic Logic Distiller (--distill): Retains formulas and state mutations
"""

import os
import sys
import re
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import Optional

INTEL_DIR_NAME = ".codebase-intel"

BOILERPLATE_PATTERNS = [
    r'^\s*_logger\.',
    r'^\s*logger\.',
    r'^\s*try\s*\{',
    r'^\s*\}\s*catch\b',
    r'^\s*if\s*\([^)]*==\s*null\)\s*throw\s+new\s+ArgumentNull',
    r'^\s*throw\s+new\s+ArgumentNullException',
    r'^\s*using\s*\(',
]

CORE_LOGIC_INDICATORS = [
    r'=', r'\+=', r'-=', r'\*=', r'/=',
    r'\bawait\b', r'\bStatus\b', r'\bState\b',
    r'\bthrow\b', r'\breturn\b'
]

def is_boilerplate(line: str) -> bool:
    for pat in BOILERPLATE_PATTERNS:
        if re.search(pat, line):
            return True
    return False

def is_core_logic(line: str) -> bool:
    for ind in CORE_LOGIC_INDICATORS:
        if re.search(ind, line):
            return True
    return False

def count_code_braces(line: str, state: dict):
    """Lexer that counts { and } strictly in executable code, ignoring strings, chars, and comments."""
    i = 0
    n = len(line)
    open_count = 0
    close_count = 0

    while i < n:
        c = line[i]
        nxt = line[i+1] if i + 1 < n else ''

        if state.get('in_block_comment'):
            if c == '*' and nxt == '/':
                state['in_block_comment'] = False
                i += 2
                continue
            i += 1
            continue

        if state.get('in_verbatim_string'):
            if c == '"':
                if nxt == '"':
                    i += 2
                    continue
                else:
                    state['in_verbatim_string'] = False
                    i += 1
                    continue
            i += 1
            continue

        if state.get('in_string'):
            if c == '\\':
                i += 2
                continue
            if c == '"':
                state['in_string'] = False
                i += 1
                continue
            i += 1
            continue

        if c == '/' and nxt == '/':
            break

        if c == '/' and nxt == '*':
            state['in_block_comment'] = True
            i += 2
            continue

        if (c == '@' and nxt == '"') or (c == '$' and nxt == '@' and i + 2 < n and line[i+2] == '"') or (c == '@' and nxt == '$' and i + 2 < n and line[i+2] == '"'):
            state['in_verbatim_string'] = True
            i += 2 if (c == '@' and nxt == '"') else 3
            continue

        if c == '"':
            state['in_string'] = True
            i += 1
            continue

        if c == "'":
            i += 1
            while i < n and line[i] != "'":
                if line[i] == '\\' and i + 1 < n:
                    i += 2
                else:
                    i += 1
            i += 1
            continue

        if c == '{':
            open_count += 1
        elif c == '}':
            close_count += 1

        i += 1

    return open_count, close_count

def generate_csharp_skeleton(csharp_code: str, focus_method: Optional[str] = None, distill: bool = False, full: bool = False) -> str:
    if full:
        return csharp_code

    lines = csharp_code.splitlines()
    output_lines = [
        "// [OTTONET INTEL NOTICE] Methods outside the focus method are skeletonized for token efficiency.",
        "// If your investigation involves side-effects across non-focus methods, run with --full to see the unabridged source."
    ]
    
    in_method_body = False
    in_method_decl = False
    pending_method_name = ""
    is_focused_method = False
    brace_depth = 0
    method_brace_depth = 0
    distilled_buffer = []

    lexer_state = {}
    omitted_lines_count = 0
    omitted_calls = []
    omitted_mutations = []
    omitted_throws = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("//") and not in_method_body:
            continue

        open_count, close_count = count_code_braces(line, lexer_state)

        if in_method_body:
            brace_depth += open_count - close_count
            
            if is_focused_method:
                output_lines.append(line)
            else:
                omitted_lines_count += 1
                if distill:
                    if is_core_logic(stripped) and not is_boilerplate(stripped):
                        distilled_buffer.append(line)
                # Track side-effects in non-focused methods
                call_m = re.search(r'\bawait\s+([A-Za-z0-9_.]+\([^)]*\))', stripped)
                if call_m and len(omitted_calls) < 2:
                    omitted_calls.append(call_m.group(1).split("(")[0] + "()")
                mut_m = re.search(r'\b([A-Za-z0-9_]+\.(?:Status|State|Stage))\s*=', stripped)
                if mut_m and len(omitted_mutations) < 2:
                    omitted_mutations.append(mut_m.group(1))
                throw_m = re.search(r'\bthrow\s+new\s+(\w+Exception)', stripped)
                if throw_m and len(omitted_throws) < 2:
                    omitted_throws.append(throw_m.group(1))

            if brace_depth <= method_brace_depth:
                in_method_body = False
                if not is_focused_method:
                    indent = line[:len(line) - len(line.lstrip())]
                    if distill and distilled_buffer:
                        output_lines.append(f"{indent}    // --- [Ottonet Distilled Core Logic] ---")
                        output_lines.extend(distilled_buffer[:8])
                        output_lines.append(f"{indent}    // ... [boilerplate/logging omitted] ...")
                    else:
                        se_items = []
                        if omitted_mutations:
                            se_items.append(f"Mutates: {', '.join(set(omitted_mutations))}")
                        if omitted_calls:
                            se_items.append(f"Calls: {', '.join(set(omitted_calls))}")
                        if omitted_throws:
                            se_items.append(f"Throws: {', '.join(set(omitted_throws))}")
                        se_desc = f" | {'; '.join(se_items)}" if se_items else ""
                        output_lines.append(f"{indent}    // ... [implementation omitted ({omitted_lines_count} lines){se_desc}] ...")
                    output_lines.append(f"{indent}}}")
                is_focused_method = False
                distilled_buffer = []
                omitted_lines_count = 0
                omitted_calls = []
                omitted_mutations = []
                omitted_throws = []
            continue

        # If we are in a multiline method signature looking for '{'
        if in_method_decl:
            output_lines.append(line)
            if "{" in line:
                in_method_decl = False
                in_method_body = True
                is_focused_method = bool(focus_method and pending_method_name.lower() == focus_method.lower())
                method_brace_depth = brace_depth
                brace_depth += open_count - close_count
                distilled_buffer = []
                omitted_lines_count = 0
                omitted_calls = []
                omitted_mutations = []
                omitted_throws = []
                if is_focused_method:
                    output_lines.append(f"    // >>> [OTTONET ZOOM-IN: FULL FIDELITY BODY OF {pending_method_name}] <<<")
                if brace_depth <= method_brace_depth:
                    in_method_body = False
                    if not is_focused_method:
                        output_lines.append("    // ... [implementation omitted by Ottonet Skill] ...\n}")
                    is_focused_method = False
            continue

        # Detect method declaration start (single line or multiline)
        is_type_decl = bool(re.search(r'\b(class|record|struct|interface|enum)\b', stripped))
        is_mod = any(stripped.startswith(mod) for mod in ["public", "private", "protected", "internal", "async", "override", "virtual"])
        if is_mod and not is_type_decl and "(" in stripped and not any(stripped.startswith(k) for k in ["if", "for", "while", "catch", "switch", "using"]):
            if not stripped.endswith(";"):
                match_name = re.search(r'\b([A-Za-z0-9_]+)\s*\(', stripped)
                method_name = match_name.group(1) if match_name else ""

                if "{" in line:
                    decl_part = line[:line.find("{")].rstrip()
                    output_lines.append(f"{decl_part} {{")
                    in_method_body = True
                    is_focused_method = bool(focus_method and method_name.lower() == focus_method.lower())
                    method_brace_depth = brace_depth
                    brace_depth += open_count - close_count
                    distilled_buffer = []

                    if is_focused_method:
                        output_lines.append(f"    // >>> [OTTONET ZOOM-IN: FULL FIDELITY BODY OF {method_name}] <<<")

                    if brace_depth <= method_brace_depth:
                        in_method_body = False
                        if not is_focused_method:
                            output_lines.append("    // ... [implementation omitted by Ottonet Skill] ...\n}")
                        is_focused_method = False
                    continue
                else:
                    # Multiline method signature starts here
                    output_lines.append(line)
                    in_method_decl = True
                    pending_method_name = method_name
                    continue

        brace_depth += open_count - close_count
        output_lines.append(line)

    return "\n".join(output_lines)

def try_roslyn_skeleton(file_path: Path, focus_method: Optional[str] = None, full: bool = False) -> Optional[str]:
    """Attempts to use native .NET Roslyn compiler AST tool if dotnet is present."""
    if not shutil.which("dotnet"):
        return None

    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    dll_path = repo_root / "tools" / "Ottonet.Roslyn" / "bin" / "Release" / "net8.0" / "Ottonet.Roslyn.dll"
    if not dll_path.exists():
        return None

    cmd = ["dotnet", "exec", str(dll_path), str(file_path)]
    if focus_method:
        cmd.extend(["--focus-method", focus_method])
    if full:
        cmd.append("--full")

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout
    except Exception:
        pass
    return None

def get_skeleton(file_path: Path, target_root: Path, focus_method: Optional[str] = None, distill: bool = False, full: bool = False, prefer_roslyn: bool = True) -> str:
    if prefer_roslyn and not distill:
        roslyn_res = try_roslyn_skeleton(file_path, focus_method=focus_method, full=full)
        if roslyn_res:
            return roslyn_res

    try:
        code = file_path.read_text(encoding="utf-8-sig", errors="ignore")
    except Exception:
        code = file_path.read_text(encoding="latin-1", errors="ignore")
    return generate_csharp_skeleton(code, focus_method=focus_method, distill=distill, full=full)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ottonet Skill Advanced C# Skeleton Generator")
    parser.add_argument("file", help="Path to C# file")
    parser.add_argument("--focus-method", help="Method name to Zoom-In with 100%% full body fidelity")
    parser.add_argument("--distill", action="store_true", help="Enable Semantic Logic Distiller")
    parser.add_argument("--full", action="store_true", help="Show full unabridged source code with zero omissions")
    parser.add_argument("--no-roslyn", action="store_true", help="Force use of Python fallback lexer")
    parser.add_argument("--root", default=".", help="Root directory")

    args = parser.parse_args()
    target_file = Path(args.file).resolve()
    if not target_file.exists():
        print(f"Error: File {target_file} not found.", file=sys.stderr)
        sys.exit(1)

    res = get_skeleton(
        target_file,
        Path(args.root).resolve(),
        focus_method=args.focus_method,
        distill=args.distill,
        full=args.full,
        prefer_roslyn=not args.no_roslyn
    )
    print(res)
