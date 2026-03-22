# Task 030 — auto-codex-exec

## Goal
Update CLAUDE.md to use `codex exec --full-auto` via Bash tool to execute tasks automatically, replacing the current workflow where Claude tells the user to manually run codex commands.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — modifies 1 file, criteria verifiable from execution log

## Target paths
- `CLAUDE.md`

## Pre-conditions
- None

## Instructions

In `CLAUDE.md`, find the `### Codex CLI execution model` section. Replace the entire section with:

```markdown
### Codex CLI execution model

Codex executes tasks via `codex exec --full-auto` invoked directly by Claude through the Bash tool. No user interaction is required for task execution.

**For implementation, code modification, and validation:** use `codex exec --full-auto` via Bash — never use subagents for implementation.

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
- Local sessions do not expire — `~/.codex/sessions/` persists indefinitely

**Full protocol details:** `.ai-collab/templates/codex-worker-protocol.md`
```

Also update `codex-worker-protocol.md` to reflect auto-exec model:

In `.ai-collab/templates/codex-worker-protocol.md`, replace the `## Invocation methods` section with:

```markdown
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
```

## Target paths (updated)
- `CLAUDE.md`
- `.ai-collab/templates/codex-worker-protocol.md`

## Acceptance criteria
- `CLAUDE.md` `### Codex CLI execution model` section contains `codex exec --full-auto` as the primary invocation method
- `CLAUDE.md` does not say "tell the user to run" for normal task execution
- `codex-worker-protocol.md` `## Invocation methods` section shows `codex exec --full-auto` as Method 1
- `codex-worker-protocol.md` includes a manual fallback method

## must_haves
- Claude 现在可以直接通过 Bash tool 触发 Codex，无需用户手动粘贴命令
- 保留 manual fallback（Method 3）以防 codex exec 不可用
- session resume 也是自动的（`codex exec --full-auto resume --last`）

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log

- 2026-03-22: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work.
- 2026-03-22: Confirmed task `030` is explicitly requested, `status: todo`, `assigned_to: codex`, and has no blocking dependencies in `board.yaml`.
- 2026-03-22: Updated [`CLAUDE.md`](../../CLAUDE.md) `### Codex CLI execution model` to make `codex exec --full-auto` via Bash the primary execution path, remove the normal user-driven "run codex" workflow, add the direct execution command, and document automatic session resume with `codex exec --full-auto resume --last`.
- 2026-03-22: Updated [`.ai-collab/templates/codex-worker-protocol.md`](../templates/codex-worker-protocol.md) `## Invocation methods` so Method 1 is automatic `codex exec --full-auto`, Method 2 is automatic resume with `resume --last`, and Method 3 is a manual fallback. Also aligned nearby session-tracking and session-lifecycle wording with the automatic execution model to avoid contradictions.
- 2026-03-22: Validation: `rg -n "codex exec --full-auto|### Method 1: New session \(automatic\)|### Method 3: Manual fallback" CLAUDE.md .ai-collab/templates/codex-worker-protocol.md` confirmed the required automatic invocation and fallback sections; `if (Select-String -Path CLAUDE.md -Pattern 'tell the user to run','Claude tells the user') { Write-Output 'unexpected manual-run phrasing in CLAUDE.md'; exit 1 } else { Write-Output 'CLAUDE.md contains no manual-run phrasing for normal execution' }` confirmed `CLAUDE.md` no longer instructs normal manual task execution.
- 2026-03-22: Validation: `python tools/check_consistency.py` passed (`0 FAIL, 0 WARN, 5 PASS, 1 SKIP`).
- 2026-03-22: No Mode B report file was written because this task is declared as invocation mode `A`.

```text
Task: task-030-auto-codex-exec
Result: review
Files changed: CLAUDE.md, .ai-collab/templates/codex-worker-protocol.md, .ai-collab/tasks/task-030-auto-codex-exec.md
Validation: rg -n "codex exec --full-auto|### Method 1: New session \(automatic\)|### Method 3: Manual fallback" CLAUDE.md .ai-collab/templates/codex-worker-protocol.md; if (Select-String -Path CLAUDE.md -Pattern 'tell the user to run','Claude tells the user') { Write-Output 'unexpected manual-run phrasing in CLAUDE.md'; exit 1 } else { Write-Output 'CLAUDE.md contains no manual-run phrasing for normal execution' }; python tools/check_consistency.py
Notes for Claude: Task metadata under `## Invocation mode` still says "modifies 1 file", but the later Instructions and updated Target paths required changes in 2 implementation files; implementation followed the later explicit scope.
```
