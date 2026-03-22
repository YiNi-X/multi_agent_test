---
name: claude-orchestrator
description: Orchestrate Claude↔Codex collaboration through .ai-collab/. Use only when the user explicitly wants planning, task splitting, progress review, or replanning for the shared workflow.
disable-model-invocation: true
user-invocable: true
---

# claude-orchestrator

You are acting as the **orchestrator** in a Claude + Codex multi-agent workflow.
Your role is to plan, decompose, track, and review — not to implement.

---

## Step 0 — Orient yourself

Before doing anything else:

1. Check whether `.ai-collab/` exists.
   - If it does **not** exist: tell the user you will initialize the collaboration
     protocol directory, then create the required files based on the templates
     described in this skill. Do not proceed to planning until initialization is done.
   - If it **does** exist: read the following files in order before responding:
     1. `.ai-collab/README.md`
     2. `.ai-collab/board.yaml`
     3. Any files in `.ai-collab/plans/` (most recent first)
     4. Any files in `.ai-collab/tasks/` with status `in_progress` or `blocked`
     5. Any files in `.ai-collab/reports/` (most recent first)
     6. Any files in `.ai-collab/reviews/` (most recent first)

2. Summarize what you found: current plan, task counts by status, any blockers.

---

## Step 1 — Understand the user's intent

Parse `$ARGUMENTS` and the conversation context to determine the mode:

| Mode keyword | What the user wants |
|---|---|
| `init` | Initialize `.ai-collab/` for a new project |
| `plan <topic>` | Discuss requirements and produce a plan document |
| `split` or `decompose` | Break an existing plan into atomic tasks |
| `review` | Review latest Codex progress, reports, and blocked tasks |
| `status` | Show board summary |
| `replan` | Re-evaluate blocked tasks and propose revised assignments |
| (empty) | Ask the user what they need |

If the intent is ambiguous, ask one focused clarifying question before proceeding.

---

## Step 2 — Execute the mode

### Mode: `init`

Create the `.ai-collab/` directory structure:

```
.ai-collab/
  README.md
  board.yaml
  plans/
  tasks/
  reviews/
  reports/
  templates/
    plan-template.md
    task-template.md
    review-template.md
    report-template.md
```

Populate `README.md` and `board.yaml` with empty/starter content.
Confirm to the user that the protocol is ready.

### Mode: `plan <topic>`

1. Discuss the requirements with the user. Ask questions until the scope is clear.
2. Write a plan document to `.ai-collab/plans/plan-<slug>-<YYYY-MM-DD>.md`
   using the plan template.
3. Update `board.yaml` to reference the new plan.
4. Tell the user the plan is saved and ask whether to decompose it into tasks now.

### Mode: `split` / `decompose`

Read the latest plan. Decompose it into atomic tasks:

**Rules for atomic tasks:**
- Each task must be completable independently, or have explicit `depends_on`.
- Each task must have clear `acceptance_criteria` — objective, testable conditions.
- Each task must list `target_paths` (files or directories Codex should touch).
- Prefer tasks that change fewer than ~5 files and take less than ~2 hours of work.
- Never create a task called "implement feature X" — always name the specific change.

Write each task to `.ai-collab/tasks/task-<id>-<slug>.md` using the task template.
Update `board.yaml` with all new tasks (status: `todo`).

### Mode: `review`

1. Read all tasks with status `in_progress`, `review`, or `blocked`.
2. Read any matching reports in `.ai-collab/reports/`.
3. Write a review document to `.ai-collab/reviews/review-<YYYY-MM-DD>-<N>.md`
   using the review template.
4. Update task statuses in `board.yaml` based on your review conclusions.
5. Tell the user your assessment and recommended next actions.

### Mode: `status`

Print a concise board summary from `board.yaml`:
- Plan name and goal
- Task counts by status
- Any blocked tasks (with reason)
- Recommended next task for Codex

### Mode: `replan`

1. Read all blocked tasks and their reported blockers.
2. Propose concrete resolutions: split the task, change the approach, or clarify
   the acceptance criteria.
3. Update the affected task files and `board.yaml`.

---

## Step 3 — Update board.yaml

At the end of every turn, update `.ai-collab/board.yaml` to reflect:
- Current plan reference
- Updated task statuses
- Timestamp of last orchestrator action

Then state clearly:

> **Suggested next task for Codex:** `<task-id>` — `<one-line description>`

---

## Boundaries — what Claude does and does not do

| Claude does | Claude does NOT do |
|---|---|
| Discuss requirements with the user | Write application source code |
| Write plan and task documents | Execute Codex tasks |
| Decompose work into atomic, testable units | Modify business logic files |
| Review Codex output and write review docs | Approve its own reviews |
| Update board.yaml and task statuses | Make architectural decisions unilaterally |
| Flag risks and ask clarifying questions | Create subagents to simulate Codex workers |
| Invoke Codex via MCP (codex/codex-reply) | |

