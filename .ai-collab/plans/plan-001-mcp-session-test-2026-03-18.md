# Plan: MCP Session Test

<!-- File: plans/plan-001-mcp-session-test-2026-03-18.md -->
<!-- Author: claude (orchestrator) -->
<!-- Status: active -->

---

## Metadata

| Field | Value |
|---|---|
| Plan ID | `plan-001` |
| Date | 2026-03-18 |
| Status | active |
| Related board entry | `board.yaml > current_plan` |

---

## Goal

Verify the end-to-end Codex MCP workflow: confirm that a first `codex()` call creates a usable session, that Claude correctly records `thread_id` and related fields in `codex-session.yaml`, and that a subsequent `codex-reply()` call successfully resumes the same session.

---

## Background and context

Tasks 001 and 002 (update-codex-probe, create-mini-py) were executed before session tracking was fully in place. This plan establishes the session continuity mechanism:

- `codex-session.yaml` tracks the active thread; **Claude owns and writes it**.
- After each Codex response, Claude updates: `active`, `thread_id`, `last_used_at`, `last_task_id`, `spec_version_at_start`, `handoff_version`.
- After Claude reviews a completed task, **Claude** updates `board.yaml`. Codex does not write to `board.yaml`.

---

## Scope

### In scope
- First Codex MCP invocation (`mcp__codex__codex`)
- Session recording in `codex-session.yaml`
- Session resumption via `mcp__codex__codex-reply` using existing `thread_id`

### Out of scope
- Session expiry / forced-new-session logic (covered by policy, not tested here)
- Spec-version-triggered session reset
- Multi-session concurrency

---

## Requirements

1. **REQ-01:** After task 003 completes, `codex-session.yaml` must contain a non-empty `thread_id` and `active: true`.
2. **REQ-02:** Task 004 must call `codex-reply()` with the `thread_id` recorded in task 003 — no new `codex()` call.
3. **REQ-03:** Codex must not write to `board.yaml` or `codex-session.yaml`; only Claude does.
4. **REQ-04:** Session fields updated by Claude are limited to: `active`, `thread_id`, `last_used_at`, `last_task_id`, `spec_version_at_start`, `handoff_version`.

---

## Risks and open questions

| # | Risk / question | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | Codex MCP tool returns no `threadId` | Low | High | Fail task 003; investigate before proceeding to task 004 |
| 2 | `codex-reply()` silently opens a new session | Low | Medium | Verify response context references prior conversation turn |

---

## Decomposition strategy

Tasks 001 and 002 are already done. This plan adds tasks 003 and 004:

1. **task-003** — first-codex-mcp-call: Invoke Codex via `mcp__codex__codex()` with a simple probe. Claude records the returned session fields.
2. **task-004** — resume-codex-mcp-session: Invoke `mcp__codex__codex-reply()` using the `thread_id` from task 003. Confirms session continuity.

### Proposed task sequence

1. `task-003` — first-codex-mcp-call
2. `task-004` — resume-codex-mcp-session (depends on task-003)

---

## Acceptance criteria for the whole plan

- [ ] `CODEX_CANARY.md` contains a line written by Codex in task 003.
- [ ] `codex-session.yaml.thread_id` is non-empty after task 003.
- [ ] `CODEX_CANARY.md` contains a second line written by Codex in task 004 (same session).
- [ ] `codex-session.yaml.handoff_version` incremented to at least `2` after task 004.
- [ ] `board.yaml` reflects final task statuses updated by Claude, not Codex.

---

## Notes and decisions log

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-18 | Claude is sole writer of `board.yaml` and `codex-session.yaml` | Prevents race conditions; keeps audit trail clear |
| 2026-03-18 | Session fields limited to: `active`, `thread_id`, `last_used_at`, `last_task_id`, `spec_version_at_start`, `handoff_version` | Avoids referencing fields not confirmed as schema requirements |
