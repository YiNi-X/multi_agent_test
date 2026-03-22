# Task 025 — migrate-to-codex-cli

## Goal
Replace all Codex MCP Server invocation references with Codex CLI workflow across the protocol. The new model: Claude writes task files → user runs `codex` CLI → Codex reads task file and executes → Claude reviews execution log. Session tracking uses local `~/.codex/session_index.jsonl` instead of MCP threadId.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`B` — report required: modifies 5 files across multiple directories, criteria require inspecting multiple files

## Target paths
- `CLAUDE.md`
- `AGENTS.md`
- `.ai-collab/templates/codex-worker-protocol.md`
- `.ai-collab/runtime/codex-session.yaml`
- `QUICKSTART.md`

## Pre-conditions
- None (this task supersedes the MCP session model entirely)

## Instructions

### Fix 1: Rewrite `### Codex MCP execution model` in CLAUDE.md

Replace the entire `### Codex MCP execution model` section (including the `#### Session continuity` subsection) with:

```markdown
### Codex CLI execution model

Codex executes tasks via the local CLI: `codex` (interactive) or `codex exec` (non-interactive).

**For implementation, code modification, and validation:** always instruct the user to run Codex CLI — never use bash directly, never use subagents for implementation.

**Workflow per task:**
1. Claude writes the task file to `.ai-collab/tasks/task-<ID>-<slug>.md`
2. Claude tells the user: "Run: `codex` and paste this prompt:" followed by the task prompt
   — OR — "Run: `codex exec '<one-line task description>'`"
3. Codex reads the task file, executes, writes `## Codex execution log` in the task file
4. User tells Claude when Codex is done
5. Claude reads the execution log, reviews, updates `board.yaml`

**Session tracking:**
- After each Codex run, record the session ID from `~/.codex/session_index.jsonl` (last entry `id` field)
- Store in `runtime/codex-session.yaml` under `last_session_id`
- To resume a previous session: user runs `codex resume <session-id>` or `codex resume --last`
- No canary probe needed — local sessions do not expire

**Full protocol details:** `.ai-collab/templates/codex-worker-protocol.md`
```

### Fix 2: Remove canary probe and MCP references from AGENTS.md

In `AGENTS.md`, replace the entire `## Codex MCP execution context` section with:

```markdown
## Codex CLI execution context

When invoked via CLI (`codex` or `codex exec`):

- **Single task focus:** Execute only the task specified in the prompt or task file. Do not pick up additional tasks from `board.yaml`.
- **Read task file first:** Before doing anything, read the full task file at `.ai-collab/tasks/task-<ID>-<slug>.md`.
- **Session continuity:** If the user runs `codex resume <session-id>`, you are continuing a previous session. Reference prior context from that session.
- **Report back:** For Mode B tasks, write a report to `.ai-collab/reports/task-<ID>-<slug>-<YYYY-MM-DD>.md`. For Mode A tasks, write a complete summary in the execution log.
- **Do not update board.yaml:** Claude will update task statuses after reviewing your execution log.
- **Do not write `runtime/codex-session.yaml`:** Claude maintains this file.
```

### Fix 3: Rewrite codex-worker-protocol.md

Replace the entire content of `.ai-collab/templates/codex-worker-protocol.md` with:

```markdown
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

## No canary probe needed

Local Codex CLI sessions are stored in `~/.codex/sessions/` and do not expire. There is no need for a canary probe. Session continuity is managed by `codex resume <session-id>`.

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
```

### Fix 4: Replace codex-session.yaml with CLI-oriented schema

Replace the contents of `.ai-collab/runtime/codex-session.yaml` with:

```yaml
# .ai-collab/runtime/codex-session.yaml
# Runtime state for Codex CLI session continuity
# Claude maintains this file. Codex does not write to it.
# Session history is stored locally in ~/.codex/session_index.jsonl

project_id: "test_of_multi_agent"

codex_session:
  last_session_id: ""        # last session ID from ~/.codex/session_index.jsonl
  last_task_id: "025"        # last task ID executed
  last_used_at: "2026-03-22"
  total_tasks_executed: 0    # total tasks executed via CLI in this project
  session_mode: "cli"        # cli | mcp (always cli after migration)

session_policy:
  resume_for_dependent_tasks: true   # use codex resume for tasks with depends_on
  new_session_for_independent: true  # use fresh session for independent tasks

notes: |
  This file tracks Codex CLI session state for project continuity.
  Claude checks this before instructing user to invoke Codex:
  - If task has depends_on referencing last_task_id → instruct user to run: codex resume <last_session_id>
  - If task is independent → instruct user to run: codex (interactive) or codex exec (non-interactive)

  To find the last session ID after a Codex run:
    tail -1 ~/.codex/session_index.jsonl
  The 'id' field is the session ID to record here.
```

### Fix 5: Update QUICKSTART.md section 4 user role table

In `QUICKSTART.md`, find the `## 4. Your role at each stage` table and update the "During Codex execution" row and add a new row for session tracking:

