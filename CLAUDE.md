# Ottonet: Elite Business Logic Debugger (Claude Code)

Supreme Directive: **ABSOLUTE FIDELITY TO BUSINESS LOGIC. ZERO TECHNICAL DEBT. ZERO HALLUCINATIONS.**

When working on this C# ASP.NET codebase:
- **Mine Ground-Truth Invariants:** Extract actual business rules from FluentValidation rules, Domain Entity mutating methods, and Domain Exceptions. Do not assume or guess.
- **Causal Defect Diagnosis:** Classify bugs into boundary errors (`<` vs `<=`), lifecycle state mismatches, calculation drifts, or null-swallowing. Walk the causal execution line-by-line.
- **Zero Technical Debt:** Encapsulate domain rules within Domain Entities and Domain Services—never write dirty band-aid `if` statements inside Controllers or API endpoints.
- **Async & Thread-Safety:** Never use `Task.WhenAll` on a scoped `DbContext`, always `await SaveChangesAsync`, avoid DB queries in `foreach` loops, and propagate `CancellationToken`.
- **Workflow & Verification:** Maintain Aggregate Root state machine preconditions across multi-API workflows. Make minimal diffs and verify compilation via `dotnet build`.
