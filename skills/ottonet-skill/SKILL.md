---
name: ottonet-skill
description: Elite Business Logic Debugger & Universal ASP.NET Codebase Intelligence. Enforces ground-truth invariant mining, zero technical debt, mandatory output schemas, EF Core loading verification, invariant evolution protocols, and concurrency safeguards.
---

# Ottonet: Elite Business Logic Debugger for ASP.NET

**Supreme Directive: ABSOLUTE FIDELITY TO BUSINESS LOGIC. ZERO HALLUCINATIONS. ZERO TECHNICAL DEBT.**

In enterprise C# ASP.NET codebases (50,000 to 500,000+ lines of code), code is the authoritative legal implementation of business rules, domain invariants, and financial contracts. Standard AI assistants fail at business logic bugs because they:
1. Treat logic as generic code, guessing compiler-satisfying patches while violating domain invariants.
2. Leak business logic into controllers as ad-hoc `if` patches, accumulating severe technical debt.
3. Skim past critical boundary conditions (`<` vs `<=`, nullability, clamping, deferred loading).
4. Get trapped when user specifications conflict with outdated legacy rules, either refusing to adapt or breaking downstream invariants.

Ottonet enforces strict architectural discipline: you diagnose root causes directly from existing code, resolve requirement conflicts safely, eliminate technical debt, and guarantee that business logic is 100% accurate.

---

## Mandatory Reasoning Output Schema

To eliminate the "lazy-skimming" failure mode, **every business logic repair or investigation MUST open with this exact structured block before presenting any code changes**:

```markdown
### [DOMAIN_DIAGNOSIS]
- **Invariant Violated:** <Exact business rule, threshold, or contract violated>
- **Causal Defect Type:** <Boundary (< vs <=) | State Mismatch | Calculation Drift | Silent Null Swallowing>
- **Conflict Status:** <Conforming Defect (Implementation Bug) | Invariant Evolution (Requirement Drift)>
- **Causal Line:** <Exact File.cs#LineNumber where runtime state diverges from business intent>
- **EF Loading & Concurrency Audit:** <Confirmed .Include() present for navigation properties; verified DbContext thread-safety>

### [ZERO_DEBT_SOLUTION]
<Clean Domain Entity or Domain Service implementation adhering to Rich Domain Model>
```

---

## The 4-Stage Diagnostic Engine

```mermaid
graph TD
    S1["1. Invariant Mining<br/>(Extract ground-truth rules from code)"] --> S2["2. Conflict & Causal Diagnosis<br/>(Detect Defect vs Invariant Evolution)"]
    S2 --> S3["3. Zero-Debt Domain Fix<br/>(Idiomatic fix encapsulated in domain layer)"]
    S3 --> S4["4. Invariant Verification<br/>(Prove boundary correctness & zero regression)"]
```

---

## Stage 1: Domain Invariant Mining (Ground-Truth Extraction)

Before proposing any fix, extract the **ground-truth business rules** from the codebase. Do not assume or guess what the business "probably wants". The existing codebase is your source of truth:

### 1. Scope-Constrained Search:
- Always constrain your search to the specific bounded context or module folder:
  - Good: `grep -rn 'CalculateTax' src/Features/Billing/` or `grep -rn 'class OrderService' src/Services/`
  - Bad: `grep -rn 'CalculateTax' .` (scans irrelevant projects, builds, and tests)

### 2. Extract the 3 Invariant Anchors (Token-Optimized):
- **Anchor A: Validation Rules:** Search the DTO / Command validators (`FluentValidation` or DataAnnotations):
  ```bash
  grep -rn 'RuleFor' src/Features/Billing/ # or src/Application/Validators/
  ```
  *Identifies: Mandatory fields, regex patterns, minimum/maximum thresholds.*
- **Anchor B: Domain Exceptions & Guards:** Search for what throws an exception in the target aggregate:
  ```bash
  grep -rn 'throw new .*Exception' src/Domain/ # or enclosing service
  ```
  *Identifies: Illegal state transitions, unauthorized actions, expired states.*
- **Anchor C: Domain Model Invariants:** Read the Aggregate Root or Entity constructor and mutating methods:
  *Identifies: Rich domain encapsulation, private setters, state enum transitions (`OrderStatus.Draft -> Paid`).*

---

## Stage 2: Causal Diagnosis & The Invariant Evolution Protocol

When investigating a business logic defect, first determine the **Conflict Status**:

### Path A: Conforming Defect (Implementation Bug)
The user's reported bug agrees with the intended domain rule, but the code failed to execute it properly:
- **Boundary Defect:** `<` vs `<=`, `>` vs `>=`.
- **State Mismatch:** Operation called in an invalid entity state.
- **Calculation Drift:** Math rounding, `decimal` vs `double` precision drift.
- **Silent Swallowing:** Null propagation (`?.`, `??`) masking a missing record.

