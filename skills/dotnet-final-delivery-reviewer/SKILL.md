---
name: dotnet-final-delivery-reviewer
description: Perform a full evidence-based final delivery review for a completed .NET company task after all approved steps are reviewed. Use before the developer manually pushes; this skill never pushes code.
---

# .NET Final Delivery Reviewer

## Purpose

Verify final branch readiness against the resolved task, acceptance criteria, repository conventions, validation evidence, workspace state, and commit history.

## When to use

Use only after every required plan step is completed and reviewed, and before the developer manually pushes. Re-run after final fixes or additional commits.

## Assumptions

- The implementation plan and step reports are available.
- The developer owns all commit and push decisions.
- Some checks may require environment access unavailable to the reviewer; those must remain visible limitations.

## Required inputs

- Resolved task specification, accepted implementation plan, and all step reports.
- Project Documentation and Team Coding Pattern reports.
- Current workspace state, diff, and commit history.
- Task dossier state and evidence registry when the task is orchestrated.

## Workflow

1. When a dossier is available, confirm `READY_FOR_FINAL_REVIEW`, reconcile the requirement-to-step coverage map, all completed-step reviews, commit decisions, source freshness, plan, workspace, and commit history. Treat any mismatch as a review finding.
2. Compare every resolved requirement, endpoint, contract, business rule, role/permission rule, and acceptance criterion with final source and tests.
3. Review input validation, output and error contracts, authorization, persistence relationships, uniqueness and delete behavior, naming, folders, dependencies, and team patterns. Inspect files changed, uncommitted changes, and relevant commit history; identify work not represented by the task or plan.
4. Run only repository-appropriate checks permitted by documentation. Possible commands include `dotnet restore`, `dotnet build`, `dotnet test`, `dotnet format --verify-no-changes`, `git status`, `git diff`, and `git log --oneline`; select rather than assume them.
5. Record every command actually executed with result. Distinguish skipped, unavailable, failed, and passed checks.
6. Summarize test coverage, remaining risks, known limitations, and manual verification that cannot be performed safely or locally.
7. Decide whether the branch is ready for manual push. Do not push or change Git state.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never push, commit, merge, switch branches, reset, rebase, force-push, or discard changes.
- Run only commands appropriate to the repository and its documented environment; do not claim any result without execution.
- Do not mark a branch ready when a required acceptance criterion, validation, or safety concern is unresolved.
- Keep external integration and manual environment gaps visible rather than simulating success.
- Do not edit the workflow state directly unless the developer explicitly asks to run this skill without the orchestrator and authorizes that update.

## Stop conditions

Stop with `Ready for push: No` if requirements are incomplete, validation fails, unreviewed/unexplained changes exist, a blocking risk remains, or required manual checks have not been accepted by the developer. Stop at the developer push gate even when ready.

## Required output

Produce a **Final Delivery Report**, using `../../templates/final-delivery-report.md`. Include completed and incomplete requirements, acceptance-criteria status, changed files, tests added, commands executed, build/test status, warnings, limitations, manual verification, commit/workspace review, and `Ready for push: Yes/No`.

## Handoff to the next skill

Stop for the **Developer Push Gate**. The developer decides whether to push manually; there is no automated downstream action.
