# Task 004 — resume-codex-mcp-session

## Goal
Verify Codex MCP session resumption. `.ai-collab/runtime/codex-session.yaml` already contains a
valid `thread_id` (written by Claude after task 003). Claude invokes `mcp__codex__codex-reply()`
with that `thread_id` — no new session is created. Codex appends a second marker to
`CODEX_CANARY.md`, demonstrating session continuity.

## Status
`done`

## Assigned to
codex

## Target paths
- `CODEX_CANARY.md`

## Pre-conditions
- Task 003 is `done`.
- `codex-session.yaml.thread_id` is non-empty.
- `codex-session.yaml.active` is `true`.

## Instructions
1. Claude reads `thread_id` from `.ai-collab/runtime/codex-session.yaml`.
2. Claude invokes `mcp__codex__codex-reply(threadId=<thread_id>, prompt=...)` — **not** `codex()` —
   with the following instruction:
   > "Append exactly the following line to `CODEX_CANARY.md`:
   > `[task-004] session-resume verified`
   > Do not modify any other file."
3. After Codex responds, Claude updates in `codex-session.yaml`:
   - `last_used_at: <ISO 8601 timestamp>`
   - `last_task_id: "004"`
   - `handoff_version: 2`
4. Claude reviews the output and — if acceptance criteria are met — sets this task to `review`,
   then `done` in `board.yaml`. Codex does not update `board.yaml`.

## Acceptance criteria
- `CODEX_CANARY.md` contains the line `[task-004] session-resume verified`.
- `codex-reply()` was used with the same `thread_id` from task 003 (session was **resumed**, not restarted).
- `codex-session.yaml.handoff_version` is `2`.
- No files other than `CODEX_CANARY.md` are modified by Codex.

## Depends on
- task-003

## Updated
2026-03-18

## Codex execution log
- 2026-03-18: Appended `[task-004] session-resume verified` to `CODEX_CANARY.md` by resuming previous Codex CLI session (pre-protocol-formalization era). Acceptance criteria met: canary line present, no other files modified.
