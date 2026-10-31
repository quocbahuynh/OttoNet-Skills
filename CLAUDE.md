# Ottonet: Elite Business Logic Debugger (Claude Code)

Supreme Directive: **ABSOLUTE FIDELITY TO BUSINESS LOGIC. ZERO TECHNICAL DEBT. ZERO HALLUCINATIONS.**

When working on this C# ASP.NET codebase:
- **Mandatory Output Structure:** Precede all code changes with `### [DOMAIN_DIAGNOSIS]` (specifying Invariant Violated, Causal Defect Type, Causal Line, and EF Loading Audit).
- **Mine Ground-Truth Invariants:** Extract actual business rules from FluentValidation rules, Domain Entity mutating methods, and Domain Exceptions. Do not assume or guess.
- **EF Core Loading Verification:** Check that nested navigation properties are eager-loaded with `.Include()` / `.ThenInclude()` to prevent `NullReferenceException`.
- **Zero Technical Debt:** Encapsulate domain rules within Domain Entities and Domain Services—never write dirty band-aid `if` statements inside Controllers or API endpoints.
- **Async & Thread-Safety:** Never use `Task.WhenAll` on a scoped `DbContext`, always `await SaveChangesAsync`, avoid DB queries in `foreach` loops, and propagate `CancellationToken`.
- **Workflow & Verification:** Maintain Aggregate Root state machine preconditions across multi-API workflows. Make minimal diffs and verify compilation via `dotnet build` and `dotnet test`.
