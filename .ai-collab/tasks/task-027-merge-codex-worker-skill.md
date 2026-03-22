# Task 027 — merge-codex-worker-skill

## Goal
Merge useful content from `.agents/skills/codex-worker/SKILL.md` into `AGENTS.md`, then replace the skill file with a redirect notice. Eliminates the redundancy between the two files.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — modifies 2 files, criteria verifiable from execution log

## Target paths
- `AGENTS.md`
- `.agents/skills/codex-worker/SKILL.md`

## Pre-conditions
- None

## Instructions

### Step 1: Identify unique content in codex-worker/SKILL.md

Read both files. The codex-worker skill has these sections not currently in AGENTS.md:
- `## Accepted inputs` — how to interpret task selector formats (`next`, `TASK-003`, `003`, file path)
- `## Task selection` — how to resolve `next` vs explicit task ID
- `## Naming compatibility` — accept `TASK-003` style, persist lowercase
- `## Closing summary` — the structured review-ready summary format

### Step 2: Merge into AGENTS.md

Add the following to `AGENTS.md` after the existing `## Codex CLI execution context` section:

```markdown
## Task selection

When Claude instructs you to execute a task, the task reference may come in these forms:
- `next` — pick the first `todo` task assigned to `codex` in `board.yaml` (check `suggested_next_for_codex` first)
- `task-003` or `003` or `TASK-003` — normalize to the repo's lowercase filename convention
- A file path like `.ai-collab/tasks/task-003-foo.md` — use that file directly

Always verify the selected task against `board.yaml`: confirm `status: todo`, `assigned_to: codex`, and all `depends_on` tasks are `done`.

## Closing summary

End every task execution with a short review-ready summary:

```text
Task: task-<ID>-<slug>
Result: done | review | blocked
Files changed: <list>
Validation: <command run or N/A>
Notes for Claude: <residual risk, blocker, or "none">
```

This summary is the first thing Claude reads when reviewing your work.
```

### Step 3: Replace codex-worker/SKILL.md with redirect

Replace the entire content of `.agents/skills/codex-worker/SKILL.md` with:

```markdown
# codex-worker

> **Deprecated:** This skill's content has been merged into `AGENTS.md` at the repository root.
> Read `AGENTS.md` for the authoritative Codex worker protocol.
>
> This file is kept for reference only and will not be updated.
```

## Acceptance criteria
- `AGENTS.md` contains `## Task selection` section with `next`/explicit/path resolution rules
- `AGENTS.md` contains `## Closing summary` section with the structured format
- `.agents/skills/codex-worker/SKILL.md` contains only the deprecation redirect notice
- No content is lost: all unique value from the skill file is present in AGENTS.md

## must_haves
- 合并后 AGENTS.md 是唯一的 Codex 行为规范文件，不存在两个文件各说各话的情况
- codex-worker/SKILL.md 保留但标注 deprecated，不删除（历史档案）

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log

- 2026-03-22: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work.
- 2026-03-22: Confirmed task `027` is explicitly requested, `status: todo`, `assigned_to: codex`, and has no unresolved dependencies in `board.yaml`.
- 2026-03-22: Read `.agents/skills/codex-worker/SKILL.md` and merged its unique task-selector and review-summary protocol into `AGENTS.md` by adding `## Task selection` and `## Closing summary` immediately after `## Codex CLI execution context`.
- 2026-03-22: Replaced `.agents/skills/codex-worker/SKILL.md` with the required deprecation redirect so `AGENTS.md` is the single authoritative Codex worker protocol file.
- 2026-03-22: Validation: `rg -n "## Task selection|## Closing summary|normalize to the repo's lowercase filename convention|Task: task-<ID>-<slug>|Notes for Claude:" AGENTS.md` confirmed the merged sections and review-ready template.
- 2026-03-22: Validation: inspected `.agents/skills/codex-worker/SKILL.md` and confirmed it now contains only the deprecation redirect notice.
- 2026-03-22: Validation: `python tools/check_consistency.py` passed (`0 FAIL, 0 WARN, 5 PASS, 1 SKIP`).

```text
Task: task-027-merge-codex-worker-skill
Result: review
Files changed: AGENTS.md, .agents/skills/codex-worker/SKILL.md, .ai-collab/tasks/task-027-merge-codex-worker-skill.md
Validation: rg -n "## Task selection|## Closing summary|normalize to the repo's lowercase filename convention|Task: task-<ID>-<slug>|Notes for Claude:" AGENTS.md; python tools/check_consistency.py
Notes for Claude: none
```
