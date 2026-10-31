# Ottonet

**Elite Business Logic Debugger & Universal ASP.NET Codebase Intelligence**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-4.5%20to%2010.0-512BD4)](https://dotnet.microsoft.com/)
[![Zero-Debt](https://img.shields.io/badge/Architecture-Zero%20Technical%20Debt-success)](skills/ottonet-skill/SKILL.md)
[![Accuracy](https://img.shields.io/badge/Fidelity-100%25%20Business%20Logic-orange)](skills/ottonet-skill/SKILL.md)
[![Multi-Agent](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Cursor%20%7C%20Claude%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline-success)](#installation)

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*'
```

---

## The Supreme Directive

> **Absolute fidelity to business logic. Zero hallucinations. Zero technical debt.**

In enterprise C# ASP.NET systems (50,000 to 500,000+ lines of code), standard AI assistants fail because they treat business logic as generic code. They apply superficial patches that satisfy the compiler but violate legal contracts, state machine transitions, and financial calculations.

**Ottonet** turns your AI assistant into an **Elite Principal Software Architect & Domain Debugger**:
- **Code is the Ground-Truth:** Invariants, validation thresholds, and domain rules are mined directly from code (FluentValidation, Aggregate Root guards, Domain Exceptions) instead of guessed.
- **Zero Technical Debt:** Business rules are encapsulated where they belong (in rich Domain Entities or Domain Services)—never leaked into controllers as dirty ad-hoc `if` patches.
- **Token-Optimized Precision:** Extracts maximal domain signal while eliminating context bloat, preventing reading-skimming and hallucinations.
- **Universal ASP.NET Support:** Operates seamlessly across N-Tier, FastEndpoints, Minimal APIs, Carter, Vertical Slices, Dapper, Modular Monoliths, and Legacy MVC.

---

## The 4-Stage Diagnostic Engine

1. **Domain Invariant Mining:** Extract ground-truth rules from validation rules, domain exceptions, and entity guards before proposing any changes.
2. **Causal Root-Cause Diagnosis:** Classify defects into Boundary Errors (`<` vs `<=`), State Mismatches, Calculation Drifts (e.g. `decimal` vs `double` banker's rounding), or Silent Null Swallowing (`?.` / `??`).
3. **Zero-Debt Domain Fix:** Encapsulate business logic cleanly within the domain layer; adhere strictly to repository conventions; guarantee async and EF Core thread-safety.
4. **Invariant Verification:** Multi-gate verification ensuring build passes, downstream multi-API workflows remain uncorrupted, and git blame is preserved via minimal diffs.

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
