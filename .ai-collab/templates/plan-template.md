# Plan: <title>

<!-- File: plans/plan-<slug>-<YYYY-MM-DD>.md -->
<!-- Author: claude (orchestrator) -->
<!-- Status: draft | active | done | superseded -->

---

## Metadata

| Field | Value |
|---|---|
| Plan ID | `plan-<NNN>` |
| Date | YYYY-MM-DD |
| Status | draft |
| Related board entry | `board.yaml > current_plan` |

---

## Goal

> One or two sentences. What does this plan achieve? What user or business outcome does it enable?

---

## Background and context

<!--
Why are we doing this now? What existing code, constraints, or decisions are relevant?
Keep this short — link to external docs rather than duplicating them.
-->

---

## Scope

### In scope
- Item 1
- Item 2

### Out of scope
- Item A (reason)
- Item B (reason)

---

## Requirements

<!--
List functional and non-functional requirements. Number them so tasks can reference them.
-->

1. **REQ-01:** ...
2. **REQ-02:** ...

---

## Risks and open questions

| # | Risk / question | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | | | | |

---

## Decomposition strategy

<!--
Describe how you intend to split this plan into tasks.
Name the sequencing rationale: what must happen before what, and why.
-->

### Proposed task sequence

1. `task-001` — ...
2. `task-002` — ... (depends on task-001)
3. `task-003` — ...

---

## Acceptance criteria for the whole plan

<!--
The plan is done when ALL of these are true.
These are plan-level; each task has its own criteria.
-->

- [ ] ...
- [ ] ...

---

## Plan review verdict

<!--
Filled in by Claude after all tasks in this plan are done and the plan-level review is complete.
Do not fill this in until all tasks are done.
-->

- [ ] **PASS** - all plan acceptance criteria met. Proceed to commit + PR.
- [ ] **REWORK** - one or more criteria failed. Specific tasks return to `todo`. See review doc.
- [ ] **BACK TO PRD** - fundamental requirement mismatch. Update SPEC.md before replanning.

**Verdict date:**
**Review doc:** `reviews/review-<YYYY-MM-DD>-<N>.md`

---

## Notes and decisions log

| Date | Decision | Rationale |
|---|---|---|
| YYYY-MM-DD | | |
