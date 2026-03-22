# Living Specification: Claude + Codex Multi-Agent Collaboration System

**Last updated:** 2026-03-21
**Status:** Active
**Version:** 0.3.0

---

## Terminology

- **Claude**: The orchestrator agent responsible for planning, task decomposition, review, and coordination
- **Codex**: The implementor agent responsible for executing tasks and making code changes
- **Board**: The `board.yaml` file serving as the single source of truth for plan and task statuses
- **Living Spec**: The evolving specification in `spec/SPEC.md` that contains only current truth
- **Artifact**: Any file produced by the protocol (plans, tasks, reviews, reports)

---

## Product intent

Enable structured, traceable collaboration between Claude (orchestrator) and Codex (implementor) through a file-based protocol that separates planning, execution, and review into distinct, auditable phases.

---

## Scope

### In scope

- Plan decomposition into atomic, verifiable tasks
- Task lifecycle management (todo → in_progress → review → done)
- Execution logging and progress tracking
- Review and acceptance workflow
- Dependency management between tasks
- Blocking and replanning mechanisms
- Living specification that evolves with the system

### Out of scope

- Direct code generation by Claude (unless explicitly requested by user)
- Real-time communication between agents
- Automated task assignment (Claude manually assigns via board.yaml)
- Version control integration beyond file-based tracking
- Multi-repository coordination

---

## Core capabilities

### 1. Plan authoring (Claude)

- Write structured plan documents in `.ai-collab/plans/`
- Define clear goals, scope, and success criteria
- Decompose plans into tasks with acceptance criteria

### 2. Task decomposition (Claude)

- Create atomic tasks (< 5 files, single focus)
- Specify `target_paths` to scope file changes
- Define `acceptance_criteria` as verifiable commands or outcomes
- Establish `depends_on` relationships for ordering

### 3. Task execution (Codex)

- Read task definition from `.ai-collab/tasks/`
- Execute within scoped `target_paths`
- Log progress without modifying Claude-authored task definitions
- Write completion report to `.ai-collab/reports/`

### 4. Review and acceptance (Claude)

- Read Codex reports and verify acceptance criteria
- Write review conclusions to `.ai-collab/reviews/`
- Update task status in `board.yaml`:
  - `done` if acceptance criteria met
  - `blocked` if work cannot continue
  - `todo` if rework needed (with review documenting reasons)

### 5. Status tracking (Claude)

- Maintain `board.yaml` as single source of truth
- Track current plan, all task statuses, and suggested next task
- Preserve all historical artifacts (plans, tasks, reviews, reports)

### 6. Session continuity

- Claude checks `runtime/codex-session.yaml` before each Codex invocation
- For dependent tasks: instructs user to run `codex resume <last_session_id>`
- For independent tasks: instructs user to run `codex` or `codex exec`
- Session history stored locally in `~/.codex/session_index.jsonl` — does not expire
- After each run: Claude updates `last_session_id` and `last_task_id` in `codex-session.yaml`

### 7. Invocation modes

- Every task declares invocation mode in the task file
- **Mode A (CLI direct):** <= 2 files, all criteria verifiable from execution log, no code logic changes. Codex does not write a report file.
- **Mode B (report required):** > 2 files, OR shell command verification needed, OR code logic changes. Codex writes a report to `reports/` before handing off to Claude.
- Mode must be declared in both the task file (`## Invocation mode`) and the user-facing Codex prompt.

### 8. Context handoff

- `runtime/codex-handoff.md` contains two mandatory sections: Codex execution state + Orchestrator state
- Claude updates both sections after each task review
- Orchestrator state includes: current plan, spec version, last review, pending open questions, next action

### 9. Living specification (Claude)

- Maintain current truth in `SPEC.md`
- Record key decisions and rationale in `DECISIONS.md`
- Track specification changes in `CHANGELOG.md`
- Trigger replanning when spec changes invalidate tasks

---

## Constraints

### Technical

- All communication is file-based (no API calls between agents)
- Artifacts must be human-readable and machine-parseable
- Status values are restricted to exactly five states: `todo`, `in_progress`, `review`, `done`, `blocked`
- Task identifiers must be unique and sortable
- Timestamps must be unambiguous and sortable

### Organizational

- Claude does not modify application source code by default
- Codex works on exactly one task at a time
- Codex never modifies `board.yaml`
- Codex never rewrites Claude-owned task definition sections
- Only Claude updates authoritative task statuses

### Process

- A task is only `done` after Claude reviews and accepts it
- Blocked tasks must document the blocker for Claude
- Tasks requiring rework return to `todo` status with review documenting reasons
- All artifacts are preserved; superseded plans and completed tasks remain in the filesystem

---

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

- **REQ-09:** Cross-file consistency (session_id, spec version, task status) must be verifiable by an automated script.
- **REQ-10:** Every milestone completion must produce a milestone-level review document summarising all delivered capabilities.

---

## Acceptance criteria

The system is working correctly when:

1. **Plan clarity**: Any task can be executed by Codex without asking Claude for clarification
2. **Traceability**: Every code change can be traced back to a task, plan, and user requirement
3. **Auditability**: The complete history of decisions, changes, and reviews is preserved in `.ai-collab/`
4. **Isolation**: Codex can work independently without blocking on Claude
5. **Verification**: All task acceptance criteria are executable commands or observable outcomes
6. **Consistency**: `board.yaml` always reflects the true state of all tasks
7. **Spec alignment**: When SPEC.md changes, Claude evaluates all `todo` and `in_progress` tasks, marks invalidated tasks as `blocked`, and updates `spec_status.replan_required` in board.yaml

---

## Open questions

1. **Spec dirty detection** - **Resolved:** `spec_dirty` is set manually by Claude whenever `SPEC.md` is modified. Claude clears it after evaluating impact on the current plan and updating `board.yaml`.

2. **Replan triggers** - **Deferred:** Threshold not defined. Current policy: Claude evaluates case-by-case when `invalidated_tasks` list is non-empty.

3. **Conflict resolution** - **Resolved:** If `spec_dirty: true` and any task is `in_progress`, Claude must resolve the conflict before the next Codex invocation. Claude must not invoke Codex while `spec_dirty: true` and tasks are active.

4. **Granularity** - **Deferred:** SPEC.md describes system-wide patterns and constraints. Feature-specific requirements live in plan documents.

---

## Related documents

- [`.ai-collab/README.md`](../README.md) - Protocol overview and role responsibilities
- [`.ai-collab/spec/DECISIONS.md`](DECISIONS.md) - Key architectural decisions
- [`.ai-collab/spec/CHANGELOG.md`](CHANGELOG.md) - Specification change history
- [`CLAUDE.md`](../../CLAUDE.md) - Project-level instructions for Claude
- [`AGENTS.md`](../../AGENTS.md) - Agent definitions and invocation patterns
