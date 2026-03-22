# Task 015 — board-yaml-cleanup

## Goal
Clean up board.yaml structure: remove the stale `next_plan` field (plan-002 is already `current_plan`), keeping a single authoritative `current_plan` field.

## Status
`done`

## Assigned to
claude

## Invocation mode
`A` — Claude direct: board.yaml is Claude-owned, Codex must not write it

## Target paths
- `.ai-collab/board.yaml`

## Codex execution log
- 2026-03-21: Handled directly by Claude. Removed `next_plan` field; `current_plan` already set to plan-002.

## Updated
2026-03-21
