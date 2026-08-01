---
name: dotnet-workspace-inspector
description: Safely inspect the current Git workspace before any .NET company-task analysis or implementation. Use at the beginning of an OttoNet workflow and immediately before a requested implementation step to protect the developer's branch and local changes.
---

# .NET Workspace Inspector

## Purpose

Establish an evidence-backed, non-mutating baseline for the current target repository. Protect every existing change before analysis or implementation begins.

## When to use

Use first in a company-task workflow, before every requested implementation step, and whenever the workspace state may have changed since the last report.

## Assumptions

- The developer already cloned the repository and selected the intended branch.
- The current directory is the target project root.
- Local changes may belong to the developer or another in-progress task and must be preserved.

## Required inputs

- Current target repository path.
- Optional intended task name or plan step, used only to label the report.
- Existing task dossier state when resuming an OttoNet task.

## Workflow

1. Confirm the directory is a Git worktree without modifying it.
2. Run read-only checks such as `git status --short --branch`, `git branch --show-current`, `git diff`, `git diff --staged`, and `git log -10 --oneline`. Use a path/status summary when reporting so existing work is protected without exposing secret values.
3. Inspect repository metadata, when present, for merge, rebase, cherry-pick, revert, or conflict state. Detect unmerged paths with `git diff --name-only --diff-filter=U`.
4. Record the current branch, HEAD, detached HEAD state, dirty and staged changes, untracked files, conflict state, and in-progress operations. Identify likely protected branch names including `main`, `master`, `develop`, and `development`.
5. When a dossier exists, compare branch, HEAD, protection boundaries, and active plan step with its baseline. Mark affected evidence stale when a mismatch can affect it; do not infer that the mismatch is harmless.
6. Describe existing changes by path and status. Do not infer their intent or overwrite them. Mark the workspace safe to continue only when there is no unresolved Git operation or conflict and the next activity can avoid changing protected existing work. A dirty workspace can be safe with explicit protection boundaries.
7. Decide whether the requested work is significant enough to warrant a recovery point before code changes. Treat migrations, authorization, external integrations, destructive data behavior, broad multi-file changes, or developer-requested checkpoints as significant. Recommend a recovery point and record the baseline commit; do not create commits or tags automatically.
8. Provide optional, non-executed rollback guidance appropriate to the observed state. Explain that the developer must inspect status and approve each command:
   - Roll back the latest commit with a new inverse commit: `git revert HEAD`.
   - Roll back a specific commit with a new inverse commit: `git revert <commit>`.
   - Restore selected files from a known commit only after protecting uncommitted work: `git restore --source=<commit> -- <path>`.
   - Abort an unfinished operation when appropriate: `git merge --abort`, `git rebase --abort`, or `git cherry-pick --abort`.
   Never recommend `reset --hard` as an automatic recovery path; never execute rollback, restore, or abort commands as part of inspection.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Never switch or create branches, clone, reset, rebase, discard changes, commit, merge, or push.
- Never stage files or use a command that changes the index or worktree.
- Treat an unknown branch as non-protected unless project documentation says otherwise; still report it.
- Do not expose secret values found in diffs; report file paths and a high-level change type instead.
- Recovery guidance is advisory only. Never create a recovery commit, restore files, abort an operation, or delete `.otto/` automatically.

## Stop conditions

Stop and report `NOT_SAFE` when there are merge conflicts, an in-progress Git operation, inaccessible repository state, or a proposed next change would overlap unidentified local work. Stop for developer direction before proceeding on a protected branch unless the developer explicitly confirms it is intended.

## Required output

Produce a **Workspace Inspection Report** containing: repository path, branch, HEAD or detached HEAD status, protected-branch warning, working-tree status, staged and untracked files, conflicts or in-progress operations, recorded protection boundaries, dossier-baseline reconciliation, recovery-point recommendation, rollback options (not executed), commands run, and `Safe to continue: Yes/No/With constraints`.

## Handoff to the next skill

Pass the report and protection boundaries to `dotnet-project-documentation-reader`. For a requested plan step, pass it to `dotnet-step-executor` instead.
