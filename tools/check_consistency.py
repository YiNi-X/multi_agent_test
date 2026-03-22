from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
COLLAB_DIR = ROOT / ".ai-collab"


@dataclass
class CheckResult:
    level: str
    message: str
    details: list[str] = field(default_factory=list)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None


def strip_inline_comment(value: str) -> str:
    result: list[str] = []
    quote: str | None = None
    escaped = False

    for char in value:
        if escaped:
            result.append(char)
            escaped = False
            continue
        if char == "\\" and quote is not None:
            result.append(char)
            escaped = True
            continue
        if char in {"'", '"'}:
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
            result.append(char)
            continue
        if char == "#" and quote is None:
            break
        result.append(char)

    return "".join(result).rstrip()


def parse_scalar(raw_value: str):
    value = strip_inline_comment(raw_value).strip()
    if not value:
        return ""

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False

    if (
        (value.startswith('"') and value.endswith('"'))
        or (value.startswith("'") and value.endswith("'"))
    ):
        return value[1:-1]

    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]

    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            return value

    return value


def parse_indented_block(text: str, block_name: str) -> dict[str, object]:
    pattern = re.compile(
        rf"(?ms)^{re.escape(block_name)}:\s*\n((?:^[ ]{{2,}}.*(?:\n|$))*)"
    )
    match = pattern.search(text)
    if not match:
        return {}

    data: dict[str, object] = {}
    for line in match.group(1).splitlines():
        cleaned = strip_inline_comment(line)
        if not cleaned.strip():
            continue
        entry = re.match(r"^\s{2}([A-Za-z0-9_]+):\s*(.*?)\s*$", cleaned)
        if not entry:
            continue
        data[entry.group(1)] = parse_scalar(entry.group(2))
    return data


