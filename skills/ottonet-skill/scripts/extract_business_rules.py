#!/usr/bin/env python3
"""
extract_business_rules.py - Semantic Business Rule & Algorithm Distiller for Ottonet Skill.
Upgraded with:
1. Semantic Logic Distiller: Extracts mathematical formulas, calculations, and cross-service calls
2. Anemic Domain Support: Slices logic inside *Service.cs / *Manager.cs
3. 5 Business Anchors: Validators, Error codes, State Enums, Guard Invariants, Unit Tests
4. Stored Procedures detection

Outputs:
- .codebase-intel/domains/<module>-rules.md
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Any

INTEL_DIR_NAME = ".codebase-intel"

VALIDATOR_CLASS_REGEX = re.compile(r'public\s+(?:(?:abstract|partial)\s+)?class\s+(\w+)[^{:]*:\s*([^{]+)', re.IGNORECASE)
RULE_FOR_REGEX = re.compile(r'RuleFor\s*\(\s*[^)]+\)(?:\s*\.[A-Za-z0-9_]+\s*\([^)]*\))+', re.MULTILINE)
DATA_ANNOTATION_REGEX = re.compile(r'\[(Required|StringLength|Range|RegularExpression|EmailAddress)(?:\(([^)]*)\))?\]\s*(?:public\s+[^\s]+\s+(\w+))?', re.MULTILINE)
ERROR_DEF_REGEX = re.compile(r'public\s+static\s+readonly\s+(?:Error|DomainError)\s+(\w+)\s*=\s*new(?:\s*(?:Error|DomainError))?\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']', re.IGNORECASE)
EXCEPTION_CLASS_REGEX = re.compile(r'public\s+(?:sealed\s+)?class\s+(\w+Exception)\s*:\s*([A-Za-z0-9_]+)', re.IGNORECASE)
ERROR_FACTORY_REGEX = re.compile(r'public\s+static\s+(?:Error|Result)\s+(\w+)\s*\([^)]*\)', re.IGNORECASE)
ENUM_REGEX = re.compile(r'public\s+enum\s+(\w+(?:Status|State|Stage|Type|Kind|Category))\s*\{([^}]+)\}', re.IGNORECASE)
GUARD_THROW_REGEX = re.compile(r'if\s*\(([^)]+)\)\s*(?:throw\s+new\s+(\w+Exception)\s*\(\s*["\']?([^"\');]+)["\']?\s*\)|throw\s+new\s+(\w+Exception)\s*\([^)]*\));', re.IGNORECASE)
PROCEDURAL_GUARD_REGEX = re.compile(
    r'if\s*\(([^)]+)\)\s*(?:\{\s*)?return\s+(BadRequest|NotFound|Conflict|Forbid|Unauthorized|UnprocessableEntity|Results\.\w+|TypedResults\.\w+)\s*\(([^;]*)\)',
    re.IGNORECASE
)
GUARD_CLAUSE_LIB_REGEX = re.compile(
    r'\b(?:Guard|Ensure|Arg)\.(?:Against|That)\.([A-Za-z0-9_]+)\s*\(([^;]+)\);',
    re.IGNORECASE
)
TEST_METHOD_REGEX = re.compile(r'\[(?:Fact|Test|Theory)\]\s*(?:public\s+(?:async\s+)?(?:Task|void)\s+([A-Za-z0-9_]+)\s*\()', re.IGNORECASE)
STORED_PROC_REGEX = re.compile(r'["\'](sp_[A-Za-z0-9_]+|usp_[A-Za-z0-9_]+)["\']', re.IGNORECASE)

# Algorithm extraction patterns
CALCULATION_REGEX = re.compile(r'^\s*(?:decimal|double|float|int|var)\s+([A-Za-z0-9_]+)\s*=\s*([^;]+[\+\-\*\/][^;]+);', re.MULTILINE)
MUTATION_REGEX = re.compile(r'^\s*([A-Za-z0-9_]+\.(?:Status|State|Stage|Phase))\s*=\s*([^;]+);', re.MULTILINE)
EXTERNAL_CALL_REGEX = re.compile(r'^\s*(?:var\s+\w+\s*=\s*)?await\s+(_[A-Za-z0-9_]+(?:Service|Client|Gateway|Repository)\.[A-Za-z0-9_]+\([^;]*\));', re.MULTILINE)

def extract_rules_from_file(file_path: Path, module_filter: str = "", is_anemic: bool = False) -> Dict[str, Any]:
    rel_path = str(file_path)
    if module_filter and module_filter.lower() not in rel_path.lower():
        return {}

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}

    results = {
        "validators": [],
        "data_annotations": [],
        "domain_errors": [],
        "state_enums": [],
        "guard_invariants": [],
        "procedural_guards": [],
        "test_specs": [],
        "stored_procs": [],
        "calculations": [],
        "mutations": [],
        "external_calls": []
    }

    # 1. Validators
    rules = []
    for r_match in RULE_FOR_REGEX.finditer(content):
        clean_rule = " ".join(r_match.group(0).split())
        if len(clean_rule) < 200:
            rules.append(clean_rule)
    if rules:
        val_name = file_path.stem
        target_model = val_name.replace("Validation", "").replace("Validator", "")
        v_class = VALIDATOR_CLASS_REGEX.search(content)
        if v_class:
            val_name = v_class.group(1)
            base_decl = v_class.group(2).strip()
            where_m = re.search(r'where\s+\w+\s*:\s*(\w+)', base_decl)
            gen_m = re.search(r'<(\w+)>', base_decl)
            if where_m:
                target_model = where_m.group(1)
            elif gen_m:
                target_model = gen_m.group(1)
        results["validators"].append({
            "validator": val_name,
            "model": target_model,
            "rules": rules[:10]
        })

    # DataAnnotations
    for da in DATA_ANNOTATION_REGEX.finditer(content):
        attr_name = da.group(1)
        attr_param = da.group(2) or ""
        prop_name = da.group(3) or "Property"
        results["data_annotations"].append(f"[{attr_name}{f'({attr_param})' if attr_param else ''}] on `{prop_name}`")

    # 2. Domain Errors & Custom Domain Exceptions
    for err_match in ERROR_DEF_REGEX.finditer(content):
        results["domain_errors"].append({
            "name": err_match.group(1),
            "code": err_match.group(2),
            "message": err_match.group(3)
        })

    for exc_match in EXCEPTION_CLASS_REGEX.finditer(content):
        exc_name = exc_match.group(1)
        base_exc = exc_match.group(2)
        if exc_name not in ["HttpRequestException", "ArgumentNullException", "InvalidOperationException", "Exception"]:
            results["domain_errors"].append({
                "name": exc_name,
                "code": base_exc,
                "message": f"Business Exception derived from {base_exc}"
            })

    for factory_match in ERROR_FACTORY_REGEX.finditer(content):
        mname = factory_match.group(1)
        if mname not in ["Problem", "Ok", "Created", "BadRequest", "NotFound", "ValidationProblem", "Success"]:
            results["domain_errors"].append({
                "name": mname,
                "code": "FactoryMethod",
                "message": f"Domain error factory {mname}()"
            })

    # 3. State Enums
    for enum_match in ENUM_REGEX.finditer(content):
        members = [m.strip().split("=")[0].strip() for m in enum_match.group(2).split(",") if m.strip() and not m.strip().startswith("//")]
        results["state_enums"].append({
            "name": enum_match.group(1),
            "members": members
        })

    # 4. Guard Invariants & Procedural HTTP Guards
    for guard_match in GUARD_THROW_REGEX.finditer(content):
        results["guard_invariants"].append({
            "type": "throw",
            "condition": guard_match.group(1).strip(),
            "target": guard_match.group(2) or guard_match.group(4) or "Exception",
            "message": (guard_match.group(3) or "").strip()
        })

    for p_match in PROCEDURAL_GUARD_REGEX.finditer(content):
        results["procedural_guards"].append({
            "type": "http_guard",
            "condition": p_match.group(1).strip(),
            "target": p_match.group(2).strip(),
            "message": (p_match.group(3) or "").strip()
        })

    for lib_match in GUARD_CLAUSE_LIB_REGEX.finditer(content):
        results["guard_invariants"].append({
            "type": "guard_clause",
            "condition": lib_match.group(2).strip(),
            "target": f"Guard.{lib_match.group(1)}",
            "message": ""
        })

    # 5. Semantic Algorithm Distiller (Calculations, Mutations, External Calls)
    for calc in CALCULATION_REGEX.finditer(content):
        results["calculations"].append(f"`{calc.group(1)} = {calc.group(2).strip()};`")

    for mut in MUTATION_REGEX.finditer(content):
        results["mutations"].append(f"`{mut.group(1)} = {mut.group(2).strip()};`")

    for ext in EXTERNAL_CALL_REGEX.finditer(content):
        results["external_calls"].append(f"`await {ext.group(1)};`")

    # 6. Test Specs
    for test_match in TEST_METHOD_REGEX.finditer(content):
        method_name = test_match.group(1)
        if any(w in method_name for w in ["Should", "When", "Given", "Must", "Throws"]):
            results["test_specs"].append(method_name.replace("_", " "))

    # 7. Stored Procedures
    for sp in STORED_PROC_REGEX.finditer(content):
        results["stored_procs"].append(sp.group(1))

    return results

def build_module_rule_card(module_name: str, target_root: str = ".") -> str:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    domains_dir = intel_dir / "domains"
    domains_dir.mkdir(parents=True, exist_ok=True)

    keys_file = intel_dir / "architecture" / "master-keys.json"
    is_anemic = False
    if keys_file.exists():
        try:
            kdata = json.loads(keys_file.read_text(encoding="utf-8"))
            is_anemic = (kdata.get("domain") == "AnemicDomain_FatService")
        except Exception:
            pass

    agg_validators = []
    agg_da = []
    agg_errors = []
    agg_enums = []
    agg_guards = []
    agg_procedural_guards = []
    agg_specs = []
    agg_sps = set()
    agg_calcs = []
    agg_muts = []
    agg_exts = []

    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git"]):
            continue
        res = extract_rules_from_file(cs_file, module_name, is_anemic)
        if not res:
            continue
        agg_validators.extend(res["validators"])
        agg_da.extend(res["data_annotations"])
        agg_errors.extend(res["domain_errors"])
        agg_enums.extend(res["state_enums"])
        agg_guards.extend(res["guard_invariants"])
        agg_procedural_guards.extend(res["procedural_guards"])
        agg_specs.extend(res["test_specs"])
        agg_sps.update(res["stored_procs"])
        agg_calcs.extend(res["calculations"])
        agg_muts.extend(res["mutations"])
        agg_exts.extend(res["external_calls"])

    card_lines = [
        f"# Business Knowledge & Distilled Algorithms: {module_name.upper()}",
        f"*Domain Mode: {'Anemic Fat Service' if is_anemic else 'Rich Domain (DDD)'}*",
        "",
        "## 1. State Lifecycles (State Machines)"
    ]
    if agg_enums:
        for en in agg_enums:
            card_lines.append(f"- **{en['name']}:** `{' -> '.join(en['members'])}`")
    else:
        card_lines.append("- *No state enums detected.*")

    card_lines.extend(["", "## 2. Forbidden Operations & Domain Errors"])
    if agg_errors:
        for err in agg_errors[:15]:
            card_lines.append(f"- **[{err['code']}]** `{err['name']}`: \"{err['message']}\"")
    else:
        card_lines.append("- *No explicit domain error constants found.*")

    card_lines.extend(["", "## 3. Core Business Algorithms & Calculations (Semantic Distiller)"])
    if agg_calcs or agg_muts or agg_exts:
        if agg_calcs:
            card_lines.append("### Key Calculations & Formulas")
            for c in list(set(agg_calcs))[:8]:
                card_lines.append(f"  - {c}")
        if agg_muts:
            card_lines.append("### State Transitions & Mutations")
            for m in list(set(agg_muts))[:6]:
                card_lines.append(f"  - {m}")
        if agg_exts:
            card_lines.append("### Cross-Service Dependencies")
            for ex in list(set(agg_exts))[:6]:
                card_lines.append(f"  - {ex}")
    else:
        card_lines.append("- *No inline mathematical formulas or state mutations detected.*")

    card_lines.extend(["", "## 4. Input Validations (FluentValidation & DataAnnotations)"])
    if agg_validators:
        for val in agg_validators[:5]:
            card_lines.append(f"### {val['validator']} (for `{val['model']}`)")
            for r in val["rules"][:6]:
                card_lines.append(f"  - `{r}`")
    elif agg_da:
        card_lines.append("### DataAnnotations Constraints")
        for da_item in sorted(list(set(agg_da)))[:10]:
            card_lines.append(f"  - `{da_item}`")
    else:
        card_lines.append("- *No validation classes or annotations detected.*")

    card_lines.extend(["", "## 5. Guard Invariants, Throws & Procedural Preconditions"])
    has_guards = False
    if agg_guards:
        has_guards = True
        for g in agg_guards[:12]:
            if g.get("type") == "guard_clause":
                card_lines.append(f"- Enforce Guard: `{g['target']}({g['condition']})`")
            else:
                msg_str = f" -> \"{g['message']}\"" if g.get('message') else ""
                card_lines.append(f"- When `{g['condition']}` throw `{g['target']}`{msg_str}")

    if agg_procedural_guards:
        has_guards = True
        card_lines.append("### Procedural HTTP Preconditions & Response Guards")
        for pg in agg_procedural_guards[:10]:
            msg_str = f" with \"{pg['message']}\"" if pg.get('message') else ""
            card_lines.append(f"- When `{pg['condition']}` return `{pg['target']}`{msg_str}")

    if not has_guards:
        card_lines.append("- *No inline guard conditions detected.*")

    if agg_sps:
        card_lines.extend(["", "## 6. Stored Procedures (Data Logic)"])
        for sp_name in sorted(list(agg_sps))[:10]:
            card_lines.append(f"- Database Procedure: `{sp_name}`")

    card_lines.extend(["", "## 7. Living Specifications (from Unit Tests)"])
    if agg_specs:
        for sp in agg_specs[:15]:
            card_lines.append(f"- {sp}")
    else:
        card_lines.append("- *No unit test specifications found.*")

    output_path = domains_dir / f"{module_name.lower()}-rules.md"
    card_content = "\n".join(card_lines)
    output_path.write_text(card_content, encoding="utf-8")
    return str(output_path)

if __name__ == "__main__":
    mod = sys.argv[1] if len(sys.argv) > 1 else "core"
    target = sys.argv[2] if len(sys.argv) > 2 else "."
    card_file = build_module_rule_card(mod, target)
    print(f"[OK] Ottonet Skill distilled rules & algorithms for [{mod}].")
    print(f"[OK] Card saved to: {card_file}")
