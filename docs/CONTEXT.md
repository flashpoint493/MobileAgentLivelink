# MobileAgentLivelink 当前上下文

## 项目概述
移动端远程控制 PC Agent IDE 的跨平台应用。用户可以在手机上向 PC 端的 Cursor 发送开发需求，启动 Vibe Development 流程。

### 核心痛点
1. Agent IDE (Cursor/CodeBuddy/OpenCode) 仅支持桌面端
2. 用户希望随时随地（如通勤、外出）向 IDE 发送开发需求
3. 手机不适合存储开发内容，仅作为"遥控器"使用

### 核心价值
- **随时发起**: 手机上随时向 PC IDE 发送需求
- **远程监控**: 查看开发进度和 AI 对话
- **轻量交互**: 手机端只做指挥，不做存储

## 当前状态
- **阶段**: Milestone 0.1 - MVP 核心通信
- **进度**: PC 端 Cursor 控制器已验证，本地通信链路测试通过
- **下一步**: 部署中转服务到公网 (腾讯云)

## 已确认决策
- ✅ 公网通信（云中转架构）
- ✅ Android (Kotlin) + Windows (Python)
- ✅ WebSocket 双向通信
- ✅ MVP 优先支持 Cursor
- ✅ 云服务商：腾讯云（待采购）

## 已完成事项
- [x] 项目初始化 (vibe-collab)
- [x] PC 端 Python 服务 (`pc-client/`)
- [x] 中转服务器 (`relay-server/`)
- [x] Android App 骨架 (`android-app/`)
- [x] 本地测试通信链路 - 已验证成功

## 待办事项
- [ ] 采购腾讯云服务器 (轻量应用服务器或 CloudBase)
- [ ] 部署 relay-server 到公网
- [ ] 获取公网 WebSocket 地址
- [ ] 修改 PC 端配置连接公网
- [ ] Android App 更新服务器地址并编译
- [ ] 端到端公网测试

## 新设备迁移方案
已在本次对话中确认：
- 新设备 AI 需读取 CONTRIBUTING_AI.md 和 docs/CONTEXT.md
- 按照部署步骤执行中转服务到腾讯云
- 部署后更新配置并完成端到端测试

---
*最后更新: 2026-01-22*
