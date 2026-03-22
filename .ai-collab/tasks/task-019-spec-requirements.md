# Task 019 — spec-requirements

## Goal
Add a `## Requirements` chapter to `SPEC.md` with numbered requirement entries (REQ-01, REQ-02...) that express system behavior as user-facing needs, not implementation constraints. This makes SPEC.md a proper PRD that plan documents can reference by REQ-ID.

## Status
`todo`

## Assigned to
codex

## Invocation mode
`A` — MCP direct: modifies 1 file, criteria verifiable from MCP response, documentation only

## Target paths
- `.ai-collab/spec/SPEC.md`

## Pre-conditions
- None

## Instructions

In `.ai-collab/spec/SPEC.md`, after the `## Constraints` section and before `## Open questions`, add:

```markdown
## Requirements

Numbered requirements that plans and tasks can reference by ID. These express what the system must do from a user perspective.

### Workflow requirements

- **REQ-01:** A user must be able to describe a goal in plain language and receive a decomposed task plan without writing any protocol files manually.
- **REQ-02:** A user must be able to restore full working context after a Claude conversation reset by issuing a single command.
- **REQ-03:** When a Codex session expires, the user must receive a clear notification with confirmation prompt before any session reset occurs.
- **REQ-04:** Every task must have objective, verifiable acceptance criteria that can be checked without running the full system.
- **REQ-05:** The protocol must detect and block Codex invocation when a spec change is unresolved (`spec_dirty: true`).

### Traceability requirements

- **REQ-06:** Every task must reference the plan it belongs to.
- **REQ-07:** Every plan must list its acceptance criteria at the plan level, separate from individual task criteria.
- **REQ-08:** Every plan completion must be followed by a commit and PR before the next plan begins.

### Quality requirements

- **REQ-09:** Cross-file consistency (thread_id, spec version, task status) must be verifiable by an automated script.
- **REQ-10:** Every milestone completion must produce a milestone-level review document summarising all delivered capabilities.
```

## Acceptance criteria
- `SPEC.md` contains a `## Requirements` section after `## Constraints`
- The section contains at least 10 numbered REQ-IDs
- Requirements are grouped into at least 2 sub-categories
- Each requirement is expressed as a user-facing need, not an implementation detail

## must_haves
- SPEC.md 现在可以作为真正的 PRD，plan 文档可以通过 REQ-ID 引用需求
- REQ-08 明确了「Plan 完成后 PR」的要求，给 task-023 提供依据

## Depends on
- (none)

## Updated
2026-03-22

## Codex execution log
- 2026-03-22: Blocked before implementation. The task instructs Codex to modify `.ai-collab/spec/SPEC.md`, but `.ai-collab/README.md` states "Codex does not modify `spec/` files" and `AGENTS.md` says Claude owns `spec/`.
- 2026-03-22: Evidence reviewed before stopping: task `019` targets `.ai-collab/spec/SPEC.md`; `.ai-collab/README.md` Role responsibilities says Codex "Does **not** modify `spec/` files"; `SPEC.md` is therefore outside Codex's allowed write scope under the repository protocol.
- 2026-03-22: Suggested next step for Claude: either reassign this spec change to Claude, or update the repository protocol/task ownership rules to explicitly permit Codex to edit `spec/` files for this task and then re-invoke Codex.
- 2026-03-22: No acceptance-criteria verification was possible because the required spec edit was not permitted. No files were modified except this Codex execution log.
