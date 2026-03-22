# .ai-collab - Multi-Agent Collaboration Protocol

This directory is the shared workspace for Claude (orchestrator) and Codex
(implementor). Planning, task assignment, progress tracking, and review all flow
through this protocol.

---

## Directory layout

Some directories are created lazily and may not exist until first use.

```text
.ai-collab/
  README.md          -> this file
  board.yaml         -> single source of truth for plan + task status
  plans/             -> Claude writes plan documents here          [lazy-created]
  tasks/             -> one file per task; Codex reads tasks and writes only the
                        Codex-owned execution section              [lazy-created]
  reviews/           -> Claude writes review conclusions here      [lazy-created]
  reports/           -> Codex writes execution reports here        [lazy-created]
  spec/              -> Living Specification: current truth, decisions, changelog
  runtime/           -> active session state (Claude-maintained)   [lazy-created]
  templates/         -> canonical templates for each document type
```

`[lazy-created]` directories are created by Claude or Codex on first use. You do not need to create them manually.

---

## Status values

Every task moves through exactly this lifecycle. Use these values verbatim in
`board.yaml` and task files. Do not invent synonyms.

| Status | Meaning |
|---|---|
| `todo` | Task is defined and waiting to be picked up |
| `in_progress` | Codex has started execution and recorded that in the task log |
| `review` | Codex has finished and Claude has been notified. `board.yaml` must be set to `review` **before** Claude begins writing the review document. Status changes to `done` only after Claude writes the review document and explicitly accepts the output. |
| `done` | Claude has reviewed and accepted the output |
| `blocked` | Work cannot continue and the blocker is documented for Claude |

**Important:** `review` is a durable state, not a transient one. External observers reading `board.yaml` during an active review will see `review`. A task must not jump from `in_progress` directly to `done`.

**Note:** Tasks requiring rework return to `todo` status. The review document explains what needs to be fixed.

---

## Role responsibilities

### Claude (orchestrator)

- Discusses requirements with the user and writes plan documents
- Decomposes plans into atomic tasks with clear acceptance criteria
- Writes to: `plans/`, `tasks/` (initial definition), `reviews/`, `board.yaml`, `spec/`
- Updates authoritative task statuses in `board.yaml` after reading Codex reports or Mode A MCP response evidence
- Maintains Living Specification in `spec/` and evaluates impact of spec changes
- Does **not** modify application source code unless the user explicitly requests it

### Codex (implementor)

- Reads `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and one task file before starting work
- Works on exactly one task at a time
- Writes only to the Codex-owned execution section in the task file
- Writes a report to `reports/` when the task uses invocation mode `B`
- Does **not** change `board.yaml`
- Does **not** rewrite Claude-owned task definition content
- Does **not** modify `spec/` files

---

## Codex invocation modes

Every task must declare its invocation mode. This determines whether Codex writes
a report file and how Claude conducts the review.

### Mode A - MCP direct

Applicable when **all** of the following are true:
- The task modifies <= 2 files
- All `acceptance_criteria` can be verified directly from the MCP response text
  (no shell commands needed)
- The task does not involve code logic changes (documentation, configuration, and
  protocol files only)

Behavior:
- Codex does **not** write a file to `reports/`
- Codex still appends `## Codex execution log` to the task file
- Claude's review document must include an `Invocation mode` row and a `Mode A evidence` row in its metadata table

### Mode B - Report required

Triggered when **any** of the following are true:
- The task modifies > 2 files
- Any `acceptance_criteria` requires running a shell command to verify
- The task involves code logic changes
- The task definition explicitly sets `invocation_mode: B`

Behavior:
- Codex **must** write a report file to `reports/` named `task-<id>-<slug>-<YYYY-MM-DD>.md`
- Codex still appends `## Codex execution log` to the task file
- Claude's review document cites the report file as its primary evidence source

### Mode declaration

The mode must be declared in two places:
1. The task file, as an `## Invocation mode` field (value: `A` or `B` with rationale)
2. The Claude prompt when invoking Codex, explicitly stating whether a report file is expected

