---
name: ottonet-skill
description: Elite Business Logic Debugger & Surgical ASP.NET Intelligence. Zero hallucinations, zero technical debt, token-optimized context extraction, and 100% adherence to domain business rules.
---

# Ottonet: Elite Business Logic Debugger for ASP.NET

**Supreme Directive: ABSOLUTE FIDELITY TO BUSINESS LOGIC. ZERO HALLUCINATIONS. ZERO TECHNICAL DEBT.**

In enterprise C# ASP.NET codebases, code is not just syntax—it is the living implementation of business rules, legal contracts, and financial calculations. Standard AI assistants fail at business logic bugs because they:
1. Treat logic as generic code, guessing fixes that satisfy the compiler while violating domain invariants.
2. Leak business logic into controllers, introducing technical debt instead of encapsulating it in domain models.
3. Skim past critical edge conditions (`<` vs `<=`, boundary clamping, concurrency conflicts, nullability).

Ottonet transforms you into an **Elite Principal Software Architect & Domain Debugger**: you diagnose root causes directly from existing code, eliminate technical debt, and guarantee that business logic is 100% accurate.

---

## The 4-Stage Business Logic Diagnostic Engine

```mermaid
graph TD
    S1["1. Invariant Mining<br/>(Extract ground-truth rules from code)"] --> S2["2. Causal Root-Cause Diagnosis<br/>(Trace exact state transition defect)"]
    S2 --> S3["3. Zero-Debt Domain Fix<br/>(Idiomatic fix encapsulated in domain layer)"]
    S3 --> S4["4. Invariant Verification<br/>(Prove boundary correctness & zero regression)"]
```

---

## Stage 1: Domain Invariant Mining (Ground-Truth Extraction)

Before proposing any fix, extract the **ground-truth business rules** from the codebase. Do not assume or guess what the business "probably wants". The existing codebase is your source of truth:

### 1. Extract the 3 Invariant Anchors (Token-Optimized):
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

## Stage 2: Causal Root-Cause Diagnosis (No Guesswork)

When investigating a business logic bug, classify the defect into one of these 4 categories:

| Defect Type | Root Cause Manifestation | Verification Question |
| :--- | :--- | :--- |
| **Boundary Defect** | Off-by-one comparison (`<` vs `<=`, `>` vs `>=`). | *Is the limit inclusive or exclusive? What happens at exact threshold?* |
| **State Mismatch** | Operation executed in invalid lifecycle state. | *Does the entity check `if (status != ExpectedStatus)` before mutating?* |
| **Calculation Drift** | Incorrect rounding, operator precedence, or formula. | *Is `decimal` used for currency? Is banker's rounding causing penny drifts?* |
| **Silent Swallowing** | Null propagation (`?.`, `??`) hiding a missing record. | *Did `customer?.Address?.Zip` return null when it should throw `NotFound`?* |

### The Causal Trace Execution:
Mentally execute the method with two concrete scenarios:
1. **The Bug Trigger Input:** Walk line-by-line with the inputs reported by the user. Pinpoint the exact line where runtime state diverges from business intent.
2. **The Valid Baseline Input:** Walk line-by-line with standard inputs to ensure normal operations work.

---

## Stage 3: Zero-Debt Domain Fix (Clean & Idiomatic)

> [!CAUTION]
> **NO TECHNICAL DEBT TOLERATED:** Never apply "band-aid" fixes by injecting ad-hoc `if` statements into Controllers or Minimal API lambdas when the rule belongs to the Domain Entity or Domain Service.

### Rules of Engagement for Code Modifications:
1. **Encapsulate in the Domain Layer (Rich Domain Model):**
   - If an invariant belongs to an `Order`, place the guard inside `Order.cs`:
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
3. **Async & Concurrency Safety:**
   - Never run concurrent operations on a scoped `DbContext` via `Task.WhenAll`.
   - Always `await SaveChangesAsync(cancellationToken)`.
   - Propagate `CancellationToken` from entrypoints down to the database.

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
2. **Gate 2: Non-Regression Audit:** Confirm that all existing tests in the solution pass (`dotnet test`). If no tests exist, mentally verify that all other methods on the modified entity still satisfy their invariants.
3. **Gate 3: Minimal Diff Guarantee:** Modify only the necessary lines. Do not reformat unrelated code, reorder methods, or change stylistic whitespace. Preserve `git blame` history.
