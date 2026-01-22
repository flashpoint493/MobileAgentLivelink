# MobileAgentLivelink 变更日志

## [0.1.2] - 2026-01-22

### Added
- 创建部署文档 (`docs/DEPLOYMENT.md`)
  - 详细的腾讯云部署步骤
  - 服务器环境准备指南
  - systemd 服务配置
  - 故障排查指南
- 创建自动化部署脚本 (`relay-server/deploy.sh`)
  - 一键部署脚本
  - 自动配置 systemd 服务
  - 部署验证功能
- 完善 QA 测试用例 (`docs/QA_TEST_CASES.md`)
  - 部署相关测试用例
  - 端到端通信测试用例
  - 可靠性测试用例

### Documentation
- 更新 README.md 和 README_zh.md，添加部署文档链接
- 更新项目结构说明，包含新增文档
- 更新开发状态，标记部署准备工作完成

---

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
