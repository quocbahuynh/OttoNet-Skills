# Universal ASP.NET Architecture Archetypes

This reference guide enables you to instantly recognize the architectural style of any ASP.NET solution and trace its execution flow without guessing.

---

## The 7 Dominant ASP.NET Architectural Archetypes

### 1. Traditional N-Tier / Layered Architecture
- **Directory Cues:** `Controllers/`, `Services/`, `Repositories/`, `Data/` or projects named `*.Web`, `*.Services`, `*.Data`.
- **Entrypoint:** `Controllers/OrdersController.cs` inheriting from `ControllerBase` or `ApiController`.
- **Flow:**
  ```
  Controller Action -> IOrderService -> OrderService -> IOrderRepository -> OrderRepository -> DbContext
  ```
- **How to Trace:**
  1. Open the Controller, look at constructor: `IOrderService _orderService`.
  2. Search for implementation: `grep -rn 'class OrderService : IOrderService' src/`.
  3. Look at `OrderService` constructor for `IOrderRepository` or direct `AppDbContext`.

---

### 2. FastEndpoints / REPR (Request-Endpoint-Response)
- **Directory Cues:** `Endpoints/` or `Features/` containing files like `CreateOrderEndpoint.cs`, `CreateOrderRequest.cs`, `CreateOrderResponse.cs`.
- **Entrypoint:** Class inheriting from `Endpoint<TRequest, TResponse>` or `EndpointWithoutRequest<TResponse>`.
- **Flow:**
  ```
  HTTP Request -> CreateOrderEndpoint.HandleAsync(req, ct) -> DbContext / Domain Services
  ```
- **How to Trace:**
  1. The business logic lives directly inside `public override async Task HandleAsync(...)`.
  2. Dependencies are injected via the endpoint's constructor or `Resolve<T>()`.

---

### 3. Minimal APIs & Carter
- **Directory Cues:** `Program.cs`, `Endpoints/`, `Modules/` containing extension methods `MapOrderEndpoints(this IEndpointRouteBuilder app)` or `ICarterModule`.
- **Entrypoint:** `app.MapGet(...)`, `app.MapPost(...)`, or `class OrderModule : ICarterModule`.
- **Flow:**
  ```
  HTTP Request -> Lambda handler / Static Method -> Injected Services -> Results.Ok(...)
  ```
- **How to Trace:**
  1. Search for routes: `grep -rn 'MapPost\|MapGet\|MapGroup' src/`.
  2. Locate the handler lambda or static method: `app.MapPost("/orders", HandleCreateOrder);`.
  3. Inspect method arguments for injected services: `([FromServices] IOrderService svc, [FromBody] OrderDto dto)`.

---

### 4. Vertical Slice Architecture (Feature Folders)
- **Directory Cues:** `Features/Orders/CreateOrder/`, `Features/Orders/GetOrderDetails/`, `Features/Invoicing/PayInvoice/`.
- **Entrypoint:** The endpoint/controller, command, validator, and handler all reside in the **same feature folder**.
- **Flow:**
  ```
  Features/Orders/CreateOrder/
  ├── CreateOrderEndpoint.cs (or Controller)
  ├── CreateOrderCommand.cs
  ├── CreateOrderValidator.cs (FluentValidation)
  └── CreateOrderHandler.cs
  ```
- **How to Trace:**
  1. Find the feature folder: `find src/Features -name "*Order*"`
  2. Everything needed to understand the feature is co-located in that single directory!

---

### 5. Dapper & Micro-ORM Direct Data Access
- **Directory Cues:** References to `Dapper`, `System.Data.SqlClient`, `Microsoft.Data.SqlClient`, `IDbConnection`, or raw SQL files/strings.
- **Entrypoint:** Service, Repository, or directly in an Endpoint action.
- **Flow:**
  ```
  Action / Handler -> IDbConnection -> db.QueryAsync<T>("SELECT ... JOIN ... WHERE ...", parameters)
  ```
- **How to Trace:**
  1. Search for raw SQL: `grep -rn 'QueryAsync\|ExecuteAsync' src/`.
  2. Inspect the raw SQL string or stored procedure call.
  3. Map the returned dynamic or POCO type to the table columns.

---

### 6. Modular Monolith & Domain-Driven Design (DDD)
- **Directory Cues:** `Modules/Billing/`, `Modules/Inventory/`, `Modules/Identity/`. Each module has its own `src/` folder and internal DI setup.
- **Entrypoint:** Module-specific Controllers or MediatR/In-Memory Event Bus.
- **Flow:**
  ```
  API Gateway / Host -> Module.Billing.Api -> BillingModule -> Domain Events -> Module.Inventory
  ```
- **How to Trace:**
  1. Do not cross module boundaries directly via database calls.
  2. Look for public contracts: `Contracts/` or `Messages/` shared between modules.
  3. Look for in-memory event handlers: `INotificationHandler<T>` or `IConsumer<T>`.

---

### 7. Legacy ASP.NET Web API 2 & MVC (.NET Framework 4.8 / Early Core)
- **Directory Cues:** `Global.asax.cs`, `App_Start/`, `packages.config`, `WebApiConfig.cs`.
- **Entrypoint:** `ApiController` actions returning `IHttpActionResult` or `HttpResponseMessage`.
- **Flow:**
  ```
  ApiController Action -> Direct DbContext LINQ queries -> Request.CreateResponse(...)
  ```
- **How to Trace:**
  1. Check `App_Start/WebApiConfig.cs` for route template conventions (e.g. `api/{controller}/{id}`).
  2. Beware of fat controllers where business logic and LINQ queries are inlined directly in the controller action.
