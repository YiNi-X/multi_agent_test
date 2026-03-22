# AGENTS.md

Repository-level instructions for agents working in this repo.

## AI collaboration protocol

- Before starting any `.ai-collab` task, read `.ai-collab/README.md` and
  `.ai-collab/board.yaml`. Then read the selected task file.
- Codex handles exactly one task at a time. If the input refers to multiple tasks,
  or no single eligible task exists, stop without changing project files and report
  the issue.
- Claude owns the overall plan, task definition, review decisions, and
  `board.yaml`. Codex must not rewrite Claude's requirements, acceptance criteria,
  target paths, or plan structure.
- Codex may write only:
  - the Codex-owned execution section in a task file, such as
    `## Codex execution log`
  - files under `.ai-collab/reports/`
  - implementation files allowed by the selected task's `target_paths`
- Codex must not write `.ai-collab/board.yaml`.
- Codex must not write `.ai-collab/runtime/codex-session.yaml`.
- Codex must run the project's existing validation commands. Use this priority
  order:
  1. commands explicitly declared in `AGENTS.md`
  2. commands named in the task acceptance criteria
  3. existing project-native validation commands already present in the repo
- This repository does not currently declare fixed global validation commands in
  `AGENTS.md`. Until it does, follow the priority order above.
- If Codex is blocked, document the reason, evidence, and suggested next step in
  the task execution log and the report. Do not expand scope, rewrite the plan, or
  silently make a broader change.

## Codex CLI execution context

When invoked via CLI (`codex` or `codex exec`):

- **Single task focus:** Execute only the task specified in the prompt or task file. Do not pick up additional tasks from `board.yaml`.
- **Read task file first:** Before doing anything, read the full task file at `.ai-collab/tasks/task-<ID>-<slug>.md`.
- **Session continuity:** If the user runs `codex resume <session-id>`, you are continuing a previous session. Reference prior context from that session.
- **Report back:** For Mode B tasks, write a report to `.ai-collab/reports/task-<ID>-<slug>-<YYYY-MM-DD>.md`. For Mode A tasks, write a complete summary in the execution log.
- **Do not update board.yaml:** Claude will update task statuses after reviewing your execution log.
- **Do not write `runtime/codex-session.yaml`:** Claude maintains this file.
