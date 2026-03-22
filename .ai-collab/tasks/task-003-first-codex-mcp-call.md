# Task 003 — first-codex-mcp-call

## Goal
Execute the first Codex MCP invocation using `mcp__codex__codex()`. Codex appends a marker line to `CODEX_CANARY.md`. After the response, Claude records session details in `codex-session.yaml` and updates `board.yaml`.

## Status
`done`

## Assigned to
codex

## Target paths
- `CODEX_CANARY.md`

## Instructions
1. Claude invokes `mcp__codex__codex(prompt=...)` with the following instruction for Codex:
   > "Append exactly the following line to `CODEX_CANARY.md` (create the file if it does not exist):
   > `[task-003] first-mcp-call verified`
   > Do not modify any other file."
2. After Codex responds, Claude records in `codex-session.yaml`:
   - `active: true`
   - `thread_id: <returned threadId>`
   - `last_used_at: <ISO 8601 timestamp>`
   - `last_task_id: "003"`
   - `spec_version_at_start: "0.2.0"`
   - `handoff_version: 1`
3. Claude reviews the output and — if acceptance criteria are met — sets this task to `review`,
   then `done` in `board.yaml`. Codex does not update `board.yaml`.

## Acceptance criteria
- `CODEX_CANARY.md` contains the line `[task-003] first-mcp-call verified`.
- `codex-session.yaml.thread_id` is non-empty.
- `codex-session.yaml.active` is `true`.
- No files other than `CODEX_CANARY.md` are modified by Codex.

## Depends on
*(none)*

## Updated
2026-03-18
