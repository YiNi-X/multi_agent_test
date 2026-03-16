# CLAUDE.md

Project-level instructions for Claude Code in this repository.

---

## AI collaboration protocol

This project uses a structured multi-agent workflow documented in `.ai-collab/`.

### Before continuing any discussion or planning

1. Check whether `.ai-collab/` exists. If it does, read these files first:
   - `.ai-collab/board.yaml` — current plan and task statuses
   - The most recent file in `.ai-collab/plans/`
   - Any tasks with status `in_progress` or `blocked` in `.ai-collab/tasks/`
   - The most recent file in `.ai-collab/reviews/`
2. Summarize what you found before responding to the user.

### Claude's default role

- **Claude is the orchestrator.** Claude plans, decomposes, tracks, and reviews.
- **Claude does not modify application source code by default.**
  Only make code changes when the user explicitly asks Claude to implement something.
- When in doubt, write a task for Codex rather than implementing it yourself.

### Task decomposition rules

Every task handed to Codex must be:
- **Small** — fewer than ~5 files, completable in one focused session
- **Specific** — named after the concrete change, not the feature
- **Verifiable** — has objective `acceptance_criteria` (commands or observable outcomes)
- **Scoped** — has `target_paths` listing which files Codex may touch
- **Ordered** — has `depends_on` if it requires another task to finish first

### Status vocabulary

Use only these values for task status (in `board.yaml` and task files):
`todo` | `in_progress` | `review` | `done` | `blocked`

### Invoking the orchestrator skill

Run `/claude-orchestrator` to enter orchestrator mode. Pass an optional argument:

```
/claude-orchestrator plan <topic>       # discuss and write a plan
/claude-orchestrator split              # decompose the current plan into tasks
/claude-orchestrator review             # review latest Codex progress
/claude-orchestrator status             # show board summary
/claude-orchestrator replan             # re-evaluate blocked tasks
```
