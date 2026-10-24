# Ottonet

**Universal Codebase Intelligence & Navigation for ASP.NET Solutions**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-4.5%20to%2010.0-512BD4)](https://dotnet.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)](https://www.python.org/)
[![Multi-Agent](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Cursor%20%7C%20Claude%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20OpenCode%20%7C%20Codex-success)](#installation)

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*'
```

---

## Overview

Enterprise .NET codebases (200,000 to 500,000+ lines of code) consistently overwhelm AI coding assistants with massive context windows, invisible runtime wiring (Scrutor decorators, reflection DI), and complex controller hierarchies.

**Ottonet** is a zero-dependency intelligence sidecar that analyzes ASP.NET solutions in sub-second timeframes. It distills 2M+ token solutions into dense, structured architectural maps under 3,500 tokens—slashing token consumption by **86% to 96%** while eliminating hallucinated architectures.

---

## 5 Core Architect Weapons

- **Universal Investigator (`ottonet inspect <target>`):** One unified command to inspect files, routes, entities, Dapper tables, or business modules with automatic target resolution.
- **Hybrid Roslyn AST & Targeted Method Zoom-In:** Compiler-level syntax tree precision via native Roslyn (`Microsoft.CodeAnalysis.CSharp`) with zero-dependency Python lexer fallback. Preserves 100% full-body fidelity for target methods while skeletonizing surrounding code with side-effect annotations (`Mutates`, `Calls`, `Throws`).
- **Modular Route Partitions & Search:** Automatically groups monolith route catalogs into bounded contexts (`.codebase-intel/entrypoints/modules/<Mod>.md`) with sub-50ms CLI filtering (`--search`, `--method`).
- **Entity & Raw SQL / Dapper Distiller:** Reverse-engineers EF Core classes, `sealed class`, `record`, and embedded raw SQL/Dapper `JOIN ON` tables into Mermaid ER diagrams.
- **Semantic Invariant Miner:** Captures domain exceptions, mathematical formulas, state machine lifecycles, and procedural HTTP response guards (`BadRequest`, `NotFound`, `Conflict`).

---

## Benchmarks

Benchmarked across **13 real-world open-source enterprise ASP.NET repositories** (over 2.28 million tokens of raw C# code):

| Repository | Domain & Architecture | Routes | Schemas | Business Guards | Scan Time | Raw Tokens | Intel Tokens | Reduction |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Jason Taylor CleanArchitecture** | Minimal APIs / Vertical Slice | 16 | 8 Ent + 3 SQL | 16 Domain + 3 HTTP | 0.17s | 30,237 | 6,171 | **79.6%** |
| **Ardalis CleanArchitecture** | FastEndpoints / Domain Events | 23 | 9 Ent + 9 SQL | 29 Domain + 5 HTTP | 0.35s | 96,561 | 17,448 | **81.9%** |
| **Microsoft eShop** | Aspire / Microservices / gRPC | 46 | 48 Ent + 8 SQL | 7 Domain + 10 HTTP | 0.58s | 232,290 | 23,708 | **89.8%** |
| **Kamil Grzybek Modular Monolith** | Modular Monolith / DDD / CQRS | 72 | 97 Ent + 6 SQL | 5 Domain | 1.05s | 350,601 | 62,928 | **82.1%** |
| **Amichai Mantinband Clean Arch** | C# 12 Primary Ctors + ErrorOr | 13 | 3 Ent + 0 SQL | 2 Domain | 0.19s | 42,962 | 7,996 | **81.4%** |
| **Conduit RealWorld Spec App** | Feature Folders / Vertical Slices | 19 | 7 Ent + 3 SQL | 15 Domain | 0.12s | 61,884 | 7,681 | **87.6%** |
| **Jason Taylor Northwind Traders** | N-Tier / Controller Inheritance | 26 | 15 Ent + 1 SQL | 4 Domain | 0.41s | 462,328 | 9,261 | **98.0%** |
| **Ivan Paulovich Clean Arch Manga** | Hexagonal Banking + API Versioning | 23 | 5 Ent + 3 SQL | 0 Domain | 0.22s | 75,611 | 8,834 | **88.3%** |
| **NikiforovAll Minimal API** | Carter Modules + Minimal APIs | 7 | 0 Ent + 1 SQL | 0 Domain | 0.03s | 2,304 | 1,971 | **14.5%** |
| **Eduardo Pires Equinox** | DDD / Event Sourcing | 23 | 8 Ent + 1 SQL | 1 Domain + 7 HTTP | 0.15s | 41,292 | 7,610 | **81.6%** |
| **SimplCommerce** | E-Commerce (44 Modules) | 344 | 99 Ent + 9 SQL | 140 HTTP Guards | 1.29s | 560,438 | 115,842 | **79.3%** |
| **Pentatomic Billing System** | Subscription Billing / Invoices | 6 | 3 Ent + 0 SQL | 43 Calculations | 0.14s | 52,976 | 7,835 | **85.2%** |
| **Tayara Accounting & WMS** | Double-Entry Bookkeeping | 96 | 83 Ent + 4 SQL | 5 Domain | 0.45s | 278,774 | 26,835 | **90.4%** |
| **OVERALL TOTALS / AVERAGE** | **13 Enterprise Solutions** | **714** | **385 Ent + 48 SQL** | **84 Domain + 165 HTTP** | **0.39s avg** | **2,288,258** | **304,120** | **86.7%** |

*Note: When querying single modules or bounded contexts, token reduction exceeds **96%**.*

---

## Installation

Install Ottonet Skill directly into your active coding agent or project using [skills.sh](https://skills.sh):

```bash
# Install to current repository (auto-detects Cursor, Antigravity, Claude, Copilot, etc.)
npx skills add quocbahuynh/OttoNet-Skills --skill '*'

# Install globally (user-level across all workspaces on your workstation)
npx skills add quocbahuynh/OttoNet-Skills -g --skill '*'

# Install for specific agents (e.g. Cursor, Claude Code, GitHub Copilot, Windsurf, Cline)
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent cursor
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent claude-code
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent copilot
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent windsurf cline

# Non-interactive install for all skills & all agents without prompts
npx skills add quocbahuynh/OttoNet-Skills --all
```

---

## Zero Git Pollution Guarantee

All generated intelligence maps, manifests, and indexes are isolated strictly inside `.codebase-intel/` and ignored by Git. Your repository working tree remains 100% pristine.

---

## License

Licensed under the [MIT License](LICENSE).