Replace:
```
| During Codex execution | Nothing | Execute tasks, write logs and reports |
| Canary fails | Type `OK` to confirm session reset (or say cancel) | Reset session, continue from same task |
```

With:
```
| During Codex execution | Run `codex` or `codex exec` as instructed by Claude | Writes task file with full prompt |
| After Codex finishes | Tell Claude "done" and paste session ID if asked | Reviews execution log, updates board.yaml |
```

Also remove the `## 3. Handle common problems` row:
```
| Session expired | Claude notifies you with details; type OK to confirm reset — your previous task progress is saved in the task file and report |
```
And replace with:
```
| Want to continue previous session | Run `codex resume --last` or `codex resume <session-id>` |
```

## Acceptance criteria
- `CLAUDE.md` contains `### Codex CLI execution model` (not MCP) with the 5-step workflow and session tracking via `session_index.jsonl`
- `CLAUDE.md` does not contain `mcp__codex__codex` or `canary probe` references
- `AGENTS.md` contains `## Codex CLI execution context` (not MCP) with no canary probe mention
- `codex-worker-protocol.md` describes CLI invocation methods (interactive, exec, resume) and has no canary probe section
- `QUICKSTART.md` stage 4 table row for "During Codex execution" says user runs `codex` command, not "Nothing"
- `QUICKSTART.md` does not contain "Canary fails" row

## must_haves
- 协议中所有 `mcp__codex__codex` 调用引用都被 CLI 调用说明取代
- canary probe 相关内容从所有文件中完全移除
- `codex-session.yaml` 已由 Claude 直接更新为 CLI 模式（Claude 专属文件，不经过 Codex）

## Codex execution log

- 2026-03-22: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work.
- 2026-03-22: Confirmed task `025` is the single eligible Codex task in `board.yaml` (`status: todo`, `suggested_next_for_codex: 025`).
- 2026-03-22: Blocked on instruction conflict. `AGENTS.md` says `Codex must not write .ai-collab/runtime/codex-session.yaml`, but this task requires replacing that file in `## Target paths` and `### Fix 4`.
- 2026-03-22: Stopped without editing implementation files. Partial documentation-only edits would leave the protocol inconsistent with the required runtime schema migration.
- 2026-03-22: Validation not run. `AGENTS.md` declares no global validation command, and this task's acceptance section is truncated after the first two bullets, so no executable task-specific command was available.
- 2026-03-22: Suggested next step for Claude: either update `.ai-collab/runtime/codex-session.yaml` directly and reissue the remaining allowed edits to Codex, or split the runtime-file change into Claude-owned work.
- 2026-03-22: Resumed after Claude updated `.ai-collab/runtime/codex-session.yaml` directly. Implemented Fix 1 (`CLAUDE.md`), Fix 2 (`AGENTS.md`), Fix 3 (`.ai-collab/templates/codex-worker-protocol.md`), and Fix 5 (`QUICKSTART.md`) only.
- 2026-03-22: Updated the four allowed documentation files from MCP-oriented guidance to Codex CLI guidance (`codex`, `codex exec`, `codex resume`, and `~/.codex/session_index.jsonl` session tracking).
- 2026-03-22: Adjusted the literal replacement text to satisfy the task acceptance criteria and must-haves by removing the remaining `canary probe` phrase from the edited files while preserving the intended "local sessions do not expire" meaning.
- 2026-03-22: Validation: `rg -n "mcp__codex__codex|canary|Codex MCP execution model|Codex MCP execution context|Codex MCP|codex-reply\\(|threadId|thread_id" CLAUDE.md AGENTS.md .ai-collab/templates/codex-worker-protocol.md QUICKSTART.md` returned no matches.
- 2026-03-22: Validation: `python tools/check_consistency.py` failed on pre-existing and out-of-scope MCP-era assumptions (`thread_id` / `spec_version_at_start` checks against the new CLI session schema, plus longstanding task status mismatches in older task files).
- 2026-03-22: Validation: `rg --hidden -n "mcp__codex__codex|canary|Codex MCP|codex-reply\\(|threadId|thread_id" .` still finds legacy references outside this task's target paths, including `.ai-collab/README.md`, `.ai-collab/spec/SPEC.md`, `.claude/skills/claude-orchestrator/SKILL.md`, and historical artifacts.
- 2026-03-22: Resumed via `codex resume --last` and used the existing task log plus report as prior-session context.
- 2026-03-22: Re-verified the scoped target files already match the CLI migration requirements, so no additional edits to `CLAUDE.md`, `AGENTS.md`, `.ai-collab/templates/codex-worker-protocol.md`, or `QUICKSTART.md` were needed in this resumed session.
- 2026-03-22: Re-ran validation from this resumed session. The scoped grep still returned no matches in the four edited files; `python tools/check_consistency.py` still fails only on pre-existing and out-of-scope MCP-era assumptions (`thread_id`, `spec_version_at_start`, `last_task_id` drift in `codex-handoff.md`, and old task status mismatches); and repo-wide hidden grep still finds legacy references outside this task's target paths.
