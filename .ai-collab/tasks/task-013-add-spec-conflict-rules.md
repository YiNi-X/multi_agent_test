# Task 013 — add-spec-conflict-rules

## Goal
Add two missing protocol rules to `CLAUDE.md`:
1. Claude must manually set `spec_dirty: true` in `board.yaml` whenever `SPEC.md` is modified
2. Claude must not invoke Codex while `spec_dirty: true` and any task is `in_progress`

These rules resolve SPEC.md open questions Q1 and Q3 at the operational level (SPEC.md now has the answers; CLAUDE.md must carry the actionable instructions).

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 1 file, criteria verifiable from MCP response, documentation change only

## Target paths
- `CLAUDE.md`

## Pre-conditions
- None

## Instructions

In `CLAUDE.md`, after the "Task decomposition rules" section and before "Status vocabulary", add a new section:

```markdown
### Spec change rules

- **When Claude modifies `SPEC.md`:** immediately set `spec_dirty: true` and update `last_spec_change` (YYYY-MM-DD) in `board.yaml > spec_status`. Then evaluate whether any `todo` or `in_progress` tasks are invalidated and update `invalidated_tasks` list.
- **When `spec_dirty: true` and any task is `in_progress`:** Claude must resolve the conflict before the next Codex invocation. Do not invoke Codex (via `codex()` or `codex-reply()`) until the conflict is resolved and `spec_dirty` is cleared.
- **Clearing `spec_dirty`:** After evaluating impact and updating affected tasks (rework to `todo` if needed), set `spec_dirty: false` in `board.yaml`.
```

## Acceptance criteria
- `CLAUDE.md` contains a "Spec change rules" section (or equivalent heading)
- The section states Claude must set `spec_dirty: true` when modifying `SPEC.md`
- The section states Claude must not invoke Codex while `spec_dirty: true` and tasks are `in_progress`
- The section describes how to clear `spec_dirty` after impact evaluation

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Added a new `Spec change rules` section to `CLAUDE.md` between task decomposition and status vocabulary, as requested.
- 2026-03-21: Documented the three operational rules: set `spec_dirty: true` and `last_spec_change` when `SPEC.md` changes, do not invoke Codex while `spec_dirty: true` and tasks are `in_progress`, and clear `spec_dirty` after impact evaluation and task updates.
- 2026-03-21: Verified the final `CLAUDE.md` wording against all four acceptance criteria.
