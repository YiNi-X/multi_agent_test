# Codex MCP Integration Upgrade Summary

**Date:** 2026-03-18

---

## Changes implemented

### A. Updated CLAUDE.md and claude-orchestrator rules

**CLAUDE.md:**
- Added "Codex MCP execution model" section
- Clarified when subagents are allowed (spec review, discovery, research)
- Mandated Codex MCP for implementation, code modification, validation
- Prohibited Claude from creating subagents to simulate Codex workers
- Added session continuity instructions

**claude-orchestrator/SKILL.md:**
- Added "Codex MCP invocation protocol" section
- Updated boundaries table to include "Create subagents to simulate Codex workers" in the "does NOT do" column
- Defined session expiry rules
- Added checklist for Codex invocation with session state checking

### B. Runtime state file

**Created:** `.ai-collab/runtime/codex-session.yaml`

**Fields:**
- `project_id` — identifies the project
- `codex_session.active` — boolean, true if session is resumable
- `codex_session.session_id` — threadId from MCP calls
- `codex_session.started_at` — ISO 8601 timestamp
- `codex_session.last_used_at` — ISO 8601 timestamp
- `codex_session.last_task_id` — last executed task ID
- `codex_session.status` — idle | executing | completed | failed | expired
- `session_policy.max_idle_minutes` — expiry threshold (default: 30)
- `session_policy.reuse_for_dependent_tasks` — continue for dependent tasks
- `session_policy.force_new_on_spec_change` — restart if spec changes

### C. Updated codex-worker protocol

**Created:** `.ai-collab/templates/codex-worker-protocol.md`

**Key rules:**
- First execution: use `mcp__codex__codex()` to start new session
- Subsequent executions: check `codex-session.yaml` for active session_id
- If valid session exists: use `mcp__codex__codex-reply(threadId, prompt)`
- If expired/missing: use `mcp__codex__codex()` to start fresh
- After execution: Claude updates `codex-session.yaml` with timestamps and task_id
- `board.yaml` remains read-only for Codex
- `runtime/codex-session.yaml` is maintained by Claude only

### D. Updated .ai-collab/README.md

**Added section:** "Codex MCP execution model"

**Content:**
- How Codex is invoked (MCP tools)
- Session continuity mechanism
- Why Claude subagents cannot replace Codex
- Codex invocation checklist
- Updated principle #11 to reference runtime state tracking

### E. Updated AGENTS.md

**Added:**
- Prohibition on writing `runtime/codex-session.yaml`
- "Codex MCP execution context" section
- Instructions for session continuity awareness
- Reporting requirements after task completion

### F. Updated board.yaml

**Added runtime metadata:**
- `runtime.codex_session_file` — path to session state
- `runtime.mcp_enabled` — flag indicating MCP integration is active

---

## Protocol field additions

### codex-session.yaml schema

```yaml
project_id: string
codex_session:
  active: boolean
  session_id: string
  started_at: ISO8601
  last_used_at: ISO8601
  last_task_id: string
  status: enum[idle, executing, completed, failed, expired]
session_policy:
  max_idle_minutes: integer
  reuse_for_dependent_tasks: boolean
  force_new_on_spec_change: boolean
```

### board.yaml additions

```yaml
runtime:
  codex_session_file: string
  mcp_enabled: boolean
```

---

## Responsibility boundaries (updated)

### Claude (orchestrator)

**Does:**
- Plan, decompose, track, review
- Invoke Codex via MCP (`codex()` or `codex-reply()`)
- Maintain `runtime/codex-session.yaml`
- Update `board.yaml` after reviewing Codex reports
- Use subagents for spec review, discovery, research

**Does NOT:**
- Modify application source code (unless explicitly requested)
- Create subagents to simulate Codex workers
- Execute implementation tasks directly
- Allow session state to become stale without checking expiry

### Codex (implementor)

**Does:**
- Execute one task at a time via MCP invocation
- Write to task execution logs
- Write reports to `.ai-collab/reports/`
- Modify files within `target_paths`
- Maintain conversation context across `codex-reply()` calls

**Does NOT:**
- Modify `board.yaml`
- Modify `runtime/codex-session.yaml`
- Pick up tasks autonomously
- Rewrite Claude's task definitions

---

## Remaining risks

### 1. Session expiry edge cases
**Risk:** Session expires between Claude's check and invocation
**Mitigation:** Implement error handling to retry with `codex()` if `codex-reply()` fails with invalid threadId

### 2. Concurrent task execution
**Risk:** Multiple Claude instances trying to use same session
**Mitigation:** Current design assumes single Claude orchestrator; add locking mechanism if concurrent access needed

### 3. Session state corruption
**Risk:** `codex-session.yaml` becomes corrupted or out of sync
**Mitigation:** Validate session_id before each `codex-reply()`; fall back to new session if validation fails

### 4. Spec changes during active session
**Risk:** Codex continues with outdated spec context
**Mitigation:** `force_new_on_spec_change` policy forces fresh session when spec changes

### 5. Claude subagent temptation
**Risk:** Claude might still create subagents for implementation when MCP call seems complex
**Mitigation:** Explicit prohibition in multiple locations (CLAUDE.md, SKILL.md, README.md); requires discipline

### 6. Lost threadId
**Risk:** If `codex-session.yaml` is deleted or reset, context is lost
**Mitigation:** Document recovery procedure: start new session and reference previous reports for context

### 7. MCP tool availability
**Risk:** MCP tools might not be available in all environments
**Mitigation:** Check `runtime.mcp_enabled` flag; fall back to manual handoff if MCP unavailable

---

## Migration path

For existing projects:

1. Create `.ai-collab/runtime/` directory
2. Initialize `codex-session.yaml` with `active: false`
3. Update `board.yaml` with runtime metadata
4. Next task execution will start fresh session via `codex()`
5. Subsequent tasks will reuse session via `codex-reply()`

---

## Verification checklist

- [x] `runtime/codex-session.yaml` created with schema
- [x] CLAUDE.md updated with MCP execution model
- [x] claude-orchestrator/SKILL.md updated with invocation protocol
- [x] .ai-collab/README.md updated with MCP section
- [x] AGENTS.md updated with MCP context instructions
- [x] board.yaml updated with runtime metadata
- [x] codex-worker-protocol.md created with detailed rules
- [x] Subagent restrictions documented in multiple locations
- [x] Session continuity mechanism defined
- [x] Error handling and expiry rules specified
