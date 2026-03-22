# Codex Worker Protocol

This document defines how Claude invokes Codex CLI automatically and how session continuity works.

---

## Invocation methods

### Method 1: New session (automatic)

Claude runs via Bash tool:
```bash
cd <project-root> && codex exec --full-auto "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first. Do not modify board.yaml or runtime/codex-session.yaml."
```

Use when:
- Task is independent (no `depends_on` referencing last task)
- Starting a new plan or a new batch of work

### Method 2: Resume previous session (automatic)

Claude runs via Bash tool:
```bash
cd <project-root> && codex exec --full-auto resume --last "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first."
```

Use when:
- Task has `depends_on` referencing the last executed task
- Continuing work that benefits from prior session context

### Method 3: Manual fallback

If `codex exec` is unavailable or fails, tell the user to run:
```bash
codex "Execute task <ID> in .ai-collab/tasks/task-<ID>-<slug>.md. Read AGENTS.md and .ai-collab/board.yaml first."
```

---

## Session tracking

After each `codex exec` run:
1. Claude gets the session ID from the output header line `session id: <id>`
2. Claude updates `runtime/codex-session.yaml`:
   - `last_session_id`: the session ID from the `codex exec` output
   - `last_task_id`: the task ID just executed
   - `last_used_at`: current date
   - `total_tasks_executed`: increment by 1

---

## Session lifecycle

```text
[New task] -> Does task have depends_on referencing last task?
              -> YES: Resume session (codex exec --full-auto resume --last)
              -> NO:  New session (codex exec --full-auto)
              -> After execution:
                 Read the session id from codex exec output
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

Local Codex CLI sessions are stored in `~/.codex/sessions/` and do not expire. Session continuity is managed by `codex exec --full-auto resume --last` when Claude wants to reuse the previous execution context.

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
