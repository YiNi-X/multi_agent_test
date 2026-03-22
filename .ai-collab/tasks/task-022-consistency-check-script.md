# Task 022 — consistency-check-script

## Goal
Write `tools/check_consistency.py` — a Python script that checks cross-file field consistency across the protocol files. Catches the class of bugs found in this session (thread_id mismatch, spec version drift, task status contradictions).

## Status
`todo`

## Assigned to
codex

## Invocation mode
`B` — report required: creates a new Python file with logic, criteria require running the script

## Target paths
- `tools/check_consistency.py`

## Pre-conditions
- Python 3 available in environment

## Instructions

Create `tools/check_consistency.py` that performs the following checks and prints a clear pass/fail report:

### Check 1: thread_id consistency
- Read `thread_id` from `.ai-collab/runtime/codex-session.yaml` (field: `codex_session.thread_id`)
- Read `thread_id` from `.ai-collab/runtime/codex-handoff.md` YAML front-matter (field: `thread_id`)
- PASS if both match, FAIL with both values if they differ

### Check 2: last_task_id consistency
- Read `last_task_id` from `codex-session.yaml` (field: `codex_session.last_task_id`)
- Read `last_task_id` from `codex-handoff.md` front-matter (field: `last_task_id`)
- PASS if both match, FAIL with both values if they differ

### Check 3: spec version consistency
- Read spec version from `board.yaml` (field: `current_spec.version`)
- Read spec version from `SPEC.md` header line (`**Version:** X.Y.Z`)
- Read spec version from `codex-session.yaml` (field: `codex_session.spec_version_at_start`)
- PASS if board.yaml and SPEC.md match (session version may differ if new session not started)
- WARN (not FAIL) if session version differs from board.yaml

### Check 4: task status consistency
- Read all task entries from `board.yaml`
- For each task, read the corresponding task file
- Check that the `## Status` line in the task file matches the status in board.yaml
- Report any mismatches

### Check 5: spec_dirty safety
- Read `spec_dirty` from `board.yaml` (field: `spec_status.spec_dirty`)
- If `spec_dirty: true`, check if any task has status `in_progress` in board.yaml
- FAIL if spec_dirty is true AND any task is in_progress (protocol violation)

### Output format
```
=== Protocol Consistency Check ===
[PASS] thread_id: 019d1335-... matches in both files
[FAIL] last_task_id: codex-session.yaml=018, handoff.md=verify-mcp
[PASS] spec version: board.yaml=0.3.0 matches SPEC.md=0.3.0
[WARN] spec version: session started at 0.2.0, current is 0.3.0
[PASS] task status: all 18 tasks consistent
[PASS] spec_dirty: false, no in_progress tasks blocked

Result: 1 FAIL, 1 WARN, 4 PASS
Run time: 2026-03-22
```

Exit code: 0 if all PASS (warnings OK), 1 if any FAIL.

## Acceptance criteria
- `tools/check_consistency.py` exists and is valid Python 3
- Running `python tools/check_consistency.py` from project root completes without Python errors
- Output includes results for all 5 checks
- Exit code is 0 when all checks pass, 1 when any check fails
- Script handles missing files gracefully (prints SKIP with explanation, does not crash)

## must_haves
- 脚本能检测出本次发现的真实 bug 类型（thread_id 不一致、spec version 漂移）
- 输出格式人类可读，每行一个 [PASS]/[FAIL]/[WARN]/[SKIP]
- 可以在每次 Plan 完成后作为测试阶段的标准步骤运行

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log
Status: completed; `python tools/check_consistency.py` ran successfully and exited `1` because it detected existing `last_task_id` and task-status inconsistencies.
Report: `reports/task-022-consistency-check-script-2026-03-22.md`
Summary: Added `tools/check_consistency.py` with all five requested checks, PASS/FAIL/WARN/SKIP output, and non-zero exit behavior when inconsistencies are present.
