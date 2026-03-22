# QUICKSTART

This project uses a Claude + Codex multi-agent workflow. Claude plans and reviews; Codex executes.

---

## 0. How this system works

This system uses a **document-driven development flow**. Documents are not just notes; they drive every decision.

```text
Stage 1: Requirement discovery -> You describe the goal; Claude asks clarifying questions
Stage 2: PRD (SPEC)            -> Claude writes the requirement into SPEC.md under Requirements
Stage 3: Plan + review         -> Claude decomposes the work into tasks; you confirm the plan
Stage 4: Implementation        -> User runs Codex CLI tasks; Claude reviews each result
Stage 5: Testing               -> Run check_consistency.py plus end-to-end verification
Stage 6: Human review          -> You review the changes; Claude writes the plan-level verdict
Stage 7: Submit PR             -> Commit + PR; milestone completion also gets a milestone review
```

**Deviation-handling rules (important):**
- If testing finds a mismatch, fix the document first (`SPEC.md`), then ask Codex to update the implementation.
- If human review is not satisfied, go back to `SPEC.md`, revise the requirement, and re-plan.
- Editing code directly while skipping the document step violates the protocol and causes the docs and implementation to drift.

---

## 1. Start a new task

1. Describe what you want in plain language.
2. Claude reads `board.yaml`, writes a plan, and breaks it into tasks.
3. Confirm the task breakdown looks right.
4. Claude writes the task and tells you to run `codex` or `codex exec`.
5. After Codex finishes, tell Claude `done` and paste the session ID if asked. Claude reviews the output and reports the result to you.

---

## 2. Resume after context reset

1. Say "restore state" or "read current progress".
2. Claude reads `board.yaml` + `runtime/codex-handoff.md` + latest review.
3. Claude outputs a status summary and tells you the next step.

---

## 3. Handle common problems

| Situation | What to do |
|---|---|
| Want to continue previous session | Run `codex resume --last` or `codex resume <session-id>` |
| Task blocked | Run `/claude-orchestrator replan` — Claude reads the blocker report and proposes a fix or asks you to decide |
| Want to change requirements | Tell Claude first; it sets `spec_dirty`, evaluates impact on existing tasks, then invokes Codex |
| Want to check status | Run `/claude-orchestrator status` |
| Task did wrong thing | Tell Claude; it marks the task `todo` for rework and explains what Codex will fix |

---

## 4. Your role at each stage

| Stage | You need to | Claude/Codex handles automatically |
|---|---|---|
| Start | Describe the goal in plain language | Read state, write plan, decompose tasks |
| After plan is written | Confirm task breakdown (or request changes) | Wait for your confirmation |
| During Codex execution | Run `codex` or `codex exec` as instructed by Claude | Writes task file with full prompt |
| After Codex finishes | Tell Claude "done" and paste session ID if asked | Reviews execution log, updates board.yaml |
| Task enters `review` | Optional: read the review doc | Claude auto-reviews and marks done |
| Task is `blocked` | Provide a decision or revised requirement | Wait for your input, then replan |
| Spec change needed | Tell Claude what changed and why | Set `spec_dirty`, evaluate impact, replan |

---

## 5. Initialize protocol in a new project

To use this collaboration protocol in a different project:

```bash
bash /path/to/this/repo/tools/init.sh /path/to/new/project
```

This copies the protocol files (CLAUDE.md, AGENTS.md, templates, agents, skills, check_consistency.py) into the new project and creates a blank board.yaml and SPEC.md with today's date. No project-specific history is copied.

After initialization:
1. `cd /path/to/new/project`
2. Open `QUICKSTART.md` and follow from Stage 1
3. Tell Claude your project goal - it reads `board.yaml` and starts planning

---

## Workflow order

```
plan → split → [Codex executes] → review → replan (if needed)
```

You only need to provide the goal. Claude handles the rest.
