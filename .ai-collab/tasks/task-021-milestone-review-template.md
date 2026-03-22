# Task 021 — milestone-review-template

## Goal
Create `spec/MILESTONE.md` as a milestone-level review template. After each milestone (a group of related plans), Claude writes a milestone review summarising all delivered capabilities, verified against the original requirements.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: creates 1 file, criteria verifiable from MCP response, documentation only

## Target paths
- `.ai-collab/templates/milestone-template.md`

## Pre-conditions
- None

## Instructions

Create `.ai-collab/templates/milestone-template.md` with the following content:

```markdown
# Milestone Review: <title>

<!-- File: spec/milestones/milestone-<NNN>-<slug>-<YYYY-MM-DD>.md -->
<!-- Author: claude (orchestrator) -->

---

## Metadata

| Field | Value |
|---|---|
| Milestone ID | `milestone-<NNN>` |
| Date | YYYY-MM-DD |
| Plans included | `plan-<NNN>`, `plan-<NNN>` |
| Spec version at start | `v<X.Y.Z>` |
| Spec version at end | `v<X.Y.Z>` |

---

## Delivered capabilities

<!--
List what the system can do now that it couldn't before this milestone.
Write from the user's perspective.
-->

- ...
- ...

---

## Requirements coverage

| REQ-ID | Requirement | Status | Evidence |
|---|---|---|---|
| REQ-01 | ... | covered / partial / not covered | task-XXX or N/A |

---

## What was NOT delivered

<!--
Honestly list anything that was planned but deferred or descoped.
Reference the decision or review that explains why.
-->

- ...

---

## Quality observations

<!--
Cross-cutting observations: consistency, protocol health, debt introduced.
-->

- ...

---

## Verdict

- [ ] **ACCEPTED** — milestone complete. Update `board.yaml > current_milestone`. Proceed to next milestone planning.
- [ ] **PARTIAL** — core capabilities delivered but gaps remain. List follow-up tasks below.
- [ ] **REJECTED** — fundamental issues. Return to PRD.

**Follow-up tasks (if PARTIAL):**
- task-XXX: ...

---

## Next milestone proposal

<!--
One paragraph: what should the next milestone focus on, and why?
-->
```

## Acceptance criteria
- `templates/milestone-template.md` exists
- Contains sections: Metadata, Delivered capabilities, Requirements coverage table, What was NOT delivered, Quality observations, Verdict (3 options), Next milestone proposal
- Requirements coverage table references REQ-IDs matching SPEC.md format

## must_haves
- 里程碑结束时有正式的「已实现功能 review」文档，不只是 board.yaml 上的 done 标记
- Requirements coverage 表格将实现结果追溯回 SPEC.md 的 REQ-ID

## Depends on
- task-019 (REQ-ID format established)

## Updated
2026-03-22

## Codex execution log
- 2026-03-22: Created `.ai-collab/templates/milestone-template.md` with the requested milestone review structure, including Metadata, Delivered capabilities, Requirements coverage, What was NOT delivered, Quality observations, Verdict, and Next milestone proposal.
- 2026-03-22: Used `REQ-01` format in the Requirements coverage table so the template matches the REQ-ID format currently present in `.ai-collab/spec/SPEC.md`.
- 2026-03-22: Verified the new template contains all required sections and the three verdict options required by the task acceptance criteria.
