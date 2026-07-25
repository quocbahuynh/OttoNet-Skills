# Team Coding Pattern Report

## Report metadata

| Item | Value |
| --- | --- |
| Target repository | |
| Evidence period examined | |
| Sources available | Git history / merge requests / reviews / code |
| Approval evidence available | Yes / No — explain |
| Evidence registry | `<path and relevant IDs>` |
| Sample freshness | `<commit range / revalidation date>` |

## Evidence-quality note

Git history proves that changes were merged into the inspected history; it does not by itself prove formal approval or resolved review feedback. Classify a finding as `APPROVED` only when approval or resolved-review evidence is available.

## Pattern findings

| Area | Finding | Classification | Evidence ID and source | Sample or enforcement basis | Reuse guidance |
| --- | --- | --- | --- | --- | --- |
| Naming | | REQUIRED / APPROVED / ESTABLISHED / COMMON / LEGACY / UNKNOWN | | | |
| Folder placement | | | | |
| Requests and responses | | | | |
| Dependency injection | | | | |
| Validation | | | | |
| Authorization | | | | |
| Data access | | | | |
| Transactions | | | | |
| Errors and logging | | | | |
| Testing | | | | |

## Classification definitions

| Classification | Meaning |
| --- | --- |
| REQUIRED | Explicitly documented, configured, or enforced. |
| APPROVED | Confirmed by an approved merge request or resolved review feedback. |
| ESTABLISHED | Repeated consistently in recent active code. |
| COMMON | Frequently used but not universal. |
| LEGACY | Older code that should not normally be copied. |
| UNKNOWN | Insufficient evidence. |

## Selected reference implementations

| Reference | Why it is comparable | Structural aspects safe to reuse | Business logic not to copy |
| --- | --- | --- | --- |

## Non-transferable business behavior

Record statuses, permissions, dates, values, and conditions that are specific to their source module.

## Handoff

State which findings are suitable for the task context investigator and planner, which remain unknown, and what must be revalidated if the source fingerprint changes.
