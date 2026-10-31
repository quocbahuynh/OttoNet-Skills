# State Machine & Multi-API Workflow Tracing

Real enterprise business logic rarely lives inside a single API endpoint. A complete business feature is typically a **multi-step stateful workflow** coordinated across several HTTP calls (e.g., Draft &rarr; Submit &rarr; Validate &rarr; Pay &rarr; Fulfill).

When debugging or implementing such workflows, you must anchor your analysis on the **Aggregate Root State Machine** rather than treating endpoints as disconnected silos.

---

## The 3-Step Multi-API Tracing Framework

### Step 1: Identify the Aggregate Root & State Enum
Search for the core entity that transitions through statuses:
- Example: `Order`, `Invoice`, `Subscription`, `LoanApplication`.
- Locate its status enum:
  ```csharp
  public enum OrderStatus
  {
      Draft = 1,
      PendingValidation = 2,
      PaymentProcessing = 3,
      Completed = 4,
      Cancelled = 99
  }
  ```

---

### Step 2: Build the State Transition & Preconditions Matrix
Create a table linking each API endpoint to the status change it causes, along with its **Preconditions** (what must be true before this API can be called) and **Invariants** (what this API must guarantee):

| Sequence | API Endpoint | Initial State | Target State | Preconditions (Guards) | State Hand-Off (Output) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01** | `POST /api/orders` | *(None)* | `Draft` | User authenticated, Cart has items | Returns `orderId`, creates order record |
| **02** | `PUT /api/orders/{id}/address` | `Draft` | `Draft` | Status == `Draft`, Address valid | Sets shipping details |
| **03** | `POST /api/orders/{id}/checkout`| `Draft` | `PendingValidation`| Status == `Draft`, Items in stock | Locks inventory, calculates final total |
| **04** | `POST /api/payments/charge` | `PendingValidation`| `PaymentProcessing` | Total > 0, Token provided | Charges gateway, sets transaction id |
| **05** | `POST /api/webhooks/payment` | `PaymentProcessing`| `Completed` | Gateway signature valid | Emits `OrderPaidDomainEvent`, triggers shipping |

---

### Step 3: Verify State Hand-Off (Preventing Cross-API Corruption)

When modifying or debugging any API in the chain:
1. **Never skip a transition:** Verify that the endpoint explicitly checks the precondition (`if (order.Status != OrderStatus.Draft) throw new ConflictException(...)`).
2. **Never leave intermediate state uncommitted:** Ensure that all related changes (e.g. status update + domain event dispatch + inventory reservation) occur in a single atomic database transaction:
   ```csharp
   using var transaction = await _context.Database.BeginTransactionAsync(cancellationToken);
   try
   {
       order.MarkAsPaid(paymentId);
       await _context.SaveChangesAsync(cancellationToken);
       await _mediator.Publish(new OrderPaidEvent(order.Id), cancellationToken);
       await transaction.CommitAsync(cancellationToken);
   }
   catch
   {
       await transaction.RollbackAsync(cancellationToken);
       throw;
   }
   ```
3. **Check Side-Effects:** Verify that the output of API $N$ provides exactly what API $N+1$ expects as input (e.g. correct ID, valid non-null status, non-zero total).
