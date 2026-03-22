# Task 023 — pr-workflow-rules

## Goal
Add PR workflow rules to `CLAUDE.md` so that every completed plan is followed by a commit + PR before the next plan begins. This closes the gap between "all tasks done" and "changes delivered".

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 1 file, criteria verifiable from MCP response, documentation only

## Target paths
- `CLAUDE.md`

## Pre-conditions
- task-019 done (REQ-08 establishes the requirement)
- task-020 done (plan verdict PASS triggers PR)

## Instructions

In `CLAUDE.md`, after the `### Spec change rules` section and before `### Status vocabulary`, add:

```markdown
### PR workflow rules

Every plan follows this delivery sequence:

1. **All tasks done** — all tasks in the plan reach `done` status in `board.yaml`
2. **Plan-level review** — Claude writes a plan-level review document in `reviews/` and fills in the `## Plan review verdict` in the plan file
3. **Run consistency check** — Claude instructs user to run `python tools/check_consistency.py` and confirms all checks pass before proceeding
4. **Commit** — stage all changed files (excluding secrets), write a conventional commit message summarising the plan goal
5. **Open PR** — create a PR targeting `main` with:
   - Title: the plan goal (≤ 70 chars)
   - Body: delivered capabilities, requirements covered (REQ-IDs), test results from consistency check
6. **Update board.yaml** — set `current_plan.status: done`, update `meta.last_action`

**When NOT to open a PR:**
- Plan verdict is REWORK or BACK TO PRD
- Consistency check has FAIL results
- `spec_dirty: true`

**Milestone PR:**
After every milestone (group of plans), Claude additionally writes a milestone review document using `templates/milestone-template.md` and opens a milestone-level PR summarising all delivered capabilities.
```

## Acceptance criteria
- `CLAUDE.md` contains a `### PR workflow rules` section
- The section lists the 6-step delivery sequence
- The section includes conditions for when NOT to open a PR
- The section mentions milestone-level PR and milestone review

## must_haves
- CLAUDE.md 现在明确规定 Plan 完成后必须 commit + PR，不再是隐式期望
- 一致性检查脚本被纳入 PR 前的必要步骤

## Depends on
- task-019
- task-020

## Updated
2026-03-22

## Codex execution log
- 2026-03-22: Added `### PR workflow rules` to `CLAUDE.md` between `### Spec change rules` and `### Status vocabulary`, defining the required delivery sequence from all tasks done through plan completion.
- 2026-03-22: Included the 6-step sequence, the explicit conditions for when not to open a PR, and the milestone-level review and PR guidance using `templates/milestone-template.md`.
- 2026-03-22: Verified the edited section by re-reading `CLAUDE.md` and confirming it satisfies all task acceptance criteria.
