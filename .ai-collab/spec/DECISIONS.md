# Architectural Decisions

This document records key decisions made during the design and evolution of the .ai-collab protocol. Each decision includes context, the decision itself, and the rationale.

**Last updated:** 2026-03-17

---

## Decision log

### D001: File-based communication over API calls

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need a communication mechanism between Claude and Codex that is auditable, version-controllable, and doesn't require runtime coordination.

**Decision:** Use file-based communication through `.ai-collab/` directory structure.

**Rationale:**
- Provides complete audit trail in version control
- Allows asynchronous work without blocking
- Makes the protocol transparent and debuggable
- Enables human inspection and intervention at any point
- No infrastructure dependencies (databases, message queues, APIs)

**Consequences:**
- Requires file system access for both agents
- Potential for file conflicts if not carefully managed
- No real-time notifications (agents must poll or be invoked)

**Implementation details:** See `.ai-collab/README.md` for directory structure and file naming conventions.

---

### D002: Single source of truth in board.yaml

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need authoritative status tracking that prevents desynchronization between agents.

**Decision:** `board.yaml` is maintained exclusively by Claude and serves as the single source of truth for plan and task statuses.

**Rationale:**
- Prevents conflicting status updates
- Clear ownership model (Claude orchestrates, Codex executes)
- Simplifies conflict resolution
- Makes status queries fast (single file read)

**Consequences:**
- Codex cannot update task status directly
- Requires Codex to write reports that Claude reads and processes
- Adds one extra step to status updates (Codex report → Claude review → board.yaml update)

**Implementation details:** See `.ai-collab/README.md` for board.yaml schema.

---

### D003: Immutable task and plan files

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need to preserve historical context and prevent accidental loss of work.

**Decision:** Never delete task or plan files from the filesystem. Archive superseded files by renaming (see D009 for archiving mechanism).

**Rationale:**
- Preserves complete project history
- Allows rollback to previous plans if needed
- Prevents accidental deletion of in-progress work
- Makes debugging easier (can trace back through decisions)

**Consequences:**
- Directory grows over time (mitigated by archiving)
- Requires discipline to archive rather than delete
- Archived files need to be excluded from active queries

**Related decisions:** D009 (archiving mechanism)

---

### D004: Atomic task decomposition

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need to balance task granularity for effective parallel work and clear acceptance criteria.

**Decision:** Tasks must be atomic (< 5 files, single focus, completable in one session) with verifiable acceptance criteria.

**Rationale:**
- Reduces risk of partial completion
- Makes review faster and more focused
- Enables better parallelization in the future
- Forces clear definition of "done"
- Limits blast radius of errors

**Consequences:**
- Requires more upfront planning effort from Claude
- May feel overly granular for simple changes
- Increases number of tasks to track

---

### D005: Codex does not modify board.yaml

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need clear separation of concerns between orchestration and execution.

**Decision:** Codex reads `board.yaml` but never writes to it. Only Claude updates the board.

**Rationale:**
- Prevents race conditions and conflicts
- Maintains clear orchestrator/implementor boundary
- Ensures Claude always has accurate view of system state
- Simplifies Codex's responsibilities

**Consequences:**
- Codex must communicate status through reports
- Status updates are not immediate (requires Claude review)
- Adds latency to status propagation

---

### D006: Living Spec as current truth only

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need specification that stays current without becoming a historical burden.

**Decision:** `SPEC.md` contains only the current truth. Historical decisions go in `DECISIONS.md`, changes go in `CHANGELOG.md`.

**Rationale:**
- Keeps SPEC.md concise and readable
- Prevents spec from becoming cluttered with outdated information
- Separates "what" (SPEC) from "why" (DECISIONS) and "when" (CHANGELOG)
- Makes it easier to onboard new agents or humans

**Consequences:**
- Requires discipline to move outdated content to CHANGELOG
- Need to maintain three separate documents
- Historical context requires reading multiple files

---

### D007: Spec changes trigger replan evaluation

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need mechanism to keep tasks aligned with evolving specification.

**Decision:** When `SPEC.md` changes, Claude must evaluate whether existing tasks are invalidated and trigger replanning if needed.

**Rationale:**
- Prevents tasks from becoming stale or misaligned
- Ensures implementation matches current requirements
- Makes spec changes explicit and traceable
- Forces conscious decision about impact of changes

**Consequences:**
- Adds overhead to spec changes
- Requires tooling or discipline to detect spec changes
- May slow down rapid iteration on spec
- Need clear criteria for what constitutes "invalidation"

**Open questions:**
- How to detect which tasks are affected by a spec change?
- What threshold of changes triggers full replan vs. incremental update?

---

