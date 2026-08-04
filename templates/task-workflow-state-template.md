# OttoNet Task Dossier — Workflow State

> Canonical, resumable workflow memory and index for one company task. Keep this file concise: link to evidence instead of copying reports, source code, or diffs. Do not record credentials, connection strings, tokens, or sensitive customer data.

## Resume state (read this first)

This is the only compact memory block required for a resume. Keep it to these fields and short IDs; never paste the task, source code, full reports, or full diffs here.

| Field | Value |
| --- | --- |
| Task identity | `<title / slug / source reference>` |
| Repository baseline | `<root / branch / HEAD / workspace status>` |
| Current gate and status | `<gate / workflow status / last confirmed stage>` |
| Next authorized action | `<one exact developer or skill action>` |
| Current step and scope | `<step ID; allowlist; forbidden paths; operations; deletions>` |
| Requirements and decisions | `<requirement, acceptance, and decision IDs>` |
| Evidence to read next | `<short list of IDs and paths>` |
| Blockers and risks | `<issue IDs and status, or none>` |
| Last validation | `<commands and result, or not run>` |
| Last checkpoint | `<timestamp / completed result / next action>` |

Resume rules:

1. Read this block, the latest continuity event, and only the current gate artifact or requested plan step before expanding context.
2. Update it after every gate, clarification, execution, review, and validation; append the continuity event rather than rewriting history.
3. If it is missing or conflicts with evidence, mark the workflow `BLOCKED`, run workspace inspection, and reconcile before analysis or editing. Never guess from chat history.

## State rules

- Create one task dossier per task at `.otto/tasks/<task-slug>/` by default. Its canonical state file is `.otto/tasks/<task-slug>/workflow-state.md`; reports and the evidence registry are sibling artifacts. Generated plans live under `.otto/plans/`. The cached project index lives at `.otto/project-index.md`.
- Treat this file as a local sidecar unless the developer explicitly chooses a repository-tracked location.
- Never stage, commit, push, or silently delete this file.
- Update it after a stage completes, when a gate changes, immediately before a code-editing step begins, and immediately after validation. Append continuity events; do not rewrite prior evidence or silently change a decision.
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
| Workflow status | `<DISCOVERY / AWAITING_FRESH_SESSION / BLOCKED / BLOCKED_SCOPE_VIOLATION / AWAITING_PLAN_APPROVAL / AWAITING_STEP_REQUEST / AWAITING_REVIEW / AWAITING_COMMIT_DECISION / READY_FOR_FINAL_REVIEW / COMPLETE>` |
| Current gate | `<0–10, 5a, and gate name>` |
| Last confirmed stage | `<skill name and timestamp>` |
| Next authorized action | `<exact developer or skill action>` |
| Blocking issue count | `<number>` |
| Open risk count | `<number>` |
| Current step scope status | `<NOT_REACHED / CLEAN / BLOCKED_SCOPE_VIOLATION>` |
| Current step allowed paths | `<exact paths or patterns>` |
| Current step forbidden paths | `<exact module/shared/generated boundaries>` |
| Current step explicit deletions | `<paths or none>` |
| Pre-step scope snapshot | `<report path / timestamp>` |
| Post-step scope snapshot | `<report path / timestamp>` |
| Unexpected path changes | `<count and paths, or none>` |
| Specialized skill decision | `<NOT_ASSESSED / NO_INSTALL_NEEDED / SEARCH_RECOMMENDED / APPROVAL_PENDING / APPROVED / DECLINED / INSTALLED>` |
| Specialized skill scope | `<technical area, candidate, and reason>` |
| Installed skill evidence | `<instructions path/revision or not applicable>` |

### Authorized state transitions

Only advance when the matching evidence and developer input exist. Do not skip a state because an earlier report looks complete.

```text
DISCOVERY → AWAITING_FRESH_SESSION | BLOCKED | AWAITING_PLAN_APPROVAL
AWAITING_FRESH_SESSION → DISCOVERY
AWAITING_PLAN_APPROVAL → AWAITING_STEP_REQUEST
AWAITING_STEP_REQUEST → AWAITING_REVIEW | BLOCKED_SCOPE_VIOLATION
AWAITING_REVIEW → AWAITING_COMMIT_DECISION | BLOCKED | BLOCKED_SCOPE_VIOLATION
AWAITING_COMMIT_DECISION → AWAITING_STEP_REQUEST | READY_FOR_FINAL_REVIEW
READY_FOR_FINAL_REVIEW → COMPLETE | BLOCKED
```

`BLOCKED` may return only to the state justified by newly recorded resolution evidence. `BLOCKED_SCOPE_VIOLATION` requires developer inspection of the preserved diff and an explicit decision to revise the plan, discard the step through a separately authorized recovery action, or stop the task; OttoNet never auto-restores it. A developer commit decision is required before another step request, even when the decision is to continue without committing.

## Gate register

