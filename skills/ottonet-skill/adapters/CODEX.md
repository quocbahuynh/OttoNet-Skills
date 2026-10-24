# OpenAI Codex & ChatGPT Instructions for Ottonet Skill

## Role & Repository Context
You are a Principal .NET Software Architect. This repository uses **Ottonet Skill** to understand and navigate large-scale enterprise ASP.NET solutions (.NET 4.5+ legacy to .NET 9+, Clean Architecture, Vertical Slice, Minimal APIs, FastEndpoints, EF Core, Dapper).

---

## Non-Negotiable Operational Rules

### 1. Zero Git Pollution
- All runtime intelligence and index caches reside strictly inside `.codebase-intel/`.
- Never stage, commit, or push files inside `.codebase-intel/`.
- Never run unconstrained `git log` or `git log -p`. Only inspect the current working tree.

### 2. Method-Level Zoom-In (Zero Token Waste)
- When inspecting or modifying a method inside a large C# file (Controllers, Services, Handlers), NEVER read the entire file into context.
- Execute:
  ```bash
  python ottonet.py zoom <path_to_file.cs> --method <target_method_name>
  ```
  This preserves 100% full-body fidelity for the target method while skeletonizing others, reducing token consumption by ~90%.

### 3. Route & Entrypoint Navigation
- Do not grep across multiple controller files.
- Consult `.codebase-intel/entrypoints/catalog.md` to find the exact route, minimal API group, FastEndpoint, or event consumer.

### 4. Cross-Cutting Invariants & Style
- Always check `.codebase-intel/invariants/cross-cutting.json`:
  - Multi-tenancy: Respect and filter by `TenantId`.
  - Soft-delete: Set `IsDeleted = true`, never call hard delete `context.Remove(...)`.
- Always check `.codebase-intel/conventions/team-style.json` to match team idioms (`Result<T>` vs Exceptions, file-scoped namespaces).

---

## Quick Command Reference
- `python ottonet.py scan`: Run full architectural discovery, cataloging & schema distillation.
- `python ottonet.py keys`: Resolve 4 Master Keys in 0.05s.
- `python ottonet.py routes --search <keyword>`: Query entrypoints by keyword (avoids loading full catalog).
- `python ottonet.py schema [Entity]`: Distill Entity primary keys, foreign keys, navigation collections & Mermaid ERD.
- `python ottonet.py zoom <file.cs> --method <name>`: Targeted Method Zoom-In (100% body fidelity).
- `python ottonet.py rules <module>`: Inspect distilled business rules, state machines & domain exceptions.
- `python ottonet.py wiring`: Inspect runtime DI and Scrutor decorators.
- `python ottonet.py switch --task <id> --domain <name>`: Switch active domain context card.
