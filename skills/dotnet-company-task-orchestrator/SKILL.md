---
name: dotnet-company-task-orchestrator
description: Coordinate OttoNet's gated .NET company-task workflow from workspace inspection through final delivery review while preserving developer control over clarification, plan approval, each implementation step, commits, and push.
---

# .NET Company Task Orchestrator

## Purpose

Coordinate specialized OttoNet skills as a controlled workflow. The orchestrator is not an unrestricted autonomous coding agent and must stop at every developer-owned decision gate.

## When to use

Use to run the complete OttoNet workflow for a BA or Team Leader task, or to resume it from a documented gate. Use individual skills directly when only one stage is needed.

## Assumptions

- The developer already cloned the target repository and checked out the intended feature branch.
- The current directory is the target project root.
- The developer owns task clarification, plan approval, step requests, commits, and pushes.
- Repository review-system access may not exist; Git history is not proof of approval.
- Agent conversation context is temporary and cannot be the source of truth for a multi-stage task.

## Required inputs

- Target repository root.
- BA or Team Leader task when the task-analysis gate is reached.
- Any prior OttoNet reports, plan path, clarification answers, and explicit developer decisions when resuming.
- A task slug for new work, or the existing `.otto/tasks/<task-slug>/workflow-state.md` path when resuming.
- Optional current `.otto/project-index.md` when resuming.
- Optional requested operating mode: `FAST`, `STANDARD`, or `STRICT`.
- The current task identity: title, source reference, domain/module, and task slug.

## Task dossier and workflow memory

Use one task dossier for each task. The canonical state file indexes its evidence registry, reports, plan, workflow position, requirement resolutions, plan approval, step/commit decisions, protection boundaries, source freshness, and append-only continuity log. It is memory, not a substitute for evidence: detailed facts remain in the linked source locations.

- Default location: `.otto/tasks/<task-slug>/` in the target repository. Create `workflow-state.md` from `../../templates/task-workflow-state-template.md`, `evidence-registry.md` from `../../templates/evidence-registry-template.md`, refresh `.otto/project-index.md` after repository exploration, and generate plans under `.otto/plans/` only after the first workspace inspection is safe enough to continue.
- Treat the default location as a local, untracked sidecar. Never stage, commit, push, delete, or add it to ignore rules automatically. A developer may explicitly choose a repository-tracked location when team policy requires reviewable task artifacts.
- On resume, read the state, latest continuity event, and evidence registry first. Then re-run workspace inspection and compare repository root, branch, HEAD, protected paths, source freshness, current gate, and plan status. Reconcile differences visibly; never assume an `IN_PROGRESS` stage finished.
- Give each stable fact an evidence ID. Cite that ID in reports and plans rather than copying source code, full task text, or repeated Git diffs. A report records only its decision, scope, and delta since the last verified artifact.
- Record paths, short summaries, identifiers, and decisions only. Never copy secrets, full diffs, credentials, or sensitive task data into state.
- Update the state only after evidence is produced, when a gate changes, or immediately before a code-editing step begins. Append to the continuity log; do not erase historical evidence or silently change a decision.

## Fresh-session boundary

Before starting or resuming work, compare the current task identity with every active task dossier in `.otto/tasks/`. A task is unrelated when its scope, domain/module, acceptance criteria, and source identity do not materially overlap the active dossier. If an unrelated task is detected, stop before implementation and show the **Fresh Session Gate**:

1. Start a new Codex session with `/new`.
2. In the target repository, delete the old `.otto/` folder only after verifying that its task memory is no longer needed.
3. Start the new task from a clean task identity and create a new dossier.

Do not execute the deletion, reuse old task evidence, or continue implementation in the current session. A new task may proceed only after the fresh session has loaded its own dossier. If no active dossier exists, treat the task as new and continue with Gate 1.

## Specialized .NET skill recommendation gate

