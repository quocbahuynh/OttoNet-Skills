---
name: ottonet-skill
description: Elite Business Logic Debugger for ASP.NET. Enforces 100% domain fidelity, zero technical debt, mandatory diagnosis schemas, EF Core loading, domain events, tenant isolation, and concurrency safeguards.
---

# Ottonet: Elite ASP.NET Business Logic Debugger

**Core Directive: Absolute business logic fidelity. Zero hallucinations. Zero technical debt.**

## 1. Mandatory Output Schema
Every business logic repair MUST open with this exact block before presenting any code changes:
```markdown
### [DOMAIN_DIAGNOSIS]
- **Invariant Violated:** <Rule/threshold violated>
- **Causal Defect Type:** <Boundary (< vs <=) | State Mismatch | Calculation Drift | Silent Null Swallowing>
- **Conflict Status:** <Conforming Defect (Bug) | Invariant Evolution (Requirement Drift)>
- **Causal Line:** <File.cs#Line>
- **EF Loading & Concurrency Audit:** <Verify .Include() for relations; verify DbContext thread-safety>

### [ZERO_DEBT_SOLUTION]
<Idiomatic Domain Entity / Service fix>
```

## 2. Invariant Mining & Scope-Constrained Search
1. **Scoped Grep:** Always search within module folders (`src/Features/X/` or `src/Services/`), never root `.`.
2. **Mine Ground-Truth (Code is Truth):**
   - Validation rules: `grep -rn 'RuleFor' <module>`
   - Domain guards & exceptions: `grep -rn 'throw new .*Exception' <domain>`
   - State transitions: Check entity mutating methods & status enums (`OrderStatus.Draft -> Paid`).

## 3. Invariant Evolution vs Conforming Defect
- **Conforming Defect:** Fix implementation bug (boundary `<` vs `<=`, math precision, null check).
- **Invariant Evolution (Requirement Drift):** If user intent contradicts legacy code, update rule at its domain root (Entity/Policy). Never patch in controllers. Audit downstream callers; update unit tests.

## 4. EF Core, Concurrency & Enterprise Invariants
- **Navigation Loading:** If accessing nested relations (`order.Customer.Address`), ensure `.Include().ThenInclude()` or `.Select()` projection exists. Never rely on disabled lazy loading. Check `HasQueryFilter` for soft-deletes.
- **Async Thread-Safety:** Never run `Task.WhenAll` on a scoped `DbContext`. Always `await SaveChangesAsync(ct)`. Propagate `CancellationToken`.
- **No Loops in DB Queries:** Never query DB inside `foreach` (N+1). Batch fetch via `.Where(x => ids.Contains(x.Id))`.
- **Domain Events & Outbox:** On state mutations (e.g. `order.Cancel()`), verify if `AddDomainEvent(...)` or Outbox messages must be emitted for downstream services.
- **Tenant Isolation:** If entity has `TenantId` / `OrgId`, never bypass tenant filters in queries or inserts.
- **Temporal Conventions:** Adhere strictly to the project's existing time conventions (e.g. `TimeProvider`, `IDateTimeService`, or UTC standards); do NOT impose arbitrary defaults.
- **Concurrency:** Handle `DbUpdateConcurrencyException` when modifying entities with `RowVersion` / `[Timestamp]`.

## 5. Multi-API Workflow Integrity
- For multi-step APIs (`Draft -> Reserved -> Paid -> Completed`), check preconditions on the Aggregate Root. Ensure modifying API $N$ preserves preconditions for API $N+1$. Wrap multi-table updates in atomic transactions.

## 6. Verification Gates
1. **Build:** Verify syntax and types with `dotnet build`.
2. **Tests:** Follow [TDD Guide](references/tdd-reproduction.md) to isolate bug with a failing test, then verify all tests turn green (`dotnet test`).
3. **Minimal Diff:** Modify only necessary lines. Preserve git blame.

*(Deep playbooks: [universal-archetypes.md](references/universal-archetypes.md), [state-machine-tracing.md](references/state-machine-tracing.md), [symbolic-dry-run.md](references/symbolic-dry-run.md)).*
