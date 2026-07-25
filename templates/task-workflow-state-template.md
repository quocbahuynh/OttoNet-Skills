# OttoNet Task Dossier — Workflow State

> Canonical, resumable workflow memory and index for one company task. Keep this file concise: link to evidence instead of copying reports, source code, or diffs. Do not record credentials, connection strings, tokens, or sensitive customer data.

## State rules

- Create one task dossier per task at `.ottonet/tasks/<task-slug>/` by default. Its canonical state file is `workflow-state.md`; reports and the evidence registry are sibling artifacts.
- Treat this file as a local sidecar unless the developer explicitly chooses a repository-tracked location.
- Never stage, commit, push, or silently delete this file.
- Update it after a stage completes, when a gate changes, or immediately before a code-editing step begins. Append continuity events; do not rewrite prior evidence or silently change a decision.
- A missing or stale state file is a reason to inspect and reconcile, not to guess or repeat implementation work.
- Store stable claims once in `evidence-registry.md`; other artifacts cite its IDs and only add their decision, scope, or delta.

## Task identity

| Field | Value |
| --- | --- |
| Task title | `<task title>` |
| Task slug | `<task-slug>` |
| Source task | `<ticket URL, file path, or stable reference>` |
| Target repository | `<canonical repository path>` |
| Repository remote | `<sanitized origin URL or unavailable>` |
| Workflow started | `<ISO 8601 timestamp>` |
| State schema | `2` |

## Repository baseline and protection boundary

| Field | Value |
| --- | --- |
| Branch at first inspection | `<branch or detached HEAD>` |
| HEAD at first inspection | `<commit SHA>` |
| Baseline workspace status | `<clean / dirty, with report path>` |
| Protected pre-existing paths | `<paths or none>` |
| Protected branch warning | `<yes/no and reason>` |
| Latest workspace inspection | `<report path and timestamp>` |

## Current workflow position

| Field | Value |
| --- | --- |
| Operating mode | `<FAST / STANDARD / STRICT>` |
| Mode decision and evidence | `<why this mode is safe; evidence ID>` |
| Workflow status | `<DISCOVERY / BLOCKED / AWAITING_PLAN_APPROVAL / AWAITING_STEP_REQUEST / AWAITING_REVIEW / AWAITING_COMMIT_DECISION / READY_FOR_FINAL_REVIEW / COMPLETE>` |
| Current gate | `<1–10 and gate name>` |
| Last confirmed stage | `<skill name and timestamp>` |
| Next authorized action | `<exact developer or skill action>` |
| Blocking issue count | `<number>` |
| Open risk count | `<number>` |

### Authorized state transitions

Only advance when the matching evidence and developer input exist. Do not skip a state because an earlier report looks complete.

```text
DISCOVERY → BLOCKED | AWAITING_PLAN_APPROVAL
AWAITING_PLAN_APPROVAL → AWAITING_STEP_REQUEST
AWAITING_STEP_REQUEST → AWAITING_REVIEW
AWAITING_REVIEW → AWAITING_COMMIT_DECISION | BLOCKED
AWAITING_COMMIT_DECISION → AWAITING_STEP_REQUEST | READY_FOR_FINAL_REVIEW
READY_FOR_FINAL_REVIEW → COMPLETE | BLOCKED
```

`BLOCKED` may return only to the state justified by newly recorded resolution evidence. A developer commit decision is required before another step request, even when the decision is to continue without committing.

## Gate register

| Gate | State | Evidence | Developer action required |
| --- | --- | --- | --- |
| 1. Workspace protection | `NOT_REACHED` | `<report path>` | `<action>` |
| 2. Project understanding | `NOT_REACHED` | `<report paths>` | `<action>` |
| 3. Team patterns | `NOT_REACHED` | `<report path>` | `<action>` |
| 4. Task extraction | `NOT_REACHED` | `<report path>` | `<action>` |
| 5. Clarification | `NOT_REACHED` | `<gap report / clarification reference>` | `<action>` |
| 6. Plan approval | `NOT_REACHED` | `<plan path and approval evidence>` | `<action>` |
| 7. Step request | `NOT_REACHED` | `<explicit requested step>` | `<action>` |
| 8. Step review | `NOT_REACHED` | `<step completion report>` | `<action>` |
| 9. Commit decision | `NOT_REACHED` | `<developer decision / commit SHA>` | `<action>` |
| 10. Final delivery | `NOT_REACHED` | `<final delivery report>` | `<action>` |

Allowed gate states: `NOT_REACHED`, `IN_PROGRESS`, `WAITING_FOR_DEVELOPER`, `BLOCKED`, `SATISFIED`.

