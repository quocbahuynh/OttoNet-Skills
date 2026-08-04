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
- Task dossier state and evidence registry under `.otto/tasks/<task-slug>/` when the task is orchestrated.

## Workflow

1. When a dossier is available, confirm `READY_FOR_FINAL_REVIEW`, reconcile the requirement-to-step coverage map, every step scope contract and scope audit, all completed-step reviews, commit decisions, source freshness, plan, workspace, and commit history. Treat any mismatch as a review finding. Treat staged or tracked `.otto/` artifacts as a blocker unless the user explicitly asked to track them.
2. Compare every resolved requirement, endpoint, contract, business rule, role/permission rule, and acceptance criterion with final source and tests.
3. Reconcile any specialized skill used for the task. Verify explicit approval, source/revision, instruction-read evidence, and that its guidance did not override repository conventions, resolved requirements, or task scope. If the plan required a specialist but evidence is missing, block delivery.
4. For every introduced API, verify local controller or endpoint documentation includes summary, description, request payload, field validation, response format, applicable `400`, `401`, `403`, `404`, `409`, and other repository-supported error responses, mock request, mock success response, and mock error responses. Treat undocumented API behavior or unapproved global Swagger, Scalar, or OpenAPI configuration as incomplete.
5. Review input validation, output and error contracts, authorization, persistence relationships, uniqueness and delete behavior, naming, folders, dependencies, and team patterns. Inspect files changed, uncommitted changes, and relevant commit history; identify work not represented by the task or plan.
6. Confirm existing services, repositories, handlers, validators, utilities, storage, extension methods, and business logic were reused where appropriate. Record justified exceptions and check that no duplicate or unrelated implementation was introduced.
7. Confirm every new or changed persisted field has resolved purpose, business meaning, type, nullability, constraints, relationships, default, update behavior, and business rules. Unknown or unapproved schema semantics are a delivery blocker.
8. Review scope boundaries by exact path across the whole branch. Every changed path must be owned by a task requirement or an approved step scope contract. Any changed path in another module, shared file, generated output, or unrelated configuration is a delivery blocker. Any deletion, rename, or move without explicit plan and step approval is a delivery blocker. Separate task-related failures from unrelated pre-existing failures; do not fix unrelated code or change existing behavior during final review without explicit approval.
9. Run only repository-appropriate checks permitted by documentation. Possible commands include `dotnet restore`, `dotnet build`, `dotnet test`, `dotnet format --verify-no-changes`, `git status`, `git diff`, and `git log --oneline`; select rather than assume them.
10. Record every command actually executed with result. Distinguish skipped, unavailable, failed, and passed checks.
11. Summarize test coverage, remaining risks, known limitations, recovery guidance, scope audit results, and manual verification that cannot be performed safely or locally.
12. Decide whether the branch is ready for manual push. Do not push or change Git state.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never push, commit, merge, switch branches, reset, rebase, force-push, or discard changes.
- Run only commands appropriate to the repository and its documented environment; do not claim any result without execution.
- Do not mark a branch ready when a required acceptance criterion, validation, or safety concern is unresolved.
- Keep external integration and manual environment gaps visible rather than simulating success.
- Keep `.otto/` artifacts untracked by default; if any are staged or tracked unexpectedly, report that as a push blocker.
- Do not fix unrelated failures, refactor unrelated modules, or broaden the task during final review.
- Do not claim API documentation, field readiness, reuse, or scope compliance without evidence from the final diff and reports.
- Do not mark the branch ready when any step has `BLOCKED_SCOPE_VIOLATION`, an unreviewed path change, or an unapproved deletion/rename/move.
- Do not claim a specialized skill was installed, read, or applied without explicit approval and source evidence.
- Do not edit the workflow state directly unless the developer explicitly asks to run this skill without the orchestrator and authorizes that update.

## Stop conditions

Stop with `Ready for push: No` if requirements are incomplete, validation fails, unreviewed/unexplained changes exist, any path is outside an approved step scope, an unapproved deletion/rename/move exists, a blocking risk remains, or required manual checks have not been accepted by the developer. Stop at the developer push gate even when ready.

## Required output

Produce a **Final Delivery Report**, using `../../templates/final-delivery-report.md`. Include completed and incomplete requirements, acceptance-criteria status, specialized-skill status, API documentation status, reuse assessment, database-field readiness, changed files, tests added, commands executed, build/test status, scope-boundary findings, recovery guidance, warnings, limitations, manual verification, commit/workspace review, and `Ready for push: Yes/No`.

## Handoff to the next skill

Stop for the **Developer Push Gate**. The developer decides whether to push manually; there is no automated downstream action.
