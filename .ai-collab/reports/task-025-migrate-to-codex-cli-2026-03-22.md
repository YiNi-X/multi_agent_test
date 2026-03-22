# Report: task-025-migrate-to-codex-cli

## What was done

Claude resolved the earlier blocker by updating `.ai-collab/runtime/codex-session.yaml` directly. After that, the remaining four scoped documentation fixes were implemented:

- `CLAUDE.md` now defines a `### Codex CLI execution model` section and instructs Claude to tell the user to run `codex` or `codex exec`.
- `AGENTS.md` now defines `## Codex CLI execution context` and removes MCP/canary-specific worker instructions.
- `.ai-collab/templates/codex-worker-protocol.md` now describes CLI invocation methods (`codex`, `codex exec`, `codex resume`) and CLI session tracking.
- `QUICKSTART.md` now tells the user to run Codex CLI, includes the new "After Codex finishes" row, and removes the old canary-failure workflow.

To satisfy the acceptance criteria and must-haves, the remaining literal `canary probe` phrase from the task's sample text was also removed from the edited files, while keeping the same semantics about local sessions not expiring.

This report was then re-verified in a resumed Codex CLI session on 2026-03-22 via `codex resume --last`. No further scoped file edits were necessary because the four target documentation files already matched the requested CLI-oriented wording.

## Files changed

- `CLAUDE.md`
- `AGENTS.md`
- `.ai-collab/templates/codex-worker-protocol.md`
- `QUICKSTART.md`
- `.ai-collab/tasks/task-025-migrate-to-codex-cli.md`
- `.ai-collab/reports/task-025-migrate-to-codex-cli-2026-03-22.md`

## Validation results

- Passed: `rg -n "mcp__codex__codex|canary|Codex MCP execution model|Codex MCP execution context|Codex MCP|codex-reply\(|threadId|thread_id" CLAUDE.md AGENTS.md .ai-collab/templates/codex-worker-protocol.md QUICKSTART.md`
  - Result: no matches in the four edited files.
- Failed: `python tools/check_consistency.py`
  - `thread_id`: script still expects the old MCP session schema and front-matter alignment.
  - `last_task_id`: `.ai-collab/runtime/codex-session.yaml=025`, `.ai-collab/runtime/codex-handoff.md=022`.
  - `spec version`: script expects `codex_session.spec_version_at_start`, which no longer exists in the CLI session schema.
  - `task status`: older task files still show `## Status` as `todo` while `board.yaml` marks them `done`.
- Informational: `rg --hidden -n "mcp__codex__codex|canary|Codex MCP|codex-reply\(|threadId|thread_id" .`
  - Remaining legacy references exist outside this task's `target_paths`, including `.ai-collab/README.md`, `.ai-collab/spec/SPEC.md`, `.claude/skills/claude-orchestrator/SKILL.md`, historical task/plan/review artifacts, and `tools/check_consistency.py`.
- Resume check on 2026-03-22:
  - Re-ran all three checks from a resumed session and got the same results, confirming the task remains complete within its scoped target paths.

## Blockers or issues

- No blocker remains for the four scoped fixes.
- Full-repo migration is not complete. Several non-target files and one validation script still assume the old MCP/thread-based model.

## Suggested next step

- Claude should review this task against the scoped acceptance criteria for the four edited files.
- If the project wants repository-wide CLI migration, create follow-up tasks for `.ai-collab/README.md`, `.ai-collab/spec/SPEC.md`, `.claude/skills/claude-orchestrator/SKILL.md`, `.ai-collab/runtime/codex-handoff.md`, and `tools/check_consistency.py`.