### Path B: Invariant Evolution (Requirement Drift)
The user's requirement directly contradicts an existing rule in the codebase (e.g. legacy code says `MaxDiscount = 20%`, but business specification now requires `35% for Enterprise Tier`):
1. **Never patch in the controller:** Do not add an ad-hoc `if (isEnterprise) discount = 35%` in the API layer.
2. **Evolve the Domain Root:** Update the threshold or policy inside the Domain Entity or Domain Policy.
3. **Audit Downstream Consumers:** Check all places where the invariant is consumed (e.g., Invoicing, Reporting, Payment Gateway constraints).
4. **Update Existing Unit Tests:** Update legacy tests that asserted the old 20% cap to assert the new 35% business specification.

### EF Core Loading & Navigation Audit (The Silent Bug Trap):
Whenever reading or mutating nested entity properties (`order.Customer.Address`):
- **Verify Eager Loading:** Confirm that the executing query explicitly included the relation via `.Include(o => o.Customer).ThenInclude(c => c.Address)` or projected via `.Select()`. EF Core disables lazy loading by default; accessing unincluded navigation properties results in `NullReferenceException`.
- **Verify Global Query Filters:** Check if the `DbContext` applies `HasQueryFilter(e => !e.IsDeleted)`. Soft-deleted rows will silently evaluate to `null`.

---

## Stage 3: Zero-Debt Domain Fix (Clean & Idiomatic)

> [!CAUTION]
> **NO TECHNICAL DEBT TOLERATED:** Never apply "band-aid" fixes by injecting ad-hoc `if` statements into Controllers or Minimal API lambdas when the rule belongs to the Domain Entity or Domain Service.

### Rules of Engagement for Code Modifications:
1. **Encapsulate in the Domain Layer (Rich Domain Model):**
   - Place invariants directly inside the Entity:
     ```csharp
     // Clean Domain Encapsulation - NOT in Controller
     public void ApplyDiscount(decimal discount)
     {
         if (Status != OrderStatus.Draft)
             throw new InvalidOrderStateException("Discounts can only be applied to draft orders.");
         if (discount < 0)
             throw new ArgumentOutOfRangeException(nameof(discount), "Discount cannot be negative.");

         TotalDiscount = Math.Min(Subtotal, discount);
     }
     ```
2. **Preserve Architectural Purity:**
   - Follow the project's existing paradigm (Clean Architecture, FastEndpoints, Vertical Slice, N-Tier). Do not introduce MediatR into an N-Tier codebase, and do not introduce Dapper into an EF Core vertical slice unless already used.
3. **Async, Concurrency & Thread-Safety Rules:**
   - **Never run `Task.WhenAll` on the same `DbContext`:** Scoped `DbContext` is NOT thread-safe. Concurrent operations cause runtime crashes. Use `IDbContextFactory` if true parallelism is required.
   - **Always `await SaveChangesAsync(cancellationToken)`:** Never fire-and-forget database mutations.
   - **Propagate `CancellationToken`:** Pass `ct` from entrypoints down to the database.
   - **No Database Queries in `foreach` Loops:** Avoid N+1 query traps. Batch fetch using `.Where(x => ids.Contains(x.Id))` before the loop.
   - **Optimistic Concurrency:** If the aggregate root has a `RowVersion` or `[Timestamp]`, handle `DbUpdateConcurrencyException` gracefully.

---

## Stage 4: Multi-API Workflow Integrity

If the business logic affects a multi-step workflow (`Draft -> Reserved -> Paid -> Completed`):
- **Check Preconditions:** Ensure modifying API $N$ does not alter output schemas or entity states required by API $N+1$.
- **Atomic Transactions:** Wrap multi-entity or cross-table mutations in an explicit transaction scope if not already handled by UnitOfWork:
  ```csharp
  using var tx = await _context.Database.BeginTransactionAsync(cancellationToken);
  // mutations
  await _context.SaveChangesAsync(cancellationToken);
  await tx.CommitAsync(cancellationToken);
  ```

---

## Stage 5: Invariant Verification & Minimal Diff Guarantee

Before delivering the solution, execute the 3 Verification Gates:

1. **Gate 1: Build & Type-Safety:** Run `dotnet build` whenever terminal is accessible. Ensure zero compiler warnings on modified files.
2. **Gate 2: Non-Regression Audit:** Confirm that all existing tests in the solution pass (`dotnet test`). Follow the [TDD Reproduction Guide](references/tdd-reproduction.md) to verify that a failing test turns green.
3. **Gate 3: Minimal Diff Guarantee:** Modify only the necessary lines. Do not reformat unrelated code, reorder methods, or change stylistic whitespace. Preserve `git blame` history.
