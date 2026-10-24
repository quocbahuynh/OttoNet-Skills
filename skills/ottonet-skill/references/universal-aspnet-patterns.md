# Universal ASP.NET Architectural Patterns

Ottonet Skill adapts to all variants of ASP.NET across .NET Framework 4.8 through .NET 9+.

---

## 1. Clean / Onion Architecture (DDD)
- **Projects:**
  - `Domain`: Core entities, Value Objects, Domain Events, Enums. No external dependencies.
  - `Application`: Use cases, CQRS Commands/Queries, MediatR Handlers, Validators, DTOs.
  - `Infrastructure`: EF Core `DbContext`, external API clients, messaging implementations.
  - `WebAPI`: Controllers or Minimal API mappings, middleware pipeline, DI composition.
- **Trace Path:** `Controller` -> `IRequest` -> `IRequestHandler` -> `Aggregate` -> `DbContext/IRepository`.

## 2. Vertical Slice Architecture (VSA)
- **Organization:** Slices by business feature instead of technical layer.
- **Directory:** `Features/<FeatureName>/` contains:
  - `Endpoint.cs`
  - `Command.cs`
  - `Handler.cs`
  - `Validator.cs`
  - `Response.cs`
- **Trace Path:** Everything relevant to a feature is self-contained within a single folder.

## 3. Classic N-Tier / Layered
- **Organization:** `Controllers/` -> `Services/` (`IOrderService`) -> `Repositories/` (`IOrderRepository`) -> `Models/` or `Entities/`.
- **Trace Path:** Follow interface registrations in `Program.cs` / `Startup.cs`.

## 4. Minimal APIs & FastEndpoints
- **Organization:** Endpoints mapped directly via `app.MapGet()` / `app.MapPost()` or `Endpoint<TRequest, TResponse>` classes.
- **Trace Path:** Look in `Endpoints/` or `Program.cs` route registries.

## 5. Event-Driven & Messaging
- **Technologies:** MassTransit, RabbitMQ, Wolverine, Rebus.
- **Trace Path:** Producer publishes `IntegrationEvent` -> Consumer receives via `IConsumer<T>` or `IHandleMessages<T>`. Check for outbox pattern.
