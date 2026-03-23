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

## 6. First-time setup (for new users)

### Prerequisites

You need three things installed before starting:

| Tool | Check if installed | Install link |
|---|---|---|
| Node.js 18+ | `node --version` | https://nodejs.org (download LTS) |
| Git | `git --version` | https://git-scm.com/downloads |
| Claude Code | `claude --version` | https://claude.ai/code |

Open a terminal (on Windows: search "Git Bash" or "PowerShell") and run the check commands above. If any show an error, install that tool first.

---

### Step 1: Get this repository

```bash
# Pick a folder where you want to keep this tool, then run:
git clone https://github.com/YiNi-X/multi_agent_test.git
cd multi_agent_test
```

This downloads the protocol files to your computer. You only need to do this once.

---

### Step 2: Install Codex CLI

```bash
npm install -g @openai/codex
```

Verify it worked:
```bash
codex --version
```

You should see a version number like `0.116.0`.

---

### Step 3: Configure your API key

Codex needs an OpenAI API key (or compatible provider key) to run.

**On Windows (Git Bash):**
```bash
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**On Mac/Linux:**
```bash
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

Replace `your-key-here` with your actual API key.

---

### Step 4: Configure Claude Code permissions

Create or edit the file `C:/Users/YourName/.claude/settings.json` (Windows) or `~/.claude/settings.json` (Mac/Linux).

Add these lines (if the file already exists, add only the `permissions` block inside the existing `{}`:

```json
{
  "permissions": {
    "allow": [
      "Bash(codex exec:*)",
      "Bash(python tools/check_consistency.py)"
    ]
  }
}
```

---

### Step 5: Initialize the protocol in your project

```bash
# Replace /path/to/your/project with your actual project folder path
# Example on Windows: /c/Users/YourName/Documents/my-project
bash /path/to/multi_agent_test/tools/init.sh /path/to/your/project
```

This copies all the protocol files into your project and creates a blank `board.yaml` and `SPEC.md`.

---

### Step 6: Verify everything works

```bash
cd /path/to/your/project
python tools/check_consistency.py
```

You should see: `0 FAIL, 0 WARN`

---

### Step 7: Start working

1. Open your project folder in Claude Code
2. Claude will read `CLAUDE.md` automatically
3. Tell Claude what you want to build — it handles the rest

**Example first message to Claude:**
> "I want to build a todo app with React. Please read the board and start planning."

---

## Workflow order

```
plan → split → [Codex executes] → review → replan (if needed)
```

You only need to provide the goal. Claude handles the rest.