Before planning or implementation, assess whether the task is advanced, unfamiliar, or high-risk enough to benefit from a specialized skill in the official [.NET skills repository](https://github.com/dotnet/skills). Examples include complex ASP.NET Core architecture, authentication or authorization, EF Core migrations, distributed systems, background processing, cloud deployment, performance, security-sensitive work, advanced testing, large-scale refactoring, or a technology/pattern not established in the repository.

1. Decide whether the current OttoNet workflow and repository evidence already provide enough guidance.
2. Identify the exact technical area where guidance is missing or risk is elevated.
3. Recommend the available `find-skills` capability (or the host's equivalent `find-skill` command) to search for a relevant skill in `https://github.com/dotnet/skills`.
4. Inspect the candidate's name, scope, source, and availability. Do not claim a skill exists or is installed without evidence.
5. Ask the developer for explicit permission to install a specific candidate, explaining the technical risk it addresses and what it will not change.
6. Stop at this gate while approval is pending. Do not install or use the skill, and do not begin implementation, without approval.
7. If no suitable skill is available or the current workflow is sufficient, record `NO_INSTALL_NEEDED` and continue with the existing workflow while stating assumptions and residual risks.

After approval and installation, read the installed skill instructions before modifying code. Combine them with repository documentation, resolved requirements, team patterns, and evidence priority. The existing codebase remains the primary source of truth; an installed skill must not introduce conflicting architecture, conventions, dependencies, or behavior. Keep its use within the current task scope.

## Operating modes

Select the least costly safe mode before discovery. Record the mode decision and evidence in the dossier; a developer may request a stricter mode. Modes reduce repeated inspection, never developer control or mandatory safety gates.

| Mode | Eligibility | Required behavior |
| --- | --- | --- |
| `FAST` | Narrow, low-risk work; a current dossier exists; no requirement ambiguity; no migrations, authorization, external integration, sensitive-domain, or architecture change. | Re-run workspace inspection and revalidate only changed or task-related documents, project areas, patterns, and context. Use the existing evidence registry. |
| `STANDARD` | Default for features, endpoints, business rules, or a new task dossier. | Establish or refresh all workflow evidence with breadth-first project mapping and task-specific investigation. |
| `STRICT` | New modules, migrations, authorization, external integrations, sensitive domains, unclear architecture, high-impact deletion/data behavior, or developer request. | Use Standard coverage plus wider dependency tracing, stronger reference sampling, explicit risk review, and proportionate extra validation. |

Reject `FAST` and choose `STANDARD` or `STRICT` when source fingerprints are stale, the task spans an unmodeled area, requirements are ambiguous, or evidence is insufficient. Do not use a mode label as a reason to skip a required gate.

## Workflow

0. Perform the Fresh Session Gate check. If the task is unrelated to an active dossier, stop and show the `/new` and `.otto/` cleanup reminder before any implementation work.
1. Run `dotnet-workspace-inspector`. If safe enough to proceed, create or reconcile the dossier, record its protection boundary and recovery-point recommendation, and select the operating mode.
2. Reuse an artifact only when its source freshness register is current and its scope covers the task. Otherwise run the relevant skill and record the delta. Never treat a previous chat response as reusable evidence.
3. Run `dotnet-project-documentation-reader`, record report and evidence IDs, then satisfy Gate 2 only after applicable documentation and architecture evidence are current.
4. Run `dotnet-repository-explorer`, then record the Project Understanding Report, refresh `.otto/project-index.md`, and record the project map fingerprint and actual request-flow evidence.
5. Run `dotnet-team-pattern-learner`, record classifications, sample limits, and selected references, then satisfy Gate 3.
6. Run `dotnet-task-analyzer` only after project understanding and patterns are current. Record source revision, requirement IDs, and the field-understanding matrix.
7. Run `dotnet-task-context-investigator` from the task dependency graph; record related modules, reusable components, API documentation conventions, database-field readiness, explored boundary, and task/code conflicts.
8. Run `dotnet-requirement-gap-analyzer`, update the resolution ledger, and stop at clarification when required. Do not permit schema work with unresolved field semantics or global API-documentation configuration changes.
9. Run the Specialized .NET Skill Recommendation Gate. Record why the current workflow is sufficient or identify the specific candidate search and approval state. Stop before planning or implementation when developer approval to install a relevant skill is pending.
10. When all blocking questions and specialist decisions are resolved, run `dotnet-implementation-planner`, register the HTML plan, recommended ordinal execution order, API documentation matrix, reuse decisions, specialist-skill evidence, and requirement-to-step coverage map, then stop for explicit plan approval.
11. After approval, record approval evidence. Before the first significant code change, show the non-executed recovery options from workspace inspection and let the developer decide whether to create a recovery point. After the developer explicitly requests one numbered step, transition only that step from `NOT_STARTED` to `IN_PROGRESS`, run `dotnet-step-executor`, then transition it to `AWAITING_REVIEW` and run `dotnet-step-reviewer`.
12. Record the review outcome. Before any commit or push, re-run workspace inspection and verify no Otto-owned `.otto/` artifact is staged or unexpectedly tracked; if one is, stop and keep it uncommitted. Stop for the developer's commit decision; record either the commit SHA after a new inspection or the developer's explicit decision to continue without a commit. Only then allow the next explicitly requested step.
13. After all required steps are reviewed and reconciled with the state, run `dotnet-final-delivery-reviewer`, record its decision, and stop for manual push.

## Evidence priority

Use this order for every skill decision: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never clone, create/switch branches, reset, rebase, force-push, discard changes, commit automatically, push, or merge.
- Never execute an entire plan or continue to a future step automatically.
- Never hide assumptions or continue through blocking ambiguity.
- Preserve existing local changes and make each gate decision visible.
- Do not claim merge-request approval or review resolution from Git history alone.
- Never treat chat history, a previous model response, or an unverified `IN_PROGRESS` state as proof that a stage or code change completed.
- Never let Otto-owned `.otto/` artifacts obscure pre-existing user changes; record them as sidecars in the protection boundary and keep them out of staged commits unless the user explicitly chooses a repository-tracked location.
- Never re-run broad discovery by default when a current dossier can answer the question; revalidate the relevant evidence boundary instead.
- Never use `FAST` mode for a task whose risk or stale evidence makes `STANDARD` or `STRICT` necessary.
- Never continue an unrelated task in the current session; stop at the Fresh Session Gate and do not delete `.otto/` automatically.
- Never plan or implement a new database field while its purpose, meaning, type, nullability, constraints, relationships, default, update behavior, or business rules are unresolved.
- Never change global Swagger, Scalar, or OpenAPI configuration without explicit developer approval; prefer local controller or endpoint documentation.
- Never create or execute rollback commands automatically; present safe recovery options for developer approval only.
- Never expand beyond task scope to fix unrelated failures, refactor unrelated code, or change existing behavior without explicit approval.
- Never install or use an external or specialized skill without explicit developer approval and a recorded candidate/scope decision.
- Never let an installed skill override repository instructions, resolved requirements, evidence priority, or established project patterns.
- Never recommend installation merely because a task uses .NET; require an advanced, unfamiliar, or risk-reducing technical justification.

## Stop conditions

Stop at each mandatory gate below. Resume only with the stated developer input or required evidence.

| Gate | Required state | Resume condition |
| --- | --- | --- |
| Fresh Session Gate | Task identity is unrelated to any active dossier | Developer starts `/new` and removes stale `.otto/` memory manually |
| 1. Workspace protection | Workspace and existing changes understood | Safe state or developer direction |
| 2. Project understanding | Documentation and architecture understood | Required reports complete |
| 3. Team patterns | Evidence and classifications documented | Pattern report complete |
| 4. Task extraction | Requirements preserved | Task report complete |
| 5. Clarification | No blocking question remains | BA/Team Leader resolution |
| 5a. Specialized skill recommendation | Current workflow suffices, or a candidate is approved/declined | Recorded decision; explicit developer approval before installation when needed |
| 6. Plan approval | Detailed HTML plan presented | Explicit developer approval |
| 7. Step request | One step selected | Explicit numbered request |
| 8. Step review | Requested step reviewed | Review pass or corrective request |
| 9. Commit | Developer controls Git commit | Developer decision, then next explicit step request |
| 10. Final delivery | Final review complete | Developer manually pushes or requests follow-up |

## Required output

Produce an **OttoNet Workflow Status** after every stage and update the dossier: session-boundary result, operating mode and rationale, completed or reused artifacts, evidence limits and freshness, recovery-point recommendation, current gate, blocking questions, approved assumptions, specialized-skill assessment and approval state, installed-skill instruction evidence when applicable, plan path, execution order, API documentation status, reuse decisions, database-field readiness, step status when present, and the exact developer action required to continue. Preserve paths and IDs to all generated or revalidated evidence.

## Handoff to the next skill

Dispatch only the next permitted named skill listed in the workflow. At a developer-controlled gate, hand off to the developer rather than another skill.
