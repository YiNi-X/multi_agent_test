# Task 016 — simplify-templates

## Goal
Simplify four template files to reduce boilerplate without losing protocol correctness:
1. Merge `Definition of done` into `Acceptance criteria` in `task-template.md`
2. Simplify Mode B execution log in `task-template.md` to summary + report reference
3. Make `Steps` section optional in `task-template.md`
4. Merge `decision-template.md` + `changelog-template.md` into one `spec-aux-template.md`

## Status
`todo`

## Assigned to
codex

## Invocation mode
`B` — report required: modifies 3 template files + creates 1 new file, criteria require inspecting multiple files

## Target paths
- `.ai-collab/templates/task-template.md`
- `.ai-collab/templates/decision-template.md`
- `.ai-collab/templates/changelog-template.md`
- `.ai-collab/templates/spec-aux-template.md` (new file)

## Pre-conditions
- None

## Instructions

### Fix 1: Merge `Definition of done` into `Acceptance criteria` in task-template.md

In `task-template.md`, find the `## Acceptance criteria` section and the `## Definition of done` section.

Append the definition-of-done checklist items as a fixed footer inside the `## Acceptance criteria` section:

```markdown
## Acceptance criteria

<!--
Objective, testable conditions. The task is done when all of these pass.
Use commands or test names where possible.
-->

- [ ] `<test command or observable outcome>`
- [ ] `<test command or observable outcome>`

**Definition of done (always required):**
- [ ] All criteria above pass
- [ ] `## Codex execution log` appended to this task file
- [ ] If invocation mode is `B`: report written to `reports/task-<ID>-<slug>-<YYYY-MM-DD>.md`
- [ ] No files modified outside `target_paths`
```

Then **delete** the separate `## Definition of done` section entirely.

### Fix 2: Make `Steps` section optional in task-template.md

In `task-template.md`, find the `## Steps` section and update its comment to mark it optional:

```markdown
## Steps

<!--
Optional for simple tasks (1-2 steps). Required for complex tasks.
If the objective is self-evident, this section may be omitted.
For tasks that need it, provide an ordered list of concrete implementation steps.
-->

1. ...
2. ...
```

### Fix 3: Simplify Mode B execution log guidance in task-template.md

In `task-template.md`, find the `## Codex execution log` section. Update the guidance comment to clarify that for Mode B tasks, the execution log should be brief (3 lines max) and reference the report file:

```markdown
## Codex execution log

<!--
Only Codex writes this section. Do not edit the task definition sections above.
Claude reads this section during review.

Mode A: Write a complete summary here (this is the primary record).
Mode B: Write 3 lines max + a reference to the report file. Full details go in the report.
  Format:
    Status: in_progress -> review
    Report: reports/task-<ID>-<slug>-<YYYY-MM-DD>.md
    Summary: (one line describing what was done)
-->
```

### Fix 4: Create spec-aux-template.md by merging decision and changelog templates

Create `.ai-collab/templates/spec-aux-template.md` with the following content (merging both existing templates into two sections):

```markdown
# Spec Auxiliary Templates

This file contains templates for two low-frequency spec/ documents.
Use the appropriate section when adding to `spec/DECISIONS.md` or `spec/CHANGELOG.md`.

---

## Decision entry template

Use this template when adding a new entry to `spec/DECISIONS.md`.

### DXXX: [Decision title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Context:** [What is the issue we're facing?]

**Decision:** [What are we doing?]

**Rationale:**
- [Why this decision?]
- [What alternatives were considered?]

**Consequences:**
- [What becomes easier?]
- [What becomes harder?]
- [What are the trade-offs?]

---

## Changelog entry template

Use this template when adding a new entry to `spec/CHANGELOG.md`.

## vX.Y.Z — YYYY-MM-DD

**Changes:**
- [What changed and why]
- [Reference task IDs where applicable]

**Resolved questions:** [list any SPEC.md open questions closed by this version]
**Deferred:** [list any questions explicitly deferred]
```

Do NOT delete `decision-template.md` or `changelog-template.md` yet — leave them in place with a deprecation notice at the top pointing to `spec-aux-template.md`. This allows a clean transition.

Add this notice at the top of `decision-template.md`:
```markdown
> **Deprecated:** This template has been merged into `spec-aux-template.md`. Use that file instead.
```

Add this notice at the top of `changelog-template.md`:
```markdown
> **Deprecated:** This template has been merged into `spec-aux-template.md`. Use that file instead.
```

## Acceptance criteria
- `task-template.md` does NOT contain a separate `## Definition of done` section
- `task-template.md` `## Acceptance criteria` section contains a "Definition of done" checklist footer
- `task-template.md` `## Steps` section comment says it is optional for simple tasks
- `task-template.md` `## Codex execution log` comment distinguishes Mode A (full summary) vs Mode B (3 lines + report reference)
- `spec-aux-template.md` exists and contains both a decision entry template and a changelog entry template
- `decision-template.md` has a deprecation notice at the top pointing to `spec-aux-template.md`
- `changelog-template.md` has a deprecation notice at the top pointing to `spec-aux-template.md`

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
Status: `in_progress` -> `review`
Report: `reports/task-016-simplify-templates-2026-03-21.md`
Summary: Simplified `task-template.md`, deprecated the old spec templates, and added merged `spec-aux-template.md`.
