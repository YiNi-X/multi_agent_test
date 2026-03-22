# Task 009 Report

## Task
`009` - `session-canary-probe`

## What was done
- Added a required canary probe procedure to `.ai-collab/templates/codex-worker-protocol.md` under Method 2 so Claude verifies session continuity before every `codex-reply()` task invocation.
- Updated the session lifecycle diagram in `.ai-collab/templates/codex-worker-protocol.md` to include the canary probe branch, the notify-user path, and the confirmed fallback to a new `codex()` session.
- Added a canary-probe note to `AGENTS.md` telling Codex to respond to the canary line first before acting on the rest of the prompt.
- Added a session-expiry note to `.ai-collab/README.md` stating that time-based expiry is only a fallback heuristic and that the canary probe is the primary validity check.
- Appended a brief execution log to the task file.

## Files changed
- `.ai-collab/templates/codex-worker-protocol.md`
- `.ai-collab/README.md`
- `AGENTS.md`
- `.ai-collab/tasks/task-009-session-canary-probe.md`
- `.ai-collab/reports/task-009-session-canary-probe-2026-03-21.md`

## Validation results
- Acceptance criterion 1: Met. `.ai-collab/templates/codex-worker-protocol.md` now contains a `Canary probe` subsection under Method 2 defining the `CANARY_OK:<last_task_id>` format, the success path, and the failure path with notify-user, wait-for-confirmation, and new-session steps.
- Acceptance criterion 2: Met. `.ai-collab/templates/codex-worker-protocol.md` session lifecycle diagram now includes the canary probe step and the notify-user branch.
- Acceptance criterion 3: Met. `AGENTS.md` now tells Codex to respond to the canary line before acting on the rest of the prompt.
- Acceptance criterion 4: Met. `.ai-collab/README.md` now states that time-based expiry is a fallback heuristic and that the canary probe is the primary check.

## Blockers or issues
- None.
