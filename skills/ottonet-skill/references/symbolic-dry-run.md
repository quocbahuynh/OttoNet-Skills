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

## 2. EF Core Eager Loading & Concurrency Audit

Before finalizing any query or mutation:

### 1. Navigation Property Loading Audit
- If code touches nested properties (e.g. `order.Customer.Address.PostalCode`), verify that the LINQ query explicitly eager-loaded the relationship:
  ```csharp
  // VULNERABLE TO RUNTIME NullReferenceException:
  var order = await _context.Orders.FirstOrDefaultAsync(o => o.Id == id, ct);
  var zip = order.Customer.Address.PostalCode; // CRASH! Customer is null

  // SAFE:
  var order = await _context.Orders
      .Include(o => o.Customer)
          .ThenInclude(c => c.Address)
      .FirstOrDefaultAsync(o => o.Id == id, ct);
  ```

### 2. Optimistic Concurrency Conflict Audit
- When updating high-contention resources (inventory balances, seat reservations, bank balances), inspect if the entity defines a concurrency token:
  ```csharp
  public class Account
  {
      public decimal Balance { get; private set; }
      [Timestamp]
      public byte[] RowVersion { get; private set; } = null!;
  }
  ```
- Wrap updates in a concurrency catch block if retry logic is required:
  ```csharp
  catch (DbUpdateConcurrencyException ex)
  {
      // Reload and re-apply business invariants or abort with Conflict HTTP 409
      throw new DomainConflictException("The record was modified by another transaction. Please retry.");
  }
  ```

---

## 3. The 3 Golden Rules of Zero Technical Debt in Business Logic Fixes

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
