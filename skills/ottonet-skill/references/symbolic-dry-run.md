# Symbolic Dry-Run & Anti-Skimming Cognitive Playbook

Why do AI models skim over C# code and miss critical bugs?
Because LLMs generate predictions based on token probability. When reading a 30-line method, the model assumes standard behavior ("this looks like normal discount calculation") unless forced to compute state transitions line-by-line.

This playbook provides the concrete protocol to force 100% token-by-token comprehension on any method.

---

## 1. The Line-by-Line Trace Table Template

When inspecting a critical method during debugging or feature extension, construct this table:

```markdown
### Line-by-Line Execution Trace: `OrderService.CalculateFinalTotal`

| Line # | Statement | Mutated State / Evaluated Branch | Business Rule / Guard Condition |
| :--- | :--- | :--- | :--- |
| `L82` | `if (order == null)` | `order` nullity | Guard: Throws `ArgumentNullException` |
| `L85` | `if (order.Status != OrderStatus.Draft)` | `order.Status` | Invariant: Only drafts can be calculated. Throws `InvalidOperationException` |
| `L89` | `var subtotal = order.Items.Sum(i => i.Price * i.Quantity);` | `subtotal` (decimal) | Accumulator: Must be >= 0 |
| `L93` | `var discount = _discountService.GetDiscount(order.CustomerId);` | `discount` (decimal) | External dependency call |
| `L96` | `if (discount > subtotal) discount = subtotal;` | `discount` clamp | Guard: Discount cannot exceed subtotal |
| `L99` | `var taxRate = order.ShippingAddress.IsTaxExempt ? 0 : 0.08m;` | `taxRate` | Business Rule: Exempt check |
| `L102`| `order.Tax = (subtotal - discount) * taxRate;` | `order.Tax` | Calculation: Tax applied after discount |
| `L105`| `order.Total = (subtotal - discount) + order.Tax;` | `order.Total` | Invariant: Final total persisted |
```

---

## 2. The 2-Scenario Symbolic Dry-Run

Immediately following the table, simulate execution with two specific test cases:

### Scenario 1: Happy Path (Standard Business Case)
- **Inputs:**
  - `order.Status = OrderStatus.Draft`
  - `Items = [ { Price: 50, Quantity: 2 } ]` &rarr; `subtotal = 100`
  - `discount = 20`
  - `IsTaxExempt = false` (`taxRate = 0.08`)
- **Step-by-Step State Propagation:**
  - `L82`: `order != null` &rarr; Pass.
  - `L85`: `order.Status == Draft` &rarr; Pass.
  - `L89`: `subtotal = 100`.
  - `L93`: `discount = 20`.
  - `L96`: `20 <= 100` &rarr; `discount = 20`.
  - `L99`: `taxRate = 0.08`.
  - `L102`: `order.Tax = (100 - 20) * 0.08 = 6.40`.
  - `L105`: `order.Total = 80 + 6.40 = 86.40`.
- **Verdict:** Logic holds for valid inputs.

---

### Scenario 2: Boundary / Edge / Failure Case (Where Bugs Hide)
- **Inputs:**
  - `order.Status = OrderStatus.Draft`
  - `Items = [ { Price: 10, Quantity: 1 } ]` &rarr; `subtotal = 10`
  - `discount = 50` *(Discount exceeds subtotal)*
  - `IsTaxExempt = true` (`taxRate = 0`)
- **Step-by-Step State Propagation:**
  - `L82`: Pass.
  - `L85`: Pass.
  - `L89`: `subtotal = 10`.
  - `L93`: `discount = 50`.
  - `L96`: `50 > 10` &rarr; clamped to `discount = 10`.
  - `L99`: `IsTaxExempt == true` &rarr; `taxRate = 0`.
  - `L102`: `order.Tax = (10 - 10) * 0 = 0`.
  - `L105`: `order.Total = 0 + 0 = 0`.
- **Verdict:** Clamping prevents negative order totals.

---

## 3. The Top 5 Logic Traps to Scan For in C# ASP.NET

When constructing the table and dry-run, explicitly audit for:

1. **Strict Inequality vs. Non-Strict Inequality (`<` vs. `<=`, `>` vs. `>=`):**
   - E.g., `if (age < 18)` vs `if (age <= 18)` or pagination `page * pageSize < total`.
2. **Nullable Reference Types & Null Propagation (`?.` and `??`):**
   - E.g., `customer?.BillingAddress?.PostalCode` silently evaluating to `null` instead of triggering a validation error.
3. **Floating Point vs. Decimal Rounding:**
   - E.g., using `double` / `float` instead of `decimal` for financial amounts, or `Math.Round` default banker's rounding (`MidpointRounding.ToEven`) causing off-by-one penny discrepancies.
4. **Unhandled Enum Members in `switch` expressions:**
   - E.g., `status switch { OrderStatus.Draft => ..., OrderStatus.Paid => ... }` throwing `SwitchExpressionException` when a new status is introduced.
5. **Entity Framework Change Tracker Assumptions:**
   - E.g., modifying a detached DTO or disconnected entity and assuming `_context.SaveChangesAsync()` will detect and persist the modification without `_context.Update(...)` or fetching the tracked entity first.
