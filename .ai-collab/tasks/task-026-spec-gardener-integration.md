# Task 026 — spec-gardener-integration

## Goal
Add spec-gardener as a systematic step in CLAUDE.md so it is called proactively before significant spec changes and before task decomposition, not just ad hoc.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 1 file, criteria verifiable from execution log

## Target paths
- `CLAUDE.md`

## Pre-conditions
- None

## Instructions

In `CLAUDE.md`, find the `### Spec change rules` section. Before it (after `### Task decomposition rules`), add a new section:

```markdown
### Spec-gardener integration

The `spec-gardener` subagent is the gatekeeper for `.ai-collab/spec/` quality. Claude must invoke it in these situations:

1. **Before modifying SPEC.md:** Run spec-gardener to check for existing drift or contradictions before adding new content. Prevents compounding existing issues.
2. **Before task decomposition (split phase):** Run spec-gardener to verify the spec is clear and consistent enough to decompose into tasks. If spec-gardener raises issues, resolve them first.
3. **After a spec version bump:** Run spec-gardener to confirm the new version is internally consistent and all open questions are correctly reflected.
4. **When user asks to check spec consistency:** Always use spec-gardener rather than reading spec files manually.

**How to invoke:**
Use the Agent tool with `subagent_type: spec-gardener`. Provide the specific question or context.

**When NOT required:**
- Minor clarification edits (typos, rephrasing without semantic change)
- Adding a single requirement entry that does not interact with existing constraints
- Routine CHANGELOG.md entries
```

## Acceptance criteria
- `CLAUDE.md` contains `### Spec-gardener integration` section
- Section lists at least 4 trigger conditions
- Section includes "How to invoke" instruction referencing Agent tool with subagent_type
- Section includes "When NOT required" to avoid over-triggering

## must_haves
- spec-gardener 从「偶尔用」变成「有明确触发条件的系统性步骤」
- 触发条件不能太宽泛（避免每次都调用），也不能太窄（避免失去价值）

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log

- 2026-03-22: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work.
- 2026-03-22: Confirmed task `026` is the single requested Codex task and that the only allowed implementation target is `CLAUDE.md`.
- 2026-03-22: Added `### Spec-gardener integration` to `CLAUDE.md` between `### Task decomposition rules` and `### Spec change rules`, with four explicit trigger conditions, an Agent-tool invocation note using `subagent_type: spec-gardener`, and a bounded `When NOT required` list.
- 2026-03-22: Validation: `rg -n "Spec-gardener integration|Before modifying SPEC\\.md|Before task decomposition \\(split phase\\)|After a spec version bump|When user asks to check spec consistency|subagent_type: spec-gardener|When NOT required" CLAUDE.md` matched the inserted section and all required subsections.
- 2026-03-22: Validation: `python tools/check_consistency.py` passed (`0 FAIL, 0 WARN, 5 PASS, 1 SKIP`). No Mode B report file was written because this task is declared as invocation mode `A`.
