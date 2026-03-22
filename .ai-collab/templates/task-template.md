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

## Invocation mode

`A` or `B` - state the mode and one-line rationale.
- `A` (MCP direct): <= 2 files, all criteria verifiable from MCP response, no code logic changes
- `B` (report required): > 2 files, OR shell command verification needed, OR code logic changes

---

## Objective

> One sentence. What concrete change does this task make?

---

## Context

<!--
What does Codex need to know before starting?
Reference relevant plan requirements (for example, REQ-01) and any existing code to
read first. Keep this to 3-5 bullet points.
-->

- ...
- ...

---

## Target paths

<!--
Files or directories that Codex is expected to create or modify.
Codex should not touch files outside this list without checking with the orchestrator.
-->

```text
src/...
tests/...
```

---

## Steps

<!--
Optional for simple tasks (1-2 steps). Required for complex tasks.
If the objective is self-evident, this section may be omitted.
For tasks that need it, provide an ordered list of concrete implementation steps.
-->

1. ...
2. ...

---

## Acceptance criteria

<!--
Objective, testable conditions. The task is done when all of these pass.
Use commands or test names where possible.
-->

- [ ] `<test command or observable outcome>`
- [ ] `<test command or observable outcome>`

**Definition of done (always required):**
- [ ] All criteria above pass
- [ ] `## Codex execution log` appended to this task file
- [ ] If invocation mode is `B`: report written to `reports/task-<ID>-<slug>-<YYYY-MM-DD>.md`
- [ ] No files modified outside `target_paths`

## must_haves (optional)

<!--
Use this section for complex tasks that modify 3+ files or where the same concept
must be expressed consistently across multiple files.

Write from the goal backward: what must be TRUE for the objective to be achieved?
Not "what did Codex write" but "what must the system guarantee after this task".

Skip this section for simple tasks (1-2 files) where acceptance_criteria already
captures the full intent.

Example:
  - "All three files describe the canary failure path with the same user-confirmation step"
  - "The spec version in board.yaml, SPEC.md, and codex-handoff.md are identical"
-->

- (optional - add goal-backward truths here for complex tasks)

### Claude review handoff

1. Claude sets task status to `review` in `board.yaml` before writing the review document.
2. Claude writes the review document in `reviews/`.
3. Claude sets task status to `done` in `board.yaml` after accepting the output.

---

## Codex execution log

<!--
Only Codex writes this section. Do not edit the task definition sections above.
Claude reads this section during review.

Mode A: Write a complete summary here (this is the primary record).
Mode B: Write 3 lines max + a reference to the report file. Full details go in the report.
  Format:
    Status: in_progress -> review
    Report: reports/task-<ID>-<slug>-<YYYY-MM-DD>.md
    Summary: (one line describing what was done)
-->
