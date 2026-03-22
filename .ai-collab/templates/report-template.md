# Report: <task title>

<!-- File: reports/report-<task-ID>-<YYYY-MM-DD>.md -->
<!-- Author: codex (implementor) -->

---

## report_id

`REPORT-<ID>-<YYYY-MM-DD>`

## task_id

`<ID>`

## summary

- Concise description of what was implemented, fixed, or investigated.
- Note any deviation from the original task steps.

## files_changed

```text
src/...
tests/...
```

## validation_run

```text
<command and relevant output>
```

## result

`review` | `blocked`

## blockers

- Leave this section as `None` if the result is `review`.
- If blocked, explain the blocker, the evidence, and what Claude needs to resolve.

## residual_risks

- List any remaining trade-offs, follow-up work, or reviewer watch-outs.
- Write `None` if there are no known residual risks.

## suggested_next_step_for_claude

- Review the report and confirm whether the task should move to `done`.
- If blocked, clarify the task or replan the next step before reassigning it.
