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
- A task slug for new work, or the existing OttoNet workflow-state path when resuming.

## Workflow memory

Use one canonical state file for each task. It records workflow position, gates, report paths, requirement resolutions, plan approval, step/commit decisions, protection boundaries, and an append-only continuity log. It is memory, not a substitute for evidence: detailed facts remain in the referenced reports and plan.

- Default location: `.ottonet/tasks/<task-slug>/workflow-state.md` in the target repository, created from `../../templates/task-workflow-state-template.md` only after the first workspace inspection is safe enough to continue.
- Treat the default location as a local, untracked sidecar. Never stage, commit, push, delete, or add it to ignore rules automatically. A developer may explicitly choose a repository-tracked location when team policy requires reviewable task artifacts.
- On resume, read the state first, then re-run workspace inspection and compare repository root, branch, HEAD, protected paths, current gate, and the latest continuity event. Reconcile differences visibly; never assume an `IN_PROGRESS` stage finished.
- Record paths, short summaries, identifiers, and decisions only. Never copy secrets, full diffs, credentials, or sensitive task data into state.
- Update the state only after evidence is produced, when a gate changes, or immediately before a code-editing step begins. Append to the continuity log; do not erase historical evidence.

## Workflow

1. Run `dotnet-workspace-inspector`. If safe enough to proceed, create or reconcile the workflow state and record its protection boundary.
2. Run `dotnet-project-documentation-reader`, record the report path and satisfy Gate 2 only after its evidence is available.
3. Run `dotnet-repository-explorer`, then record the Project Understanding Report.
4. Run `dotnet-team-pattern-learner`, record its classifications and satisfy Gate 3.
5. Run `dotnet-task-analyzer` only after project understanding and patterns are documented; record the source task and requirement report.
6. Run `dotnet-task-context-investigator` and record related modules, references, and task/code conflicts.
7. Run `dotnet-requirement-gap-analyzer`, update the resolution ledger, and stop at clarification when required.
8. When all blocking questions are resolved, run `dotnet-implementation-planner`, register the HTML plan, and stop for explicit plan approval.
9. After approval, record the approval evidence. After the developer explicitly requests one numbered step, mark only that step `IN_PROGRESS`, run `dotnet-step-executor`, then mark it `AWAITING_REVIEW` and run `dotnet-step-reviewer`.
10. Record the review outcome. Stop for the developer's commit decision; record either the commit SHA after a new inspection or the developer's explicit decision to continue without a commit. Repeat only when the developer explicitly requests the next numbered step.
11. After all required steps are reviewed and reconciled with the state, run `dotnet-final-delivery-reviewer`, record its decision, and stop for manual push.

## Evidence priority

Use this order for every skill decision: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never clone, create/switch branches, reset, rebase, force-push, discard changes, commit automatically, push, or merge.
- Never execute an entire plan or continue to a future step automatically.
- Never hide assumptions or continue through blocking ambiguity.
- Preserve existing local changes and make each gate decision visible.
- Do not claim merge-request approval or review resolution from Git history alone.
- Never treat chat history, a previous model response, or an unverified `IN_PROGRESS` state as proof that a stage or code change completed.
- Never let the workflow-state file obscure pre-existing user changes; record it as an OttoNet-owned sidecar in the protection boundary.

## Stop conditions

Stop at each mandatory gate below. Resume only with the stated developer input or required evidence.

| Gate | Required state | Resume condition |
| --- | --- | --- |
| 1. Workspace protection | Workspace and existing changes understood | Safe state or developer direction |
| 2. Project understanding | Documentation and architecture understood | Required reports complete |
| 3. Team patterns | Evidence and classifications documented | Pattern report complete |
| 4. Task extraction | Requirements preserved | Task report complete |
| 5. Clarification | No blocking question remains | BA/Team Leader resolution |
| 6. Plan approval | Detailed HTML plan presented | Explicit developer approval |
| 7. Step request | One step selected | Explicit numbered request |
| 8. Step review | Requested step reviewed | Review pass or corrective request |
| 9. Commit | Developer controls Git commit | Developer decision, then next explicit step request |
| 10. Final delivery | Final review complete | Developer manually pushes or requests follow-up |

## Required output

Produce an **OttoNet Workflow Status** after every stage and update the workflow state: completed reports, evidence limits, current gate, blocking questions, approved assumptions, plan path and step status when present, and the exact developer action required to continue. Preserve links or paths to all generated reports.

## Handoff to the next skill

Dispatch only the next permitted named skill listed in the workflow. At a developer-controlled gate, hand off to the developer rather than another skill.