---

## Living Specification

The `spec/` directory contains the evolving specification for the system:

- **`spec/SPEC.md`** — Current truth about system behavior, capabilities, and constraints. This is the single source of truth for what the system should do. Only contains current state; historical information is moved to CHANGELOG.md.

- **`spec/DECISIONS.md`** — Architectural decision log. Records key decisions, their context, rationale, and consequences. Answers "why did we choose this approach?"

- **`spec/CHANGELOG.md`** — Specification change history. Tracks what changed, when, why, and what impact it has on existing plans and tasks.

### Spec change workflow

When `SPEC.md` changes:

1. Claude records the change in `CHANGELOG.md` with impact assessment
2. Claude evaluates whether existing tasks are invalidated
3. If tasks are affected, Claude updates `board.yaml` with:
   - `spec_dirty: true`
   - `invalidated_tasks: [list of affected task IDs]`
   - `replan_required: true/false`
4. Claude reviews and replans affected tasks before continuing

---

## Codex MCP execution model

### How Codex is invoked

Claude does not manually hand off tasks to Codex. Instead, Claude invokes Codex programmatically via MCP tools:

- **`mcp__codex__codex(prompt)`** — Start a new Codex session
- **`mcp__codex__codex-reply(threadId, prompt)`** — Continue an existing session

### Session continuity

To avoid losing context between tasks, Claude maintains session state in `runtime/codex-session.yaml`:

- **First task:** Claude calls `codex()` and stores the returned `threadId`
- **Subsequent tasks:** Claude calls `codex-reply(threadId, ...)` to continue the conversation
- **Session expires when:**
  - Idle for more than `max_idle_minutes` (default: 30)
  - Spec changes and `force_new_on_spec_change == true`
  - User explicitly requests a fresh start

**Note:** Time-based expiry is a fallback heuristic only. The primary session
validity check is the canary probe sent at the start of every
`codex-reply()` call. If the canary fails, Claude notifies the user and waits
for confirmation before starting a new session.

### Why Claude subagents cannot replace Codex

Claude may use subagents (Agent tool) for:
- Spec review and impact analysis
- Codebase discovery and exploration
- Research and documentation tasks

But Claude must NOT create subagents to:
- Execute implementation tasks
- Modify application source code
- Run validation commands
- Simulate Codex workers

**Reason:** Codex has specialized context, tools, and approval policies for code execution. Claude subagents lack this context and would duplicate work incorrectly.

### Codex invocation checklist

Before invoking Codex, Claude must:

1. Read `runtime/codex-session.yaml` to check for active session
2. Decide: `codex()` (new) or `codex-reply()` (continue)
3. Prepare prompt with references to:
   - `AGENTS.md`
   - `.ai-collab/README.md`
   - `.ai-collab/board.yaml`
   - `.ai-collab/spec/SPEC.md` (if exists)
   - The specific task file
4. After completion, update `codex-session.yaml` with:
   - `session_id`
   - `last_used_at`
   - `last_task_id`
   - `status`

---

## Update principles

1. `board.yaml` is the authoritative status record and is maintained by Claude.
2. Never delete task or plan files. Superseded plans are renamed with `-archived-YYYY-MM-DD` suffix. Completed tasks remain in place with `done` status in board.yaml.
3. Timestamps use ISO 8601 date format: `YYYY-MM-DD`.
4. Task IDs are sequential integers, zero-padded to three digits: `001`, `002`, `003`.
5. All filenames use kebab-case.
6. A task is only `done` after Claude has written a review and explicitly marked it so.
7. Tasks requiring rework return to `todo` status with review documenting the reasons.
8. If a task file contains a `Codex execution log` section, only Codex writes that section. Claude-owned task definition sections stay unchanged unless Claude replans.
9. `SPEC.md` contains only current truth. Move outdated content to `CHANGELOG.md`.
10. Task files use markdown with structured sections for human readability and machine parseability.
11. `runtime/codex-session.yaml` tracks active Codex MCP session for continuity.
