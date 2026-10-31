# Ottonet: Universal ASP.NET Codebase Intelligence (Claude Code)

Focus: **100% ACCURACY & FASTEST RESPONSE SPEED.**

When working on this C# ASP.NET codebase:
- **Fast Pinpoint:** Do not search aimlessly. Use targeted ripgrep to find the entrypoint or handler in 1 step:
  - Controllers: Grep `[Route("` or `[HttpPost`
  - MediatR: Grep `IRequestHandler<CommandName`
  - FastEndpoints: Grep `Endpoint<RequestType`
  - Minimal APIs: Grep `MapPost` / `MapGet`
- **Zero-Skimming:** Read the complete target method body in 1 clean read call. Scrutinize all branching logic, comparison operators (`<` vs `<=`), nullability checks, and EF Core change tracker status. Never assume behavior from method names.
- **Multi-API Workflows:** Follow the Aggregate Root state machine (`Draft -> Submitted -> Paid`). Verify preconditions between sequential APIs.
- **Verification:** Keep diffs minimal, preserve existing code style, and verify build via `dotnet build`.
