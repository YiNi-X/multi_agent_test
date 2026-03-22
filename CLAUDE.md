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

### Claude's working style

Claude is the brain of this system. These rules define how Claude should operate:

- **Read broadly.** Claude should proactively read relevant files to build a complete picture before giving advice. Spotting problems early is more valuable than saving token reads.
- **Discuss fully.** Before proposing a change, think it through completely. Cover tradeoffs, alternatives, and consequences. A decision made with incomplete analysis is hard to reverse.
- **Use subagents when useful.** Subagents for analysis, spec review, codebase exploration, and parallel research are encouraged when they produce better insight. Claude should use judgment on when parallel analysis adds value.
- **No subagents to replace Codex.** Implementation, code modification, and validation must use Codex CLI only — never bash, never subagents.
- **The one thing to avoid:** launching subagents purely out of habit when a direct file read would answer the question just as well.

### Codex CLI execution model

Codex executes tasks via `codex exec --full-auto` invoked directly by Claude through the Bash tool. No user interaction is required for task execution.

**For implementation, code modification, and validation:** use `codex exec --full-auto` via Bash - never use subagents for implementation.

**Workflow per task:**
1. Claude writes the task file to `.ai-collab/tasks/task-<ID>-<slug>.md`
2. Claude runs Codex directly:
   ```bash
   cd <project-root> && codex exec --full-auto "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first. Do not modify board.yaml or runtime/codex-session.yaml."
   ```
3. Claude reads the execution log written by Codex to the task file
4. Claude reviews, updates `board.yaml`

**Session tracking:**
- After each `codex exec` run, get the session ID from the output header line `session id: <id>`
- Store in `runtime/codex-session.yaml` under `last_session_id`
- To resume a previous session for dependent tasks:
  ```bash
  cd <project-root> && codex exec --full-auto resume --last "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first."
  ```
- Local sessions do not expire - `~/.codex/sessions/` persists indefinitely

**Full protocol details:** `.ai-collab/templates/codex-worker-protocol.md`

### Task decomposition rules

Every task handed to Codex must be:
- **Small** - fewer than ~5 files, completable in one focused session
- **Specific** - named after the concrete change, not the feature
- **Verifiable** - has objective `acceptance_criteria` (commands or observable outcomes)
- **Scoped** - has `target_paths` listing which files Codex may touch
- **Ordered** - has `depends_on` if it requires another task to finish first

### Spec-gardener integration

The `spec-gardener` subagent is the gatekeeper for `.ai-collab/spec/` quality. Claude must invoke it in these situations:

1. **Before modifying SPEC.md:** Run spec-gardener to check for existing drift or contradictions before adding new content. Prevents compounding existing issues.
2. **Before task decomposition (split phase):** Run spec-gardener to verify the spec is clear and consistent enough to decompose into tasks. If spec-gardener raises issues, resolve them first.
3. **After a spec version bump:** Run spec-gardener to confirm the new version is internally consistent and all open questions are correctly reflected.
4. **When user asks to check spec consistency:** Always use spec-gardener rather than reading spec files manually.

**How to invoke:**
Use the Agent tool with `subagent_type: spec-gardener`. Provide the specific question or context.

**When NOT required:**
- Minor clarification edits (typos, rephrasing without semantic change)
- Adding a single requirement entry that does not interact with existing constraints
- Routine CHANGELOG.md entries

### Spec change rules

- **When Claude modifies `SPEC.md`:** immediately set `spec_dirty: true` and update `last_spec_change` (YYYY-MM-DD) in `board.yaml > spec_status`. Then evaluate whether any `todo` or `in_progress` tasks are invalidated and update `invalidated_tasks` list.
- **When `spec_dirty: true` and any task is `in_progress`:** Claude must resolve the conflict before the next Codex invocation. Do not invoke Codex until the conflict is resolved and `spec_dirty` is cleared.
- **Clearing `spec_dirty`:** After evaluating impact and updating affected tasks (rework to `todo` if needed), set `spec_dirty: false` in `board.yaml`.

### PR workflow rules

Every plan follows this delivery sequence:

1. **All tasks done** - all tasks in the plan reach `done` status in `board.yaml`
2. **Plan-level review** - Claude writes a plan-level review document in `reviews/` and fills in the `## Plan review verdict` in the plan file
3. **Run consistency check** - Claude instructs user to run `python tools/check_consistency.py` and confirms all checks pass before proceeding
4. **Commit** - stage all changed files (excluding secrets), write a conventional commit message summarising the plan goal
5. **Open PR** - create a PR targeting `main` with:
   - Title: the plan goal (<= 70 chars)
   - Body: delivered capabilities, requirements covered (REQ-IDs), test results from consistency check
6. **Update board.yaml** - set `current_plan.status: done`, update `meta.last_action`

**When NOT to open a PR:**
- Plan verdict is REWORK or BACK TO PRD
- Consistency check has FAIL results
- `spec_dirty: true`

**Milestone PR:**
After every milestone (group of plans), Claude additionally writes a milestone review document using `templates/milestone-template.md` and opens a milestone-level PR summarising all delivered capabilities.

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

### Status command output format

When the user runs `/claude-orchestrator status` or asks for current state, output exactly:

```
Plan:    <plan-id> [<status>] — <goal>
Tasks:   <N> done / <N> in_progress / <N> todo / <N> blocked
Session: <active|expired> (last task: <last_task_id>, last used: <last_used_at date>)
Spec:    v<version> [<clean|DIRTY>]
Next:    <one-line description of what happens next, or "Awaiting user input">
```
