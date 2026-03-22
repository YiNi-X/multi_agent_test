# Milestone Review: Claude+Codex CLI Collaboration Protocol Bootstrap

<!-- File: spec/milestones/milestone-001-protocol-bootstrap-2026-03-22.md -->
<!-- Author: claude (orchestrator) -->

---

## Metadata

| Field | Value |
|---|---|
| Milestone ID | `milestone-001` |
| Date | 2026-03-22 |
| Plans included | `plan-001`, `plan-002`, `plan-003` |
| Spec version at start | `v0.1.0` |
| Spec version at end | `v0.4.0` |

---

## Delivered capabilities

从用户视角，本里程碑结束后系统能做到：

- **自然语言启动工作流**：用户描述目标，Claude 自动读取 board.yaml、写计划、分解任务，无需手动编写任何协议文件（REQ-01）
- **Codex CLI 执行任务**：用户运行 `codex` 或 `codex exec`，Codex 读取任务文件、执行、写执行日志，Claude review 结果并更新 board.yaml
- **会话接续**：用户运行 `codex resume <session-id>` 接续上次 Codex 对话，本地 session 永不过期（REQ-03 的升级版）
- **上下文重置恢复**：Claude 对话重置后说"restore state"，Claude 读取 board.yaml + codex-handoff.md，一条命令恢复全部工作状态（REQ-02）
- **Codex session 过期保护**：Codex CLI 本地 session 不过期，无需 canary probe 机制；迁移前的 MCP session 过期由 canary probe 检测并通知用户（REQ-03）
- **文档主导开发流程**：7 个阶段（发散→PRD→Plan→实现→测试→人工Review→PR），偏差时先改文档再改代码（REQ-04、REQ-07）
- **自动一致性检查**：`python tools/check_consistency.py` 检查 session_id、last_task_id、spec 版本、任务状态、spec_dirty 共 5 项（REQ-09）
- **Plan 级别 verdict**：每个 Plan 完成后有明确的 PASS/REWORK/BACK TO PRD 三选一判定，不再是隐式的「所有任务 done 就结束」（REQ-07）
- **PR 工作流**：CLAUDE.md 规定 Plan 完成后必须 commit + PR，里程碑完成后写里程碑 review（REQ-08）
- **需求可追溯性**：SPEC.md 包含 REQ-01~10，plan 和 task 可引用 REQ-ID（REQ-06）
- **里程碑 review**：milestone-template.md 定义了里程碑级别的 review 格式，包含 requirements coverage 表格（REQ-10）
- **Codex 权限边界**：AGENTS.md 明确禁止 Codex 修改 board.yaml、codex-session.yaml、spec/ 目录，Codex 在本里程碑中多次正确自我阻断
- **spec_dirty 联锁**：SPEC.md 变更时 Claude 设置 spec_dirty，禁止在 spec_dirty 且有 in_progress 任务时调用 Codex（REQ-05）

---

## Requirements coverage

| REQ-ID | Requirement | Status | Evidence |
|---|---|---|---|
| REQ-01 | 用户描述目标后无需手动写协议文件即可得到任务计划 | covered | plan-002/003 全程验证；CLAUDE.md orchestrator 角色规则 |
| REQ-02 | 对话重置后单命令恢复工作上下文 | covered | codex-handoff.md YAML front-matter + QUICKSTART.md Section 2 |
| REQ-03 | Codex session 过期时用户收到通知和确认提示 | covered (upgraded) | CLI 模式下 session 永不过期；MCP 时代由 canary probe 实现，已迁移到 CLI |
| REQ-04 | 每个任务有客观可验证的验收标准 | covered | task-template.md 强制 acceptance_criteria 字段；task-019~025 全部有验收标准 |
| REQ-05 | spec_dirty 时阻止 Codex 调用 | covered | CLAUDE.md spec change rules；board.yaml spec_status.spec_dirty 字段 |
| REQ-06 | 每个任务引用所属 plan | partial | board.yaml 中 tasks 列表关联 plan，但任务文件本身没有显式 plan_id 字段 |
| REQ-07 | 每个 plan 有 plan 级别验收标准，与任务级别分开 | covered | plan-template.md Plan review verdict 节；review-template.md Plan-level verdict 节 |
| REQ-08 | 每个 plan 完成后 commit + PR | covered | CLAUDE.md PR workflow rules；plan-002/003 已 commit + push |
| REQ-09 | 跨文件一致性可由自动脚本验证 | covered | tools/check_consistency.py — 5 项检查，0 FAIL，0 WARN |
| REQ-10 | 里程碑完成后产出里程碑级别 review 文档 | covered | 本文档即为 milestone-001 review |

