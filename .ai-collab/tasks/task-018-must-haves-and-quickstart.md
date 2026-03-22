# Task 018 — must-haves-and-quickstart

## Goal
Two small protocol improvements:
1. Add an optional `must_haves` field to `task-template.md` for complex multi-file tasks
2. Add a "Your role at each stage" table to `QUICKSTART.md` so users know when and why to intervene

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 2 files, all criteria verifiable from MCP response, documentation change only

## Target paths
- `.ai-collab/templates/task-template.md`
- `QUICKSTART.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Add optional `must_haves` to task-template.md

In `task-template.md`, after the `## Acceptance criteria` section and before `### Claude review handoff`, add:

```markdown
## must_haves (optional)

<!--
Use this section for complex tasks that modify 3+ files or where the same concept
must be expressed consistently across multiple files.

Write from the goal backward: what must be TRUE for the objective to be achieved?
Not "what did Codex write" but "what must the system guarantee after this task".

Skip this section for simple tasks (1-2 files) where acceptance_criteria already
captures the full intent.

Example:
  - "All three files describe the canary failure path with the same user-confirmation step"
  - "The spec version in board.yaml, SPEC.md, and codex-handoff.md are identical"
-->

- (optional — add goal-backward truths here for complex tasks)
```

### Fix 2: Add user role table to QUICKSTART.md

In `QUICKSTART.md`, after the `## 3. Handle common problems` section and before `## Workflow order`, add:

```markdown
## 4. Your role at each stage

| Stage | You need to | Claude/Codex handles automatically |
|---|---|---|
| Start | Describe the goal in plain language | Read state, write plan, decompose tasks |
| After plan is written | Confirm task breakdown (or request changes) | Wait for your confirmation |
| During Codex execution | Nothing | Execute tasks, write logs and reports |
| Canary fails | Type `OK` to confirm session reset (or say cancel) | Reset session, continue from same task |
| Task enters `review` | Optional: read the review doc | Claude auto-reviews and marks done |
| Task is `blocked` | Provide a decision or revised requirement | Wait for your input, then replan |
| Spec change needed | Tell Claude what changed and why | Set `spec_dirty`, evaluate impact, replan |
```

## Acceptance criteria
- `task-template.md` contains an `## must_haves (optional)` section after `## Acceptance criteria`
- The section comment explains when to use it (complex/3+ file tasks) and when to skip it (simple tasks)
- `QUICKSTART.md` contains a `## 4. Your role at each stage` section with a table
- The table covers at minimum: start, plan confirmation, Codex execution, canary failure, review, blocked

## must_haves
- 用户读完 QUICKSTART.md 能知道自己在 6 个关键时刻各自需要做什么
- task-template.md 的 must_haves 字段说明了何时值得写、何时可跳过，不增加简单任务的填写负担

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log
- 2026-03-22: Added `## must_haves (optional)` to `.ai-collab/templates/task-template.md` after the acceptance criteria block and before the Claude review handoff section.
- 2026-03-22: Added the usage comment explaining when to use the section for complex 3+ file tasks and when to skip it for simple tasks, plus the placeholder bullet.
- 2026-03-22: Added `## 4. Your role at each stage` to `QUICKSTART.md` before `## Workflow order`, covering start, plan confirmation, Codex execution, canary failure, review, blocked, and spec change needed.
- 2026-03-22: Verified both edited sections by re-reading the files and confirming the required headings, placement, and table/comment content match the task acceptance criteria.
