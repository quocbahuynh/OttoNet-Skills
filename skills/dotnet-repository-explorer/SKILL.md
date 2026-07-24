---
name: dotnet-repository-explorer
description: Map the complete .NET base code, its actual module responsibilities, and request execution flows after project documentation is understood. Use before analyzing a BA task to build project understanding from repository evidence.
---

# .NET Repository Explorer

## Purpose

Create a complete, evidence-based model of the existing base code without assuming any architecture or library.

## When to use

Use after `dotnet-project-documentation-reader` and before task analysis. Re-run focused mapping if a later task reveals a previously unexamined project area.

## Assumptions

- Workspace protection and applicable documentation reports are available.
- The repository may contain multiple solutions, executable services, shared libraries, tests, tools, and legacy code.
- Names such as CQRS, repository, or clean architecture are conclusions only when code or documentation demonstrates them.

## Required inputs

- Workspace Inspection Report.
- Project Documentation Report.
- Target repository root.

## Workflow

1. Inventory solution files, project files, project references, target frameworks, package references, and configuration roots.
2. Map every active project and its responsibility. Read startup paths, composition roots, dependency injection registration, host configuration, and primary entry points.
3. Trace representative real request paths from controller, endpoint, consumer, or UI boundary through application and data access to responses. Describe the actual sequence, for example `Endpoint → service → DbContext → response`, only when evidenced.
4. Identify controllers/endpoints, commands/queries and handlers if present, domain models, persistence, Entity Framework Core setup if present, authentication, authorization, validation, logging, errors, background jobs, file storage, and external services.
5. Identify all test projects and the current business modules. Record dependency direction from project references and call paths rather than folder names alone.
6. Inspect breadth first, then relevant representative files in each active area. Mark generated, deprecated, sample, and legacy areas to avoid treating them as active conventions.
7. Do not inspect a BA task or recommend implementation; explain only the current system.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Use read-only inspection; do not alter code, configuration, data, branches, or packages.
- Do not label a pattern as project-wide from one source file.
- Do not assume CQRS, MediatR, Clean Architecture, repositories, EF Core, or a test framework because their names are familiar.
- Keep secrets out of the report.

## Stop conditions

Stop and report limited coverage when solutions cannot restore or parse, modules are unavailable, or documentation identifies protected areas that cannot be inspected. Do not compensate with generic .NET assumptions.

## Required output

Produce a **Project Understanding Report**, using `../../templates/project-understanding-report.md` as the report structure. Include solution/project map, target frameworks and dependencies, architecture and dependency direction, actual request flows, cross-cutting implementation map, tests, active business modules, evidence paths, and uncertainties.

## Handoff to the next skill

Pass the Project Understanding Report, documentation rules, and module map to `dotnet-team-pattern-learner`.
