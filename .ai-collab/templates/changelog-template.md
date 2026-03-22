> **Deprecated:** This template has been merged into `spec-aux-template.md`. Use that file instead.

# Specification Changelog

This document tracks changes to the Living Specification. Each entry records what changed, why, and what impact it has on existing plans and tasks.

**Format:** Each entry includes date, change summary, rationale, and impact assessment.

---

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
