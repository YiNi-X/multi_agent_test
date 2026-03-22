# Task 024 — quickstart-workflow-overview

## Goal
Add a `## 0. How this system works` section to `QUICKSTART.md` that shows the full 7-stage document-driven development flow, so users understand the big picture before diving into individual commands.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 1 file, criteria verifiable from MCP response, documentation only

## Target paths
- `QUICKSTART.md`

## Pre-conditions
- task-023 done (PR workflow rules established)

## Instructions

In `QUICKSTART.md`, before `## 1. Start a new task`, insert:

```markdown
## 0. How this system works

This system uses a **document-driven development flow**. Documents are not just notes — they drive every decision.

```
阶段 1: 需求发散    → 你描述目标，Claude 提问澄清
阶段 2: PRD (SPEC)  → Claude 将需求沉淀为 SPEC.md 的 Requirements 章节
阶段 3: Plan+Review → Claude 拆分任务，你确认计划
阶段 4: 实现        → Codex MCP 执行任务，Claude review 每个结果
阶段 5: 测试        → 运行 check_consistency.py + 端到端验证
阶段 6: 人工Review  → 你 review 变动，Claude 写 Plan 级别 verdict
阶段 7: 提交 PR     → commit + PR，里程碑完成时写里程碑 review
```

**偏差处理规则（重要）：**
- 测试发现偏差 → 先改文档（SPEC.md），再让 Codex 修代码
- 人工 Review 不满意 → 回到 SPEC.md 修改需求，重新 Plan
- 直接改代码跳过文档 → 违反协议，会导致文档与实现不一致
```

## Acceptance criteria
- `QUICKSTART.md` 第一个内容章节是 `## 0. How this system works`
- 包含 7 个阶段的流程说明
- 包含偏差处理规则（先改文档的原则）
- 位于 `## 1. Start a new task` 之前

## must_haves
- 用户打开 QUICKSTART.md 第一眼就看到完整工作流，而不是直接跳到操作步骤
- 偏差处理规则明确说明了「先改文档」的优先级

## Depends on
- task-023

## Updated
2026-03-22

## Codex execution log
- 2026-03-22: Blocked before implementation. Task `024` declares a pre-condition and dependency on `task-023`, but `.ai-collab/board.yaml` still marks task `023` status as `todo`, so this task is not yet eligible for execution.
- 2026-03-22: Evidence reviewed before stopping: `board.yaml > tasks[id=023].status` is `todo`, and task `024` lists `task-023` in both `## Pre-conditions` and `## Depends on`.
- 2026-03-22: No changes were made to `QUICKSTART.md`. Suggested next step for Claude: mark task `023` done in `board.yaml` after review, then re-invoke task `024`.
- 2026-03-22: Re-ran task `024` after confirming `.ai-collab/board.yaml` now marks task `023` as `done`, then added `## 0. How this system works` to `QUICKSTART.md` before `## 1. Start a new task`.
- 2026-03-22: Inserted a 7-stage document-driven workflow overview plus deviation-handling rules that explicitly require updating documents first when tests or review reveal a mismatch.
- 2026-03-22: Verified the new section is the first content section in `QUICKSTART.md`, appears before `## 1. Start a new task`, and satisfies all task acceptance criteria.
