---
name: dotnet-task-context-investigator
description: Investigate all direct and indirect .NET repository context for a documented BA task, including related entities, permissions, workflows, tests, and persistence. Use after task analysis and before requirement-gap resolution.
---

# .NET Task Context Investigator

## Purpose

Return to the repository with task terminology and establish what existing code, data relationships, workflows, and reusable components directly affect the requested behavior.

## When to use

Use after `dotnet-task-analyzer`. Re-run when clarification changes a task rule or reveals a new related domain concept.

## Assumptions

- The task requirements are structured and retained verbatim.
- The initial repository map is available but cannot substitute for detailed task-specific investigation.
- A relationship may be indirect, for example through users, roles, assignments, files, statuses, or a shared service.

## Required inputs

- Task Requirement Report.
- Project Documentation Report and Project Understanding Report.
- Team Coding Pattern Report.
- Repository root and workspace protection boundaries.

## Workflow

1. Build search terms from domain names, endpoint names, entity names, related entities, permissions, roles, statuses, business terminology, and database terminology in the task.
2. Search definitions and references. Inspect directly related documentation, entities, mappings/configurations, DTOs, endpoints, handlers or services, authorization, validations, tests, migrations, workflows, relationships, and analogous behavior.
3. Follow indirect relationships. For example, a task that prevents deletion for assigned records requires inspection of the assignment owner, relationship mapping, queries, and assignment creation paths—not merely the record's delete endpoint.
4. Identify existing reusable components and candidate references, documenting what is structurally reusable and what differs in business meaning.
5. Compare observed behavior with task wording. Record task/code conflicts, missing codebase support, unsupported dependencies, and missing database relationships without resolving business ambiguity.
6. Keep investigation read-only and do not plan or implement changes.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Do not modify code, migrations, configuration, data, or Git state.
- Do not infer a business rule just because a similar module has one.
- Do not treat a candidate reference as proof that its business semantics apply.
- Observe workspace protection boundaries and redact secrets in evidence.

## Stop conditions

Stop when the repository is unreadable, a required related component is unavailable, or investigation exposes a missing task decision that must be classified by the next skill. Do not proceed to planning.

## Required output

Produce a **Task Context Report**, using `../../templates/task-context-report.md`. Include relevant files, related modules and relationships, reusable components, current behavior, candidate references, conflicts, missing support, search terms, and direct evidence.

## Handoff to the next skill

Pass the Task Context Report and all prior reports to `dotnet-requirement-gap-analyzer`.
