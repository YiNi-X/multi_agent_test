# Task 029 — update-quickstart-init

## Goal
Add a `## 5. Initialize protocol in a new project` section to `QUICKSTART.md` explaining how to use `tools/init.sh` to bootstrap the collaboration protocol in a new project folder.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — modifies 1 file, criteria verifiable from execution log

## Target paths
- `QUICKSTART.md`

## Pre-conditions
- task-028 done (init.sh exists)

## Instructions

In `QUICKSTART.md`, after `## 4. Your role at each stage` and before `## Workflow order`, add:

```markdown
## 5. Initialize protocol in a new project

To use this collaboration protocol in a different project:

```bash
bash /path/to/this/repo/tools/init.sh /path/to/new/project
```

This copies the protocol files (CLAUDE.md, AGENTS.md, templates, agents, skills, check_consistency.py) into the new project and creates a blank board.yaml and SPEC.md with today's date. No project-specific history is copied.

After initialization:
1. `cd /path/to/new/project`
2. Open `QUICKSTART.md` and follow from Stage 1
3. Tell Claude your project goal — it reads `board.yaml` and starts planning
```

## Acceptance criteria
- `QUICKSTART.md` contains `## 5. Initialize protocol in a new project` section
- Section includes the `bash tools/init.sh` command with example path
- Section explains what is and is not copied
- Section lists the 3 steps to take after initialization

## must_haves
- 用户看到这个章节就能独立完成新项目初始化，无需额外文档

## Depends on
- task-028

## Updated
2026-03-22

## Codex execution log

- 2026-03-22: Read `AGENTS.md`, `.ai-collab/README.md`, `.ai-collab/board.yaml`, `.ai-collab/spec/SPEC.md`, and this task file before starting work.
- 2026-03-22: Confirmed task `029` is explicitly requested, `status: todo`, `assigned_to: codex`, and dependency `028` is `done` in `board.yaml`.
- 2026-03-22: Added `## 5. Initialize protocol in a new project` to `QUICKSTART.md` after `## 4. Your role at each stage` and before `## Workflow order`, including the `bash /path/to/this/repo/tools/init.sh /path/to/new/project` example, a summary of what is copied versus not copied, and the three post-initialization steps.
- 2026-03-22: Validation: `rg -n "## 5\\. Initialize protocol in a new project|bash /path/to/this/repo/tools/init\\.sh /path/to/new/project|No project-specific history is copied|After initialization:|1\\. \`cd /path/to/new/project\`|2\\. Open \`QUICKSTART\\.md\` and follow from Stage 1|3\\. Tell Claude your project goal" QUICKSTART.md` matched the inserted section and required guidance.
- 2026-03-22: Validation: `python tools/check_consistency.py` passed (`0 FAIL, 0 WARN, 5 PASS, 1 SKIP`). No Mode B report file was written because this task is declared as invocation mode `A`.

```text
Task: task-029-update-quickstart-init
Result: review
Files changed: QUICKSTART.md, .ai-collab/tasks/task-029-update-quickstart-init.md
Validation: rg -n "## 5\. Initialize protocol in a new project|bash /path/to/this/repo/tools/init\.sh /path/to/new/project|No project-specific history is copied|After initialization:|1\. `cd /path/to/new/project`|2\. Open `QUICKSTART\.md` and follow from Stage 1|3\. Tell Claude your project goal" QUICKSTART.md; python tools/check_consistency.py
Notes for Claude: none
```
