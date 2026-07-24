# OttoNet Skills

> Read. Learn. Ship.

Agent Skills that help .NET developers understand existing codebases, follow team conventions, and ship production-ready company tasks.

OttoNet is for .NET developers working on Business Analyst (BA) and Team Leader tasks in established company repositories. It treats a task as work to be understood in the context of a real codebase, not as a prompt to generate code immediately.

## Why understanding comes first

Existing projects have architecture, domain language, operational constraints, conventions, and sometimes local rules that are not visible in a single task description. OttoNet first protects the workspace, reads project guidance, maps the implementation, and learns from evidence before it interprets a BA task or changes code. This reduces invented requirements and keeps implementation aligned with the team.

## Workflow

```text
Inspect workspace
→ Read project documentation
→ Explore the base code
→ Learn completed team implementations
→ Read the BA task
→ Investigate task-specific context
→ Find requirement gaps and clarify blocking questions
→ Build and approve a detailed plan
→ Execute one developer-requested step
→ Review that step
→ Developer commits manually
→ Repeat as needed
→ Perform final delivery review
→ Developer pushes manually
```

## Skills

| Skill | Responsibility |
| --- | --- |
| [dotnet-workspace-inspector](skills/dotnet-workspace-inspector/SKILL.md) | Protect and describe the current Git workspace. |
| [dotnet-project-documentation-reader](skills/dotnet-project-documentation-reader/SKILL.md) | Extract project rules and operational guidance. |
| [dotnet-repository-explorer](skills/dotnet-repository-explorer/SKILL.md) | Map the actual .NET solution, modules, and request flow. |
| [dotnet-team-pattern-learner](skills/dotnet-team-pattern-learner/SKILL.md) | Learn evidence-backed implementation conventions. |
| [dotnet-task-analyzer](skills/dotnet-task-analyzer/SKILL.md) | Preserve and structure the BA or Team Leader task. |
| [dotnet-task-context-investigator](skills/dotnet-task-context-investigator/SKILL.md) | Find task-related code, relationships, and reuse points. |
| [dotnet-requirement-gap-analyzer](skills/dotnet-requirement-gap-analyzer/SKILL.md) | Resolve technical conventions and expose business ambiguity. |
| [dotnet-implementation-planner](skills/dotnet-implementation-planner/SKILL.md) | Produce an approved, stepwise HTML implementation plan. |
| [dotnet-step-executor](skills/dotnet-step-executor/SKILL.md) | Implement exactly one explicitly requested plan step. |
| [dotnet-step-reviewer](skills/dotnet-step-reviewer/SKILL.md) | Review a completed step before the developer commits. |
| [dotnet-final-delivery-reviewer](skills/dotnet-final-delivery-reviewer/SKILL.md) | Perform the final evidence-based delivery review. |
| [dotnet-company-task-orchestrator](skills/dotnet-company-task-orchestrator/SKILL.md) | Coordinate skills and enforce developer-controlled gates. |

## Usage concept

Keep this repository available to Codex as a skills source. In a cloned target project on an existing feature branch, begin with the orchestrator or invoke the first skill directly. Supply the BA task only after the documentation, repository, and team-pattern stages have completed.

Example invocation:

```text
Use dotnet-company-task-orchestrator to prepare a plan for
examples/certificate-management-task.md. Stop for clarification and plan approval;
do not implement code.
```

The report formats are in [templates](templates), and the Certificate Management task is a realistic, analysis-only example in [examples/certificate-management-task.md](examples/certificate-management-task.md).

## Safety boundaries

OttoNet assumes the developer already cloned the target repository and checked out a feature branch. It never clones, creates or switches branches, resets, rebases, discards changes, force-pushes, merges, or pushes. It never runs an entire implementation plan automatically. The developer explicitly approves the plan, requests each step, and commits and pushes manually.

Existing local changes are evidence to preserve, not obstacles to erase. Generic .NET guidance is used only when it does not conflict with resolved task requirements, project rules, or observed team patterns.

## Current status

Initial workflow version. The repository contains the complete skill set, report templates, HTML plan template, and an example BA task. It deliberately does not include application implementation code.
