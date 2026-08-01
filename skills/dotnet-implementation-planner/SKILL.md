---
name: dotnet-implementation-planner
description: Create a detailed, developer-approved, stepwise HTML implementation plan for a resolved .NET company task. Use only after requirement-gap analysis confirms that no blocking clarification remains.
---

# .NET Implementation Planner

## Purpose

Turn a resolved task and its repository context into small, independently understandable vertical slices. Each slice delivers one testable endpoint or business capability across every repository layer it requires. Produce a lightweight standalone HTML plan; do not write production code.

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
- Task dossier state and evidence registry when the task is orchestrated.
- Cached project index when resuming.
- Task-context findings for API documentation, reusable components, database-field readiness, and scope boundaries.
- Specialized-skill assessment and, only when explicitly approved and installed, the installed skill's instructions and source reference.

## Workflow

1. Confirm the Requirement Gap Report contains no unresolved `BLOCKING` or `BA_CONFIRMATION_REQUIRED` issue and the specialized-skill gate is resolved as `NO_INSTALL_NEEDED`, `DECLINED`, or `INSTALLED`. Reconcile the dossier state, requirement ledger, project index, specialist evidence, and evidence freshness first. Stop otherwise.
2. Select only current references that match required structure and document their reuse limits.
3. Build an endpoint-and-capability coverage map before dividing work. Map every stated endpoint, acceptance criterion, and non-endpoint behavior to one primary delivery step. Keep a capability separate only when it has a distinct, testable outcome.
4. Produce a recommended ordinal execution order before implementation. Order steps by real repository dependencies and reviewability, state the reason for each dependency, and keep the order separate from the vertical-slice ownership map. The order may start with a technical prerequisite only when repository evidence shows it is required by multiple flows.
5. Default to one vertical step per endpoint or user-visible business flow. A vertical step includes every necessary layer for that flow—contract, controller or endpoint documentation, authorization, validation, application/domain behavior, persistence, endpoint wiring, errors, and focused tests—according to repository evidence. Use the repository's actual execution flow; do not assume a particular architecture.
6. Do not create phase steps such as “create entities”, “add DTOs”, “add handlers”, “add controllers”, or “add tests” for a task that defines endpoint behavior. Such layer-by-layer plans are invalid unless a documented technical prerequisite genuinely blocks multiple flows and has its own small, reviewable outcome. State that exception, its dependency, and why it cannot belong to the first affected flow.
7. Keep each endpoint's related validation, authorization, error behavior, API documentation, response examples, and tests in its own step. API documentation must cover applicable `400`, `401`, `403`, `404`, `409`, and other repository-supported error statuses without inventing responses. Do not combine endpoints merely because they edit the same files. Combine them only when the resolved task and repository evidence establish one atomic outcome; record the reason in the coverage map.
8. For every step specify: number, title, primary endpoint or business flow, request-to-result flow, goal, files to inspect/create/modify, detailed actions, reference implementations and reuse decision, controller-level API documentation, business rules, acceptance criteria, risks, dependencies, validation commands, expected result, rollback/recovery guidance, and suggested commit message. Cite requirement and evidence IDs. Use the HTTP method and route in an endpoint step title.
9. Check the coverage map before rendering: no endpoint, API documentation requirement, acceptance criterion, or test case may be unowned; no endpoint may appear in multiple steps without an explicit dependency reason; no new database field may be planned while field-readiness evidence is incomplete.
10. Render a standalone HTML plan from the supplied template. Include task summary, requirement status, architecture context, recommended ordinal execution order, references, endpoint-and-capability coverage, API documentation matrix, specialist-skill decision and evidence when applicable, table of contents, status-aware step cards, risk badges, validation checklist, commit suggestion, progress status, and final acceptance checklist.
11. Write the plan to `.otto/plans/<task-slug>-plan.html` in the target project unless project documentation specifies a different approved planning location. Create only the plan artifact required for this task.
12. Present the plan for developer approval. When invoked by the orchestrator, return the plan path, task slug, plan version/checksum when practical, and `AWAITING_PLAN_APPROVAL` transition for workflow-state recording. Do not execute a step, edit production code, or silently revise the plan after approval.

## Vertical-slice example

For the Certificate Management task, a normal plan shape is one step for `POST /api/certificates`, one for `GET /api/certificates`, one for `PUT /api/certificates/{id}`, and one for `DELETE /api/certificates/{id}`. A recommended order may place a proven shared persistence prerequisite before the first endpoint, followed by create, list, update, and delete only when repository dependencies justify that order. The create step may include the Certificate persistence model and any required schema change because they are needed to make creation work; it must also include create-specific uniqueness, authorization, controller-level API documentation, response/error examples, and tests. The delete step owns the assigned-user check and its test. Add a separate User-module step only if task-context investigation shows the acceptance criterion needs a change beyond the list endpoint.

This is a planning-shape example, not permission to assume endpoint contracts, data access, authorization, errors, or implementation technologies.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never plan from unresolved blocking ambiguity.
- Do not write production code, alter migrations, or modify unrelated documentation.
- Do not conceal assumptions, conflicts, risks, or unavailable validation.
- Do not segment an endpoint task by technical layer or separate an endpoint's tests from its behavior without a documented, explicit reason.
- Do not plan a new table, column, or persisted field while its field-understanding matrix has unknown purpose, meaning, type, nullability, constraints, relationships, default, update behavior, or business rules.
- Plan local controller or endpoint documentation for every introduced API. Do not change global Swagger, Scalar, or OpenAPI configuration; stop for developer approval if it is required.
- Prefer existing services, repositories, handlers, validators, utilities, storage, extension methods, and business logic. Record why a new implementation is necessary when no safe reusable component exists.
- Use an installed specialized skill only after explicit developer approval and after reading its instructions. Treat it as supplemental guidance; repository evidence and resolved requirements remain authoritative.
- Do not add dependencies, architecture, patterns, or future work merely because a specialized skill recommends them.
- Do not auto-approve the plan, auto-execute steps, commit, push, switch branches, or update the plan silently.
- Do not edit the workflow state directly unless the developer explicitly asks to run this skill without the orchestrator and authorizes that update.

## Stop conditions

Stop for clarification if a planned action requires an unresolved decision. Stop at the plan approval gate after generating the plan; continue only after the developer explicitly approves it.

## Required output

Produce a **Detailed Implementation Plan** and its standalone HTML file. Report its path, recommended ordinal execution order with dependency rationale, endpoint-and-capability coverage map, API documentation matrix, specialized-skill decision/evidence, reuse decisions, database-field readiness, all vertical-step details, source reports, assumptions, open non-blocking risks, rollback guidance, and the explicit **Plan Approval Gate**. The plan must use `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, or `BLOCKED` for each step status. Do not restate dossier facts in every step; cite their IDs and include only step-specific context.

## Handoff to the next skill

After explicit developer approval and an explicit request for one numbered step, pass the HTML plan path, requested step, resolved task specification, reports, and workspace boundaries to `dotnet-step-executor`.
