# Task 007 — fix-handoff-orchestrator-state

## Goal
The current `codex-handoff.md` only records Codex execution state. When Claude's context resets, it cannot reconstruct its own decision-making context from `codex-handoff.md` alone — it must re-read all plans, reviews, and tasks. Add an `orchestrator_state` block to the handoff template and to the current handoff file.

## Status
`todo`

## Assigned to
codex

## Target paths
- `.ai-collab/runtime/codex-handoff.md`
- `.ai-collab/templates/codex-worker-protocol.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Update current `codex-handoff.md`
Rewrite `.ai-collab/runtime/codex-handoff.md` to include an `## Orchestrator state` section with the following fields (populate with current values based on reading `board.yaml` and `spec/SPEC.md`):

```markdown
## Orchestrator state

| Field | Value |
|---|---|
| Current plan | plan-001 (done) |
| Current spec version | 0.2.0 |
| Spec last updated | 2026-03-17 |
| Last review | review-2026-03-18-1 (task-004 accepted) |
| Pending decisions | See SPEC.md open questions section |
| Next action | No pending tasks — awaiting new plan from user |

### Open questions requiring resolution before next plan
1. How should `spec_dirty` be detected? (manual vs auto)
2. What threshold of invalidated tasks triggers full replan vs incremental?
3. When SPEC.md conflicts with active plan, block or complete first?
4. What level of detail should SPEC.md contain vs individual plan documents?
```

### Fix 2: Add `orchestrator_state` block to codex-worker-protocol.md
In `.ai-collab/templates/codex-worker-protocol.md`, add a section:

```markdown
## Handoff document requirements

The `runtime/codex-handoff.md` file must contain two sections:

### 1. Codex execution state
- Last task executed and its outcome
- Active session thread_id
- Files modified in this session

### 2. Orchestrator state
- Current plan ID and status
- Current spec version
- Last review document reference
- Pending open questions from SPEC.md
- Next intended action (and why)

Claude must update both sections after each task review.
```

## Acceptance criteria
- `codex-handoff.md` contains an `## Orchestrator state` section with current plan, spec version, last review, pending decisions, and next action
- `codex-worker-protocol.md` defines the required two-section structure for `codex-handoff.md`
- The four open questions from `SPEC.md` are listed in `codex-handoff.md` under "Open questions"

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Rewrote `.ai-collab/runtime/codex-handoff.md` into separate `Codex execution state` and `Orchestrator state` sections, and populated the orchestrator fields from the current `board.yaml`, `SPEC.md`, and the latest review artifact present on disk.
- 2026-03-21: Updated `.ai-collab/templates/codex-worker-protocol.md` to require the two-section handoff structure and to state that Claude updates both sections after each task review.
- 2026-03-21: Verified that the handoff file now carries the four `SPEC.md` open questions and wrote the task report.
