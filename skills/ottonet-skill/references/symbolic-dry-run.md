# Symbolic Dry-Run & Business Logic Causal Diagnostic Playbook

This playbook provides the concrete protocol to diagnose, trace, and repair subtle business logic bugs in C# ASP.NET without hallucinations or technical debt.

---

## 1. The 4-Column Causal Trace Table

When investigating a business logic defect, construct this causal trace in your thinking process:

```markdown
### Causal Trace: `InvoiceService.ApplySpecialDiscount`

| Line # | Code Statement | Evaluated Condition / State Mutation | Domain Invariant / Business Rule | Defect Detected? |
| :--- | :--- | :--- | :--- | :---: |
| `L42` | `if (invoice.Status != InvoiceStatus.Unpaid)` | `invoice.Status == Unpaid` | Rule: Only unpaid invoices can be discounted. | No |
| `L46` | `if (customer.Tier == Tier.VIP && invoice.Amount > 1000)` | Condition: `VIP` AND `> 1000` | Rule: VIP discount threshold is $1,000 inclusive (`>= 1000`). | **BUG!** Uses `>` instead of `>=`. |
| `L50` | `discount = invoice.Amount * 0.15m;` | `discount = 150` | Formula: 15% discount for eligible VIPs. | No |
| `L54` | `invoice.BalanceDue -= discount;` | `BalanceDue` mutation | Invariant: Balance due must not be negative. | Risk (no clamp) |
```

---

## 2. The 3 Golden Rules of Zero Technical Debt in Business Logic Fixes

### Rule 1: Never Patch in the Presentation Layer (Controller / Endpoint)
- **Bad (Technical Debt):**
  ```csharp
  // In OrdersController.cs - WRONG! Leaks domain logic into API layer
  if (dto.Total < 0) dto.Total = 0;
  var order = new Order { Total = dto.Total };
  ```
- **Good (Clean Domain Encapsulation):**
  ```csharp
  // In Domain/Entities/Order.cs - RIGHT!
  public void SetTotal(decimal total)
  {
      if (total < 0) throw new ArgumentOutOfRangeException(nameof(total), "Order total cannot be negative.");
      Total = total;
  }
  ```

### Rule 2: Guard Every State Mutation with Lifecycle Preconditions
- If an order is `Shipped`, it must NOT be possible to call `Cancel()` or `UpdateShippingAddress()`.
- Explicitly enforce lifecycle guards:
  ```csharp
  if (Status == OrderStatus.Shipped || Status == OrderStatus.Completed)
      throw new InvalidOrderStateException($"Cannot modify order in {Status} state.");
  ```

### Rule 3: Use Value Objects for Complex Domain Concepts
- Do not pass loose primitives (like `string currency, decimal amount`) if the codebase uses or would benefit from a `Money` or `Address` Value Object.
- Ensure rounding and currency matching are encapsulated within the Value Object.

---

## 3. The Elite Debugger's Checklist for Edge Cases

Before submitting a business logic fix, verify:
- [ ] **Exact Boundary Equality:** Did the requirement state "above 100" (`> 100`) or "100 and above" (`>= 100`)?
- [ ] **Zero and Negative Input Handling:** What happens if the input quantity, price, or discount is `0` or negative?
- [ ] **Nullability & Null-Safety:** Are all optional navigation properties checked before accessing nested properties?
- [ ] **Timezone & Temporal Invariants:** Does the logic compare UTC with Local time? Always ensure `DateTimeOffset.UtcNow` or `DateTime.UtcNow` consistency.
- [ ] **Idempotency:** Can this method be called twice with the same inputs without causing duplicate billing, duplicate status transitions, or double discounts?
