# MobileAgentLivelink 变更日志

## [0.1.6] - 2026-01-23

### Added
- PC 客户端启动指南 (`pc-client/启动指南.md`)
  - 详细的依赖安装步骤（包括国内镜像源配置）
  - 配置说明和环境变量设置
  - 启动步骤和故障排查指南

### Documentation
- 添加 PC 客户端中文启动指南，帮助用户快速上手

---

## [0.1.5] - 2026-01-23

### Added
- 配对密钥校验（PC 注册携带 AUTH_TOKEN，Web 配对需输入）
- Web 上下文请求与回传（默认 docs/CONTEXT.md）
- 新对话入口（清空 Cursor 对话）
- 任务开始/完成保底通知
- PC 状态回传包含工程目录
- Web 端连接配置与聊天历史持久化

### Changed
- Web 增强：新增状态/上下文/新对话操作区
- PC 端支持上下文读取与状态扩展

### Documentation
- 更新部署文档，补充中转服务器应用更新流程

---

## [0.1.4] - 2026-01-22


### Changed
- **废弃Android App方案**，改用Web客户端作为唯一客户端
- 删除 `android-app/` 目录及所有Android相关代码
- 更新项目架构图，移除Android引用
- PC端配置改为支持环境变量（不持久化真实IP地址）

### Documentation
- 更新 README.md：移除Android相关内容，添加Web客户端设置说明
- 更新 PRD.md：标记REQ-001为已取消，REQ-002为进行中
- 更新 docs/ROADMAP.md：更新Milestone 0.1状态
- 更新 docs/DECISIONS.md：添加决策A-003（废弃Android）
- 更新 docs/QA_TEST_CASES.md：删除Android测试用例（TC-COMM-002, TC-COMM-003）
- 更新 docs/CONTEXT.md：记录重要变更和当前状态
- 更新技术栈：移除Android，添加Web客户端技术栈

### Decisions
- [A-003] 废弃Android App方案，采用Web客户端作为唯一客户端

### Security
- PC端配置改为通过环境变量读取服务器地址，避免在`.env`文件中持久化真实IP

---

## [0.1.3] - 2026-01-22

### Added
- **Web客户端** (`web-client.html`)
  - 单文件HTML，零依赖，无需构建
  - 支持连接云中转服务器
  - 实时PC列表显示和配对功能
  - 聊天界面发送开发需求
  - 消息确认和状态显示
  - 响应式设计，支持桌面/平板/手机

### Changed
- 项目客户端策略：优先使用Web客户端替代Android App
- Web客户端作为完整载体，支持所有基础功能

### Documentation
- 更新 PRD.md，记录REQ-002 Web客户端需求
- 更新 docs/DECISIONS.md，记录A-002 Web客户端技术选型
- 更新 docs/QA_TEST_CASES.md，添加Web客户端测试用例（TC-WEB-001 至 TC-WEB-005）
- 更新 docs/CONTEXT.md，更新项目概述和当前状态

### Decisions
- [A-002] 确认Web客户端技术选型：单文件HTML（零依赖，易分发）

---

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
