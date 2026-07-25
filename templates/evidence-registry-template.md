# OttoNet Evidence Registry

> Store each stable fact once and cite its ID from reports, the plan, and workflow state. Keep evidence concise and verifiable. Do not include credentials, private tokens, full diffs, or copied source files.

## Rules

- Use an ID such as `E-001` for each evidence item.
- Record the strongest applicable evidence only; link lower-strength evidence only when it explains a conflict or limitation.
- A source file proves its own behavior, not a project-wide convention. Record the sample size or configuration that supports broader claims.
- A merged commit proves history, not approval. Use `APPROVED` only with explicit approval or resolved-review evidence.
- Mark evidence `STALE` when its source fingerprint changes. Revalidate only the affected claim before reusing it.

## Evidence register

| ID | Claim or observed fact | Priority source | Strength | Location / revision | Scope and reuse limit | Freshness |
| --- | --- | --- | --- | --- | --- | --- |
| `E-001` | `<fact>` | `<task / docs / MR / code>` | `<REQUIRED / APPROVED / ESTABLISHED / COMMON / LEGACY / UNKNOWN>` | `<path:line, ticket, MR, commit>` | `<what this proves and does not prove>` | `<CURRENT / STALE / UNVERIFIED>` |

## Decision links

| Decision or report section | Evidence IDs | Outcome | Owner / date |
| --- | --- | --- | --- |
| `<requirement, plan step, or risk>` | `<E-001, E-002>` | `<decision>` | `<person or role / date>` |
