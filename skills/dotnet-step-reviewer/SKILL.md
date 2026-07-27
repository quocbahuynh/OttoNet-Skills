---
name: dotnet-step-reviewer
description: Review one completed .NET implementation-plan step for requirement compliance, project consistency, validation evidence, and scope control before the developer manually commits. Use immediately after a step executor report.
---

# .NET Step Reviewer

## Purpose

Provide a focused pre-commit review of exactly one completed plan step. Decide whether it is ready for the developer to commit without implementing future work.

## When to use

Use after `dotnet-step-executor` finishes a requested step and before the developer decides whether to commit. Re-run after corrective changes to the same step.

## Assumptions

- The review target is an approved plan step and its current workspace diff.
- Existing developer changes may be present and must be distinguished from executor changes.
- A passing build or test suite is evidence only when it actually ran.

## Required inputs

- Step Execution Report and approved plan step.
- Resolved task specification, relevant reports, and selected references.
- Current `git status` and diff for the review boundary.
- Task dossier state and evidence registry under `.otto/tasks/<task-slug>/` when the task is orchestrated.

## Workflow

1. When a dossier is available, confirm the current state is `AWAITING_REVIEW`, the plan and requested step match the execution report, and no freshness or protection-boundary mismatch exists. Stop on an unsafe mismatch. Treat staged or tracked `.otto/` artifacts as a blocker unless the user explicitly asked to track them.
2. Reconfirm the step goal, stated requirements, acceptance criteria, files, risks, and expected result from the plan.
3. Inspect the current diff and distinguish pre-existing protected changes from the step's changes.
4. Review requirement compliance: goal complete, stated business rules covered, acceptance criteria covered where this step owns them, and no invented requirement.
5. Review project consistency: names, folders, architecture/dependency direction, authorization, validation, data access, errors, logging, tests, formatting, and documented rules as applicable.
6. Review scope: no unrelated changes, future-step work, accidental refactoring, or overwritten developer work.
7. Check validation evidence. Run only proportionate repository-appropriate read/build/test/format checks when the execution report did not cover them or when a review finding warrants it. Record commands actually run.
8. State whether the step is ready for commit and list exact required fixes or risks. When invoked by the orchestrator, return the exact state transition (`AWAITING_COMMIT_DECISION` or `BLOCKED`) with report evidence so it can be recorded. Do not make changes unless separately and explicitly asked to execute the same step again.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Review only the declared step boundary; do not implement fixes, future steps, or unrelated refactors.
- Never commit, push, stage, switch branches, reset, rebase, or discard changes.
- Do not declare a check passed without execution evidence.
- Treat unexplained diff overlap with pre-existing changes as a review blocker.
- Do not edit the workflow state directly unless the developer explicitly asks to run this skill without the orchestrator and authorizes that update.

## Stop conditions

Stop with `Ready for commit: No` when requirement coverage is incomplete, scope leaked, validation fails or is materially missing, a safety issue exists, or a blocking ambiguity remains. Stop at the developer commit gate even when the review passes.

## Required output

Produce a **Step Completion Report**, using `../../templates/step-completion-report.md`. Include step executed, changed files, requirements and evidence IDs covered, validation commands and results, build/test status, warnings, plan deviations, unresolved issues, `Ready for commit: Yes/No`, and a suggested commit message.

## Handoff to the next skill

If ready, stop for the **Developer Commit Gate**. After the developer decides and any state change is inspected, the next explicitly requested plan step may go to `dotnet-step-executor`; do not advance automatically.
