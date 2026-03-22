# Task 006 — fix-review-state-rule

## Goal
Enforce that `review` is a persistent, observable state in the task lifecycle — not a transient step that gets skipped. Currently all four completed tasks went directly from `in_progress` to `done` without ever showing `review` status in `board.yaml`.

## Status
`todo`

## Assigned to
codex

## Target paths
- `.ai-collab/README.md`
- `.ai-collab/templates/task-template.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Clarify `review` state duration in README.md
In `.ai-collab/README.md`, in the **Status values** table, update the `review` row description to:
> Codex has finished and Claude has been notified. `board.yaml` must be set to `review` **before** Claude begins writing the review document. Status changes to `done` only after Claude writes the review document and explicitly accepts the output.

Also add a note under the status table:
> **Important:** `review` is a durable state, not a transient one. External observers reading `board.yaml` during an active review will see `review`. A task must not jump from `in_progress` directly to `done`.

### Fix 2: Add `review` state requirement to task template
In `.ai-collab/templates/task-template.md`, in the Instructions section template, ensure there is a step that reads:
> X. Claude sets task status to `review` in `board.yaml` before writing the review document.
> X+1. Claude writes the review document in `reviews/`.
> X+2. Claude sets task status to `done` in `board.yaml` after accepting the output.

If the template already has a combined step, split it into these three separate steps.

## Acceptance criteria
- `README.md` status table `review` description states that `board.yaml` must be set to `review` before Claude starts writing the review document
- `README.md` contains a note that `review` is a durable state, not transient
- `task-template.md` has three separate steps: set `review` → write review doc → set `done`

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Updated `.ai-collab/README.md` so the `review` status explicitly requires `board.yaml` to be set to `review` before Claude starts the review document, and added a durability note forbidding direct `in_progress` to `done` jumps.
- 2026-03-21: Updated `.ai-collab/templates/task-template.md` to split Claude's post-report workflow into three separate handoff steps: set `review`, write the review document, then set `done`.
- 2026-03-21: Verified the final wording in both target files and wrote the task report.
