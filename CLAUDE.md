# Ottonet: Elite Business Logic Debugger (Claude Code)
Directive: Absolute business logic fidelity. Zero technical debt. Zero hallucinations.

- Output Schema: Start every fix with `### [DOMAIN_DIAGNOSIS]` (Invariant Violated, Causal Defect Type, Conflict Status, Causal Line, EF Loading Audit) followed by `### [ZERO_DEBT_SOLUTION]`.
- Scoped Search: Search within bounded modules (`src/Features/X/` or `src/Services/`), never root `.`.
- Invariant Evolution: When requirements conflict with legacy code, update rules inside Domain Entities or Policies. Never patch controllers. Update unit tests.
- EF Core & Concurrency: Check `.Include()` / `.Select()` before accessing navigation properties. Never use `Task.WhenAll` on a DbContext. Always `await SaveChangesAsync(ct)`. Avoid DB queries in loops.
- Enterprise Guards: Emit `AddDomainEvent` / Outbox records on state changes. Preserve `TenantId` / `OrgId` isolation. Use `DateTimeOffset.UtcNow` / `TimeProvider`.
- Verification: Verify compilation (`dotnet build`), run tests (`dotnet test`), maintain Aggregate Root state transitions, and keep diffs minimal.
