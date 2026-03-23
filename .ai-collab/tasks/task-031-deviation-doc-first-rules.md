# Task 031 — deviation-doc-first-rules

## Goal
Add explicit "deviation → fix document first" rules to both `CLAUDE.md` and `AGENTS.md` so that the document-driven workflow is enforced at the protocol level, not just in QUICKSTART.md.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 2 files, criteria verifiable from file readback, documentation only

## Target paths
- `CLAUDE.md`
- `AGENTS.md`

## Pre-conditions
- None

## Instructions

### Fix 1: CLAUDE.md — add deviation rule to `### Spec change rules`

In `CLAUDE.md`, find the section `### Spec change rules`. After the existing bullet points in that section, add:

```markdown
- **When review or testing finds a mismatch between implementation and docs:** update `SPEC.md` first, then write a new task for Codex to fix the code. Never propose a code fix that skips the document update step.
```

### Fix 2: AGENTS.md — add deviation rule to blocker/stop behavior

In `AGENTS.md`, find the section that describes what Codex should do when it encounters a blocker or finds that implementation does not match the task requirements. Add or extend the guidance with:

```markdown
- If you discover that the implementation does not match the task requirements or the spec, record the deviation in the execution log, stop, and explicitly write: "Claude must update SPEC.md before this task is re-issued." Do not attempt to self-correct by expanding scope.
```

### Fix 3: CLAUDE.md — clarify runtime path (low priority, same task)

In `CLAUDE.md`, find the line referencing `runtime/codex-session.yaml`. Add a parenthetical clarification:

Change:
```
codex_session_file: "runtime/codex-session.yaml"
```
to reference in prose (wherever it appears in CLAUDE.md body text) as:
```
runtime/codex-session.yaml  (path is relative to .ai-collab/)
```

If no prose reference exists in CLAUDE.md body, skip Fix 3.

## Acceptance criteria
- `CLAUDE.md` `### Spec change rules` section contains a bullet about "fix document first before proposing code changes"
- `AGENTS.md` contains guidance that when implementation mismatches spec, Codex must stop and write "Claude must update SPEC.md before this task is re-issued"
- `python tools/check_consistency.py` returns 0 FAIL

## must_haves
- CLAUDE.md 的规则约束的是 Claude 自己的行为（不是给用户看的说明）
- AGENTS.md 的规则约束的是 Codex 的行为（明确指向「先改文档」而不只是「停止」）

## Depends on
- (none)

## Updated
2026-03-23

## Codex execution log

- 2026-03-23: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work.
- 2026-03-23: Confirmed task `031` is explicitly requested, `status: todo`, `assigned_to: codex`, and has no dependencies in `board.yaml`.
- 2026-03-23: Updated [`CLAUDE.md`](../../CLAUDE.md) to add a document-first deviation rule under `### Spec change rules` and to clarify that `runtime/codex-session.yaml` is a path relative to `.ai-collab/` in the session-tracking prose.
- 2026-03-23: Updated [`AGENTS.md`](../../AGENTS.md) to require Codex to stop on implementation/spec mismatches, record the deviation in the execution log, and explicitly write: "Claude must update SPEC.md before this task is re-issued."
- 2026-03-23: Validation: `rg -n "When review or testing finds a mismatch between implementation and docs|runtime/codex-session\\.yaml|Claude must update SPEC\\.md before this task is re-issued" CLAUDE.md AGENTS.md` confirmed the required text is present.
- 2026-03-23: Validation: `python tools/check_consistency.py` passed (`0 FAIL, 0 WARN, 5 PASS, 1 SKIP`).
- 2026-03-23: No Mode B report file was written because this task is declared as invocation mode `A`.

```text
Task: task-031-deviation-doc-first-rules
Result: review
Files changed: CLAUDE.md, AGENTS.md, .ai-collab/tasks/task-031-deviation-doc-first-rules.md
Validation: rg -n "When review or testing finds a mismatch between implementation and docs|runtime/codex-session\.yaml|Claude must update SPEC\.md before this task is re-issued" CLAUDE.md AGENTS.md; python tools/check_consistency.py
Notes for Claude: none
```
