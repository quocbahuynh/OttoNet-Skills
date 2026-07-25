---
name: dotnet-task-analyzer
description: Preserve and structure a complete BA or Team Leader task after project understanding and team patterns are documented. Use to create a task requirement report without inventing product or API behavior.
---

# .NET Task Analyzer

## Purpose

Read the complete task and turn it into a faithful, traceable requirement model. This stage captures what was stated; it does not fill gaps from code or generic practices.

## When to use

Use after project documentation, repository exploration, and team-pattern learning are complete. Use again when the task owner provides a revised specification.

## Assumptions

- A complete source task is available as text, file, ticket export, or approved conversation.
- Project context exists but cannot be used to silently alter task wording.
- Readiness is preliminary because repository-specific investigation follows.

## Required inputs

- Complete BA or Team Leader task, including linked material that is in scope.
- Project Understanding Report.
- Team Coding Pattern Report.
- Task dossier state and evidence registry when the task is part of an orchestrated workflow.

## Workflow

1. Read the task in full and preserve the original source or a stable reference to it. When the task has changed since a prior analysis, record the revision and mark superseded requirements rather than blending versions.
2. Extract task name, overview, objective, scope, out of scope, endpoints, inputs, outputs, request/response contracts, field rules, validation rules, business rules, roles, permissions, test cases, acceptance criteria, dependencies, notes, and undefined information.
3. Assign stable IDs to requirements, acceptance criteria, and undefined decisions. Attribute each extracted fact to its source section. Keep wording exact for rules, contract fields, and acceptance criteria where possible.
4. Record omissions explicitly. Do not invent roles, permissions, fields, endpoints, pagination, search, sorting, delete strategy, status behavior, or error contracts.
5. Classify preliminary readiness: `READY` when stated requirements appear complete; `READY_WITH_ASSUMPTIONS` when only clearly bounded technical assumptions may be needed; `BLOCKED` when the task itself contains a material unresolved decision. Mark this as subject to task-context investigation.
6. Do not select implementation files or resolve repository conflicts in this stage. Return requirement IDs and source references for the dossier; do not duplicate task text in unrelated reports.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Preserve task intent; do not rewrite business decisions as technical conventions.
- Do not treat an example or acceptance criterion as permission to add unstated behavior.
- Read task material only; do not modify target source code or Git state.
- Keep sensitive business data limited to what is necessary for the report.

## Stop conditions

Stop with `BLOCKED` if the supplied source is incomplete, contradictory, or lacks the information required even to state the requested capability. Do not ask a clarification question already answered in the task.

## Required output

Produce a **Task Requirement Report**, using `../../templates/task-requirement-report.md`. Include the complete extracted requirement model, stable requirement IDs, source attribution, undefined information, and preliminary `READY`, `READY_WITH_ASSUMPTIONS`, or `BLOCKED` classification. Add task-source evidence to the registry and cite those IDs from later artifacts.

## Handoff to the next skill

Pass the Task Requirement Report, project reports, and pattern report to `dotnet-task-context-investigator` for task-specific repository investigation.
