# Task 005 — fix-protocol-orphan-fields

## Goal
Fix three orphan fields in the protocol that have definitions but no write rules:
1. `total_tasks_executed` in `codex-session.yaml` — never incremented
2. `spec_hash_at_start` in `codex-session.yaml` — no write procedure
3. `suggested_next_for_codex` in `board.yaml` — no validity condition documented

## Status
`todo`

## Assigned to
codex

## Target paths
- `.ai-collab/templates/codex-worker-protocol.md`
- `.ai-collab/board.yaml`

## Pre-conditions
- None

## Instructions

### Fix 1: `total_tasks_executed` write rule
In `.ai-collab/templates/codex-worker-protocol.md`, under the session lifecycle section, add an explicit rule:
> After Claude updates `last_task_id`, it must also increment `total_tasks_executed` by 1.

Add this to the "Update codex-session.yaml" step in the session lifecycle diagram and in the post-invocation checklist (if present).

### Fix 2: `spec_hash_at_start` write procedure
In `.ai-collab/templates/codex-worker-protocol.md`, under the "Start new session" section (Method 1), add a step:
> Before calling `codex()`, Claude writes `spec_hash_at_start` as the combination of `spec version + spec last_updated` (e.g. `"0.2.0/2026-03-17"`). This value is compared on subsequent invocations to detect spec changes.

### Fix 3: `suggested_next_for_codex` validity condition
In `.ai-collab/board.yaml`, add a comment above the `suggested_next_for_codex` block:
```yaml
# suggested_next_for_codex is only valid when current_plan.status == "in_progress".
# When current_plan.status == "done", set task_id to "" and reason to explain there are no pending tasks.
```

## Acceptance criteria
- `codex-worker-protocol.md` contains a rule that `total_tasks_executed` must be incremented when `last_task_id` is updated
- `codex-worker-protocol.md` contains a step for writing `spec_hash_at_start` (format: `"<version>/<last_updated>"`) before a new `codex()` call
- `board.yaml` comment above `suggested_next_for_codex` states it is only valid when `current_plan.status == "in_progress"`

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Updated `.ai-collab/templates/codex-worker-protocol.md` to define the `spec_hash_at_start` write procedure before a new `codex()` call and to require incrementing `total_tasks_executed` when `last_task_id` is updated.
- 2026-03-21: Verified `.ai-collab/board.yaml` already contained the required `suggested_next_for_codex` validity comment, so no board edit was necessary.
- 2026-03-21: Validated the acceptance criteria by inspecting the final file contents and wrote the task report.