| Gate | State | Evidence | Developer action required |
| --- | --- | --- | --- |
| 0. Fresh session boundary | `NOT_REACHED` | `<task identity comparison>` | `<start /new and remove stale .otto/ manually, or continue as new task>` |
| 1. Workspace protection | `NOT_REACHED` | `<report path>` | `<action>` |
| 2. Project understanding | `NOT_REACHED` | `<report paths>` | `<action>` |
| 3. Team patterns | `NOT_REACHED` | `<report path>` | `<action>` |
| 4. Task extraction | `NOT_REACHED` | `<report path>` | `<action>` |
| 5. Clarification | `NOT_REACHED` | `<gap report / clarification reference>` | `<action>` |
| 5a. Specialized skill recommendation | `NOT_REACHED` | `<assessment, search, or approval evidence>` | `<action>` |
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
| Project index | `<path>` | `<source fingerprint / freshness>` | `<timestamp>` |
| Project documentation | `<path>` | `<new / reused / delta>` | `<timestamp>` |
| Project understanding | `<path>` | `<new / reused / delta>` | `<timestamp>` |
| Team patterns | `<path>` | `<new / reused / delta>` | `<timestamp>` |
| Task requirements | `<path>` | `<new / revised>` | `<timestamp>` |
| Task context | `<path>` | `<new / revised>` | `<timestamp>` |
| Requirement gaps | `<path>` | `<new / resolved / blocked>` | `<timestamp>` |
| Specialized skill assessment | `<path or state section>` | `<not needed / approval pending / approved / declined>` | `<timestamp>` |
| Installed skill instructions | `<path or unavailable>` | `<read / not applicable>` | `<timestamp>` |
| Implementation plan | `<path>` | `<draft / approved / superseded>` | `<timestamp>` |
| Recommended execution order | `<path or plan section>` | `<current / stale>` | `<timestamp>` |
| API documentation matrix | `<path or plan section>` | `<current / incomplete / blocked>` | `<timestamp>` |
| Reuse assessment | `<path or report section>` | `<current / incomplete>` | `<timestamp>` |
| Database-field readiness | `<path or report section>` | `<ready / blocked / not applicable>` | `<timestamp>` |
| Step execution reports | `<paths>` | `<complete / partial / unavailable>` | `<timestamp>` |
| Step completion reports | `<paths>` | `<complete / partial / unavailable>` | `<timestamp>` |
| Final delivery report | `<path>` | `<complete / limited / unavailable>` | `<timestamp>` |

## Source freshness register

Use this to decide whether an earlier artifact can be reused. A changed fingerprint requires targeted revalidation; it does not by itself require re-reading the whole repository.

| Source area | Fingerprint or revision | Last verified | Reuse decision | Evidence |
| --- | --- | --- | --- | --- |
| Repository baseline | `<HEAD / branch / workspace report>` | `<timestamp>` | `<current / stale>` | `<evidence ID>` |
| Project index | `<path + fingerprint>` | `<timestamp>` | `<current / stale>` | `<evidence ID>` |
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
| Recommended execution order | `<plan section or unavailable>` |
| Step scope contracts | `<plan sections or unavailable>` |
| API documentation status | `<complete / partial / blocked / not applicable>` |
| Reuse assessment | `<complete / partial / blocked>` |
| Database-field readiness | `<ready / blocked / not applicable>` |
| Specialized skill | `<candidate / no installation / not applicable>` |
| Specialized skill approval | `<explicit developer decision and timestamp>` |
| Installed skill instructions read | `<path/revision or not applicable>` |
| Last plan reconciliation | `<timestamp and summary>` |

| Step | Title | Execution state | Review | Commit decision | Scope audit | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `<title>` | `NOT_STARTED` | `NOT_REVIEWED` | `NOT_DECIDED` | `<clean / blocked / not audited>` | `<plan section / report paths>` |

Allowed execution states: `NOT_STARTED`, `IN_PROGRESS`, `AWAITING_REVIEW`, `AWAITING_COMMIT_DECISION`, `COMMITTED`, `BLOCKED`, `BLOCKED_SCOPE_VIOLATION`.

## Risk and handoff register

| Type | Description | Status | Evidence / owner | Next action |
| --- | --- | --- | --- | --- |
| `<blocking question, risk, or constraint>` | `<concise description>` | `<OPEN / ACCEPTED / RESOLVED>` | `<evidence>` | `<exact next action>` |

## Continuity log (append only)

| Timestamp | Actor | Event | Evidence or affected paths | Result / next action |
| --- | --- | --- | --- | --- |
| `<ISO 8601 timestamp>` | `<developer / agent>` | `<event>` | `<paths or report>` | `<outcome>` |

## Resume checklist

1. Read **Resume state** before any other artifact.
2. Verify the repository identity, branch, HEAD, and workspace status against this state file.
3. Read the current gate artifact and the most recent continuity event.
4. Reconcile any difference before doing work; never infer that an in-progress step completed.
5. Continue only with the exact action listed in **Next authorized action** and the required developer decision.
