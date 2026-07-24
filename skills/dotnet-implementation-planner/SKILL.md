---
name: dotnet-implementation-planner
description: Create a detailed, developer-approved, stepwise HTML implementation plan for a resolved .NET company task. Use only after requirement-gap analysis confirms that no blocking clarification remains.
---

# .NET Implementation Planner

## Purpose

Turn a resolved task and its repository context into small, independently understandable implementation steps. Produce a lightweight standalone HTML plan; do not write production code.

## When to use

Use only after `dotnet-requirement-gap-analyzer` explicitly permits planning. Re-plan if a clarification changes scope, requirements, or selected references.

## Assumptions

- The developer controls approval and execution.
- The plan may create a documentation artifact but must not change application code.
- Resolved task requirements include task-owner clarifications and must be distinguishable from allowed technical assumptions.

## Required inputs

- Resolved task specification.
- Project Documentation, Project Understanding, Team Coding Pattern, Task Context, and Requirement Gap reports.
- Selected reference implementations.
- `../../templates/implementation-plan-template.html`.

## Workflow

1. Confirm the Requirement Gap Report contains no unresolved `BLOCKING` or `BA_CONFIRMATION_REQUIRED` issue. Stop otherwise.
2. Select only references that match required structure and document their reuse limits.
3. Divide required work into small, controllable steps with no fixed maximum. Keep unrelated concerns separate and do not add future work.
4. For every step specify: number, title, goal, files to inspect/create/modify, detailed actions, reference implementations, business rules, acceptance criteria, risks, dependencies, validation commands, expected result, and suggested commit message.
5. Render a standalone HTML plan from the supplied template. Include task summary, requirement status, architecture context, references, table of contents, status-aware step cards, risk badges, validation checklist, commit suggestion, progress status, and final acceptance checklist.
6. Write the plan to `docs/implementation-plans/<task-slug>-plan.html` in the target project unless project documentation specifies a different approved planning location. Create only the plan artifact required for this task.
7. Present the plan for developer approval. Do not execute a step, edit production code, or silently revise the plan after approval.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never plan from unresolved blocking ambiguity.
- Do not write production code, alter migrations, or modify unrelated documentation.
- Do not conceal assumptions, conflicts, risks, or unavailable validation.
- Do not auto-approve the plan, auto-execute steps, commit, push, switch branches, or update the plan silently.

## Stop conditions

Stop for clarification if a planned action requires an unresolved decision. Stop at the plan approval gate after generating the plan; continue only after the developer explicitly approves it.

## Required output

Produce a **Detailed Implementation Plan** and its standalone HTML file. Report its path, all step details, source reports, assumptions, open non-blocking risks, and the explicit **Plan Approval Gate**. The plan must use `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, or `BLOCKED` for each step status.

## Handoff to the next skill

After explicit developer approval and an explicit request for one numbered step, pass the HTML plan path, requested step, resolved task specification, reports, and workspace boundaries to `dotnet-step-executor`.
