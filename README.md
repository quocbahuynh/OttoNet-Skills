# OttoNet Skills

> Ship GitLab task to production-ready code. AI skills think like your team, code like your team.

OttoNet is a collection of Agent Skills for .NET teams delivering Business Analyst, Team Leader, and GitLab tasks in existing company codebases. It establishes evidence-based project understanding before implementation, so every change follows the repository architecture, conventions, and delivery practices already in place.

## Why OttoNet

- **Codebase-aware** — documentation, architecture, active code, and approved patterns are examined before the task is planned.
- **Evidence-led** — repository rules and resolved requirements take precedence over generic .NET practices.
- **Developer-controlled** — the developer approves the plan, requests each implementation step, and decides when to commit and push.

## Get started

From the root of an existing .NET project on the feature branch you intend to work on:

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent codex
```

Start a new agent task with the BA, Team Leader, or GitLab requirement, then use this prompt:

```text
Use dotnet-company-task-orchestrator for this GitLab task, but stop at every required developer-controlled gate.
```

OttoNet first learns the repository, then creates an HTML implementation plan for approval. After approval, it executes and reviews only the single step the developer requests.

### Resume safely with workflow memory

For a multi-step task, the orchestrator maintains one canonical state file at `.ottonet/tasks/<task-slug>/workflow-state.md`. It records the current gate, report paths, resolved decisions, approved plan, step/review/commit status, and a short append-only handoff log. This lets a later agent or session resume from verified evidence instead of relying on chat memory.

The file is a local sidecar by default: OttoNet does not stage, commit, push, delete, or add it to ignore rules. Teams that require task artifacts in version control can explicitly choose a repository-tracked location.

## Workflow

```mermaid
flowchart TD
    A[Inspect workspace] --> B[Read project documentation]
    B --> C[Explore .NET repository]
    C --> D[Learn team patterns]
    D --> E[Analyze task]
    E --> F[Investigate task context]
    F --> G[Resolve requirement gaps]
    G --> H{Blocking questions?}
    H -- Yes --> I[Ask BA or Team Leader]
    I --> E
    H -- No --> J[Create HTML implementation plan]
    J --> K{Developer approves plan?}
    K -- Yes --> L[Execute one requested step]
    K -- No --> J
    L --> M[Review completed step]
    M --> N{Developer commits?}
    N -- Yes --> O{More steps?}
    N -- No --> L
    O -- Yes --> L
    O -- No --> P[Final delivery review]
    P --> Q[Developer pushes manually]
```

## Skills

| Skill | Purpose | Typical usage |
| --- | --- | --- |
| [dotnet-workspace-inspector](skills/dotnet-workspace-inspector/SKILL.md) | Protect the current Git workspace before analysis or implementation. | Inspect the target project before work begins or a requested step starts. |
| [dotnet-project-documentation-reader](skills/dotnet-project-documentation-reader/SKILL.md) | Extract repository rules, guidance, and operating instructions. | Read project documentation before the task. |
| [dotnet-repository-explorer](skills/dotnet-repository-explorer/SKILL.md) | Map the solution, modules, dependencies, and request flow. | Build project understanding from the existing codebase. |
| [dotnet-team-pattern-learner](skills/dotnet-team-pattern-learner/SKILL.md) | Identify evidence-backed coding conventions and classify their strength. | Study active code, history, and review evidence. |
| [dotnet-task-analyzer](skills/dotnet-task-analyzer/SKILL.md) | Preserve and structure a BA or Team Leader task without inventing behavior. | Extract requirements, contracts, rules, and unknowns. |
| [dotnet-task-context-investigator](skills/dotnet-task-context-investigator/SKILL.md) | Find task-related code, relationships, and reusable references. | Investigate a task’s domain and related modules. |
| [dotnet-requirement-gap-analyzer](skills/dotnet-requirement-gap-analyzer/SKILL.md) | Expose missing, ambiguous, conflicting, or blocked requirements. | Decide whether the task is ready for planning. |
| [dotnet-implementation-planner](skills/dotnet-implementation-planner/SKILL.md) | Produce a small-step HTML implementation plan. | Plan a fully clarified task for developer approval. |
| [dotnet-step-executor](skills/dotnet-step-executor/SKILL.md) | Implement exactly one approved plan step. | Execute a specifically requested step only. |
| [dotnet-step-reviewer](skills/dotnet-step-reviewer/SKILL.md) | Review one completed step before commit. | Check scope, requirements, validation, and consistency. |
| [dotnet-final-delivery-reviewer](skills/dotnet-final-delivery-reviewer/SKILL.md) | Review complete delivery readiness. | Verify the branch before a manual push. |
| [dotnet-company-task-orchestrator](skills/dotnet-company-task-orchestrator/SKILL.md) | Coordinate the workflow while enforcing developer-controlled gates. | Manage a GitLab task from inspection to final review. |

## Installation

OttoNet is distributed directly from this public GitHub repository through the `skills` CLI; no npm package or project dependency is required.

```bash
# Add the repository and choose skills interactively
npx skills add quocbahuynh/OttoNet-Skills

