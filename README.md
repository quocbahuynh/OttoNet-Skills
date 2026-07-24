# OttoNet Skills

> Ship GitLab task to production-ready code. AI skills think like your team, code like your team.

Agent Skills that help .NET developers understand existing codebases, follow team conventions, and ship production-ready company tasks.

OttoNet is for .NET developers working on Business Analyst, Team Leader, or GitLab tasks in established company repositories. It reads the project before planning code, so implementation follows the repository architecture, local conventions, and team delivery style.

## Workflow

```mermaid
flowchart TD
    A[Inspect workspace] --> B[Read project documentation]
    B --> C[Explore .NET repository]
    C --> D[Learn team patterns]
    D --> E[Analyze task]
    E --> F[Investigate task context]
    F --> G[Check requirement gaps]
    G --> H{Blocking questions?}
    H -- Yes --> I[Ask BA or Team Leader]
    I --> E
    H -- No --> J[Create HTML implementation plan]
    J --> K{Developer approves plan?}
    K -- No --> J
    K -- Yes --> L[Execute one requested step]
    L --> M[Review completed step]
    M --> N{Ready to commit?}
    N -- No --> L
    N -- Yes --> O[Developer commits manually]
    O --> P{More steps?}
    P -- Yes --> L
    P -- No --> Q[Final delivery review]
    Q --> R[Developer pushes manually]
```

## Skills

| Stage | Skills |
| --- | --- |
| Understand project | [dotnet-workspace-inspector](skills/dotnet-workspace-inspector/SKILL.md), [dotnet-project-documentation-reader](skills/dotnet-project-documentation-reader/SKILL.md), [dotnet-repository-explorer](skills/dotnet-repository-explorer/SKILL.md), [dotnet-team-pattern-learner](skills/dotnet-team-pattern-learner/SKILL.md) |
| Understand task | [dotnet-task-analyzer](skills/dotnet-task-analyzer/SKILL.md), [dotnet-task-context-investigator](skills/dotnet-task-context-investigator/SKILL.md), [dotnet-requirement-gap-analyzer](skills/dotnet-requirement-gap-analyzer/SKILL.md) |
| Plan and ship | [dotnet-implementation-planner](skills/dotnet-implementation-planner/SKILL.md), [dotnet-step-executor](skills/dotnet-step-executor/SKILL.md), [dotnet-step-reviewer](skills/dotnet-step-reviewer/SKILL.md), [dotnet-final-delivery-reviewer](skills/dotnet-final-delivery-reviewer/SKILL.md) |
| Orchestrate | [dotnet-company-task-orchestrator](skills/dotnet-company-task-orchestrator/SKILL.md) |

## Usage

Keep this repository available to Codex as a skills source. In a cloned target .NET project on an existing feature branch, start with the orchestrator.

Example:

```text
Use dotnet-company-task-orchestrator to prepare a plan for
examples/certificate-management-task.md. Stop for clarification and plan approval;
do not implement code.
```

Templates are in [templates](templates). The sample task is [examples/certificate-management-task.md](examples/certificate-management-task.md).

## Safety

OttoNet does not clone, create or switch branches, reset, rebase, discard changes, merge, force-push, push, or run the whole plan automatically. The developer approves the plan, requests one step at a time, and commits manually.

## Current status

Initial workflow version with 12 skills, report templates, an HTML plan template, and one example task.
