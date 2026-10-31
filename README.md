# Ottonet

**Elite Business Logic Debugger & Universal ASP.NET Codebase Intelligence**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-4.5%20to%2010.0-512BD4)](https://dotnet.microsoft.com/)
[![Tokens](https://img.shields.io/badge/Skill%20Footprint-~450%20Tokens-brightgreen)](skills/ottonet-skill/SKILL.md)
[![Zero-Debt](https://img.shields.io/badge/Architecture-Zero%20Technical%20Debt-success)](skills/ottonet-skill/SKILL.md)
[![Multi-Agent](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Cursor%20%7C%20Claude%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline-success)](#installation)

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*'
```

---

## The Supreme Directive

> **Absolute fidelity to business logic. Zero hallucinations. Zero technical debt. Ultra-compact token footprint (~450 tokens).**

In enterprise C# ASP.NET systems (50,000 to 500,000+ lines of code), standard AI assistants fail because they treat business logic as generic code and clutter context windows with verbose prompts.

**Ottonet** turns your AI assistant into an **Elite Principal Software Architect & Domain Debugger** while injecting only **~450 tokens** into your context window:
- **Ultra-Compact Token Footprint:** Compressed from 2,300 tokens down to ~450 tokens (-70%), saving ~1,850 tokens on every conversational turn while offloading deep guides into on-demand references.
- **Code is the Ground-Truth:** Invariants, validation thresholds, and domain rules are mined directly from code (FluentValidation, Aggregate Root guards, Domain Exceptions) instead of guessed.
- **Mandatory Output Schema:** Enforces `### [DOMAIN_DIAGNOSIS]` (Invariant Violated, Causal Defect Type, Conflict Status, EF Loading Audit) before any code is generated.
- **Invariant Evolution Protocol:** Differentiates between implementation bugs and requirement drift, cleanly evolving rules at the domain root without band-aid controller patches.
- **Universal ASP.NET Support:** Operates seamlessly across N-Tier, FastEndpoints, Minimal APIs, Carter, Vertical Slices, Dapper, Modular Monoliths, and Legacy MVC.

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

No Python scripts, no secondary C# projects, and no binary clutter in your repository. Ottonet functions as an ultra-lean, high-density cognitive skill for AI agents.

---

## License

Licensed under the [MIT License](LICENSE).
