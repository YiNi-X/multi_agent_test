# Task 011 — sync-claude-md-canary

## Goal
Update `CLAUDE.md` to reflect the canary-first session validation introduced in task-009. Currently CLAUDE.md's "Session continuity" section still describes the old time-based heuristic ("if session_id exists and not expired") without mentioning the canary probe. A new Claude instance reading only CLAUDE.md will skip the canary step.

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

In `CLAUDE.md`, find the **"Codex MCP execution model"** section and replace the "Session continuity" bullet with the updated canary-first logic:

**Current text (replace this):**
```
- **Session continuity:** Check `.ai-collab/runtime/codex-session.yaml` before invoking Codex:
  - If `session_id` exists and not expired → use `codex-reply()` to continue the conversation
  - If session missing, expired, or user explicitly requests reset → use `codex()` to start new
  - Update `codex-session.yaml` after each Codex invocation with session_id and timestamps
```

**New text (replace with this):**
```
- **Session continuity:** Check `.ai-collab/runtime/codex-session.yaml` before invoking Codex:
  - If `thread_id` exists → send canary probe first: prepend `CANARY_OK:<last_task_id>` check to prompt and use `codex-reply()`
    - If Codex responds with expected `CANARY_OK:<last_task_id>` → session alive, proceed with task
    - If canary fails → notify user, wait for confirmation, then use `codex()` to start new session
  - If session missing or user explicitly requests reset → use `codex()` to start new
  - After each invocation: update `codex-session.yaml` with `last_task_id`, `last_used_at`, increment `total_tasks_executed`, and write `spec_hash_at_start` (format: `"<version>/<last_updated>"`) when starting a new session
  - Full canary and session protocol details: see `.ai-collab/templates/codex-worker-protocol.md`
```

## Acceptance criteria
- `CLAUDE.md` "Session continuity" bullet mentions canary probe as the first check step
- `CLAUDE.md` describes the canary failure path (notify user → wait → new session)
- `CLAUDE.md` references `codex-worker-protocol.md` for full details
- `CLAUDE.md` mentions `total_tasks_executed` increment and `spec_hash_at_start` in post-invocation update list

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Updated `CLAUDE.md` in the "Codex MCP execution model" section so session continuity is canary-first rather than time-heuristic-first.
- 2026-03-21: Added the explicit canary failure path (notify user, wait for confirmation, then start a new session), the post-invocation update requirements (`last_task_id`, `last_used_at`, `total_tasks_executed`, `spec_hash_at_start`), and a reference to `.ai-collab/templates/codex-worker-protocol.md` for full details.
- 2026-03-21: Verified the final `CLAUDE.md` wording against all four acceptance criteria.
