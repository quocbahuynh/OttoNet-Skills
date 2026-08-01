---
name: dotnet-step-executor
description: Execute exactly one explicitly requested and developer-approved step from an OttoNet HTML implementation plan in a .NET repository. Use only after plan approval and never advance to future steps automatically.
---

# .NET Step Executor

## Purpose

Implement one approved plan step within its stated scope, validate it, and report the resulting diff without committing or advancing the plan.

## When to use

Use only when the developer explicitly requests a numbered step from an approved HTML plan, for example: “Read the implementation plan and execute Step 3 only.”

## Assumptions

- The developer already approved the plan.
- The target project is on the intended existing branch.
- The resolved task specification and all plan dependencies are available.
- A developer may have uncommitted work that must be protected.

## Required inputs

- HTML implementation plan path and explicit requested step number.
- Resolved task specification and supporting reports.
- Workspace Inspection Report or permission to perform a new inspection.
- Task dossier state and evidence registry under `.otto/tasks/<task-slug>/` when the task is orchestrated; otherwise state that no workflow-state update is available.
- Specialized-skill decision and, when installed with explicit approval, the installed skill's instructions and source reference.

## Workflow

1. Run `dotnet-workspace-inspector` behavior first. Record current branch, local changes, staged files, conflicts, and protection boundaries.
2. When a dossier is available, reconcile its plan approval, source freshness, `AWAITING_STEP_REQUEST` state, requested step, protected paths, and latest continuity event with the current workspace. Stop on a mismatch that could make the step unsafe. Read the requested step from the HTML plan, including goal, files, actions, references, dependencies, risks, validation, and expected result. Confirm the plan was approved and that Otto-owned artifacts remain in `.otto/`.
3. Reconcile the specialist-skill decision. Stop if approval is pending or if an installed skill's instructions have not been read. When installed, read its instructions before editing and record its source/revision; use it only as supplemental guidance under repository evidence and resolved requirements.
4. Read only the step's cited requirements, evidence, project files, and selected reference implementations before editing. Confirm dependencies are complete and no unresolved blocking issue applies; expand the context only when the step reveals a documented dependency.
5. Search for existing services, repositories, handlers, validators, utility methods, storage implementations, extension methods, shared response/error builders, and business logic before creating a new component. Reuse a suitable implementation and record why it is appropriate; if reuse is unsafe or incomplete, record the evidence and boundary for the new code.
6. If the step introduces or changes an API, update the local controller-level or endpoint-level documentation with a summary, description, request payload, per-field validation, response format, applicable `400`, `401`, `403`, `404`, `409`, and other repository-supported error responses, mock request, mock success response, and mock error responses. Follow the repository's actual documentation mechanism. Stop if the change would require global Swagger, Scalar, or OpenAPI configuration without explicit developer approval.
7. If the step introduces a table, column, or persisted field, reconcile every field against the approved field-understanding matrix: purpose, business meaning, type, nullability, constraints, relationships, default, update behavior, and business rules. Stop before migrations or schema changes when any item is unknown.
8. Compare planned files with existing dirty and staged paths. Stop if the step could overwrite, stage over, or obscure unrelated developer changes.
9. Make only changes required by the requested step. Follow project documentation, resolved requirements, the highest-evidence team patterns, and any approved specialist guidance. Do not prepare code for a future step or fix unrelated existing failures.
10. Run the plan's applicable validation commands, respecting repository instructions and environment limitations. Inspect the resulting diff and confirm scope.
11. Report exact files changed, commands actually run, results, specialist-skill evidence used, API documentation coverage, reuse decisions, field-readiness confirmation, recovery guidance shown (not executed), deviations, and unresolved issues. If invoked by the orchestrator, provide the precise state transition (`AWAITING_REVIEW` or `BLOCKED`), cited evidence IDs, and new evidence paths; the orchestrator records it. Leave commit and HTML-plan-status updates to explicit developer instruction.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Execute exactly one explicitly requested step; never auto-run future steps.
- Never commit, push, create/switch branches, reset, rebase, discard changes, or rewrite history.
- Do not refactor unrelated files, create speculative future code, or silently modify the HTML plan.
- Do not overwrite or stage existing developer changes. Stop on uncertain overlap. Keep `.otto/` artifacts untracked unless the user explicitly asks to track them.
- Do not claim validation passed unless the actual command ran and its result was inspected.
- Do not create duplicate logic when an existing repository component satisfies the requirement; explain any justified exception.
- Do not modify global Swagger, Scalar, or OpenAPI configuration without explicit approval.
- Do not implement a persisted field with unresolved semantics or scope outside the approved task.
- Do not execute rollback or recovery commands; only report optional commands for the developer.
- Do not fix unrelated test failures, refactor unrelated modules, or change unrelated behavior.
- Do not install, update, or invoke a specialized skill from this step; installation requires the earlier explicit approval gate.
- Do not allow installed skill guidance to override project architecture, task requirements, or task scope.
- Do not edit the workflow state directly unless the developer explicitly asks to run this skill without the orchestrator and authorizes that update.

## Stop conditions

Stop before editing if plan approval or the requested step is unclear, dependencies are incomplete, a blocking requirement remains, expected files conflict with uncommitted work, or repository instructions prohibit the change. Stop after the requested step is complete; wait for review and developer commit decision.

## Required output

Produce a **Step Execution Report** containing the requested step, workspace status, files inspected and changed, requirements covered, specialist-skill evidence used, API documentation coverage, reuse decisions, database-field readiness, validation commands actually executed and results, diff summary, recovery guidance, deviations, blockers, scope-boundary findings, and a recommendation to proceed to review. Do not label it ready for commit until the reviewer completes.

## Handoff to the next skill

Pass the execution report, plan step, changed-file diff, and supporting requirements to `dotnet-step-reviewer`.