def parse_front_matter(text: str) -> tuple[dict[str, object], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing YAML front-matter"

    data: dict[str, object] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data, None
        cleaned = strip_inline_comment(line)
        if not cleaned.strip():
            continue
        if cleaned.lstrip().startswith("#"):
            continue
        if ":" not in cleaned:
            continue
        key, value = cleaned.split(":", 1)
        data[key.strip()] = parse_scalar(value)

    return {}, "unterminated YAML front-matter"


def parse_board_tasks(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    in_tasks = False
    current: dict[str, object] | None = None
    tasks: list[dict[str, object]] = []

    for line in lines:
        if not in_tasks:
            if line.strip() == "tasks:":
                in_tasks = True
            continue

        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s*$", line):
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        task_start = re.match(r"^  - id:\s*(.*?)\s*$", line)
        if task_start:
            if current is not None:
                tasks.append(current)
            current = {"id": parse_scalar(task_start.group(1))}
            continue

        if current is None:
            continue

        item = re.match(r"^    ([A-Za-z0-9_]+):\s*(.*?)\s*$", line)
        if item:
            current[item.group(1)] = parse_scalar(item.group(2))

    if current is not None:
        tasks.append(current)
    return tasks


def extract_task_status(text: str) -> str | None:
    match = re.search(r"(?ms)^## Status\s*\n(.*?)(?=^## |\Z)", text)
    if not match:
        return None

    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("`") and stripped.endswith("`") and len(stripped) >= 2:
            stripped = stripped[1:-1]
        return stripped
    return None


def resolve_collab_relative(path_value: str) -> Path:
    relative_path = Path(path_value)
    root_candidate = ROOT / relative_path
    if root_candidate.exists():
        return root_candidate
    return COLLAB_DIR / relative_path


def relative_display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def main() -> int:
    results: list[CheckResult] = []

    board_path = COLLAB_DIR / "board.yaml"
    session_path = COLLAB_DIR / "runtime" / "codex-session.yaml"
    handoff_path = COLLAB_DIR / "runtime" / "codex-handoff.md"

    board_text = read_text(board_path)
    session_text = read_text(session_path)
    handoff_text = read_text(handoff_path)

    board_data = parse_indented_block(board_text, "current_spec") if board_text else {}
    spec_status_data = parse_indented_block(board_text, "spec_status") if board_text else {}
    board_tasks = parse_board_tasks(board_text) if board_text else []
    session_data = parse_indented_block(session_text, "codex_session") if session_text else {}
    handoff_data, handoff_error = parse_front_matter(handoff_text) if handoff_text else ({}, None)

    if session_text is None:
        results.append(
            CheckResult(
                "SKIP",
                f"session_id: missing {relative_display(session_path)}",
            )
        )
    elif handoff_text is None:
        results.append(
            CheckResult(
                "SKIP",
                f"session_id: missing {relative_display(handoff_path)}",
            )
        )
    elif handoff_error:
        results.append(CheckResult("FAIL", f"session_id: {handoff_error} in {relative_display(handoff_path)}"))
    else:
        session_id = session_data.get("last_session_id")
        handoff_id = handoff_data.get("last_session_id")
        if not session_id and not handoff_id:
            results.append(CheckResult("SKIP", "session_id: no last_session_id recorded yet (CLI mode, first run)"))
        elif not session_id or not handoff_id:
            results.append(
                CheckResult(
                    "WARN",
                    "session_id: last_session_id missing in one file",
                    [
                        f"codex-session.yaml: {session_id or '(missing)'}",
                        f"handoff.md: {handoff_id or '(missing)'}",
                    ],
                )
            )
        elif str(session_id) == str(handoff_id):
            results.append(
                CheckResult(
                    "PASS",
                    f"session_id: {session_id} matches in both files",
                )
            )
        else:
            results.append(
                CheckResult(
                    "FAIL",
                    f"session_id: codex-session.yaml={session_id}, handoff.md={handoff_id}",
                )
            )

    if session_text is None:
        results.append(
            CheckResult(
                "SKIP",
                f"last_task_id: missing {relative_display(session_path)}",
            )
        )
    elif handoff_text is None:
        results.append(
            CheckResult(
                "SKIP",
                f"last_task_id: missing {relative_display(handoff_path)}",
            )
        )
    elif handoff_error:
        results.append(CheckResult("FAIL", f"last_task_id: {handoff_error} in {relative_display(handoff_path)}"))
    else:
        session_task = session_data.get("last_task_id")
        handoff_task = handoff_data.get("last_task_id")
        if session_task in {None, ""} or handoff_task in {None, ""}:
            results.append(
                CheckResult(
                    "FAIL",
                    "last_task_id: missing field in codex-session.yaml or codex-handoff.md front-matter",
                )
            )
        elif str(session_task) == str(handoff_task):
            results.append(
                CheckResult(
                    "PASS",
                    f"last_task_id: {session_task} matches in both files",
                )
            )
        else:
            results.append(
                CheckResult(
                    "FAIL",
                    f"last_task_id: codex-session.yaml={session_task}, handoff.md={handoff_task}",
                )
            )

    if board_text is None:
        results.append(CheckResult("SKIP", f"spec version: missing {relative_display(board_path)}"))
    else:
        board_spec_version = board_data.get("version")
        spec_rel_path = str(board_data.get("file") or "spec/SPEC.md")
        spec_path = resolve_collab_relative(spec_rel_path)
        spec_text = read_text(spec_path)

        if spec_text is None:
            results.append(CheckResult("SKIP", f"spec version: missing {relative_display(spec_path)}"))
        else:
            spec_match = re.search(r"^\*\*Version:\*\*\s*([^\s]+)\s*$", spec_text, re.MULTILINE)
            spec_version = spec_match.group(1) if spec_match else None
            if not board_spec_version or not spec_version:
                results.append(
                    CheckResult(
                        "FAIL",
                        "spec version: missing current_spec.version in board.yaml or **Version:** line in SPEC.md",
                    )
                )
            elif str(board_spec_version) == str(spec_version):
                results.append(
                    CheckResult(
                        "PASS",
                        f"spec version: board.yaml={board_spec_version} matches SPEC.md={spec_version}",
                    )
                )
            else:
                results.append(
                    CheckResult(
                        "FAIL",
                        f"spec version: board.yaml={board_spec_version}, SPEC.md={spec_version}",
                    )
                )

            if session_text is None:
                results.append(
                    CheckResult(
                        "SKIP",
                        f"spec version: missing {relative_display(session_path)} for session-start comparison",
                    )
                )
            else:
                # CLI mode: spec_version_at_start is not tracked per-session
                # Only check if the field exists (MCP legacy); skip gracefully if absent
                session_version = session_data.get("spec_version_at_start")
                if session_version in {None, ""}:
                    results.append(
                        CheckResult(
                            "SKIP",
                            "spec version: spec_version_at_start not present (CLI mode — field not required)",
                        )
                    )
                elif board_spec_version and str(session_version) != str(board_spec_version):
                    results.append(
                        CheckResult(
                            "WARN",
                            f"spec version: session started at {session_version}, current is {board_spec_version}",
                        )
                    )

    if board_text is None:
        results.append(CheckResult("SKIP", f"task status: missing {relative_display(board_path)}"))
    elif not board_tasks:
        results.append(CheckResult("SKIP", "task status: no task entries found in board.yaml"))
    else:
        missing_files: list[str] = []
        missing_logs: list[str] = []

        for task in board_tasks:
            task_file = task.get("file")
            expected_status = task.get("status")
            task_id = task.get("id")

            if not task_file or expected_status in {None, ""}:
                missing_files.append(f"task-{task_id}: missing file or status in board.yaml")
                continue

            task_path = resolve_collab_relative(str(task_file))
            task_text = read_text(task_path)
            if task_text is None:
                missing_files.append(f"task-{task_id}: missing {relative_display(task_path)}")
                continue

            # board.yaml is authoritative for status.
            # Task files record initial status at definition time and are not updated by Codex.
            # We only verify that done/review tasks have a Codex execution log (evidence of work).
            if expected_status in {"done", "review"}:
                if "## Codex execution log" not in task_text and "## codex execution log" not in task_text.lower():
                    missing_logs.append(
                        f"task-{task_id}: status={expected_status} in board.yaml but no execution log in {relative_display(task_path)}"
                    )

        if missing_files:
            results.append(
                CheckResult(
                    "FAIL",
                    f"task status: {len(missing_files)} missing task files",
                    missing_files,
                )
            )
        elif missing_logs:
            results.append(
                CheckResult(
                    "WARN",
                    f"task status: {len(missing_logs)} done/review tasks missing execution log",
                    missing_logs,
                )
            )
        else:
            results.append(CheckResult("PASS", f"task status: all {len(board_tasks)} tasks verified"))

    if board_text is None:
        results.append(CheckResult("SKIP", f"spec_dirty: missing {relative_display(board_path)}"))
    else:
        spec_dirty = spec_status_data.get("spec_dirty")
        if spec_dirty in {None, ""}:
            results.append(CheckResult("FAIL", "spec_dirty: missing spec_status.spec_dirty in board.yaml"))
        else:
            in_progress_tasks = [str(task.get("id")) for task in board_tasks if task.get("status") == "in_progress"]
            if spec_dirty is True and in_progress_tasks:
                results.append(
                    CheckResult(
                        "FAIL",
                        f"spec_dirty: true while tasks {', '.join(in_progress_tasks)} are in_progress",
                    )
                )
            elif spec_dirty is True:
                results.append(CheckResult("PASS", "spec_dirty: true, no in_progress tasks blocked"))
            else:
                results.append(CheckResult("PASS", "spec_dirty: false, no in_progress tasks blocked"))

    counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "SKIP": 0}

    print("=== Protocol Consistency Check ===")
    for result in results:
        counts[result.level] += 1
        print(f"[{result.level}] {result.message}")
        for detail in result.details:
            print(f"  - {detail}")

    summary_parts = [
        f"{counts['FAIL']} FAIL",
        f"{counts['WARN']} WARN",
        f"{counts['PASS']} PASS",
    ]
    if counts["SKIP"]:
        summary_parts.append(f"{counts['SKIP']} SKIP")

    print()
    print(f"Result: {', '.join(summary_parts)}")
    print(f"Run time: {date.today().isoformat()}")

    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
