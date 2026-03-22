# Task 017 — handoff-frontmatter

## Goal
Add a YAML front-matter block to `codex-handoff.md` so key fields (thread_id, last_task_id, plan status, spec version) are machine-readable. Claude can then parse the front-matter for quick consistency checks without reading the full markdown body.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 1 file, all criteria verifiable from MCP response, documentation change only

## Target paths
- `.ai-collab/runtime/codex-handoff.md`

## Pre-conditions
- None

## Instructions

Replace the current `codex-handoff.md` header section with a YAML front-matter block followed by the existing markdown content. The front-matter must come before the `# Codex Handoff Summary` heading.

Add this front-matter at the very top of the file (before line 1):

```yaml
---
# machine-readable snapshot — Claude-maintained, updated after every task review
handoff_version: 3
snapshot_at: "2026-03-22"
thread_id: "019d1335-848f-7ab1-ad48-ad6af62bfdb8"   # must match codex-session.yaml
last_task_id: "verify-mcp"                           # must match codex-session.yaml
plan_id: "plan-002"
plan_status: "done"
spec_version: "0.3.0"
spec_dirty: false
suggested_next_task_id: ""                           # "" = no pending tasks
open_questions_count: 0                              # 0 = all resolved or deferred
---
```

Do not modify any content below the front-matter block.

## Acceptance criteria
- `codex-handoff.md` begins with a `---` YAML front-matter block
- Front-matter contains: `thread_id`, `last_task_id`, `plan_id`, `plan_status`, `spec_version`, `spec_dirty`, `suggested_next_task_id`, `open_questions_count`
- `thread_id` value matches current `codex-session.yaml` thread_id (`019d1335-848f-7ab1-ad48-ad6af62bfdb8`)
- Existing markdown content below the front-matter is unchanged

## must_haves
- Claude 读 handoff.md 时可以直接解析 thread_id 并与 codex-session.yaml 对比，无需扫描 markdown 表格
- front-matter 中的 thread_id 与 codex-session.yaml 中的 thread_id 一致（消除当前的不一致 bug）

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log
- 2026-03-22: Added the requested YAML front-matter block to `.ai-collab/runtime/codex-handoff.md` before `# Codex Handoff Summary` and left the existing markdown body unchanged.
- 2026-03-22: Verified the front-matter fields are valid YAML scalars and that `thread_id` (`019d1335-848f-7ab1-ad48-ad6af62bfdb8`) and `last_task_id` (`verify-mcp`) match `.ai-collab/runtime/codex-session.yaml`.
