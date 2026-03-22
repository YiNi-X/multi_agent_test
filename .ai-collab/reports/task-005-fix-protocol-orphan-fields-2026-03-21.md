# Task 005 Report

## Task
`005` - `fix-protocol-orphan-fields`

## What was done
- Updated `.ai-collab/templates/codex-worker-protocol.md` to document how Claude writes `spec_hash_at_start` before starting a new `codex()` session.
- Updated `.ai-collab/templates/codex-worker-protocol.md` to require incrementing `total_tasks_executed` immediately after `last_task_id` is updated.
- Verified `.ai-collab/board.yaml` already contained the required validity comment above `suggested_next_for_codex`, so no board change was needed.
- Appended a brief execution log to the task file.

## Files changed
- `.ai-collab/templates/codex-worker-protocol.md`
- `.ai-collab/tasks/task-005-fix-protocol-orphan-fields.md`
- `.ai-collab/reports/task-005-fix-protocol-orphan-fields-2026-03-21.md`

## Validation results
- Acceptance criterion 1: Met. `codex-worker-protocol.md` now states that after Claude updates `last_task_id`, it must also increment `total_tasks_executed` by 1.
- Acceptance criterion 2: Met. `codex-worker-protocol.md` now states that before a new `codex()` call, Claude writes `spec_hash_at_start` using the format `"<version>/<last_updated>"`, with `"0.2.0/2026-03-17"` as the example.
- Acceptance criterion 3: Met. `.ai-collab/board.yaml` already states that `suggested_next_for_codex` is only valid when `current_plan.status == "in_progress"`.

## Blockers or issues
- None.
