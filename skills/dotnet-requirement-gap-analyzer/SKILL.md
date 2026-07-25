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

## Workflow

1. Compare every requirement ID and acceptance criterion against documentation, current code, related modules, data relationships, and selected patterns.
2. Identify missing information, ambiguous or conflicting rules, task/code and task/documentation conflicts, missing relationships, permissions, delete/status/uniqueness/error behavior, incomplete acceptance criteria, and impossible or unsupported requirements.
3. Classify every issue exactly once: `BLOCKING`, `NON_BLOCKING`, `ASSUMPTION_ALLOWED`, `REPOSITORY_RESOLVED`, or `BA_CONFIRMATION_REQUIRED`. Give each issue a stable ID and link it to requirement and evidence IDs.
4. Resolve a technical convention as `REPOSITORY_RESOLVED` only with direct repository evidence. Do not ask questions the repository already answers.
5. Require business confirmation when a decision changes product behavior, even if another module suggests an analogy. Do not resolve such ambiguity by copying that module.
6. For each blocking or BA-confirmation issue, produce a focused question that states what is unclear, why it affects implementation, repository evidence, and suggested options where useful.
7. Permit planning only when no unresolved blocking question remains. Record the resolution in the dossier ledger and carry all allowed assumptions visibly into the plan.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Do not write implementation code or alter task wording.
- Do not hide an assumption, downgrade a business ambiguity, or use generic .NET practice to override repository/task evidence.
- Do not claim a requirement is repository-resolved without a path, configuration, or other concrete evidence.
- Do not create a plan while an unresolved `BLOCKING` or `BA_CONFIRMATION_REQUIRED` issue remains.

## Stop conditions

Stop at the clarification gate whenever an unresolved blocking issue exists. Resume only with a task-owner response or new repository evidence that genuinely resolves it.

## Required output

Produce a **Requirement Gap Report**, using `../../templates/requirement-gap-report.md`. Include the full issue register, classification, requirement and evidence IDs, allowed assumptions, and a planning decision. When needed, add **Clarification Questions for BA** with rationale, evidence, and options. Preserve prior resolutions as superseded history rather than reopening a settled issue without new evidence.

## Handoff to the next skill

If planning is permitted, pass all reports and the resolved task specification to `dotnet-implementation-planner`. Otherwise stop for clarification; do not bypass the gate.