### D008: Five-state task lifecycle without needs_revision

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need clear, minimal status vocabulary that covers all task states without ambiguity.

**Decision:** Task status is restricted to exactly five values: `todo`, `in_progress`, `review`, `done`, `blocked`. Tasks requiring rework return to `todo` status with review documenting the reasons.

**Rationale:**
- Keeps status vocabulary minimal and unambiguous
- `needs_revision` is redundant: a task needing rework is simply not done yet
- Returning to `todo` preserves the linear lifecycle and makes rework explicit
- Review documents provide the context for why rework is needed
- Simpler state machine is easier to reason about and implement

**Consequences:**
- Tasks may cycle through `todo → in_progress → review → todo` multiple times
- Review history shows all rework cycles
- No separate "revision" queue; rework tasks compete with new tasks in `todo`
- Claude must write clear review feedback to guide rework

**Alternatives considered:**
- Adding `needs_revision` status: rejected as redundant
- Using `blocked` for rework: rejected because blocked implies external blocker, not quality issue

---

### D009: Archiving mechanism for superseded artifacts

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need clear mechanism to preserve historical artifacts while distinguishing active from superseded content.

**Decision:** Superseded plans are renamed with `-archived-YYYY-MM-DD` suffix. Completed tasks remain in place with `done` status in board.yaml. No files are deleted from the filesystem.

**Rationale:**
- Renaming with date suffix makes superseded plans easy to identify and exclude from queries
- Completed tasks don't need renaming because board.yaml already tracks their `done` status
- Date suffix provides chronological context
- Keeping everything on filesystem enables full audit trail

**Consequences:**
- `.ai-collab/plans/` directory grows over time with archived plans
- Need to exclude `-archived-*` files when querying active plans
- Completed tasks remain in `.ai-collab/tasks/` indefinitely
- Git history provides additional layer of versioning

**Implementation details:**
- Archive format: `plan-001-user-auth-2025-01-01.md` → `plan-001-user-auth-2025-01-01-archived-2026-03-17.md`
- Tasks are never renamed; board.yaml status is sufficient

---

### D010: Implementation details belong in README, not SPEC

**Date:** 2026-03-17
**Status:** Accepted
**Context:** SPEC.md was mixing requirements (what) with implementation details (how), reducing flexibility.

**Decision:** SPEC.md contains only requirements and constraints at the conceptual level. Specific file formats, naming conventions, and structural details belong in `.ai-collab/README.md`.

**Rationale:**
- Separates "what we need" from "how we implement it"
- Allows implementation changes without spec changes
- Makes SPEC.md more stable and focused on product requirements
- README.md is the natural place for protocol mechanics

**Consequences:**
- SPEC.md becomes more abstract and requirement-focused
- README.md becomes more detailed and implementation-focused
- Changes to file formats or conventions don't require spec version bumps
- Need to read both documents for complete understanding

**Examples moved to README:**
- Task IDs are zero-padded 3-digit integers
- Timestamps use ISO 8601 format (YYYY-MM-DD)
- Task files use markdown with structured sections
- Filenames use kebab-case

---

### D011: Semantic versioning for SPEC.md

**Date:** 2026-03-17
**Status:** Accepted
**Context:** Need clear versioning scheme to track spec evolution and signal breaking changes.

**Decision:** SPEC.md uses semantic versioning (MAJOR.MINOR.PATCH). Version bumps follow these rules:
- **MAJOR**: Breaking changes that invalidate existing plans or tasks (e.g., removing capabilities, changing core constraints)
- **MINOR**: Additive changes that don't break existing work (e.g., new capabilities, refined open questions)
- **PATCH**: Clarifications, typo fixes, or documentation improvements with no functional impact

**Rationale:**
- Semantic versioning is widely understood
- Clear signal of impact: major version bump means "review your plans"
- Enables automated detection of breaking changes
- Aligns with software engineering best practices

**Consequences:**
- Requires judgment to classify changes correctly
- Major version bumps should trigger replan evaluation
- Version appears in SPEC.md header and board.yaml

**Examples:**
- 0.1.0 → 0.2.0: Added terminology section, clarified status lifecycle (minor)
- 0.2.0 → 1.0.0: Removed a core capability or changed status vocabulary (major)
- 0.2.0 → 0.2.1: Fixed typo in acceptance criteria (patch)

---

## Decision template

Use this template for new decisions:

```markdown
### DXXX: [Decision title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Context:** [What is the issue we're facing?]

**Decision:** [What are we doing?]

**Rationale:**
- [Why this decision?]
- [What alternatives were considered?]

**Consequences:**
- [What becomes easier?]
- [What becomes harder?]
- [What are the trade-offs?]

**Open questions:**
- [What remains unclear?]
```
