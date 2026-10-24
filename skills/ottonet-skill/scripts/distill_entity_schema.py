#!/usr/bin/env python3
"""
distill_entity_schema.py - Entity-Relationship & Navigation Properties Distiller for Ottonet Skill.
Extracts:
1. Primary Keys & Foreign Keys
2. Navigation Properties (1-to-Many collections, Many-to-One references)
3. Value Objects and Domain Enums
4. Generates Mermaid ER Diagrams & Architecture Schema Card

Outputs:
- .codebase-intel/architecture/schema.md
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

INTEL_DIR_NAME = ".codebase-intel"

ENTITY_CLASS_REGEX = re.compile(
    r'public\s+(?:(?:abstract|partial|sealed)\s+)*(?:class|record(?:\s+class)?)\s+(\w+)[^{:(]*(?::\s*([^{:(]+))?',
    re.IGNORECASE
)

PROPERTY_REGEX = re.compile(
    r'public\s+([A-Za-z0-9_<>?,]+)\s+([A-Za-z0-9_]+)\s*\{\s*get\b',
    re.MULTILINE
)

DBSET_REGEX = re.compile(
    r'public\s+DbSet<(\w+)>\s+(\w+)\s*\{\s*get;',
    re.IGNORECASE
)

PRIMITIVE_TYPES = {
    "int", "int?", "long", "long?", "short", "short?", "byte", "byte?",
    "double", "double?", "float", "float?", "decimal", "decimal?",
    "bool", "bool?", "string", "string?", "datetime", "datetime?",
    "datetimeoffset", "datetimeoffset?", "guid", "guid?", "timespan", "timespan?"
}

SQL_FROM_JOIN_REGEX = re.compile(
    r'\b(?:FROM|JOIN)\s+(?:\[?(?:dbo|public)\]?\.)?\[?([A-Za-z0-9_]+)\]?(?:\s+(?:AS\s+)?([A-Za-z0-9_]+))?',
    re.IGNORECASE
)

SQL_MUTATION_REGEX = re.compile(
    r'\b(INSERT\s+INTO|UPDATE|DELETE\s+FROM)\s+(?:\[?(?:dbo|public)\]?\.)?\[?([A-Za-z0-9_]+)\]?',
    re.IGNORECASE
)

SQL_JOIN_ON_REGEX = re.compile(
    r'\bON\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)',
    re.IGNORECASE
)

SQL_PARAM_REGEX = re.compile(r'@([A-Za-z0-9_]+)')

SQL_EXCLUDED_KEYWORDS = {
    "select", "where", "group", "order", "having", "openjson", "string_split",
    "values", "set", "inner", "left", "right", "full", "cross", "outer", "join",
    "table", "sys", "information_schema"
}

def scan_raw_sql_tables(root: Path) -> Dict[str, Dict[str, Any]]:
    """Mines raw SQL, Dapper, and ADO.NET queries to infer tables, operations, and joins."""
    sql_tables: Dict[str, Dict[str, Any]] = {}

    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git", "TestResults"]):
            continue
        try:
            content = cs_file.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue

        rel = str(cs_file.relative_to(root))

        # Check for presence of SQL query markers
        if not any(k in content.upper() for k in ["SELECT ", "INSERT INTO", "UPDATE ", "DELETE FROM", "EXEC "]):
            continue

        alias_map: Dict[str, str] = {}

        # Scan FROM and JOIN tables
        for m in SQL_FROM_JOIN_REGEX.finditer(content):
            tbl = m.group(1)
            alias = m.group(2) or ""
            if tbl.lower() in SQL_EXCLUDED_KEYWORDS:
                continue
            # Filter out C# keywords / types that might match
            if tbl in ["string", "int", "var", "Task", "bool", "void"]:
                continue

            sql_tables.setdefault(tbl, {
                "name": tbl,
                "operations": set(),
                "files": set(),
                "parameters": set(),
                "joins": []
            })
            sql_tables[tbl]["operations"].add("SELECT")
            sql_tables[tbl]["files"].add(rel)
            if alias and alias.lower() not in SQL_EXCLUDED_KEYWORDS:
                alias_map[alias.lower()] = tbl

        # Scan INSERT, UPDATE, DELETE
        for m in SQL_MUTATION_REGEX.finditer(content):
            op = "INSERT" if "INSERT" in m.group(1).upper() else ("UPDATE" if "UPDATE" in m.group(1).upper() else "DELETE")
            tbl = m.group(2)
            if tbl.lower() in SQL_EXCLUDED_KEYWORDS:
                continue
            sql_tables.setdefault(tbl, {
                "name": tbl,
                "operations": set(),
                "files": set(),
                "parameters": set(),
                "joins": []
            })
            sql_tables[tbl]["operations"].add(op)
            sql_tables[tbl]["files"].add(rel)

        # Scan JOIN ON conditions (e.g. o.CustomerId = c.Id)
        for m in SQL_JOIN_ON_REGEX.finditer(content):
            left_alias, left_col = m.group(1).lower(), m.group(2)
            right_alias, right_col = m.group(3).lower(), m.group(4)
            left_tbl = alias_map.get(left_alias, left_alias)
            right_tbl = alias_map.get(right_alias, right_alias)

            for tbl_cand in sql_tables:
                if tbl_cand.lower() == left_tbl:
                    left_tbl = tbl_cand
                if tbl_cand.lower() == right_tbl:
                    right_tbl = tbl_cand

            if left_tbl in sql_tables:
                join_rel = f"{left_tbl}.{left_col} = {right_tbl}.{right_col}"
                if join_rel not in sql_tables[left_tbl]["joins"]:
                    sql_tables[left_tbl]["joins"].append(join_rel)

        # Scan SQL Parameters
        for p in SQL_PARAM_REGEX.findall(content):
            if len(p) > 1 and not p.isdigit():
                # Associate with tables found in this file
                for t in sql_tables:
                    if rel in sql_tables[t]["files"] and len(sql_tables[t]["parameters"]) < 12:
                        sql_tables[t]["parameters"].add(f"@{p}")

    # Convert sets to sorted lists for serialization
    for t, info in sql_tables.items():
        info["operations"] = sorted(info["operations"])
        info["files"] = sorted(info["files"])
        info["parameters"] = sorted(info["parameters"])

    return sql_tables

def scan_entities(root: Path) -> Dict[str, Dict[str, Any]]:
    entities: Dict[str, Dict[str, Any]] = {}
    dbset_entities: Set[str] = set()

    # Pass 1: Discover DbSet entities from DbContexts
    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git", "TestResults"]):
            continue
        try:
            content = cs_file.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue
        for m in DBSET_REGEX.finditer(content):
            dbset_entities.add(m.group(1))

    # Pass 2: Discover and parse entity classes
    for cs_file in root.rglob("*.cs"):
        parts = cs_file.parts
        if any(x in parts for x in [INTEL_DIR_NAME, "bin", "obj", "node_modules", ".git", "TestResults"]):
            continue
        rel = str(cs_file.relative_to(root))
        try:
            content = cs_file.read_text(encoding="utf-8-sig", errors="ignore")
        except Exception:
            continue

        for m in ENTITY_CLASS_REGEX.finditer(content):
            cname = m.group(1)
            raw_base = m.group(2) or ""
            base_decl = raw_base.split("where")[0].strip()

            is_in_entity_dir = any(d in parts for d in ["Entities", "Models", "Domain", "Aggregates"])
            is_entity_base = any(b in base_decl for b in ["Entity", "EntityBase", "BaseEntity", "AggregateRoot"])
            is_dbset = cname in dbset_entities

            if not (is_in_entity_dir or is_entity_base or is_dbset):
                continue
            if cname.endswith("Tests") or cname.endswith("Context") or cname.endswith("Config") or cname.endswith("Configuration"):
                continue

            props = PROPERTY_REGEX.findall(content)
            if not props:
                continue

            entity_info = {
                "name": cname,
                "file": rel,
                "base_class": base_decl.split("<")[0].split(",")[0].strip() if base_decl else "",
                "pk": "Id",
                "pk_type": "int",
                "foreign_keys": [],
                "collections": [],
                "references": [],
                "attributes": []
            }

            for ptype, pname in props:
                ptype_clean = ptype.strip()
                pname_clean = pname.strip()

                if pname_clean.lower() == "id":
                    entity_info["pk"] = pname_clean
                    entity_info["pk_type"] = ptype_clean
                elif pname_clean.endswith("Id") and len(pname_clean) > 2:
                    ref_entity = pname_clean[:-2]
                    entity_info["foreign_keys"].append({
                        "name": pname_clean,
                        "type": ptype_clean,
                        "references": ref_entity
                    })
                elif any(col in ptype_clean for col in ["ICollection<", "IList<", "List<", "IEnumerable<"]):
                    match_col = re.search(r'<(\w+)>', ptype_clean)
                    if match_col:
                        target = match_col.group(1)
                        entity_info["collections"].append({
                            "property": pname_clean,
                            "type": target,
                            "relation": "1-to-Many"
                        })
                elif ptype_clean.lower() not in PRIMITIVE_TYPES:
                    entity_info["references"].append({
                        "property": pname_clean,
                        "type": ptype_clean.rstrip("?")
                    })
                else:
                    entity_info["attributes"].append({
                        "name": pname_clean,
                        "type": ptype_clean
                    })

            entities[cname] = entity_info

    return entities

def build_schema_documentation(entities: Dict[str, Dict[str, Any]], target_root: str = ".", sql_tables: Optional[Dict[str, Dict[str, Any]]] = None) -> str:
    root = Path(target_root).resolve()
    intel_dir = root / INTEL_DIR_NAME
    arch_dir = intel_dir / "architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    schema_file = arch_dir / "schema.md"
    sql_file = arch_dir / "sql_tables.md"

    if sql_tables is None:
        sql_tables = scan_raw_sql_tables(root)

    # Write separate sql_tables.md if any raw SQL queries exist
    if sql_tables:
        sql_lines = [
            "# Raw SQL & Dapper Inferred Database Tables",
            f"*Discovered: {len(sql_tables)} tables in embedded SQL / Dapper / ADO.NET queries*",
            "",
            "| Table | Operations | Parameters | Inferred Joins | Referenced In Files |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]
        for tname, tinfo in sorted(sql_tables.items()):
            ops_str = ", ".join(f"`{op}`" for op in tinfo["operations"]) or "*None*"
            params_str = ", ".join(f"`{p}`" for p in tinfo["parameters"][:5]) or "*None*"
            joins_str = "<br/>".join(f"`{j}`" for j in tinfo["joins"][:3]) or "*None*"
            files_str = ", ".join(f"[{Path(f).name}]({f})" for f in tinfo["files"][:3])
            sql_lines.append(f"| **{tname}** | {ops_str} | {params_str} | {joins_str} | {files_str} |")
        sql_file.write_text("\n".join(sql_lines), encoding="utf-8")

    lines = [
        "# Database & Domain Entity Schema Map",
        f"*Discovered: {len(entities)} Domain Entities, {len(sql_tables)} Raw SQL Tables*",
        ""
    ]

    # Mermaid ER Diagram for Top Relationships (EF Core + Dapper Joins)
    if entities or sql_tables:
        lines.extend([
            "## Entity Relationship Overview",
            "```mermaid",
            "erDiagram"
        ])
        edge_count = 0
        added_edges = set()

        for ename, einfo in sorted(entities.items()):
            for fk in einfo["foreign_keys"]:
                if fk["references"] in entities and edge_count < 30:
                    edge = (fk['references'], ename, fk['name'])
                    if edge not in added_edges:
                        added_edges.add(edge)
                        lines.append(f"    {fk['references']} ||--o{{ {ename} : \"{fk['name']}\"")
                        edge_count += 1
            for col in einfo["collections"]:
                if col["type"] in entities and edge_count < 30:
                    edge = (ename, col['type'], col['property'])
                    if edge not in added_edges:
                        added_edges.add(edge)
                        lines.append(f"    {ename} ||--o{{ {col['type']} : \"{col['property']}\"")
                        edge_count += 1

        # Add Dapper inferred join relationships to Mermaid
        if sql_tables:
            for tname, tinfo in sorted(sql_tables.items()):
                for join in tinfo["joins"]:
                    # join is like "Orders.CustomerId = Customers.Id"
                    if "=" in join and edge_count < 35:
                        parts = join.split("=")
                        left_t = parts[0].strip().split(".")[0]
                        right_t = parts[1].strip().split(".")[0]
                        if left_t != right_t:
                            edge = (right_t, left_t, "inferred_join")
                            if edge not in added_edges:
                                added_edges.add(edge)
                                lines.append(f"    {right_t} ||--o{{ {left_t} : \"join\"")
                                edge_count += 1

        lines.extend(["```", ""])

    lines.extend([
        "## Entity Catalog & Navigation Properties",
        "| Entity | Primary Key | Foreign Keys | Navigation Collections | File |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])

    for ename, einfo in sorted(entities.items()):
        fks_str = ", ".join(f"`{fk['name']} -> {fk['references']}`" for fk in einfo["foreign_keys"][:4]) or "*None*"
        cols_str = ", ".join(f"`{col['property']} ({col['type']})`" for col in einfo["collections"][:3]) or "*None*"
        lines.append(f"| **{ename}** | `{einfo['pk_type']} {einfo['pk']}` | {fks_str} | {cols_str} | [{einfo['file']}]({einfo['file']}) |")

    if sql_tables:
        lines.extend([
            "",
            "## Raw SQL & Dapper Inferred Tables",
            "| Table | Operations | Inferred Joins | Queried In Files |",
            "| :--- | :--- | :--- | :--- |"
        ])
        for tname, tinfo in sorted(sql_tables.items()):
            ops_str = ", ".join(f"`{op}`" for op in tinfo["operations"]) or "*None*"
            joins_str = ", ".join(f"`{j}`" for j in tinfo["joins"][:2]) or "*None*"
            files_str = ", ".join(f"[{Path(f).name}]({f})" for f in tinfo["files"][:2])
            lines.append(f"| **{tname}** | {ops_str} | {joins_str} | {files_str} |")

    schema_file.write_text("\n".join(lines), encoding="utf-8")
    return str(schema_file)

def get_entity_card(entity_name: str, entities: Dict[str, Dict[str, Any]], sql_tables: Optional[Dict[str, Dict[str, Any]]] = None) -> str:
    matched = None
    for name, info in entities.items():
        if name.lower() == entity_name.lower():
            matched = info
            break

    # If found in EF Core entities
    if matched:
        lines = [
            f"# Entity Schema: {matched['name']}",
            f"**File:** `{matched['file']}` | **Base Class:** `{matched['base_class'] or 'None'}`",
            "",
            f"### Primary Key",
            f"- `{matched['pk_type']} {matched['pk']}`",
            ""
        ]

        if matched["foreign_keys"]:
            lines.extend(["### Foreign Keys (Many-to-One Relationships)"])
            for fk in matched["foreign_keys"]:
                lines.append(f"- `{fk['type']} {fk['name']}` -> References **{fk['references']}**")
            lines.append("")

        if matched["collections"]:
            lines.extend(["### Navigation Collections (1-to-Many Relationships)"])
            for col in matched["collections"]:
                lines.append(f"- `{col['property']}` (`{col['relation']}` to `{col['type']}`)")
            lines.append("")

        if matched["references"]:
            lines.extend(["### Object References / Value Objects"])
            for r in matched["references"][:8]:
                lines.append(f"- `{r['type']} {r['property']}`")
            lines.append("")

        if matched["attributes"]:
            lines.extend(["### Core Attributes"])
            for a in matched["attributes"][:10]:
                lines.append(f"- `{a['type']} {a['name']}`")
            lines.append("")

        # Check if there are raw SQL references
        if sql_tables:
            for st, sinfo in sql_tables.items():
                if st.lower() == entity_name.lower() or st.lower() == f"{entity_name}s".lower():
                    lines.extend([
                        f"### Raw SQL / Dapper Queries Referencing This Table",
                        f"- **Operations:** {', '.join(sinfo['operations'])}",
                        f"- **Parameters:** {', '.join(sinfo['parameters']) if sinfo['parameters'] else 'None'}",
                        f"- **Inferred Joins:** {', '.join(sinfo['joins']) if sinfo['joins'] else 'None'}",
                        ""
                    ])
                    break

        return "\n".join(lines)

    # If not found in EF Core, check if it's a Raw SQL Table
    if sql_tables:
        for tname, tinfo in sql_tables.items():
            if tname.lower() == entity_name.lower() or tname.lower() == f"{entity_name}s".lower() or f"{tname}s".lower() == entity_name.lower():
                lines = [
                    f"# Raw SQL Database Table: {tname}",
                    f"*Inferred from Dapper / ADO.NET query strings*",
                    "",
                    f"### Operations",
                    f"- {', '.join(f'`{op}`' for op in tinfo['operations'])}",
                    "",
                    f"### Parameters / Filters",
                    f"- {', '.join(f'`{p}`' for p in tinfo['parameters']) if tinfo['parameters'] else '*None*'}",
                    "",
                    f"### Inferred Joins & Foreign Keys",
                    f"- {', '.join(f'`{j}`' for j in tinfo['joins']) if tinfo['joins'] else '*None*'}",
                    "",
                    f"### Repositories / Files",
                ]
                for f in tinfo["files"]:
                    lines.append(f"- [{f}]({f})")
                return "\n".join(lines)

    avail = sorted(list(entities.keys()) + (list(sql_tables.keys()) if sql_tables else []))
    return f"[WARN] Entity/Table '{entity_name}' not found. Available entities & tables: {', '.join(avail[:15])}"

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    entity_arg = sys.argv[2] if len(sys.argv) > 2 else ""

    # Smart swap if target is an entity name
    if entity_arg and Path(entity_arg).is_dir() and not Path(target).is_dir():
        target, entity_arg = entity_arg, target

    root_path = Path(target).resolve()
    all_ents = scan_entities(root_path)
    all_sqls = scan_raw_sql_tables(root_path)

    if entity_arg:
        card = get_entity_card(entity_arg, all_ents, all_sqls)
        print(card)
    else:
        out_doc = build_schema_documentation(all_ents, target, all_sqls)
        print(f"[OK] Discovered {len(all_ents)} entities and {len(all_sqls)} raw SQL tables.")
        print(f"[OK] Schema written to: {out_doc}")
