# 5 Business Rule Anchors in ASP.NET Codebases

When working with massive enterprise .NET solutions, business logic is strictly anchored across five predictable structural points. AI agents using Ottonet Skill inspect these anchors first rather than reading hundreds of raw implementation files.

---

### Anchor 1: Input Validators (`FluentValidation`)
- **Location:** Typically under `Validators/` or nested within CQRS Command/Query folders.
- **Pattern:** `public class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>`
- **Value:** Encapsulates 40% of the domain rules (field requirements, value boundaries, cross-field conditions, conditional checks).

### Anchor 2: Domain Errors & Error Catalogs
- **Location:** `Errors/`, `DomainErrors.cs`, `*Errors.cs`, or domain exceptions.
- **Pattern:** `public static readonly Error CannotCancel = new("Order.CannotCancel", "...");`
- **Value:** Every error code is an inverted business invariant. Reading 20 error declarations immediately teaches the agent 20 forbidden domain states.

### Anchor 3: State Enums & Aggregate Lifecycle
- **Location:** `Domain/Enums/`, `Common/Enums/`, or within Entity class files.
- **Pattern:** `public enum OrderStatus { Draft, Submitted, Processing, Shipped, Delivered, Cancelled }`
- **Value:** State transitions form the backbone of business processes. Aggregate methods enforcing status preconditions (e.g. `if (Status != OrderStatus.Draft) throw ...`) define valid workflows.

### Anchor 4: Guard Clauses in Aggregate Roots
- **Location:** Domain entities and aggregate roots.
- **Pattern:** Methods throwing `InvalidOperationException`, `DomainException`, or returning `Result.Failure`.
- **Value:** Defines immutable domain rules that can never be bypassed, even if UI or API validation fails.

### Anchor 5: Unit & Behavioral Tests
- **Location:** `tests/` or `test/` projects.
- **Pattern:** `[Fact]` / `[Test]` methods named `Should_*`, `When_*`, `Given_*`.
- **Value:** Tests are living specifications written in human-readable developer language explaining expected behavior under edge conditions.
