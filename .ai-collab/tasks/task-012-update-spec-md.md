# Task 012 — update-spec-md

## Goal
Update `SPEC.md` from version 0.2.0 (last updated 2026-03-17) to 0.3.0 to reflect all protocol changes made since then: Mode A/B invocation modes, session canary probe, handoff orchestrator state structure, review state durability rule, and orphan field fixes. Also resolve open questions Q1 and Q3 in SPEC.md, and append a changelog entry.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`B` — report required: modifies 2 spec files, criteria require cross-checking multiple protocol documents

## Target paths
- `.ai-collab/spec/SPEC.md`
- `.ai-collab/spec/CHANGELOG.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Update SPEC.md header

Change:
```
**Last updated:** 2026-03-17
**Version:** 0.2.0
```
To:
```
**Last updated:** 2026-03-21
**Version:** 0.3.0
```

### Fix 2: Add new capabilities to Core capabilities section

In the "Core capabilities" section, add the following after the existing sections:

```markdown
### 6. Session continuity

- Claude checks `runtime/codex-session.yaml` before each Codex invocation
- Sends canary probe (`CANARY_OK:<last_task_id>`) before every `codex-reply()` call
- On canary failure: notifies user, waits for confirmation, then starts new session with `codex()`
- Time-based expiry (`max_idle_minutes`) is a fallback heuristic only; canary probe is the primary check

### 7. Invocation modes

- Every task declares invocation mode in the task file
- **Mode A (MCP direct):** ≤ 2 files, all criteria verifiable from MCP response, no code logic changes. Codex does not write a report file.
- **Mode B (report required):** > 2 files, OR shell command verification needed, OR code logic changes. Codex writes a report to `reports/` before handing off to Claude.
- Mode must be declared in both the task file (`## Invocation mode`) and the Claude invocation prompt.

### 8. Context handoff

- `runtime/codex-handoff.md` contains two mandatory sections: Codex execution state + Orchestrator state
- Claude updates both sections after each task review
- Orchestrator state includes: current plan, spec version, last review, pending open questions, next action
```

### Fix 3: Resolve open questions Q1 and Q3, mark Q2 and Q4 deferred

In the "Open questions" section, replace the four questions with:

```markdown
1. **Spec dirty detection** — **Resolved:** `spec_dirty` is set manually by Claude whenever `SPEC.md` is modified. Claude clears it after evaluating impact on the current plan and updating `board.yaml`.

2. **Replan triggers** — **Deferred:** Threshold not defined. Current policy: Claude evaluates case-by-case when `invalidated_tasks` list is non-empty.

3. **Conflict resolution** — **Resolved:** If `spec_dirty: true` and any task is `in_progress`, Claude must resolve the conflict before the next Codex invocation. Claude must not invoke Codex while `spec_dirty: true` and tasks are active.

4. **Granularity** — **Deferred:** SPEC.md describes system-wide patterns and constraints. Feature-specific requirements live in plan documents.
```

### Fix 4: Append changelog entry to CHANGELOG.md

Append to `.ai-collab/spec/CHANGELOG.md`:

```markdown
## v0.3.0 — 2026-03-21

**Changes:**
- Added Mode A / Mode B invocation mode protocol (task-008)
- Added session canary probe mechanism; time-based expiry is now fallback only (task-009)
- Added mandatory two-section structure for `codex-handoff.md` (task-007)
- Added `review` state durability rule: tasks must not jump from `in_progress` to `done` (task-006)
- Fixed orphan fields: `total_tasks_executed` increment rule, `spec_hash_at_start` write procedure, `suggested_next_for_codex` validity condition (task-005)

**Resolved open questions:** Q1 (spec_dirty detection), Q3 (conflict resolution rule)
**Deferred:** Q2 (replan threshold), Q4 (SPEC granularity)
```

## Acceptance criteria
- `SPEC.md` header shows `Version: 0.3.0` and `Last updated: 2026-03-21`
- `SPEC.md` contains sections 6 (Session continuity), 7 (Invocation modes), 8 (Context handoff)
- `SPEC.md` open questions Q1 and Q3 are marked "Resolved" with the agreed answers
- `SPEC.md` open questions Q2 and Q4 are marked "Deferred"
- `CHANGELOG.md` contains a `## v0.3.0 — 2026-03-21` entry listing all five changes

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Updated `.ai-collab/spec/SPEC.md` from version `0.2.0` to `0.3.0`, added the new core capability sections for session continuity, invocation modes, and context handoff, and renumbered the existing living-spec section to keep the capability numbering coherent.
- 2026-03-21: Replaced the `SPEC.md` open-questions section so Q1 and Q3 are marked resolved with concrete protocol rules, while Q2 and Q4 are explicitly marked deferred.
- 2026-03-21: Added a `v0.3.0` entry to `.ai-collab/spec/CHANGELOG.md` covering tasks 005 through 009 and the resolved/deferred question outcomes.
- 2026-03-21: Cross-checked `SPEC.md` and `CHANGELOG.md` for version/date consistency and wrote the task report.
