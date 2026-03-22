# Task 008 — define-report-modes

## Goal
Document two distinct Codex invocation modes in the protocol. Currently the protocol assumes Codex always writes a report, but in practice some tasks (task-003, task-004) used MCP direct review without a report file. This ambiguity must be resolved by defining clear mode selection criteria and making the mode explicit in task files and review documents.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`B` — report required (modifies README, task-template, review-template; acceptance criteria require inspection of multiple files)

## Target paths
- `.ai-collab/README.md`
- `.ai-collab/templates/task-template.md`
- `.ai-collab/templates/review-template.md`

## Pre-conditions
- None

## Instructions

### Fix 1: Add invocation mode definitions to README.md

In `.ai-collab/README.md`, after the "Role responsibilities" section, add a new section titled `## Codex invocation modes` with the following content:

```markdown
## Codex invocation modes

Every task must declare its invocation mode. This determines whether Codex writes a report file and how Claude conducts the review.

### Mode A — MCP direct

Applicable when **all** of the following are true:
- The task modifies ≤ 2 files
- All `acceptance_criteria` can be verified directly from the MCP response text (no shell commands needed)
- The task does not involve code logic changes (documentation, configuration, and protocol files only)

Behavior:
- Codex does **not** write a file to `reports/`
- Codex still appends `## Codex execution log` to the task file
- Claude's review document must include an `Invocation mode` row and a `MCP response excerpt` row in its metadata table

### Mode B — Report required

Triggered when **any** of the following are true:
- The task modifies > 2 files
- Any `acceptance_criteria` requires running a shell command to verify
- The task involves code logic changes
- The task definition explicitly sets `invocation_mode: B`

Behavior:
- Codex **must** write a report file to `reports/` named `task-<id>-<slug>-<YYYY-MM-DD>.md`
- Codex still appends `## Codex execution log` to the task file
- Claude's review document cites the report file as its primary evidence source

### Mode declaration

The mode must be declared in two places:
1. The task file, as an `## Invocation mode` field (value: `A` or `B` with rationale)
2. The Claude prompt when invoking Codex, explicitly stating whether a report file is expected
```

### Fix 2: Add `## Invocation mode` field to task-template.md

In `.ai-collab/templates/task-template.md`, after the `## Assigned to` section and before `## Target paths`, add:

```markdown
## Invocation mode
`A` or `B` — state the mode and one-line rationale.
- `A` (MCP direct): ≤ 2 files, all criteria verifiable from MCP response, no code logic changes
- `B` (report required): > 2 files, OR shell command verification needed, OR code logic changes
```

### Fix 3: Add invocation mode rows to review-template.md

In `.ai-collab/templates/review-template.md`, in the Metadata table, add two rows after the `Report read` row:

```markdown
| Invocation mode | `A — MCP direct` or `B — report required` |
| Mode A evidence | *(Mode A only)* Key excerpt from MCP response confirming acceptance criteria |
```

For Mode B tasks, the `Mode A evidence` row should be omitted or set to `N/A`.

## Acceptance criteria
- `README.md` contains a `## Codex invocation modes` section defining Mode A and Mode B with their conditions and behaviors
- `README.md` states that mode must be declared in both the task file and the Claude invocation prompt
- `task-template.md` contains an `## Invocation mode` field with the A/B options and their conditions
- `review-template.md` metadata table contains `Invocation mode` and `Mode A evidence` rows

## Depends on
- (none)

## Updated
2026-03-21

## Codex execution log
- 2026-03-21: Updated `.ai-collab/README.md` to define Mode A and Mode B, their selection criteria, and their review/report behavior, and removed the prior always-report assumption from role responsibilities.
- 2026-03-21: Updated `.ai-collab/templates/task-template.md` to add an explicit `## Invocation mode` section and made the definition-of-done report requirement depend on the selected mode.
- 2026-03-21: Updated `.ai-collab/templates/review-template.md` so review metadata records invocation mode and Mode A MCP evidence, with `Report read` compatible with both Mode A and Mode B tasks.
- 2026-03-21: Verified the final wording across all three target files and wrote the task report.