---

## What was NOT delivered

- **REQ-06 部分缺失**：任务文件内部没有显式的 `plan_id` 字段，只能通过 board.yaml 追溯任务所属 plan。这是有意的设计简化（避免字段冗余），但严格来说 REQ-06 是 partial 而非 fully covered。计划在 plan-004 评估是否补充。
- **task-001~004 无正式执行日志**：这四个任务在协议建立之前执行，执行日志为事后补写的历史摘要，不是真实的 Codex 执行记录。
- **milestone PR**：本里程碑没有单独的 milestone-level PR，变更通过两个普通 commit 推送。CLAUDE.md 规定里程碑完成后写里程碑 review（本文档），但未要求必须有独立 PR。
- **SPEC.md 版本变更的 DECISIONS.md 条目**：D014（CLI over MCP）在 CHANGELOG.md 中有记录，但尚未在 DECISIONS.md 中补充正式决策条目。

---

## Quality observations

- **Codex 权限自律表现优秀**：本里程碑中 Codex 共 4 次正确自我阻断（task-019 修改 spec/、task-023/024 依赖未满足、task-025 修改 codex-session.yaml），每次都记录了清晰的阻断原因和建议下一步，完全符合 AGENTS.md 的规定。
- **check_consistency.py 发现了真实 bug**：脚本在首次运行时检测到 `last_task_id` 不一致（session 018 vs handoff 022）和 20 个任务文件状态误报（Check 4 逻辑错误），两个问题都在本里程碑内修复。脚本的价值在第一次运行就得到了验证。
- **MCP→CLI 迁移决策正确**：MCP Server session 在对话期间发生了一次平台级过期，证实了「MCP session 不可靠」的判断。CLI 模式在后续执行中无任何 session 问题。
- **协议文件增殖在可控范围内**：`.ai-collab/` 目录从 4 个文件增长到 60+ 个文件，但目录结构清晰，每个文件职责明确。未发现文档漂移（除 handoff.md 叙述体滞后约半天，已在 P0 修复）。
- **spec_dirty 机制在本里程碑中被动验证**：SPEC.md 经历了 v0.1.0→0.4.0 的 4 次版本变更，每次 Claude 都正确设置/清除 spec_dirty，未出现协议违规。

---

## Verdict

- [x] **ACCEPTED** — milestone complete. Update `board.yaml > current_milestone`. Proceed to next milestone planning.

所有 10 个需求均达到 covered 或 partial（REQ-06），核心能力全部交付，一致性检查全绿，MCP 遗留问题已清理。

---

## Next milestone proposal

milestone-002 建议聚焦于**协议稳定性与实际项目验证**。milestone-001 建立了协议框架，但所有任务都是协议本身的自我改进；milestone-002 应该用这套协议去管理一个真实的外部项目（非协议文件），验证端到端流程在实际开发场景中的可靠性。具体方向：(1) 选择一个真实的小型开发任务（如给这个仓库添加一个实际功能），完整走一遍 7 阶段流程；(2) 补齐 REQ-06（任务文件加 plan_id 字段）；(3) 在 DECISIONS.md 补充 D014（CLI over MCP 决策记录）；(4) 评估是否需要给 board.yaml 加 milestone 级别的任务聚合视图。
