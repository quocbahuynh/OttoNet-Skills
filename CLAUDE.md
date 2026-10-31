# Ottonet: Elite Business Logic Debugger (Claude Code)

Supreme Directive: **ABSOLUTE FIDELITY TO BUSINESS LOGIC. ZERO TECHNICAL DEBT. ZERO HALLUCINATIONS.**

When working on this C# ASP.NET codebase:
- **Mandatory Output Structure:** Precede all code changes with `### [DOMAIN_DIAGNOSIS]` (specifying Invariant Violated, Causal Defect Type, Conflict Status, Causal Line, and EF Loading Audit).
- **Invariant Evolution:** If user requirements conflict with legacy code rules, classify as `Invariant Evolution`. Update the rule at its domain root (Entity or Policy)—never apply dirty band-aid `if` statements inside Controllers. Update unit tests to reflect the new specification.
- **EF Core Loading Verification:** Check that nested navigation properties are eager-loaded with `.Include()` / `.ThenInclude()` to prevent `NullReferenceException`.
- **Zero Technical Debt:** Encapsulate domain rules within Domain Entities and Domain Services.
- **Async & Thread-Safety:** Never use `Task.WhenAll` on a scoped `DbContext`, always `await SaveChangesAsync`, avoid DB queries in `foreach` loops, and propagate `CancellationToken`.
- **Workflow & Verification:** Maintain Aggregate Root state machine preconditions across multi-API workflows. Make minimal diffs and verify compilation via `dotnet build` and `dotnet test`.
