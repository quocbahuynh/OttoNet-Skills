---
name: ottonet-skill
description: Universal ASP.NET intelligence and navigation skill for large-scale enterprise .NET codebases. Uses 4 Master Keys for fast discriminator routing, resolves generic base controller inheritance and partial classes, extracts distilled business algorithms and invariants, provides Targeted Method Zoom-In (--focus-method), traces runtime DI and Scrutor decorators, and operates in zero-click autonomous mode.
---

# Ottonet Skill: Universal ASP.NET Codebase Intelligence

Ottonet Skill equips Antigravity with the instincts of a Principal .NET Architect. It conquers massive, messy enterprise ASP.NET solutions (.NET 4.5+ legacy to .NET 9+, Clean Architecture, Vertical Slice, MVC, Minimal APIs, FastEndpoints, Carter, Dapper, Stored Procedures, generic controllers, partial classes) with **zero-click autonomy**, **zero Git pollution**, and **under 3,500 tokens**.

---

## 5 Core Architect Weapons

1. **4 Master Keys Discriminator:** Resolves `bootstrap_key`, `api_key`, `domain_key`, and `persistence_key` in 0.05s to bypass irrelevant scanners.
2. **Inheritance & Modular Route Resolver:** Resolves generic base controllers (`CrudController<T>`), primary constructors, `[action]` route inheritance, and automatically partitions routes by bounded context (`.codebase-intel/entrypoints/modules/<Mod>.md`) with instant CLI search (`ottonet routes --search <kw>`).
3. **Universal Entity & Dapper SQL Distiller (`ottonet schema [Entity]`):** Automatically extracts Primary Keys, Foreign Keys, 1-to-Many navigation collections, embedded Raw SQL / Dapper tables, and Mermaid ER diagrams without reading massive DbContext files.
4. **Hybrid Roslyn AST & Targeted Method Zoom-In (`ottonet zoom` / `ottonet inspect`):** Powered by native Roslyn compiler AST when `dotnet` is present with seamless zero-dependency Python lexer fallback. Skeletonizes non-relevant methods while keeping **100% full-body fidelity** of the target method being modified.
5. **Semantic Logic Distiller & Invariant Scanner:** Captures mathematical formulas, state transitions, procedural HTTP response guards (`BadRequest`, `NotFound`, `Conflict`), custom Domain Exceptions (`*Exception : DomainException`), and cross-service calls while respecting Scrutor runtime decorators.

---

## Universal Single-Target Investigator (`ottonet inspect`)

When an agent needs intelligence on ANY target, use one command:
```bash
python ottonet.py inspect <target> [--method <method_name>] [--full]
```
- **If target is a File** (`path/to/OrderService.cs`): Returns Roslyn AST skeleton or targeted zoom-in method.
- **If target is a Route** (`/api/orders` or `POST /api/orders`): Returns matching endpoints, handlers, verbs, and source files.
- **If target is an Entity / Table** (`Order` or `Invoices`): Returns entity relationships, foreign keys, and Dapper queries referencing it.
- **If target is a Module** (`Orders` or `Billing`): Returns distilled business rules, calculations, and preconditions.

---

## Autonomous Zero-Click Operation (CRITICAL FOR AGENT)

**NEVER ask the user to manually run CLI commands.** Antigravity MUST execute all needed commands autonomously in the background:

1. **On First Turn in an ASP.NET Codebase:**
   Autonomously verify if `.codebase-intel/` exists. If not, silently run:
   ```bash
   python skills/ottonet-skill/scripts/intel_init.py
   python skills/ottonet-skill/scripts/resolve_master_keys.py
   python skills/ottonet-skill/scripts/trace_di_decorators.py
   python skills/ottonet-skill/scripts/detect_conventions.py
   ```

2. **On Topic/Task/Module Switch:**
   When the user mentions a specific feature, bug, or module (e.g. "Incident SLA", "Project Schedule", "Order Checkout"):
   - Autonomously switch domain, distill rules, and inspect entity relationships:
     ```bash
     python skills/ottonet-skill/scripts/domain_manager.py switch --task <ID_or_Name> --domain <ModuleName>
     python skills/ottonet-skill/scripts/extract_business_rules.py <ModuleName>
     python skills/ottonet-skill/scripts/distill_entity_schema.py . <EntityName>
     ```
   - Read `.codebase-intel/domains/<ModuleName>-rules.md` to align with invariants and formulas.

3. **On Route & Entrypoint Investigation:**
   - NEVER read the entire 350-line `catalog.md` if the user is asking about a specific feature.
   - Run filtered route discovery directly:
     ```bash
     python ottonet.py routes --search "<feature_name>" --method <POST/GET>
     ```
   - Or read the modular catalog `.codebase-intel/entrypoints/modules/<ModuleName>.md`.

4. **On Method-Level Investigation:**
   When locating and reading the code for a target method `ProcessOrderAsync`:
   - NEVER read a 3,000-line service file in full.
   - Run Targeted Method Zoom-In:
     ```bash
     python skills/ottonet-skill/scripts/csharp_skeleton.py path/to/OrderService.cs --focus-method ProcessOrderAsync
     ```
   - This returns 150 lines (full body of `ProcessOrderAsync` + skeletons of other methods), eliminating token bloat and preventing hallucinations.

---

## Non-Negotiable Rules of Engagement

1. **Zero Git Pollution:**
   - All runtime caches remain exclusively in `.codebase-intel/` (protected by internal `.gitignore` and `.git/info/exclude`).
   - Never stage, commit, or push files inside `.codebase-intel/`.
   - Never run unconstrained `git log` or `git log -p`. Only inspect the current working tree.

2. **Honor Runtime Decorators & Invariants:**
   - Check `.codebase-intel/architecture/runtime-wiring.json`. If Scrutor decorators exist on a service, respect the decorator wrapping.
   - Check `.codebase-intel/invariants/cross-cutting.json`. If Multi-Tenancy or Soft-Delete is enabled, respect `TenantId` and never perform hard deletes.
   - Check `.codebase-intel/conventions/team-style.json` to match team code style (`Result<T>` vs Exceptions, file-scoped namespaces).
