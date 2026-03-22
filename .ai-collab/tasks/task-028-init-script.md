# Task 028 — init-script

## Goal
Create `tools/init.sh` — a shell script that copies the collaboration protocol files into a new project directory, creating a clean starting point without any project-specific history (tasks, reports, reviews, runtime state).

## Status
`todo`

## Assigned to
codex

## Invocation mode
`B` — report required: creates a new script with logic, criteria require running it

## Target paths
- `tools/init.sh`

## Pre-conditions
- None

## Instructions

Create `tools/init.sh` with the following behavior:

### Usage
```bash
bash tools/init.sh /path/to/new/project
# or from anywhere:
bash /path/to/this/repo/tools/init.sh /path/to/new/project
```

### What the script copies

From this repo to `<target>/`:

**Protocol core (always copy):**
- `CLAUDE.md` → `<target>/CLAUDE.md`
- `AGENTS.md` → `<target>/AGENTS.md`
- `QUICKSTART.md` → `<target>/QUICKSTART.md`
- `.claude/agents/spec-gardener.md` → `<target>/.claude/agents/spec-gardener.md`
- `.claude/skills/claude-orchestrator/SKILL.md` → `<target>/.claude/skills/claude-orchestrator/SKILL.md`
- `.agents/skills/codex-worker/SKILL.md` → `<target>/.agents/skills/codex-worker/SKILL.md`
- `tools/check_consistency.py` → `<target>/tools/check_consistency.py`

**Protocol templates (always copy):**
- `.ai-collab/README.md` → `<target>/.ai-collab/README.md`
- `.ai-collab/templates/` (entire directory) → `<target>/.ai-collab/templates/`

**Blank board.yaml (generate fresh, not copy):**
Generate a minimal `<target>/.ai-collab/board.yaml` with empty plan and no tasks:
```yaml
# .ai-collab/board.yaml
# Single source of truth for the current plan and all task statuses.
# Claude maintains this file. Codex reads it but does not write to it.

meta:
  last_updated: "YYYY-MM-DD"
  last_action: "project initialized"
  orchestrator: claude

runtime:
  codex_session_file: "runtime/codex-session.yaml"
  mcp_enabled: false

current_plan:
  id: ""
  goal: ""
  status: "none"

current_milestone:
  id: ""
  goal: ""
  plans: []
  status: "none"
  review_file: ""

current_spec:
  version: "0.1.0"
  file: "spec/SPEC.md"
  last_updated: "YYYY-MM-DD"

spec_status:
  spec_dirty: false
  replan_required: false
  invalidated_tasks: []
  last_spec_change: ""

tasks: []

suggested_next_for_codex:
  task_id: ""
  reason: "no tasks yet"
```

**Blank spec files (generate fresh):**
Create `<target>/.ai-collab/spec/SPEC.md` with minimal header:
```markdown
# Living Specification: <Project Name>

**Last updated:** YYYY-MM-DD
**Status:** Draft
**Version:** 0.1.0

---

## Product intent

> Describe what this project does and why it exists.

---

## Requirements

- **REQ-01:** ...

---

## Open questions

1. ...
```

Create empty `<target>/.ai-collab/spec/DECISIONS.md` and `<target>/.ai-collab/spec/CHANGELOG.md` with minimal headers.

**Create empty directories:**
- `<target>/.ai-collab/tasks/`
- `<target>/.ai-collab/plans/`
- `<target>/.ai-collab/reviews/`
- `<target>/.ai-collab/reports/`
- `<target>/.ai-collab/runtime/`
- `<target>/.ai-collab/spec/milestones/`

### Script behavior

- If `<target>` does not exist: create it
- If `<target>/.ai-collab/` already exists: print warning and ask for confirmation before overwriting
- Replace `YYYY-MM-DD` placeholders in generated files with the current date
- Print a summary of what was created
- End with: `Done. Open <target>/QUICKSTART.md to get started.`

### Script must NOT copy
- `.ai-collab/tasks/` (project-specific)
- `.ai-collab/plans/` (project-specific)
- `.ai-collab/reviews/` (project-specific)
- `.ai-collab/reports/` (project-specific)
- `.ai-collab/runtime/` (session state)
- `.ai-collab/spec/SPEC.md` from this repo (replaced with blank)
- `.ai-collab/spec/milestones/` (project-specific)
- `mini.py`, `mini.png`, `codex_probe.txt`, `CODEX_CANARY.md` (experiment artifacts)
- `.git/` (obviously)

