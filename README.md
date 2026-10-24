# Ottonet

**Universal Codebase Intelligence & Navigation for ASP.NET Solutions**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-4.5%20to%2010.0-512BD4)](https://dotnet.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)](https://www.python.org/)
[![Multi-Agent](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Cursor%20%7C%20Claude%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20OpenCode%20%7C%20Codex-success)](#multi-agent-compatibility)

---

## Overview

Large-scale enterprise .NET codebases—spanning .NET Framework 4.5 monoliths to modern .NET 10 microservices—consistently overwhelm AI coding assistants. Repositories containing 200,000 to 500,000+ lines of code exhaust context windows, hallucinate cross-project dependencies, and remain blind to runtime patterns like Scrutor decorators, reflection-based dependency injection, and procedural guards.

**Ottonet** is a lightweight, zero-dependency intelligence sidecar that bridges this gap. It analyzes solutions in sub-second timeframes, distill architecture, schemas, and invariants into high-density reference maps, and feeds AI coding agents exactly what they need—reducing token consumption by **86% to 96%** while preventing hallucinated architectures.

---

## Core Capabilities

### 1. Universal Single-Command Investigator (`ottonet inspect`)
Eliminates context switching and command memorization. Pass any target, and Ottonet resolves it automatically:
- **File path** (`src/Services/OrderService.cs`) &rarr; Generates an AST skeleton with method signatures and side-effect annotations.
- **Route / Verb** (`/api/orders` or `POST /api/orders`) &rarr; Locates matching endpoints, controller actions, HTTP verbs, and exact source file lines.
- **Entity / Table** (`Order` or `Invoices`) &rarr; Generates primary key, foreign key, 1-to-many collection schemas, and raw SQL/Dapper queries.
- **Module / Domain** (`Billing` or `Orders`) &rarr; Compiles distilled business rules, state machine transitions, and procedural HTTP response guards.

### 2. Hybrid Roslyn AST & Targeted Method Zoom-In
- **Dual-Engine Execution:** When the .NET SDK is available, Ottonet leverages native Roslyn (`Microsoft.CodeAnalysis.CSharp`) for compiler-level AST precision. In lightweight environments, it seamlessly falls back to a zero-dependency Python lexer.
- **Targeted Method Zoom-In:** When modifying a single method in a 2,500-line service, Ottonet preserves **100% full-body fidelity** for the targeted method while skeletonizing non-relevant methods into dense one-line summaries annotating side-effects (`Mutates: ... | Calls: ... | Throws: ...`).

### 3. Modular Entrypoint Cataloger & Search
- Handles standard MVC controllers, generic base controller inheritance (`CrudController<T>`), primary constructors, Minimal APIs (`MapGroup`, `IEndpointGroup`), FastEndpoints, Carter modules, and gRPC services.
- Automatically partitions monolith route tables into bounded contexts (`.codebase-intel/entrypoints/modules/<Module>.md`), with sub-50ms CLI filtering via `--search` and `--method`.

### 4. Entity Schema & Raw SQL / Dapper Distiller
- Reverse-engineers domain models, EF Core `DbSet<T>` definitions, `sealed class`, `record`, and primary constructors without scanning massive DbContext files.
- **Heuristic SQL Invariant Miner:** Parses embedded SQL strings (`FROM <table>`, `JOIN <table> ON ...`, `INSERT INTO ...`, `UPDATE ...`) in Dapper, ADO.NET, and repository implementations, mapping inferred foreign keys and query parameters (`@Param`) into Mermaid ER diagrams.

### 5. Semantic Logic & Procedural Preconditions Miner
- **Domain Invariants:** Captures custom domain exceptions (`*Exception : DomainException`), guard clauses (`Ensure.That`), and mathematical algorithms.
- **Procedural HTTP Guards:** Captures business checks in traditional controllers (`if (amount <= 0) return BadRequest(...)`, `NotFound`, `Conflict`, `Results.BadRequest`).
- **State Machines:** Reconstructs domain lifecycle states from status enums.

### 6. Git-Aware Incremental Cache
Tracks file modification timestamps combined with the current Git `HEAD` commit reference. Cache invalidation occurs automatically upon branch checkout or pull, eliminating stale cache poisoning.

---

## Benchmarks

Benchmarked across **13 real-world open-source enterprise ASP.NET repositories** (over 2.28 million tokens of raw C# code):

| Repository | Domain & Architecture | Routes | Schemas | Business Guards | Scan Time | Raw Tokens | Intel Tokens | Reduction |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Jason Taylor CleanArchitecture** | Minimal APIs / Vertical Slice | 16 | 8 Ent + 3 SQL | 16 Domain + 3 HTTP | 0.17s | 30,237 | 6,171 | **79.6%** |
| **Ardalis CleanArchitecture** | FastEndpoints / Domain Events | 23 | 9 Ent + 9 SQL | 29 Domain + 5 HTTP | 0.35s | 96,561 | 17,448 | **81.9%** |
| **Microsoft eShop** | Aspire / Microservices / gRPC | 46 | 48 Ent + 8 SQL | 7 Domain + 10 HTTP | 0.58s | 232,290 | 23,708 | **89.8%** |
| **Kamil Grzybek Modular Monolith** | Modular Monolith / DDD / CQRS | 72 | 97 Ent + 6 SQL | 5 Domain | 1.05s | 350,601 | 62,928 | **82.1%** |
| **Jason Taylor Northwind Traders** | N-Tier / Controller Inheritance | 26 | 15 Ent + 1 SQL | 4 Domain | 0.41s | 462,328 | 9,261 | **98.0%** |
| **Eduardo Pires Equinox** | DDD / Event Sourcing | 23 | 8 Ent + 1 SQL | 1 Domain + 7 HTTP | 0.15s | 41,292 | 7,610 | **81.6%** |
| **SimplCommerce** | E-Commerce (44 Modules) | 344 | 99 Ent + 9 SQL | 140 HTTP Guards | 1.29s | 560,438 | 115,842 | **79.3%** |
| **Pentatomic Billing System** | Subscription Billing / Invoices | 6 | 3 Ent + 0 SQL | 43 Calculations | 0.14s | 52,976 | 7,835 | **85.2%** |
| **Tayara Accounting & WMS** | Double-Entry Bookkeeping | 96 | 83 Ent + 4 SQL | 5 Domain | 0.45s | 278,774 | 26,835 | **90.4%** |
| **OVERALL TOTALS / AVERAGE** | **13 Enterprise Solutions** | **714** | **385 Ent + 48 SQL** | **84 Domain + 165 HTTP** | **0.39s avg** | **2,288,258** | **304,120** | **86.7%** |

*Note: When querying single modules or bounded contexts, token reduction exceeds **96%**.*

---

## Installation & Setup

Ottonet operates in two modes:
1. **Global Workstation Sidecar (Recommended):** Installed once in your user directory, accessible from any .NET solution on your machine.
2. **Embedded Repository Sidecar:** Bundled directly into a specific project or team repository via Git submodule.

### Prerequisites
- **Python 3.9+** (Standard library only; zero pip dependencies)
- *(Optional)* **.NET 8.0+ SDK** (Enables 100% official Microsoft Roslyn compiler AST mode; falls back to Python lexer if absent)

---

### Method A: Global Workstation Setup (Recommended)

1. Clone Ottonet into a permanent location on your workstation:
```bash
git clone https://github.com/quocbahuynh/OttoNet-Skills.git ~/.ottonet
```

2. Add the `ottonet` CLI alias to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
echo 'alias ottonet="python3 ~/.ottonet/ottonet.py"' >> ~/.zshrc
source ~/.zshrc
```

3. *(Optional)* Build the native Roslyn AST tool for maximum parsing speed:
```bash
dotnet build ~/.ottonet/tools/Ottonet.Roslyn/Ottonet.Roslyn.csproj -c Release
```

Now you can run `ottonet` inside **any** ASP.NET repository:
```bash
cd /path/to/any-dotnet-project
ottonet scan
ottonet inspect Order
ottonet inspect "/api/orders"
```

---

### Method B: Embedding in a Target .NET Solution

To equip an existing ASP.NET team repository with Ottonet:

1. Add Ottonet as a Git submodule inside your solution:
```bash
cd /path/to/your-solution
git submodule add https://github.com/quocbahuynh/OttoNet-Skills.git .ottonet
```

2. Generate native instructions for all AI coding agents used by your team:
```bash
python3 .ottonet/skills/ottonet-skill/scripts/install_adapters.py .
```
This automatically writes configuration files (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.windsurfrules`, `.clinerules`, `CODEX.md`, `OPENCODE.md`) to your repository root.

---

## Agent-Specific Integration Guide

Ottonet provides tailored integration adapters so your AI coding assistant invokes Ottonet autonomously in the background:

### 1. Google Antigravity
Ottonet is built natively as an Antigravity Skill.
- **Global Skill (Available across all Antigravity conversations):**
  ```bash
  mkdir -p ~/.gemini/antigravity/skills
  ln -s ~/.ottonet/skills/ottonet-skill ~/.gemini/antigravity/skills/ottonet-skill
  ```
- **Workspace Skill (Restricted to a single project):**
  Copy `skills/ottonet-skill` into your workspace at `<project_root>/.gemini/antigravity/skills/ottonet-skill`.
  *Antigravity automatically detects the skill and activates Principal .NET Architect instincts on all ASP.NET solutions.*

### 2. Cursor
In your project root, run:
```bash
python3 ~/.ottonet/skills/ottonet-skill/scripts/install_adapters.py . --agents cursor
```
This creates `.cursorrules`. Cursor will automatically reference architectural master keys, invoke `ottonet inspect`, and use targeted method zoom-in without manual prompts.

### 3. Claude Code (CLI)
In your project root, run:
```bash
python3 ~/.ottonet/skills/ottonet-skill/scripts/install_adapters.py . --agents claude
```
This writes `CLAUDE.md` to your project root. Claude Code respects the architectural constraints, examines Scrutor wiring, and queries modular catalogs automatically.

### 4. GitHub Copilot
In your project root, run:
```bash
python3 ~/.ottonet/skills/ottonet-skill/scripts/install_adapters.py . --agents copilot
```
This generates `.github/copilot-instructions.md`, enforcing team patterns, soft-delete invariants, and controller inheritance across Copilot Chat and inline edits.

### 5. Windsurf, Cline / Roo Code, OpenCode, Codex
Run the installer with your agent of choice:
```bash
# Windsurf
python3 ~/.ottonet/skills/ottonet-skill/scripts/install_adapters.py . --agents windsurf

# Cline / Roo Code
python3 ~/.ottonet/skills/ottonet-skill/scripts/install_adapters.py . --agents cline

# OpenCode
python3 ~/.ottonet/skills/ottonet-skill/scripts/install_adapters.py . --agents opencode

# OpenAI Codex / ChatGPT
python3 ~/.ottonet/skills/ottonet-skill/scripts/install_adapters.py . --agents codex
```

---

## Autonomous Operation (How AI Agents Use Ottonet)

Once installed, **you do not need to run commands manually.** Your AI assistant operates Ottonet autonomously:

1. **On Solution Discovery:** The agent silently runs `ottonet scan` to determine the 4 Master Keys (`Bootstrap`, `API`, `Domain`, `Persistence`) and map cross-cutting invariants.
2. **On Feature & Route Investigation:** When you ask about a feature, the agent queries `ottonet inspect "/api/target"` or reads `.codebase-intel/entrypoints/modules/<Mod>.md` instead of dumping hundreds of irrelevant routes.
3. **On Method Refactoring:** The agent runs `ottonet inspect <file> --method <name>` to load the exact method body while keeping surrounding methods skeletonized—preventing token bloat, hallucinations, and context loss.

---

## CLI Reference

### Universal Inspection
```bash
# Inspect a specific file with Roslyn AST skeletonization
python ottonet.py inspect src/Services/OrderService.cs

# Zoom into a specific method with 100% full body fidelity
python ottonet.py inspect src/Services/OrderService.cs --method ProcessOrderAsync

# Inspect a route path or verb
python ottonet.py inspect "/api/orders"
python ottonet.py inspect "POST /api/orders"

# Inspect an entity or raw SQL table
python ottonet.py inspect Order
python ottonet.py inspect Invoices

# Inspect a module or bounded context
python ottonet.py inspect Orders
```

### Targeted Commands
```bash
# Full architectural scan (Entrypoints, Schemas, DI Wiring, Invariants)
python ottonet.py scan [path_to_solution]

# Route catalog with instant keyword and method filtering
python ottonet.py routes --search "checkout" --method POST

# Entity relationship extraction & Mermaid ERD generation
python ottonet.py schema [EntityName] [path_to_solution]

# Extract business algorithms, formulas, and procedural guards
python ottonet.py rules <ModuleName> [path_to_solution]

# Trace runtime DI wiring and Scrutor decorators
python ottonet.py wiring [path_to_solution]

# Switch task and bounded context card
python ottonet.py switch --task 102 --domain billing [path_to_solution]
```

---

## Multi-Agent Compatibility

Ottonet provides first-class instruction sets and integration rules for all major AI coding agents:

| AI Coding Agent | Configuration File | Integration Mode |
| :--- | :--- | :--- |
| **Google Antigravity** | `skills/ottonet-skill/SKILL.md` | Native Skill |
| **Cursor** | `.cursorrules` | System Rule |
| **Claude Code** | `CLAUDE.md` | Workspace Context |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Workspace Instructions |
| **Windsurf** | `.windsurfrules` | Memory Rule |
| **Cline / Roo Code** | `.clinerules` | Workflow Profile |
| **OpenCode** | `OPENCODE.md` / `.opencoderules` | Agent Configuration |
| **OpenAI Codex / ChatGPT** | `CODEX.md` / `.codexrules` | Repository Prompt |

---

## Repository Structure

```
.
├── ottonet.py                         # Single-entrypoint universal CLI
├── skills/
│   └── ottonet-skill/
│       ├── SKILL.md                   # Antigravity skill specification
│       └── scripts/
│           ├── catalog_entrypoints.py  # Route resolver & modular cataloger
│           ├── csharp_skeleton.py      # Roslyn AST & Python brace lexer zoom-in
│           ├── detect_architecture.py  # TargetFramework & MSBuild analyzer
│           ├── detect_conventions.py   # Code style & naming convention detector
│           ├── distill_entity_schema.py# Entity & Dapper SQL table extractor
│           ├── domain_manager.py       # Task & context card switcher
│           ├── extract_business_rules.py# Invariant, formula, & guard miner
│           ├── install_adapters.py     # Multi-agent adapter generator
│           ├── intel_init.py           # Safe workspace initializer
│           ├── resolve_master_keys.py  # 4 Master Keys discriminator
│           ├── scan_invariants.py      # Cross-cutting invariant detector
│           └── trace_di_decorators.py  # Scrutor & runtime DI tracer
├── tools/
│   └── Ottonet.Roslyn/                # High-speed native C# Roslyn analyzer
│       ├── Ottonet.Roslyn.csproj
│       └── Program.cs
└── tests/
    ├── run_tests.py                   # 5-suite comprehensive verification test
    ├── benchmark_all_repos.py         # Automated real-world benchmark runner
    └── fixtures/                      # Mock legacy, clean arch, & FastEndpoints
```

---

## Zero Git Pollution Guarantee

Ottonet never pollutes your repository history:
- All generated intelligence maps and caches are isolated strictly inside `.codebase-intel/`.
- Every `.codebase-intel/` directory is automatically configured with a self-contained `.gitignore` and registered in Git exclusions.
- Clean working trees remain 100% untouched.

---

## License

This project is licensed under the [MIT License](LICENSE).
