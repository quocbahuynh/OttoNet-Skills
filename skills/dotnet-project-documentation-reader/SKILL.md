---
name: dotnet-project-documentation-reader
description: Extract repository rules, architecture guidance, and operational instructions before reading a BA task or exploring .NET business implementation. Use after workspace inspection in an OttoNet company-task workflow.
---

# .NET Project Documentation Reader

## Purpose

Read repository documentation and configuration that constrain future work, without yet performing deep business-implementation analysis.

## When to use

Use after a safe workspace inspection and before the BA task, repository exploration, or implementation planning. Re-run when documentation changes or a task concerns a documented integration.

## Assumptions

- The current repository was inspected and existing changes are protected.
- Documentation can be incomplete, stale, or distributed across configuration files.
- A task file is not the primary source for this stage and should not drive implementation exploration yet.

## Required inputs

- Workspace Inspection Report.
- Target repository root.
- Task dossier state and evidence registry when the workflow is being resumed.
- Cached project index when resuming.

## Workflow

1. When a dossier exists, check the documentation fingerprint, evidence registry, and `.otto/project-index.md` first. Reuse only claims whose source paths and revisions remain current; inspect changed or task-relevant documents instead of blindly re-reading every file.
2. Locate and read applicable `AGENTS.md` files first, including nested files that govern subdirectories.
3. Search for and review `README.md`, `CONTRIBUTING.md`, `docs/**`, `architecture/**`, `adr/**`, and relevant `*.md` files. Use file location and recency to distinguish active guidance from historical context.
4. Inspect project-level configuration: `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`, `global.json`, `docker-compose*`, `appsettings*.json`, and `launchSettings.json`. Redact secrets; record configuration keys and behavior, not secret values.
5. Extract the project purpose, domain terminology, architecture and coding rules, build and test instructions, database guidance, authentication/authorization notes, integrations, AI-specific instructions, and explicit prohibitions.
6. Resolve conflicting documents by scope and explicitness. Record unresolved conflicts rather than selecting a rule silently. Do not deeply trace controllers, entities, handlers, or business modules; identify them only as documentation references for the next skill.

## Evidence priority

Use this order for any interpretation: 1) resolved task requirements, 2) original task requirements, 3) repository instructions and documentation, 4) approved merge requests, 5) resolved review comments, 6) recent merged code, 7) repeated current project patterns, 8) similar implementations, 9) generic .NET practices. Generic practices never override explicit task or project rules.

## Safety rules

- Read files and configuration only; do not modify source, configuration, dependencies, branches, or Git state.
- Do not treat an undocumented convention as a rule.
- Do not read or print credential values, connection strings, tokens, or private keys.
- Respect the most specific applicable repository instruction.

## Stop conditions

Stop when required repository instructions are unreadable, contradictory without a scope rule, or explicitly prohibit the proposed workflow. Report missing documentation as a gap, not a reason to invent policy.

## Required output

Produce a **Project Documentation Report** with sources read or revalidated, scoped rules, project purpose and terminology, build/test/database instructions, security and integration notes, AI instructions, explicit prohibitions, documentation conflicts, and open questions. Clearly separate documented facts from inferences. Cite evidence-registry IDs when available; record only new or changed facts rather than duplicating stable content.

## Handoff to the next skill

Pass the Workspace Inspection Report and Project Documentation Report to `dotnet-repository-explorer`.
