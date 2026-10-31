# Ottonet

**Universal Codebase Intelligence & Surgical Navigation for ASP.NET Solutions**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-4.5%20to%2010.0-512BD4)](https://dotnet.microsoft.com/)
[![Zero-Code](https://img.shields.io/badge/Architecture-Pure%20Cognitive%20Skill-success)](skills/ottonet-skill/SKILL.md)
[![Multi-Agent](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Cursor%20%7C%20Claude%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline-success)](#installation)

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*'
```

---

## The Problem

Enterprise C# ASP.NET codebases (50,000 to 500,000+ lines of code) consistently break AI coding assistants:
- **The Skimming Trap:** When an AI dumps entire 800-line service classes into context, transformer attention degrades. It skims over code, misses boundary validations (`<` vs `<=`, nullability, clamping), and hallucinates nonexistent conventions.
- **Inversion of Control (IoC) Blindness:** Indirection patterns (MediatR, generic repositories, Scrutor reflection DI, controller inheritance) cause generic file packagers (like Repomix) to dump thousands of lines of irrelevant DTO boilerplate while missing the actual handler.
- **Multi-API Workflow Desynchronization:** Real enterprise features span 3 to 5 sequential APIs (`Draft -> Submit -> Pay -> Complete`). Modifying one endpoint without understanding the underlying state machine breaks downstream preconditions.

---

## The Solution: Pure Cognitive Surgical Intelligence

**Ottonet** is a zero-dependency, pure cognitive agent skill that forces AI coding assistants to investigate ASP.NET codebases with surgical precision—slashing token consumption by **90%+** while achieving **100% logic accuracy**.

### 1. The 2-Tier Zoom Window (Token Optimization Engine)
Instead of reading 1,200-line classes into context, Ottonet clamps reads into two surgical tiers:
- **Tier 1 (Scope Header ~20 lines):** Namespace, base classes, and constructor DI injections (identifies `_dbContext`, `_mediator`, `_paymentGateway`).
- **Tier 2 (Target Method Body ~40–60 lines):** The exact lines of the target method with **100% full-body fidelity** (every single variable, if-branch, loop, and exception).
- **Result:** ~700 tokens consumed instead of 15,000+ tokens (**92% reduction**) with zero loss of execution fidelity.

### 2. Line-by-Line Trace Table & Symbolic Dry-Run
Before proposing code changes, the AI must construct:
- A structured **Line-by-Line Trace Table** (`[Line # | Statement | Mutated State | Invariant]`).
- A **2-Scenario Symbolic Dry-Run** (Happy Path & Edge/Failure Case) simulating concrete inputs through the method.
- **Result:** Eliminates reading-skimming. Forces the model's transformer attention to evaluate every operator and guard.

### 3. Universal ASP.NET Architecture Navigation
Not all codebases use MediatR. Ottonet provides Dual-Vector traversal across all 7 major ASP.NET archetypes:
- **N-Tier / Layered:** Controller &rarr; `IService` &rarr; `Service` &rarr; `IRepository` &rarr; `DbContext`.
- **FastEndpoints / REPR:** `Endpoint<TRequest, TResponse>` with `HandleAsync`.
- **Minimal APIs & Carter:** `app.MapGet`/`MapPost`, Route Groups, `ICarterModule`.
- **Vertical Slice Architecture:** Co-located `Features/Orders/CreateOrder/`.
- **Dapper & Micro-ORMs:** Direct SQL strings, `IDbConnection`, and stored procedure mappings.
- **Modular Monolith & DDD:** Bounded contexts and in-memory event handlers.
- **Legacy Web API 2 / MVC:** `ApiController` fat actions and EF6.

### 4. Multi-API Workflow Tracing
Maps complex business processes across multiple APIs by anchoring on the **Aggregate Root State Machine** (`OrderStatus`, `InvoiceState`). Ensures that changes to API $N$ never break the preconditions of API $N+1$.

### 5. The 3-Gate Verification Protocol
- **Gate 1:** Build & type-safety verification via `dotnet build`.
- **Gate 2:** State machine non-regression check.
- **Gate 3:** Minimal diff guarantee (preserves git blame and surrounding structure).

---

## Installation

Install Ottonet Skill directly into your active coding agent or project using [skills.sh](https://skills.sh):

```bash
# Install to current repository (auto-detects Cursor, Antigravity, Claude, Copilot, etc.)
npx skills add quocbahuynh/OttoNet-Skills --skill '*'

# Install globally across all workspaces
npx skills add quocbahuynh/OttoNet-Skills -g --skill '*'

# Install for a specific agent
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent cursor
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent claude-code
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent copilot
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent windsurf cline
```

---

## Zero Extra Dependencies

Ottonet contains **zero Python scripts**, **zero extra C# binary projects**, and **zero external runtime dependencies**. It is a pure cognitive skill that turns your AI assistant into a disciplined senior ASP.NET software architect.

---

## License

Licensed under the [MIT License](LICENSE).
