#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash tools/init.sh /path/to/new/project
  bash /path/to/this/repo/tools/init.sh /path/to/new/project
EOF
}

copy_file() {
  local src="$1"
  local dst="$2"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
}

copy_dir() {
  local src="$1"
  local dst="$2"
  mkdir -p "$dst"
  cp -R "$src"/. "$dst"
}

reset_existing_protocol() {
  local target="$1"

  rm -rf "$target/.ai-collab"
  rm -f "$target/CLAUDE.md"
  rm -f "$target/AGENTS.md"
  rm -f "$target/QUICKSTART.md"
  rm -f "$target/tools/check_consistency.py"
  rm -f "$target/.claude/agents/spec-gardener.md"
  rm -f "$target/.claude/skills/claude-orchestrator/SKILL.md"
  rm -f "$target/.agents/skills/codex-worker/SKILL.md"
}

generate_board() {
  local path="$1"
  local today="$2"

  cat >"$path" <<EOF
# .ai-collab/board.yaml
# Single source of truth for the current plan and all task statuses.
# Claude maintains this file. Codex reads it but does not write to it.

meta:
  last_updated: "$today"
  last_action: "project initialized"
  orchestrator: claude

runtime:
  codex_session_file: "runtime/codex-session.yaml"
  mcp_enabled: false

current_plan:
  id: ""
  goal: ""
  status: "none"

current_milestone:
  id: ""
  goal: ""
  plans: []
  status: "none"
  review_file: ""

current_spec:
  version: "0.1.0"
  file: "spec/SPEC.md"
  last_updated: "$today"

spec_status:
  spec_dirty: false
  replan_required: false
  invalidated_tasks: []
  last_spec_change: ""

tasks: []

suggested_next_for_codex:
  task_id: ""
  reason: "no tasks yet"
EOF
}

generate_spec() {
  local path="$1"
  local today="$2"
  local project_name="$3"

  cat >"$path" <<EOF
# Living Specification: $project_name

**Last updated:** $today
**Status:** Draft
**Version:** 0.1.0

---

## Product intent

> Describe what this project does and why it exists.

---

## Requirements

- **REQ-01:** ...

---

## Open questions

1. ...
EOF
}

generate_decisions() {
  local path="$1"
  local project_name="$2"

  cat >"$path" <<EOF
# Decisions: $project_name

Record important architectural and process decisions here.
EOF
}

generate_changelog() {
  local path="$1"
  local project_name="$2"

  cat >"$path" <<EOF
# Changelog: $project_name

Track specification and protocol changes here.
EOF
}

print_summary() {
  local target="$1"

  cat <<EOF
Created protocol bootstrap in: $target

Copied files:
  - CLAUDE.md
  - AGENTS.md
  - QUICKSTART.md
  - .claude/agents/spec-gardener.md
  - .claude/skills/claude-orchestrator/SKILL.md
  - .agents/skills/codex-worker/SKILL.md
  - tools/check_consistency.py
  - .ai-collab/README.md
  - .ai-collab/templates/

Generated fresh files:
  - .ai-collab/board.yaml
  - .ai-collab/spec/SPEC.md
  - .ai-collab/spec/DECISIONS.md
  - .ai-collab/spec/CHANGELOG.md

Created empty directories:
  - .ai-collab/tasks/
  - .ai-collab/plans/
  - .ai-collab/reviews/
  - .ai-collab/reports/
  - .ai-collab/runtime/
  - .ai-collab/spec/milestones/

Done. Open $target/QUICKSTART.md to get started.
EOF
}

main() {
  if [[ $# -ne 1 ]]; then
    usage
    exit 1
  fi

  local target_input="$1"
  local script_dir
  local repo_root
  local target_dir
  local today
  local project_name

  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  repo_root="$(cd "$script_dir/.." && pwd)"
  mkdir -p "$target_input"
  target_dir="$(cd "$target_input" && pwd)"
  today="$(date +%F)"
  project_name="$(basename "$target_dir")"

  if [[ -d "$target_dir/.ai-collab" ]]; then
    printf 'Warning: %s/.ai-collab already exists and will be overwritten.\n' "$target_dir"
    read -r -p "Continue? [y/N] " confirm
    case "${confirm:-}" in
      y|Y|yes|YES)
        reset_existing_protocol "$target_dir"
        ;;
      *)
        echo "Aborted."
        exit 1
        ;;
    esac
  fi

  copy_file "$repo_root/CLAUDE.md" "$target_dir/CLAUDE.md"
  copy_file "$repo_root/AGENTS.md" "$target_dir/AGENTS.md"
  copy_file "$repo_root/QUICKSTART.md" "$target_dir/QUICKSTART.md"
  copy_file "$repo_root/.claude/agents/spec-gardener.md" "$target_dir/.claude/agents/spec-gardener.md"
  copy_file "$repo_root/.claude/skills/claude-orchestrator/SKILL.md" "$target_dir/.claude/skills/claude-orchestrator/SKILL.md"
  copy_file "$repo_root/.agents/skills/codex-worker/SKILL.md" "$target_dir/.agents/skills/codex-worker/SKILL.md"
  copy_file "$repo_root/tools/check_consistency.py" "$target_dir/tools/check_consistency.py"
  copy_file "$repo_root/.ai-collab/README.md" "$target_dir/.ai-collab/README.md"
  copy_dir "$repo_root/.ai-collab/templates" "$target_dir/.ai-collab/templates"

  mkdir -p "$target_dir/.ai-collab/spec"
  mkdir -p "$target_dir/.ai-collab/tasks"
  mkdir -p "$target_dir/.ai-collab/plans"
  mkdir -p "$target_dir/.ai-collab/reviews"
  mkdir -p "$target_dir/.ai-collab/reports"
  mkdir -p "$target_dir/.ai-collab/runtime"
  mkdir -p "$target_dir/.ai-collab/spec/milestones"

  generate_board "$target_dir/.ai-collab/board.yaml" "$today"
  generate_spec "$target_dir/.ai-collab/spec/SPEC.md" "$today" "$project_name"
  generate_decisions "$target_dir/.ai-collab/spec/DECISIONS.md" "$project_name"
  generate_changelog "$target_dir/.ai-collab/spec/CHANGELOG.md" "$project_name"

  print_summary "$target_dir"
}

main "$@"
