# Review: <task or plan title>

<!-- File: reviews/review-<YYYY-MM-DD>-<N>.md -->
<!-- Author: claude (orchestrator) -->

---

## Metadata

| Field | Value |
|---|---|
| Review ID | `review-<YYYY-MM-DD>-<N>` |
| Reviewing | Task `<ID>` / Plan `<NNN>` |
| Report read | `reports/task-<ID>-<slug>-<YYYY-MM-DD>.md` or `N/A (Mode A)` |
| Invocation mode | `A - MCP direct` or `B - report required` |
| Mode A evidence | *(Mode A only)* Key excerpt from MCP response confirming acceptance criteria, or `N/A` for Mode B |
| Date | YYYY-MM-DD |
| Reviewer | claude |

---

## Summary

> Two to four sentences. What did Codex do? Did it meet the objective?

---

## Acceptance criteria check

| Criterion | Result | Notes |
|---|---|---|
| (copy from task) | pass / fail / partial | |
| (copy from task) | pass / fail / partial | |

---

## Code / output observations

<!--
Specific observations about what was produced.
Reference file paths and line numbers where relevant.
-->

- ...
- ...

---

## Decision

- [ ] **Accepted** — task is done. Status → `done`.
- [ ] **Rework required** — task goes back to `todo` or `in_progress`. See rework instructions below.
- [ ] **Blocked by external factor** — status remains `blocked`. See notes below.

---

## Rework instructions

<!--
If decision is "Rework required", list exactly what Codex must fix.
Be specific: file, function, behaviour expected.
-->

1. ...
2. ...

---

## Next step recommendation

<!--
After this review, what should happen next?
Suggest the next task ID for Codex, or any replanning needed.
-->

**Suggested next task for Codex:** `task-<ID>` — <one-line description>

**Board updates made:**
- Task `<ID>` status → `done` / `todo` / `blocked`
- `board.yaml > suggested_next_for_codex` updated

---

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
- [ ] PASS -> commit all changes, open PR, update `board.yaml > current_plan.status: done`
- [ ] REWORK -> list tasks that need rework, return them to `todo`
- [ ] BACK TO PRD -> describe the mismatch, set `spec_dirty: true`, update SPEC.md before next plan
