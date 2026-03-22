# Report: task-028-init-script

## What was done

Implemented `tools/init.sh` as a bootstrap script for new projects using this collaboration protocol.

The script:
- copies the protocol core files (`CLAUDE.md`, `AGENTS.md`, `QUICKSTART.md`, `spec-gardener`, `claude-orchestrator`, `codex-worker`, `check_consistency.py`, `.ai-collab/README.md`, and `.ai-collab/templates/`)
- generates a fresh `.ai-collab/board.yaml` with today's date and `tasks: []`
- generates fresh `.ai-collab/spec/SPEC.md`, `DECISIONS.md`, and `CHANGELOG.md`
- creates empty `.ai-collab/tasks`, `plans`, `reviews`, `reports`, `runtime`, and `spec/milestones` directories
- prompts before overwriting an existing `.ai-collab/` target and clears the existing protocol bootstrap only after confirmation
- prints a summary ending with `Done. Open <target>/QUICKSTART.md to get started.`

## Files changed

- `tools/init.sh`
- `.ai-collab/tasks/task-028-init-script.md`
- `.ai-collab/reports/task-028-init-script-2026-03-22.md`

## Validation results

- Passed: `C:\Program Files\Git\bin\bash.exe tools/init.sh .tmp/test-project-028`
  - Result: created `.tmp/test-project-028` with the required copied files, fresh generated board/spec files, empty collaboration directories, and the required final completion message.
- Passed: inspection of `.tmp/test-project-028/.ai-collab/board.yaml`
  - Result: `tasks: []`, `meta.last_updated: "2026-03-22"`, and `current_spec.version: "0.1.0"`.
- Passed: inspection of `.tmp/test-project-028/.ai-collab/spec/SPEC.md`
  - Result: fresh starter spec with `**Last updated:** 2026-03-22` and `**Version:** 0.1.0`.
- Passed: presence/absence checks in `.tmp/test-project-028`
  - Result: required bootstrap files exist; excluded project-specific artifacts do not exist (`mini.py`, `mini.png`, `codex_probe.txt`, `CODEX_CANARY.md`, copied task/report history, `.ai-collab/runtime/codex-session.yaml`, `.git`); required `.ai-collab` work directories exist and are empty.
- Passed: `rg -n "already exists and will be overwritten|Continue\\? \\[y/N\\]" tools/init.sh`
  - Result: overwrite warning and confirmation prompt are present in the script.
- Passed: `python tools/check_consistency.py`
  - Result: `0 FAIL, 0 WARN, 5 PASS, 1 SKIP`.

## Blockers or issues

- The default `bash` command in this Windows sandbox maps to `C:\Windows\System32\bash.exe` and failed with `Bash/Service/CreateInstance/E_ACCESSDENIED`.
- End-to-end validation therefore used explicit Git Bash at `C:\Program Files\Git\bin\bash.exe`, which succeeded.

## Suggested next step

- Claude can review task `028` against the validation evidence and, if accepted, update `board.yaml` before proceeding to task `029`.
