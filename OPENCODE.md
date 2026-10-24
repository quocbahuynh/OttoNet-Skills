# OpenCode Instructions for Ottonet Skill

## Core Principles & Navigation Engine
- **ASP.NET Architecture Intelligence:** This repository is managed with Ottonet Skill.
- **Zero Git Pollution:** All runtime caches and index cards remain strictly inside `.codebase-intel/`. Never stage, commit, or mention `.codebase-intel/` files in commits.
- **Zero-Token Waste Inspection:** When inspecting or modifying a method in a large C# file, NEVER read the full file. Run:
  ```bash
  python ottonet.py zoom <path_to_file.cs> --method <target_method_name>
  ```
  This preserves 100% full-body fidelity for the target method while skeletonizing others.

## Operational Commands
- `python ottonet.py scan`: Run full architectural discovery, cataloging & schema distillation.
- `python ottonet.py routes --search <kw>`: Query routes by keyword (avoids dumping full catalog).
- `python ottonet.py schema [Entity]`: Distill Entity primary keys, foreign keys, navigation collections & Mermaid ERD.
- `python ottonet.py zoom <file.cs> --method <name>`: Targeted Method Zoom-In (100% body fidelity).
- `python ottonet.py rules <module>`: Inspect distilled business rules, state machines, and calculations.
- `python ottonet.py wiring`: Check runtime DI and Scrutor decorators.
- `python ottonet.py switch --task <id> --domain <name>`: Switch active domain context card.

## Non-Negotiable Invariants
- Check `.codebase-intel/invariants/cross-cutting.json`: If Multi-Tenancy or Soft-Delete is active, always respect `TenantId` and never perform hard deletes.
- Check `.codebase-intel/conventions/team-style.json`: Match team coding idioms (`Result<T>` vs Exceptions, file-scoped namespaces).
