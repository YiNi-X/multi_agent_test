# Task 020 — plan-review-verdict

## Goal
Add a plan-level Review verdict field to `plan-template.md` and `review-template.md` so that a completed plan has an explicit pass/fail/back-to-PRD decision, not just individual task reviews.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 2 files, criteria verifiable from MCP response, documentation only

## Target paths
- `.ai-collab/templates/plan-template.md`
- `.ai-collab/templates/review-template.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Add plan-level verdict to plan-template.md

In `plan-template.md`, after `## Acceptance criteria for the whole plan`, add:

```markdown
## Plan review verdict

<!--
Filled in by Claude after all tasks in this plan are done and the plan-level review is complete.
Do not fill this in until all tasks are done.
-->

- [ ] **PASS** — all plan acceptance criteria met. Proceed to commit + PR.
- [ ] **REWORK** — one or more criteria failed. Specific tasks return to `todo`. See review doc.
- [ ] **BACK TO PRD** — fundamental requirement mismatch. Update SPEC.md before replanning.

**Verdict date:**
**Review doc:** `reviews/review-<YYYY-MM-DD>-<N>.md`
```

### Fix 2: Add plan-level review section to review-template.md

In `review-template.md`, after `## Next step recommendation`, add:

```markdown
## Plan-level verdict (fill only when reviewing a completed plan, not individual tasks)

<!--
When all tasks in a plan are done, Claude writes a plan-level review.
This section determines what happens next at the plan level.
-->

| Criterion | Result |
|---|---|
| All task acceptance criteria passed | pass / fail |
| Plan-level acceptance criteria met | pass / fail |
| No unresolved spec conflicts | pass / fail |

**Verdict:**
- [ ] PASS → commit all changes, open PR, update `board.yaml > current_plan.status: done`
- [ ] REWORK → list tasks that need rework, return them to `todo`
- [ ] BACK TO PRD → describe the mismatch, set `spec_dirty: true`, update SPEC.md before next plan
```

## Acceptance criteria
- `plan-template.md` contains a `## Plan review verdict` section with 3 options (PASS/REWORK/BACK TO PRD)
- `review-template.md` contains a `## Plan-level verdict` section with a criteria table and 3 verdict options
- Both sections include a comment explaining when to fill them in

## must_haves
- 每个 Plan 结束时有明确的三选一判定，不再是隐式的「所有任务 done 就结束」
- BACK TO PRD 选项为「回到文档修正」提供了正式的协议路径

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log
- 2026-03-22: Added `## Plan review verdict` to `.ai-collab/templates/plan-template.md` after the plan-level acceptance criteria section, with PASS / REWORK / BACK TO PRD options and verdict metadata fields.
- 2026-03-22: Added `## Plan-level verdict` to `.ai-collab/templates/review-template.md` after `## Next step recommendation`, including the criteria table, the three verdict options, and a comment explaining it is only for completed-plan reviews.
- 2026-03-22: Verified both sections by re-reading the edited templates and confirming the required headings, comments, table, and verdict options match the task acceptance criteria.
