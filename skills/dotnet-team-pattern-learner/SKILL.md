---
name: dotnet-team-pattern-learner
description: Learn evidence-backed .NET team implementation conventions from active code, Git history, and review evidence. Use after repository exploration and before reading a BA task or planning code changes.
---

# .NET Team Pattern Learner

## Purpose

Identify reusable implementation structure while separating documented rules and approved practices from common, legacy, or unknown behavior.

## When to use

Use after `dotnet-repository-explorer` and before `dotnet-task-analyzer`. Use focused follow-up analysis if a task needs conventions not covered in the initial report.

## Assumptions

- Recent merged code is useful evidence but not automatic approval evidence.
- Merge request, approval, and resolved-discussion data may be unavailable locally.
- Business rules in another module are not transferable merely because its structure is useful.

## Required inputs

- Project Documentation Report.
- Project Understanding Report.
- Read-only Git history and, only when available, merge request or review evidence.
- Task dossier state and evidence registry when resuming.
- Cached project index when it helps scope active modules.

## Workflow

1. When a dossier exists, check its commit range, selected references, `.otto/project-index.md`, and evidence freshness. Revalidate changed samples or task-relevant pattern areas; do not repeat an unbounded history scan when the recorded evidence remains current.
2. Inspect recent history, changed paths, final merged diffs, authors when useful, and current active implementations. Prefer comparable modules and recent code over isolated examples.
3. When available, inspect approved merge requests, approval state, resolved review comments, and resolved discussions. State the source and accessibility limits.
4. Learn naming, folders, request/response and DTO organization, handlers/services, dependency injection, validation, authorization, data-access and transaction style, errors, logging, API documentation, and tests.
5. Treat recent production code from experienced maintainers as the preferred structural reference unless the task or stronger evidence explicitly requires a different approach. This preference does not transfer business-specific roles, statuses, conditions, values, or permissions.
6. Classify each finding: `REQUIRED` for documented/configured/enforced rules; `APPROVED` only for explicit approval or resolved-review evidence; `ESTABLISHED` for consistent recent active repetition; `COMMON` for frequent but non-universal use; `LEGACY` for old code not normally copied; `UNKNOWN` for insufficient evidence.
7. Select references for their reusable structural characteristics. Explicitly exclude source-module statuses, permissions, dates, magic values, and business conditions unless the task itself requires them. Explain that Git history confirms historical merge state, while approval evidence requires actual approval or resolved-review data; never claim review occurred from a merge commit alone.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Inspect history and code read-only; do not alter Git state or source files.
- Do not call a single file a convention or infer approval without explicit evidence.
- Do not copy business-specific conditions, roles, statuses, time semantics, or magic values into a reusable pattern.
- Do not assume GitLab, GitHub, or another review API exists.

## Stop conditions

Stop classification at `UNKNOWN` if evidence is insufficient. If only legacy examples exist, report that they are unsuitable as default references rather than promoting them.

## Required output

Produce a **Team Coding Pattern Report**, using `../../templates/team-pattern-report.md`. Include each finding's classification, direct evidence, reusable boundary, selected references, non-transferable business behavior, available approval evidence, and data-access limitations. Cite evidence-registry IDs, sample size or enforcement source, and any revalidation delta.

## Handoff to the next skill

Pass the Project Understanding Report and Team Coding Pattern Report to `dotnet-task-analyzer`. Do not begin task-specific code investigation here.
