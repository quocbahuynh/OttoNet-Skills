# Ottonet: Universal ASP.NET Codebase Intelligence (Claude Code)

Follow the **ottonet-skill** protocol when working on this ASP.NET repository:

- **2-Tier Zoom-In:** Never load full C# classes > 80 lines into context. Grep for the method line number, read lines 1-25 (Scope Header: constructor DI & base classes), then read only the target method body (100% full-body fidelity). Cuts token bloat by 90%+.
- **Universal Architecture Navigation:** Do not assume MediatR. Check for N-Tier (Controller -> Service -> Repo), FastEndpoints (`Endpoint<TReq, TRes>`), Minimal APIs (`MapPost`/`MapGet`), Carter, Vertical Slices, or Dapper raw SQL.
- **Line-by-Line Trace & Dry-Run:** In your thinking process, output a `[Line | Statement | Variable Mutated | Invariant]` table and run 2 symbolic dry-run scenarios (Happy & Edge case) to guarantee you never skim over subtle logic errors.
- **Multi-API State Machine:** Anchor multi-step workflows to Aggregate Root status transitions (`Draft -> Submitted -> Paid`). Ensure preconditions are satisfied between API calls.
- **3-Gate Verification:** Ensure C# build passes, verify downstream state transitions are uncorrupted, and keep diffs minimal.
