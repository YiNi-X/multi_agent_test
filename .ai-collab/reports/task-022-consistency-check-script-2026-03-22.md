# Task 022 Report: consistency-check-script

## What was done
- Added `tools/check_consistency.py` as a self-contained Python 3 script to check cross-file protocol consistency.
- Implemented checks for `thread_id`, `last_task_id`, spec version alignment, task status alignment, and `spec_dirty` safety.
- Added graceful missing-file handling that reports `SKIP` instead of crashing.

## Files changed
- `tools/check_consistency.py`

## Validation results
- Command: `python tools/check_consistency.py`
- Exit code: `1`
- Result summary: `2 FAIL, 0 WARN, 3 PASS`
- PASS: `thread_id` matches between `.ai-collab/runtime/codex-session.yaml` and `.ai-collab/runtime/codex-handoff.md`.
- FAIL: `last_task_id` differs between `.ai-collab/runtime/codex-session.yaml` (`018`) and `.ai-collab/runtime/codex-handoff.md` (`verify-mcp`).
- PASS: `board.yaml` spec version `0.3.0` matches `SPEC.md` version `0.3.0`.
- FAIL: task status check found 14 mismatches where `board.yaml` says `done` but the task file `## Status` remains `todo`.
- PASS: `spec_dirty` is `false`, so there is no active protocol violation involving `in_progress` tasks.

## Blockers or issues
- No implementation blocker prevented completion of this task.
- The non-zero exit code came from detected repository inconsistencies, not from a Python/runtime error.
- Missing-file `SKIP` paths are implemented in the script but were not exercised by the current repository state.
