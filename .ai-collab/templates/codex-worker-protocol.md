# Codex Worker Protocol

This document defines how Claude instructs the user to invoke Codex CLI and how session continuity works.

---

## Invocation methods

### Method 1: Start new session (interactive)

Claude tells the user to run:
```
codex
```
Then paste the task prompt when Codex starts.

Use when:
- Starting a new task with no prior session context needed
- Task is independent (no `depends_on`)

### Method 2: Start new session (non-interactive)

Claude tells the user to run:
```
codex exec "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first."
```

Use when:
- Task is self-contained and instructions are clear in the task file
- Faster than interactive mode for simple tasks

### Method 3: Resume previous session

Claude tells the user to run:
```
codex resume <session-id>
```
or:
```
codex resume --last
```

Use when:
- Task has `depends_on` referencing the last executed task
- Continuing work that benefits from prior session context

---

## Session tracking

After each Codex run:
1. User reports the session ID (or Claude reads `~/.codex/session_index.jsonl` last entry)
2. Claude updates `runtime/codex-session.yaml`:
   - `last_session_id`: the session ID from `session_index.jsonl`
   - `last_task_id`: the task ID just executed
   - `last_used_at`: current date
   - `total_tasks_executed`: increment by 1

To find the session ID after a run:
```bash
tail -1 ~/.codex/session_index.jsonl
```
The `id` field is the session ID.

---

## Session lifecycle

```text
[New task] -> Does task have depends_on referencing last task?
              -> YES: Resume session (codex resume <last_session_id>)
              -> NO:  New session (codex or codex exec)
              -> After execution:
                 Read ~/.codex/session_index.jsonl last entry
                 Update runtime/codex-session.yaml
                 Claude reviews execution log
                 Claude updates board.yaml
```

---

## Prompt template for Codex invocation

```
You are Codex, the implementation agent in a Claude + Codex multi-agent workflow.

**Context files to read first:**
- AGENTS.md
- .ai-collab/README.md
- .ai-collab/board.yaml
- .ai-collab/spec/SPEC.md (if relevant)

**Your task:**
Execute task `<task-id>` defined in `.ai-collab/tasks/task-<id>-<slug>.md`

**Instructions:**
1. Read the task file completely
2. Implement changes within `target_paths`
3. Run validation from `acceptance_criteria`
4. Write execution log to task file under `## Codex execution log`
5. For Mode B tasks: write report to `reports/task-<id>-<slug>-<YYYY-MM-DD>.md`
6. Do NOT modify `board.yaml` or `runtime/codex-session.yaml`
```

---

## Local session continuity

Local Codex CLI sessions are stored in `~/.codex/sessions/` and do not expire. Session continuity is managed by `codex resume <session-id>`.

---

## Why not use Claude subagents?

Claude subagents lack:
- Codex-specific execution context and tool access
- Access to the local filesystem sandbox
- Session continuity with previous implementation work

**Allowed subagent use cases:**
- Spec review and impact analysis
- Codebase discovery and exploration
- Research and documentation tasks
