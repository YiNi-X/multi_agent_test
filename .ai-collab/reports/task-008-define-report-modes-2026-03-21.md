# Task 008 Report

## Task
`008` - `define-report-modes`

## What was done
- Added a new `## Codex invocation modes` section to `.ai-collab/README.md` defining Mode A and Mode B, their trigger conditions, behavior, and where the mode must be declared.
- Updated `.ai-collab/README.md` role responsibilities so Mode A tasks are reviewed from MCP evidence and Mode B tasks require a report file.
- Added an explicit `## Invocation mode` section to `.ai-collab/templates/task-template.md` with the A/B rules and updated the definition-of-done checklist so the report requirement is mode-aware.
- Updated `.ai-collab/templates/review-template.md` metadata so reviews record invocation mode and Mode A evidence, and so the `Report read` row works for both modes.
- Appended a brief execution log to the task file.

## Files changed
- `.ai-collab/README.md`
- `.ai-collab/templates/task-template.md`
- `.ai-collab/templates/review-template.md`
- `.ai-collab/tasks/task-008-define-report-modes.md`
- `.ai-collab/reports/task-008-define-report-modes-2026-03-21.md`

## Validation results
- Acceptance criterion 1: Met. `.ai-collab/README.md` now contains a `## Codex invocation modes` section defining Mode A and Mode B with their conditions and behaviors.
- Acceptance criterion 2: Met. `.ai-collab/README.md` now states that the mode must be declared in both the task file and the Claude invocation prompt.
- Acceptance criterion 3: Met. `.ai-collab/templates/task-template.md` now contains an `## Invocation mode` field with the A/B options and their conditions.
- Acceptance criterion 4: Met. `.ai-collab/templates/review-template.md` metadata table now contains `Invocation mode` and `Mode A evidence` rows.

## Blockers or issues
- None.
