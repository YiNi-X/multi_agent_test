# Task 032 — resume-session-policy

## Goal
Update `CLAUDE.md` Session tracking section to prefer `codex exec --full-auto resume --last` for ALL tasks within the same working session, not just dependent tasks.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — modifies 1 file, criteria verifiable from readback

## Target paths
- `CLAUDE.md`

## Pre-conditions
- None

## Instructions

In `CLAUDE.md`, find the `**Session tracking:**` bullet list under `### Codex CLI execution model`.

Replace the existing resume/new-session decision rule with:

```markdown
**Session tracking:**
- After each `codex exec` run, get the session ID from the output header line `session id: <id>`
- Store in `runtime/codex-session.yaml` (path is relative to `.ai-collab/`) under `last_session_id`
- **Default: prefer `resume --last` within the same working session** — use `codex exec --full-auto resume --last "..."` for all tasks unless one of the exceptions below applies
- Only start a **fresh session** when:
  1. `last_session_id` is empty (first task ever)
  2. Explicitly starting a new plan after a gap of days
  3. The previous session is confirmed expired (resume returns session-not-found error)
- To resume:
  ```bash
  cd <project-root> && codex exec --full-auto resume --last "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first. Do not modify board.yaml or runtime/codex-session.yaml."
  ```
- To start fresh:
  ```bash
  cd <project-root> && codex exec --full-auto "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first. Do not modify board.yaml or runtime/codex-session.yaml."
  ```
```

## Acceptance criteria
- `CLAUDE.md` Session tracking section says "prefer resume --last within the same working session"
- The three fresh-session exceptions are listed
- Both resume and fresh-session command templates are present

## must_haves
- 默认行为改为 resume，减少 Codex 每次重新翻阅项目文件的 token 消耗
- 三种例外情况明确列出，避免歧义

## Depends on
- (none)

## Updated
2026-03-23

## Codex execution log

- 2026-03-23: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work; confirmed task `032` is `todo`, assigned to `codex`, and has no dependencies in `board.yaml`.
- 2026-03-23: Updated [`CLAUDE.md`](../../CLAUDE.md) `**Session tracking:**` under `### Codex CLI execution model` to prefer `codex exec --full-auto resume --last` for all tasks within the same working session, list the three fresh-session exceptions, and include both resume and fresh-session command templates with the `Do not modify board.yaml or runtime/codex-session.yaml` guardrail.
- 2026-03-23: Validation: `rg -n --fixed-strings "Default: prefer " CLAUDE.md`, `rg -n --fixed-strings "Only start a **fresh session** when" CLAUDE.md`, `rg -n --fixed-strings "To start fresh:" CLAUDE.md`, and a line readback of [`CLAUDE.md`](../../CLAUDE.md) confirmed the required session-tracking text and both command templates are present.
- 2026-03-23: Validation: `python tools/check_consistency.py` failed due a pre-existing mismatch between `.ai-collab/runtime/codex-session.yaml` and `.ai-collab/runtime/codex-handoff.md` (`session_id` and `last_task_id` differ). This task does not permit modifying runtime state, so the mismatch was left untouched for Claude.

```text
Task: task-032-resume-session-policy
Result: review
Files changed: CLAUDE.md, .ai-collab/tasks/task-032-resume-session-policy.md
Validation: rg -n --fixed-strings "Default: prefer " CLAUDE.md; rg -n --fixed-strings "Only start a **fresh session** when" CLAUDE.md; rg -n --fixed-strings "To start fresh:" CLAUDE.md; python tools/check_consistency.py
Notes for Claude: Existing modifications in .ai-collab/board.yaml and .ai-collab/runtime/codex-session.yaml were left untouched; `python tools/check_consistency.py` currently fails because `.ai-collab/runtime/codex-session.yaml` and `.ai-collab/runtime/codex-handoff.md` are out of sync (`session_id` and `last_task_id` mismatch).
```