## Acceptance criteria
- `tools/init.sh` exists and is valid bash
- Running `bash tools/init.sh /tmp/test-project` creates the target directory with all required files
- Generated `board.yaml` has `tasks: []` and today's date
- Generated `SPEC.md` has `Version: 0.1.0` and today's date
- `.ai-collab/tasks/`, `plans/`, `reviews/`, `reports/`, `runtime/` exist as empty directories in target
- No project-specific files from this repo appear in target
- Script prints `Done. Open <target>/QUICKSTART.md to get started.`

## must_haves
- 新项目初始化后可以直接开始使用协议，无需任何手动配置
- 生成的 board.yaml 和 SPEC.md 有正确的今日日期，不是占位符
- 脚本对已存在的目标目录有保护性提示，不会静默覆盖

## Depends on
- task-027 (AGENTS.md 已是合并后的最终版本，init.sh 复制的是最新版)

## Updated
2026-03-22

## Codex execution log

- 2026-03-22: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work.
- 2026-03-22: Confirmed task `028` is explicitly requested, `status: todo`, `assigned_to: codex`, and its dependency `027` is `done` in `board.yaml`.
- 2026-03-22: Created `tools/init.sh`, a bash bootstrap script that copies the protocol core files and templates, generates fresh `.ai-collab/board.yaml` and spec starter files with today's date, creates the required empty collaboration directories, and protects existing `.ai-collab/` targets with a confirmation prompt before reset.
- 2026-03-22: Validation note: the default `bash` command in this Windows sandbox resolves to `C:\Windows\System32\bash.exe` and failed with `Bash/Service/CreateInstance/E_ACCESSDENIED`, so end-to-end validation used explicit Git Bash (`C:\Program Files\Git\bin\bash.exe`) with approval.
- 2026-03-22: Validation: `C:\Program Files\Git\bin\bash.exe tools/init.sh .tmp/test-project-028` succeeded and printed `Done. Open /c/Users/X/Desktop/test_of_multi_agent/.tmp/test-project-028/QUICKSTART.md to get started.` after creating the target bootstrap.
- 2026-03-22: Validation: inspected generated `.tmp/test-project-028/.ai-collab/board.yaml` and confirmed `tasks: []`, `last_updated: "2026-03-22"`, and `current_spec.version: "0.1.0"`.
- 2026-03-22: Validation: inspected generated `.tmp/test-project-028/.ai-collab/spec/SPEC.md`, `DECISIONS.md`, and `CHANGELOG.md` and confirmed fresh starter content with today's date and version `0.1.0`.
- 2026-03-22: Validation: confirmed required copied files exist in `.tmp/test-project-028`, forbidden project-specific artifacts do not exist (`mini.py`, `mini.png`, `codex_probe.txt`, `CODEX_CANARY.md`, copied task/report history, `.ai-collab/runtime/codex-session.yaml`, `.git`), and `.ai-collab/tasks`, `plans`, `reviews`, `reports`, `runtime`, and `spec/milestones` are present as empty directories.
- 2026-03-22: Validation: `rg -n "already exists and will be overwritten|Continue\\? \\[y/N\\]" tools/init.sh` confirmed the overwrite-protection warning and confirmation prompt are present in the script.
- 2026-03-22: Validation: `python tools/check_consistency.py` passed (`0 FAIL, 0 WARN, 5 PASS, 1 SKIP`).

```text
Task: task-028-init-script
Result: review
Files changed: tools/init.sh, .ai-collab/tasks/task-028-init-script.md, .ai-collab/reports/task-028-init-script-2026-03-22.md
Validation: C:\Program Files\Git\bin\bash.exe tools/init.sh .tmp/test-project-028; rg -n "already exists and will be overwritten|Continue\? \[y/N\]" tools/init.sh; python tools/check_consistency.py
Notes for Claude: default Windows bash launcher was blocked in the sandbox, so end-to-end validation used explicit Git Bash instead
```