# List available skills without installing
npx skills add quocbahuynh/OttoNet-Skills --list

# Install the orchestrator only
npx skills add quocbahuynh/OttoNet-Skills \
  --skill dotnet-company-task-orchestrator

# Install every skill for Codex globally
npx skills add quocbahuynh/OttoNet-Skills \
  --skill '*' \
  --agent codex \
  --global
```

Use the flags supported by your installed `skills` CLI and target agent.

## Supported AI agents

OttoNet uses the portable Agent Skills format: each skill is a `SKILL.md` file with `name` and `description` frontmatter. It does not depend on vendor-specific hooks or metadata.

Common `skills` CLI targets include:

| Agent | `--agent` value |
| --- | --- |
| Codex | `codex` |
| Claude Code | `claude-code` |
| Cursor | `cursor` |
| Cline | `cline` |
| Gemini CLI | `gemini-cli` |
| GitHub Copilot | `github-copilot` |
| Kiro CLI | `kiro-cli` |
| OpenCode | `opencode` |
| OpenHands | `openhands` |
| Roo Code | `roo` |
| Windsurf | `windsurf` |

For example, install all OttoNet skills for Claude Code in the current project:

```bash
npx skills add quocbahuynh/OttoNet-Skills --skill '*' --agent claude-code
```

The [skills CLI supported-agent list](https://github.com/vercel-labs/skills#supported-agents) is the source of truth for the current full target list. Core OttoNet instructions are portable, while tool access, discovery behavior, and advanced capabilities remain agent-specific.

## Example prompts

```text
Use dotnet-project-documentation-reader to understand this repository before reading the task.
```

```text
Use dotnet-team-pattern-learner to study completed implementations and identify the team's coding conventions.
```

```text
Read the approved implementation plan and execute Step 3 only.
```

Supported agents can select skills from the frontmatter description. Use `dotnet-company-task-orchestrator` when the full gated workflow is required.

## Safety model

OttoNet never automatically:

- Clones repositories, creates or switches branches, resets changes, or discards local work.
- Commits unless explicitly instructed, pushes, or merges.
- Executes an entire implementation plan without developer approval.
- Continues when a business requirement remains unresolved.

The developer remains accountable for plan approval, step selection, commits, and pushes.

## Repository resources

- [Templates](templates) for project, task, review, and standalone HTML plan reports.
- [Workflow state template](templates/task-workflow-state-template.md) for resumable task memory.
- [Certificate Management example](examples/certificate-management-task.md) with a realistic source task.
- `python3 scripts/validate-skills.py` to validate skill metadata.
- [MIT License](LICENSE).

## Recommended GitHub topics

`agent-skills` · `dotnet` · `codex` · `claude-code` · `developer-tools` · `gitlab` · `software-engineering`

## Author and support

Built by [Quoc Ba Huynh](https://github.com/quocbahuynh). If OttoNet helps you save time and ship better .NET tasks, you can support the project on [Buy Me a Coffee](https://buymeacoffee.com/quochb).
