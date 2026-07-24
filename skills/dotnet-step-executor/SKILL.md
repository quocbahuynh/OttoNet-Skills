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

## Workflow

1. Run `dotnet-workspace-inspector` behavior first. Record current branch, local changes, staged files, conflicts, and protection boundaries.
2. Read the requested step from the HTML plan, including goal, files, actions, references, dependencies, risks, validation, and expected result. Confirm the plan was approved.
3. Read the referenced project files and selected reference implementations before editing. Confirm dependencies are complete and no unresolved blocking issue applies.
4. Compare planned files with existing dirty and staged paths. Stop if the step could overwrite, stage over, or obscure unrelated developer changes.
5. Make only changes required by the requested step. Follow project documentation, resolved requirements, and the highest-evidence team patterns. Do not prepare code for a future step.
6. Run the plan's applicable validation commands, respecting repository instructions and environment limitations. Inspect the resulting diff and confirm scope.
7. Report exact files changed, commands actually run, results, deviations, and unresolved issues. Leave commit and plan-status updates to explicit developer instruction.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Execute exactly one explicitly requested step; never auto-run future steps.
- Never commit, push, create/switch branches, reset, rebase, discard changes, or rewrite history.
- Do not refactor unrelated files, create speculative future code, or silently modify the HTML plan.
- Do not overwrite or stage existing developer changes. Stop on uncertain overlap.
- Do not claim validation passed unless the actual command ran and its result was inspected.

## Stop conditions

Stop before editing if plan approval or the requested step is unclear, dependencies are incomplete, a blocking requirement remains, expected files conflict with uncommitted work, or repository instructions prohibit the change. Stop after the requested step is complete; wait for review and developer commit decision.

## Required output

Produce a **Step Execution Report** containing the requested step, workspace status, files inspected and changed, requirements covered, validation commands actually executed and results, diff summary, deviations, blockers, and a recommendation to proceed to review. Do not label it ready for commit until the reviewer completes.

## Handoff to the next skill

Pass the execution report, plan step, changed-file diff, and supporting requirements to `dotnet-step-reviewer`.