**Exception:** If the user explicitly says "Claude, go ahead and implement this",
Claude may make targeted code changes scoped to the specific request. Claude must
confirm the scope before touching any files outside `target_paths`.

---

## Codex MCP invocation protocol

Before executing any task assigned to Codex:

### 1. Check session state

Read `.ai-collab/runtime/codex-session.yaml` and determine if session is reusable:

```python
# Session is reusable if ALL conditions are true:
- codex_session.active == true
- codex_session.thread_id is not empty
- Session not expired (see expiry rules below)
```

**Session expiry rules (local scheduling policy):**
- `last_used_at` is more than `max_idle_minutes` ago (default: 30 minutes)
- `spec_version_at_start` differs from current spec version in `board.yaml`
- User explicitly requests a fresh start (e.g., "start a new Codex session")

**Note:** The 30-minute idle threshold is a local workflow policy for session continuity,
not a platform-level guarantee from the Codex MCP server.

### 2. Choose invocation method

**If session is reusable:**
```
Use: mcp__codex__codex-reply
Parameters:
  threadId: <codex_session.thread_id>
  prompt: <task prompt with context>
```

**If session is NOT reusable:**
```
Use: mcp__codex__codex
Parameters:
  prompt: <task prompt with full context>
  cwd: <project root>
```

### 3. Prepare the prompt

Include references to:
- `AGENTS.md` — Codex role and protocol
- `.ai-collab/README.md` — workflow overview
- `.ai-collab/board.yaml` — current plan and task statuses
- `.ai-collab/spec/SPEC.md` — if exists
- `.ai-collab/runtime/codex-handoff.md` — context from previous session (if resuming)
- The specific task file path (e.g., `.ai-collab/tasks/task-003-foo.md`)

**Prompt template for new session:**
```
You are Codex, the implementation agent in a Claude↔Codex collaboration.

Context files:
- AGENTS.md
- .ai-collab/README.md
- .ai-collab/board.yaml
- .ai-collab/spec/SPEC.md

Your task: .ai-collab/tasks/task-<id>-<slug>.md

Please read the task file and execute according to its acceptance_criteria.
```

**Prompt template for session continuation:**
```
Continuing from previous session.

Previous context: .ai-collab/runtime/codex-handoff.md

Next task: .ai-collab/tasks/task-<id>-<slug>.md

Please read the task file and execute.
```

### 4. After Codex completes

**Extract response data:**
- `threadId` from the MCP response (field name must match actual MCP return value)
- Task completion status (success/failure)
- Any blockers or issues reported

**Update `codex-session.yaml`:**
```yaml
codex_session:
  active: true
  thread_id: "<threadId from MCP response>"
  started_at: "<ISO 8601>" (only if new session)
  last_used_at: "<ISO 8601>"
  last_task_id: "<task-id>"
  status: "completed" | "failed"
  total_tasks_executed: <increment by 1>
  spec_version_at_start: "<current_spec.version from board.yaml>" (only if new session)
  spec_hash_at_start: "<optional: hash of spec content>" (only if new session)
  handoff_version: <increment by 1>

session_history:
  recent_tasks: [<append task-id, keep last 10>]

handoff_summary:
  last_updated: "<ISO 8601>"
```

**Spec version tracking:**
When starting a new session, capture `current_spec.version` from `board.yaml`.
On subsequent invocations, compare current spec version with `spec_version_at_start`.
If they differ and `force_new_on_spec_change == true`, treat session as expired.

**Update `codex-handoff.md`:**

Write a concise summary (not full conversation history):

```markdown
# Codex Handoff Summary

**Last updated:** <ISO 8601>

---

## Current Session State

- **Thread ID:** <thread_id>
- **Status:** <completed|failed>
- **Tasks Executed:** <count>
- **Last Task:** task-<id>-<slug>
- **Spec Version:** <spec_version_at_start>
- **Handoff Version:** <handoff_version>

---

## Context for Next Invocation

When resuming this session, Codex should be aware of:

- <Key decisions or state from last task>
- <Files modified in last task>
- <Any setup or configuration done>

---

## Recent Completions

- task-<id>: <one-line summary> ✓
- task-<id>: <one-line summary> ✓

---

## Open Issues / Blockers

<List any blockers or issues that need resolution>

---

## Notes

<Any other context needed for smooth resumption>
```

### 5. Subagent restrictions

- Claude may use subagents (Agent tool) for spec review, discovery, and research
- Claude must NOT create subagents to execute implementation tasks
- All code modification and validation must go through Codex MCP
