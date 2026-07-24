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

## Required inputs

- Target repository root.
- BA or Team Leader task when the task-analysis gate is reached.
- Any prior OttoNet reports, plan path, clarification answers, and explicit developer decisions when resuming.

## Workflow

1. Run `dotnet-workspace-inspector`.
2. Run `dotnet-project-documentation-reader`.
3. Run `dotnet-repository-explorer`.
4. Run `dotnet-team-pattern-learner`.
5. Run `dotnet-task-analyzer` only after project understanding and patterns are documented.
6. Run `dotnet-task-context-investigator`.
7. Run `dotnet-requirement-gap-analyzer` and stop at clarification when required.
8. When all blocking questions are resolved, run `dotnet-implementation-planner` and stop for plan approval.
9. After the developer explicitly requests one step, run `dotnet-step-executor`, then `dotnet-step-reviewer`.
10. Stop for the developer's commit decision. Repeat only when the developer explicitly requests the next numbered step.
11. After all required steps are reviewed, run `dotnet-final-delivery-reviewer` and stop for manual push.

## Evidence priority

Use this order for every skill decision: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never clone, create/switch branches, reset, rebase, force-push, discard changes, commit automatically, push, or merge.
- Never execute an entire plan or continue to a future step automatically.
- Never hide assumptions or continue through blocking ambiguity.
- Preserve existing local changes and make each gate decision visible.
- Do not claim merge-request approval or review resolution from Git history alone.

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

Produce an **OttoNet Workflow Status** after every stage: completed reports, evidence limits, current gate, blocking questions, approved assumptions, plan path and step status when present, and the exact developer action required to continue. Preserve links or paths to all generated reports.

## Handoff to the next skill

Dispatch only the next permitted named skill listed in the workflow. At a developer-controlled gate, hand off to the developer rather than another skill.
