---
name: dotnet-requirement-gap-analyzer
description: Compare a BA task with .NET repository rules, code, and team patterns to resolve technical conventions, expose business ambiguity, and create clarification questions before planning. Use after task-context investigation.
---

# .NET Requirement Gap Analyzer

## Purpose

Decide whether the task is ready to plan without hiding missing, ambiguous, conflicting, or impossible requirements.

## When to use

Use after `dotnet-task-context-investigator` and before implementation planning. Re-run after BA or Team Leader clarification until no blocking issue remains.

## Assumptions

- All earlier reports are available and task wording has not been silently changed.
- Repository evidence can resolve technical conventions but cannot make an unclear business decision on behalf of the task owner.
- A lack of a repository feature may be an implementation gap, a product decision gap, or both.

## Required inputs

- Task Requirement Report.
- Project Documentation, Project Understanding, Team Coding Pattern, and Task Context reports.
- Any explicit clarification responses, which become resolved task requirements.
- Task dossier state and evidence registry when resuming.
- Cached project index when resuming.

## Workflow

1. Compare every requirement ID and acceptance criterion against documentation, the cached project index, current code, related modules, data relationships, and selected patterns.
2. Identify missing information, ambiguous or conflicting rules, task/code and task/documentation conflicts, missing relationships, permissions, delete/status/uniqueness/error behavior, incomplete acceptance criteria, and impossible or unsupported requirements.
3. Classify every issue exactly once: `BLOCKING`, `NON_BLOCKING`, `ASSUMPTION_ALLOWED`, `REPOSITORY_RESOLVED`, or `BA_CONFIRMATION_REQUIRED`. Give each issue a stable ID and link it to requirement and evidence IDs.
4. Resolve a technical convention as `REPOSITORY_RESOLVED` only with direct repository evidence. Do not ask questions the repository already answers.
5. Require business confirmation when a decision changes product behavior, even if another module suggests an analogy. Do not resolve such ambiguity by copying that module.
6. Treat any unresolved database-field detail as blocking before planning or schema work. A field is not ready until purpose, business meaning, type, nullability, constraints, relationships, default, update behavior, and governing business rules are all stated or explicitly resolved. Do not use another module to fill a missing business decision.
7. For every API in scope, check whether controller or endpoint-level documentation can be added locally. If the task would require global Swagger, Scalar, or OpenAPI configuration changes, classify that change and stop for explicit developer approval before planning it.
8. For each blocking or BA-confirmation issue, produce a context-aware question. State the affected feature, the affected business flow, what is unclear, why the decision is needed, the repository evidence, the implementation impact, current assumptions, and suggested options where useful. Avoid questions that are already answered by the task or repository.
9. Assess whether the task is advanced, unfamiliar, or high-risk enough to justify searching the official `dotnet/skills` repository. Consider the task's architecture, security, migrations, distributed behavior, background processing, cloud, performance, testing, refactoring, and technology novelty against the current repository evidence. Do not install or use a skill here; record a recommendation or `NO_INSTALL_NEEDED` for the orchestrator's approval gate.
10. Permit planning only when no unresolved blocking question remains and the specialized-skill decision is recorded. Record the resolution in the dossier ledger and carry all allowed assumptions visibly into the plan.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Do not write implementation code or alter task wording.
- Do not hide an assumption, downgrade a business ambiguity, or use generic .NET practice to override repository/task evidence.
- Do not claim a requirement is repository-resolved without a path, configuration, or other concrete evidence.
- Do not approve a new table, column, or persisted field while any required field-understanding item is unknown.
- Do not approve global Swagger, Scalar, or OpenAPI configuration changes without explicit developer authorization.
- Do not recommend a specialized skill without naming the technical area, the evidence gap or risk, and why current project guidance is insufficient.
- Do not claim a candidate skill exists, is relevant, or is installed without repository/search evidence and explicit developer approval.
- Do not create a plan while an unresolved `BLOCKING` or `BA_CONFIRMATION_REQUIRED` issue remains.

## Stop conditions

Stop at the clarification gate whenever an unresolved blocking issue exists. Resume only with a task-owner response or new repository evidence that genuinely resolves it.

## Required output

Produce a **Requirement Gap Report**, using `../../templates/requirement-gap-report.md`. Include the full issue register, classification, requirement and evidence IDs, field-readiness decisions, API-documentation configuration decisions, specialized-skill assessment, allowed assumptions, and a planning decision. When needed, add **Clarification Questions for BA** with the affected feature and flow, implementation impact, rationale, evidence, assumptions, and options. Preserve prior resolutions as superseded history rather than reopening a settled issue without new evidence.

## Handoff to the next skill

If planning is permitted, pass all reports and the resolved task specification to `dotnet-implementation-planner`. Otherwise stop for clarification; do not bypass the gate.
