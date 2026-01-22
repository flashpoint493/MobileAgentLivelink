# MobileAgentLivelink 变更日志

## [0.1.1] - 2026-01-22

### Planned
- 确认腾讯云为云服务供应商
- 确定新设备迁移方案和工作流程
- 明确公网部署步骤和验收标准

### Documentation
- 更新 docs/CONTEXT.md 记录当前规划和待办事项
- 更新 CHANGELOG.md 记录本次对话产出

---

## [0.1.0] - 2026-01-22

### Added
- 项目初始化 (vibe-collab 协作框架)
- PC 端 Python 客户端 (`pc-client/`)
  - Cursor 窗口控制器 (pyautogui + ctypes)
  - WebSocket 中转客户端
- 中转服务器 (`relay-server/`)
  - FastAPI + WebSocket
  - 设备注册、配对、消息转发
- Android App 骨架 (`android-app/`)
  - Kotlin + Jetpack Compose
  - Material 3 UI
  - WebSocket 客户端
- 本地测试脚本 (`test_auto.py`)

### Fixed
- 修复 Cursor 窗口激活问题（管理员权限兼容）

### Verified
- ✅ PC 端 Cursor 控制器本地测试通过
- ✅ 消息发送到 Cursor 对话面板成功

### Decisions
- [S-001] 确认公网通信架构
- [S-002] 确认目标平台 Android + Windows
- [S-003] MVP 优先支持 Cursor

---
