# Task <ID>: <title>

<!-- File: tasks/task-<ID>-<slug>.md -->
<!-- Defined by: claude (orchestrator) -->
<!-- Executed by: codex -->

---

## Metadata

| Field | Value |
|---|---|
| Task ID | `<ID>` |
| Plan | `plan-<NNN>` |
| Status | `todo` |
| Assigned to | `codex` |
| Depends on | `[]` |
| Date defined | YYYY-MM-DD |
| Date started | |
| Date completed | |

---

## Objective

> One sentence. What concrete change does this task make?

---

## Context

<!--
What does Codex need to know before starting?
Reference relevant plan requirements (e.g. REQ-01) and any existing code to read first.
Keep this to 3–5 bullet points.
-->

- ...
- ...

---

## Target paths

<!--
Files or directories that Codex is expected to create or modify.
Codex should not touch files outside this list without checking with the orchestrator.
-->

```
src/...
tests/...
```

---

## Steps

<!--
Ordered list of concrete implementation steps.
Each step should be small enough that Codex can verify it independently.
-->

1. ...
2. ...
3. ...

---

## Acceptance criteria

<!--
Objective, testable conditions. The task is done when ALL of these pass.
Use commands or test names where possible.
-->

- [ ] `<test command or observable outcome>`
- [ ] `<test command or observable outcome>`
- [ ] No new linter errors in target paths

---

## Definition of done

- [ ] All acceptance criteria above pass
- [ ] Report written to `reports/report-<ID>-<YYYY-MM-DD>.md`
- [ ] Task status updated to `review` in this file
- [ ] `board.yaml` status updated to `review` ← Claude will do this after reading the report

---

## Codex execution log

<!-- Codex fills this section in. Claude reads it during review. -->

**Status update:** `todo` → `in_progress` on YYYY-MM-DD

**Approach taken:**
<!--
Brief description of what Codex actually did. Note any deviations from the steps above.
-->

**Blockers encountered:**
<!--
If status is `blocked`, describe the blocker here in detail so Claude can replan.
-->

**Verification results:**
<!--
Paste test output, lint output, or other evidence that acceptance criteria pass.
-->

**Final status:** `review` | `blocked`
