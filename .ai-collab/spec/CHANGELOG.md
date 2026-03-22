# Specification Changelog

This document tracks changes to the Living Specification. Each entry records what changed, why, and what impact it has on existing plans and tasks.

**Format:** Each entry includes date, change summary, rationale, and impact assessment.

---

## v0.4.0 - 2026-03-22

**Changes:**
- Migrated Codex invocation from MCP Server to local CLI (`codex`, `codex exec`, `codex resume`) (task-025)
- Removed canary probe mechanism — local CLI sessions do not expire (task-025)
- Replaced `thread_id` / `threadId` session tracking with `last_session_id` from `~/.codex/session_index.jsonl` (task-025)
- Added numbered requirements REQ-01~10 to SPEC.md for plan-level traceability (task-019)
- Added plan-level verdict (PASS/REWORK/BACK TO PRD) to plan and review templates (task-020)
- Added milestone review template with requirements coverage tracking (task-021)
- Added `tools/check_consistency.py` for automated cross-file consistency validation (task-022)
- Added PR workflow rules to CLAUDE.md: 6-step delivery sequence per plan (task-023)
- Added 7-stage document-driven workflow overview to QUICKSTART.md (task-024)
- Updated session continuity section to reflect CLI model (README, SPEC, SKILL, codex-worker-protocol)

**Rationale:** MCP Server sessions expired on the platform side (no local persistence), causing canary failures and requiring complex session management. Codex CLI stores sessions locally in `~/.codex/` and never expires them, making the entire canary/threadId mechanism unnecessary.

**Impact:**
- No tasks invalidated — all existing task files remain valid
- `codex-session.yaml` schema updated: `thread_id` → `last_session_id`, removed MCP-only fields
- `codex-handoff.md` front-matter updated: `thread_id` → `last_session_id`
- `check_consistency.py` Check 1 updated to verify `last_session_id` instead of `thread_id`

**Related decisions:** D014 (CLI over MCP for session persistence)

---

## v0.3.0 - 2026-03-21

**Changes:**
- Added Mode A / Mode B invocation mode protocol (task-008)
- Added session canary probe mechanism; time-based expiry is now fallback only (task-009)
- Added mandatory two-section structure for `codex-handoff.md` (task-007)
- Added `review` state durability rule: tasks must not jump from `in_progress` to `done` (task-006)
- Fixed orphan fields: `total_tasks_executed` increment rule, `spec_hash_at_start` write procedure, `suggested_next_for_codex` validity condition (task-005)

**Resolved open questions:** Q1 (spec_dirty detection), Q3 (conflict resolution rule)
**Deferred:** Q2 (replan threshold), Q4 (SPEC granularity)

---

## [0.2.0] - 2026-03-17

### Added

- **Terminology section** defining Claude, Codex, Board, Living Spec, and Artifact
- **Semantic versioning decision** (D011) with clear rules for MAJOR/MINOR/PATCH bumps
- **Archiving mechanism decision** (D009) specifying how to rename superseded plans
- **Implementation details separation decision** (D010) clarifying SPEC vs README scope

### Changed

- **Status vocabulary clarified**: Removed `needs_revision` from review outcomes; tasks requiring rework return to `todo` with review documenting reasons (D008)
- **Archiving language**: Changed from "never delete (archive with suffix)" to "preserve all artifacts; superseded plans renamed with `-archived-YYYY-MM-DD`"
- **Technical constraints**: Removed implementation details (markdown format, 3-digit IDs, ISO 8601) and replaced with requirements (human-readable, unique identifiers, sortable timestamps)
- **Acceptance criterion #7 (Spec alignment)**: Made verifiable by specifying concrete actions (evaluate tasks, mark as blocked, update spec_status)
- **Open questions**: Refined to be more specific and actionable; removed outdated versioning question
- **Status**: Changed from "Initial draft" to "Active"

### Fixed

- **Contradiction resolved**: Clarified that task execution logs progress "without modifying Claude-authored task definitions" instead of prescribing "Codex-owned execution section"
- **Ambiguity resolved**: Acceptance criterion #3 now specifies artifacts are preserved "in `.ai-collab/`"

### Removed

- **Vague open questions**: Removed "Should spec changes go through review?" and "Should SPEC.md use semantic versioning?" (now decided)
- **Implementation leakage**: Moved file format and naming conventions to README.md

**Rationale:**
- Address spec-gardener review findings (9 issues: 1 critical, 1 high, 4 medium, 3 low)
- Resolve status vocabulary contradiction that blocked planning
- Separate requirements (SPEC) from implementation details (README)
- Make acceptance criteria verifiable and actionable
- Improve clarity and reduce ambiguity

**Impact:**
- **No existing tasks affected** (no active plan yet)
- **Spec now ready for planning** (critical issues resolved)
- **Future tasks must align with five-state lifecycle** (todo/in_progress/review/done/blocked)
- **Implementation details can change without spec version bumps** (moved to README)

**Related decisions:** D007 (accepted), D008, D009, D010, D011 (all new)

---

## [0.1.0] - 2026-03-17

### Added

- **Living Spec layer initialization**
  - Created `SPEC.md` with initial system specification
  - Created `DECISIONS.md` with architectural decision log
  - Created `CHANGELOG.md` (this file)
  - Added spec-related templates

**Rationale:** Establish single source of truth for system behavior and requirements that evolves with the project.

**Impact:**
- No existing tasks affected (initial creation)
- Future tasks must align with SPEC.md
- Spec changes will trigger replan evaluation

**Related decisions:** D006 (Living Spec as current truth only), D007 (Spec changes trigger replan evaluation)

---

## Changelog template

Use this template for new entries:

```markdown
## [Version] - YYYY-MM-DD

### Added
- [New capabilities, constraints, or requirements]

### Changed
- [Modifications to existing spec]

### Deprecated
- [Features marked for removal]

### Removed
- [Deleted capabilities or constraints]

### Fixed
- [Corrections to spec errors or ambiguities]

**Rationale:** [Why these changes?]

**Impact:**
- [Which tasks/plans are affected?]
- [What needs to be replanned?]
- [What becomes possible/impossible?]

**Related decisions:** [Link to DECISIONS.md entries]
```

---

## Impact assessment guidelines

When recording a spec change, evaluate impact using these categories:

- **No impact**: Change is clarification only, no tasks affected
- **Minor impact**: Affects < 3 tasks, can be handled with small updates
- **Major impact**: Affects ≥ 3 tasks or requires architectural changes
- **Breaking change**: Invalidates current plan, requires full replan

Include specific task IDs when known.
