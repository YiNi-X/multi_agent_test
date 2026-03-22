# Task 009 — session-canary-probe

## Goal
Harden session expiry detection by adding a canary probe step to the Codex invocation protocol. Currently Claude estimates session validity using a time-based heuristic (`last_used_at` + `max_idle_minutes`), which is unreliable because Claude cannot know the real current time. A canary probe actively verifies session continuity before executing any task.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`B` — report required (modifies 2 protocol files + AGENTS.md; criteria require inspecting multiple files)

## Target paths
- `.ai-collab/templates/codex-worker-protocol.md`
- `.ai-collab/README.md`
- `AGENTS.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Add canary probe procedure to codex-worker-protocol.md

In `.ai-collab/templates/codex-worker-protocol.md`, in the "Method 2: Continue existing session" section, add a canary probe step **before** the actual task prompt is sent:

```markdown
### Canary probe (required before every codex-reply() call)

Before sending the actual task prompt, Claude must prepend the following canary instruction to the prompt:

> Before doing anything else, reply with exactly one line:
> `CANARY_OK:<last_task_id>`
> where `<last_task_id>` is the ID of the last task you executed in this session.
> Expected value: `CANARY_OK:<value of codex-session.yaml last_task_id>`

**If Codex responds with the expected `CANARY_OK:<last_task_id>` line:** session is alive. Proceed with the task.

**If Codex responds with anything else, or the call errors:** session is invalid. Claude must:
1. Stop the current invocation
2. Notify the user: "Session `<thread_id>` failed canary probe (expected `CANARY_OK:<last_task_id>`, got `<actual_response>`). Session will be reset. Starting new session with `codex()`."
3. Wait for user confirmation before proceeding
4. On confirmation: mark the old session `status: expired` in `codex-session.yaml`, then call `codex()` to start a new session
```

### Fix 2: Update session lifecycle diagram in codex-worker-protocol.md

Update the session lifecycle diagram to include the canary step:

```
[New task] → Check codex-session.yaml
             ↓
             Is session active and not expired?
             ↓                    ↓
            YES                  NO
             ↓                    ↓
     Send canary probe       codex(prompt)
             ↓
     CANARY_OK received?
             ↓            ↓
            YES           NO
             ↓             ↓
   codex-reply(task)   Notify user → wait for confirmation
             ↓             ↓ (confirmed)
             └──────┬───── codex(prompt) [new session]
                    ↓
           Update codex-session.yaml
```

### Fix 3: Add canary protocol note to AGENTS.md

In `AGENTS.md`, under the "Codex MCP execution context" section, add:

```markdown
**Canary probe:** When invoked via `codex-reply()`, the prompt may begin with a canary instruction asking you to confirm the last task ID before proceeding. Respond to the canary line first, exactly as instructed, before reading or acting on the rest of the prompt.
```

### Fix 4: Update README.md session expiry note

In `.ai-collab/README.md`, find any mention of session expiry or the 30-minute idle policy and add a note:

```markdown
**Note:** Time-based expiry is a fallback heuristic only. The primary session validity check is the canary probe sent at the start of every `codex-reply()` call. If the canary fails, Claude notifies the user and waits for confirmation before starting a new session.
```

## Acceptance criteria
- `codex-worker-protocol.md` contains a "Canary probe" subsection under Method 2 describing the probe format (`CANARY_OK:<last_task_id>`), the success path, and the failure path (notify user → wait for confirmation → new session on confirmation)
- `codex-worker-protocol.md` session lifecycle diagram includes the canary probe step and the notify-user branch
- `AGENTS.md` contains a note telling Codex to respond to the canary line before acting on the rest of the prompt
- `README.md` contains a note that time-based expiry is a fallback and the canary probe is the primary check

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Updated `.ai-collab/templates/codex-worker-protocol.md` to require a canary probe before every `codex-reply()` call and to define the success path and failure path, including user notification and confirmation before resetting the session.
- 2026-03-21: Updated the session lifecycle diagram in `.ai-collab/templates/codex-worker-protocol.md` to include the canary step, the notify-user branch, and the confirmed new-session fallback.
- 2026-03-21: Updated `.ai-collab/README.md` and `AGENTS.md` so the canary probe is documented as the primary session-validity check and Codex is instructed to answer the canary line before acting on the rest of the prompt.
- 2026-03-21: Verified the final canary wording across all three target files and wrote the task report.