## Dossier index

| Artifact | Path | Scope / freshness | Recorded at |
| --- | --- | --- | --- |
| Workspace inspection | `<path>` | `<complete / limited / unavailable>` | `<timestamp>` |
| Evidence registry | `<path>` | `<source fingerprint / freshness>` | `<timestamp>` |
| Project documentation | `<path>` | `<new / reused / delta>` | `<timestamp>` |
| Project understanding | `<path>` | `<new / reused / delta>` | `<timestamp>` |
| Team patterns | `<path>` | `<new / reused / delta>` | `<timestamp>` |
| Task requirements | `<path>` | `<new / revised>` | `<timestamp>` |
| Task context | `<path>` | `<new / revised>` | `<timestamp>` |
| Requirement gaps | `<path>` | `<new / resolved / blocked>` | `<timestamp>` |
| Implementation plan | `<path>` | `<draft / approved / superseded>` | `<timestamp>` |
| Step execution reports | `<paths>` | `<complete / partial / unavailable>` | `<timestamp>` |
| Step completion reports | `<paths>` | `<complete / partial / unavailable>` | `<timestamp>` |
| Final delivery report | `<path>` | `<complete / limited / unavailable>` | `<timestamp>` |

## Source freshness register

Use this to decide whether an earlier artifact can be reused. A changed fingerprint requires targeted revalidation; it does not by itself require re-reading the whole repository.

| Source area | Fingerprint or revision | Last verified | Reuse decision | Evidence |
| --- | --- | --- | --- | --- |
| Repository baseline | `<HEAD / branch / workspace report>` | `<timestamp>` | `<current / stale>` | `<evidence ID>` |
| Documentation and configuration | `<paths + revision>` | `<timestamp>` | `<current / stale>` | `<evidence ID>` |
| Architecture map | `<solution/project files + revision>` | `<timestamp>` | `<current / stale>` | `<evidence ID>` |
| Team-pattern sample | `<commit range / references>` | `<timestamp>` | `<current / stale>` | `<evidence ID>` |
| Task-specific context | `<search terms + revision>` | `<timestamp>` | `<current / stale>` | `<evidence ID>` |

## Requirement resolution ledger

| Requirement or question | Status | Resolution or assumption | Evidence | Owner / date |
| --- | --- | --- | --- | --- |
| `<item>` | `<OPEN / RESOLVED / ASSUMPTION_ALLOWED / REJECTED>` | `<concise decision>` | `<task section, report, or task-owner response>` | `<person or role / date>` |

## Evidence registry summary

| Evidence ID | Claim or source | Strength | Location / revision | Reuse limit |
| --- | --- | --- | --- | --- |
| `E-001` | `<concise evidence-backed fact>` | `<REQUIRED / APPROVED / ESTABLISHED / COMMON / LEGACY / UNKNOWN>` | `<path:line, ticket, or commit>` | `<what it does not prove>` |

## Plan and step register

| Field | Value |
| --- | --- |
| Approved plan | `<path or not approved>` |
| Plan approval evidence | `<explicit developer approval and timestamp>` |
| Plan version / checksum | `<identifier or unavailable>` |
| Last plan reconciliation | `<timestamp and summary>` |

| Step | Title | Execution state | Review | Commit decision | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | `<title>` | `NOT_STARTED` | `NOT_REVIEWED` | `NOT_DECIDED` | `<plan section / report paths>` |

Allowed execution states: `NOT_STARTED`, `IN_PROGRESS`, `AWAITING_REVIEW`, `AWAITING_COMMIT_DECISION`, `COMMITTED`, `BLOCKED`.

## Risk and handoff register

| Type | Description | Status | Evidence / owner | Next action |
| --- | --- | --- | --- | --- |
| `<blocking question, risk, or constraint>` | `<concise description>` | `<OPEN / ACCEPTED / RESOLVED>` | `<evidence>` | `<exact next action>` |

## Continuity log (append only)

| Timestamp | Actor | Event | Evidence or affected paths | Result / next action |
| --- | --- | --- | --- | --- |
| `<ISO 8601 timestamp>` | `<developer / agent>` | `<event>` | `<paths or report>` | `<outcome>` |

## Resume checklist

1. Verify the repository identity, branch, HEAD, and workspace status against this state file.
2. Read the latest artifact for the current gate and the most recent continuity event.
3. Reconcile any difference before doing work; never infer that an in-progress step completed.
4. Continue only with the exact action listed in **Next authorized action** and the required developer decision.
