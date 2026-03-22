# Task 006 Report

## Task
`006` - `fix-review-state-rule`

## What was done
- Updated `.ai-collab/README.md` so the `review` status description now requires `board.yaml` to be set to `review` before Claude starts writing the review document, and clarifies that `done` is only set after explicit acceptance.
- Added an explicit note to `.ai-collab/README.md` that `review` is a durable state and that tasks must not jump from `in_progress` directly to `done`.
- Updated `.ai-collab/templates/task-template.md` to split Claude's post-execution handoff into three separate steps: set `review`, write the review document, then set `done`.
- Appended a brief execution log to the task file.

## Files changed
- `.ai-collab/README.md`
- `.ai-collab/templates/task-template.md`
- `.ai-collab/tasks/task-006-fix-review-state-rule.md`
- `.ai-collab/reports/task-006-fix-review-state-rule-2026-03-21.md`

## Validation results
- Acceptance criterion 1: Met. `.ai-collab/README.md` now states that `board.yaml` must be set to `review` before Claude begins writing the review document.
- Acceptance criterion 2: Met. `.ai-collab/README.md` now contains a note stating that `review` is a durable state, not a transient one.
- Acceptance criterion 3: Met. `.ai-collab/templates/task-template.md` now has three separate Claude handoff steps: set `review`, write the review document, then set `done`.

## Blockers or issues
- None.
