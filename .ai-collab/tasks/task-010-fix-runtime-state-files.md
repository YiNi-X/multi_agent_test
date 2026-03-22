# Task 010 — fix-runtime-state-files

## Goal
Fix two stale runtime state files that will cause context confusion on next session resume:
1. `codex-session.yaml`: `recent_tasks` only lists ["003","004"] but 5 tasks were executed; `handoff_summary.last_updated` is from 2026-03-18
2. `codex-handoff.md`: reflects task-007 in-progress state, but tasks 007/008/009 are all done; session status says `executing`, last review is wrong

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 2 runtime files, all criteria verifiable from MCP response, no code logic changes

## Target paths
- `.ai-collab/runtime/codex-session.yaml`
- `.ai-collab/runtime/codex-handoff.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Update `codex-session.yaml`

Update the following fields:
- `session_history.recent_tasks`: change from `["003", "004"]` to `["005", "006", "007", "008", "009"]`
- `handoff_summary.last_updated`: change from `"2026-03-18T00:01:00Z"` to `"2026-03-21T00:07:00Z"`

Do NOT modify any other fields — Claude owns this file and only these two fields are stale.

### Fix 2: Rewrite `codex-handoff.md`

Rewrite the file to reflect the current state as of task-009 completion:

```markdown
# Codex Handoff Summary

**Last updated:** 2026-03-21

---

## Codex execution state

| Field | Value |
|---|---|
| Active session thread_id | `019d0ead-cadd-7341-86d0-877d215983ef` |
| Session status | `completed` |
| Last task executed | `task-009-session-canary-probe` |
| Tasks executed this session | 005, 006, 007, 008, 009 |
| Files modified this session | `.ai-collab/templates/codex-worker-protocol.md`, `.ai-collab/README.md`, `.ai-collab/templates/task-template.md`, `.ai-collab/templates/review-template.md`, `.ai-collab/runtime/codex-handoff.md`, `AGENTS.md`, plus task execution logs and reports for tasks 005–009 |

---

## Orchestrator state

| Field | Value |
|---|---|
| Current plan | `plan-002` (`in_progress`) |
| Current spec version | `0.2.0` (stale — needs update after batch-1 fixes) |
| Spec last updated | `2026-03-17` |
| Last review | `review-2026-03-21-3` (task-009 accepted) |
| Pending decisions | See SPEC.md open questions section |
| Next action | Executing batch-1 fixes (tasks 010–013); batch-2 and batch-3 follow |

### Open questions requiring resolution before next plan
1. How should `spec_dirty` be detected? (manual vs auto) — scheduled for batch-2
2. What threshold of invalidated tasks triggers full replan vs incremental? — deferred
3. When `SPEC.md` conflicts with active plan, block or complete first? — scheduled for batch-2
4. What level of detail should `SPEC.md` contain vs individual plan documents? — deferred
```

## Acceptance criteria
- `codex-session.yaml` field `session_history.recent_tasks` equals `["005", "006", "007", "008", "009"]`
- `codex-session.yaml` field `handoff_summary.last_updated` equals `"2026-03-21T00:07:00Z"`
- `codex-handoff.md` `Session status` row says `completed`
- `codex-handoff.md` `Last task executed` row says `task-009-session-canary-probe`
- `codex-handoff.md` `Last review` row says `review-2026-03-21-3`

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Blocked before runtime-file edits. Task 010 explicitly requires updates to `.ai-collab/runtime/codex-session.yaml`, but `AGENTS.md` states that Codex must not write `.ai-collab/runtime/codex-session.yaml`.
- 2026-03-21: Verified the stale fields still exist in `.ai-collab/runtime/codex-session.yaml` (`recent_tasks: ["003", "004"]`, `handoff_summary.last_updated: "2026-03-18T00:01:00Z"`) and that `.ai-collab/runtime/codex-handoff.md` is also stale relative to task 009 completion.
- 2026-03-21: Suggested next step: Claude or a human should either update `AGENTS.md` to permit this narrow runtime-state maintenance task, or apply the `codex-session.yaml` changes directly and then re-invoke Codex for the handoff rewrite if still needed.
