# Review: <task or plan title>

<!-- File: reviews/review-<YYYY-MM-DD>-<N>.md -->
<!-- Author: claude (orchestrator) -->

---

## Metadata

| Field | Value |
|---|---|
| Review ID | `review-<YYYY-MM-DD>-<N>` |
| Reviewing | Task `<ID>` / Plan `<NNN>` |
| Report read | `reports/report-<ID>-<YYYY-MM-DD>.md` |
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
