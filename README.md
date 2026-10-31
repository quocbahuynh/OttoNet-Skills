# Ottonet

**Universal ASP.NET Codebase Intelligence — Engineered for 100% Accuracy & Blazing-Fast Navigation**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-4.5%20to%2010.0-512BD4)](https://dotnet.microsoft.com/)
[![Focus](https://img.shields.io/badge/Focus-100%25%20Accuracy%20%26%20Speed-orange)](skills/ottonet-skill/SKILL.md)
[![Multi-Agent](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Cursor%20%7C%20Claude%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline-success)](#installation)

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*'
```

---

## Philosophy: 100% Accuracy & Maximum Inference Speed

In large C# ASP.NET codebases (50,000 to 500,000+ lines of code), the primary failure mode of AI is **reading-skimming**, guessing Inversion of Control (IoC/DI/MediatR) wiring, and wasting tool round-trips.

**Ottonet** strips out all procedural overhead and enforces:
1. **1-Step Pinpoint Traversal:** Resolve from Route or Symbol directly to implementation in a single search step.
2. **Zero-Skimming Rigor:** Read complete target method context in one tool call, auditing boundary operators (`<` vs `<=`), nullability, enum exhaustiveness, and EF Core change tracker status.
3. **Multi-API State Machine Tracing:** Anchor complex workflows to Aggregate Root status transitions (`Draft -> Reserved -> Paid -> Completed`), ensuring changes in one API never break downstream preconditions.

---

## Universal Architecture Support

Ottonet works across all 7 major ASP.NET architectural archetypes:
- **N-Tier / Layered:** Controller &rarr; `IService` &rarr; `Service` &rarr; `IRepository` &rarr; `DbContext`.
- **FastEndpoints / REPR:** `Endpoint<TRequest, TResponse>` with `HandleAsync`.
- **Minimal APIs & Carter:** `app.MapGet`/`MapPost`, Route Groups, `ICarterModule`.
- **Vertical Slice Architecture:** Co-located `Features/Orders/CreateOrder/`.
- **Dapper & Micro-ORMs:** Direct SQL strings, `IDbConnection`, and stored procedure mappings.
- **Modular Monolith & DDD:** Bounded contexts and in-memory event handlers.
- **Legacy Web API 2 / MVC:** `ApiController` actions and EF6.

---

## Installation

Install directly into your AI coding assistant or workspace via [skills.sh](https://skills.sh):

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

## Zero Dependencies

No Python scripts, no secondary C# projects, and no binary clutter in your repository. Ottonet functions as a pure cognitive mental model and execution protocol for AI agents.

---

## License

Licensed under the [MIT License](LICENSE).
