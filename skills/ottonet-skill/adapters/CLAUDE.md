# Ottonet Skill Instructions for Claude Code

## Principles & Operational Guidelines
- **Architecture Intelligence:** This ASP.NET repository is analyzed by Ottonet Skill.
- **Zero Git Pollution:** All generated caches and index cards are stored in `.codebase-intel/`. Never stage, commit, or mention `.codebase-intel/` files in commits.
- **Token Optimization:** When examining large C# files, never dump full file contents. Always use:
  ```bash
  python ottonet.py zoom <path_to_file.cs> --method <target_method_name>
  ```
  This keeps full 100% body fidelity for the target method while skeletonizing others.

## Common Workflows
- **Initialize & Scan:** `python ottonet.py scan` (runs full discovery & schema distillation)
- **Filtered Route Search:** `python ottonet.py routes --search <keyword>` (avoids loading massive catalogs)
- **Entity Schema Map:** `python ottonet.py schema [Entity]` (extracts PKs, FKs, navigation collections & Mermaid ERD)
- **Business Rules:** Check `.codebase-intel/domains/<module>-rules.md` for invariants, state machines, and calculations.
- **Runtime Wiring:** Check `.codebase-intel/architecture/runtime-wiring.json` for Scrutor decorators.
