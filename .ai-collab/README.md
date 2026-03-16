# .ai-collab — Multi-Agent Collaboration Protocol

This directory is the shared workspace for Claude (orchestrator) and Codex (implementor).
All planning, task assignment, progress tracking, and review happens here.

---

## Directory layout

```
.ai-collab/
  README.md          ← this file
  board.yaml         ← single source of truth for plan + task status
  plans/             ← Claude writes plan documents here
  tasks/             ← one file per task; Codex reads and back-fills results
  reviews/           ← Claude writes review conclusions here
  reports/           ← Codex writes progress/completion reports here
  templates/         ← canonical templates for each document type
```

---

## Status values

Every task moves through exactly this lifecycle. Use these values verbatim in
`board.yaml` and task files — do not invent synonyms.

| Status | Meaning |
|---|---|
| `todo` | Task is defined and waiting to be picked up |
| `in_progress` | Codex has claimed the task and is working on it |
| `review` | Codex has finished; waiting for Claude to review |
| `done` | Claude has reviewed and accepted the output |
| `blocked` | Work cannot continue; blocker is documented in the task file |

---

## Role responsibilities

### Claude (orchestrator)
- Discusses requirements with the user and writes plan documents
- Decomposes plans into atomic tasks with clear acceptance criteria
- Writes to: `plans/`, `tasks/` (initial definition), `reviews/`, `board.yaml`
- Updates task statuses after reviewing Codex reports
- Does **not** modify application source code unless the user explicitly requests it

### Codex (implementor)
- Reads tasks from `tasks/` and picks up items with status `todo`
- Updates the task file status to `in_progress` when starting
- Writes a report to `reports/` when finished or blocked
- Updates the task file status to `review` or `blocked`
- Does **not** change `board.yaml` — that is Claude's responsibility

---

## Update principles

1. `board.yaml` is the authoritative status record. Keep it in sync after every action.
2. Never delete task or plan files. Archive them by appending `-archived` to the filename
   if they are superseded.
3. Timestamps use ISO 8601 date format: `YYYY-MM-DD`.
4. Task IDs are sequential integers, zero-padded to three digits: `001`, `002`, …
5. All filenames use kebab-case.
6. A task is only `done` after Claude has written a review and explicitly marked it so.
