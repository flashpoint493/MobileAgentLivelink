# MobileAgentLivelink

一个跨平台应用，支持移动设备远程控制 PC 端的 Agent IDE（Cursor、CodeBuddy、OpenCode）。从手机发送开发需求，在 PC 端触发 Vibe Development 工作流。

## 🎯 核心价值

- **随时发起**: 在移动设备上随时向 PC IDE 发送开发需求
- **远程监控**: 实时查看开发进度和 AI 对话
- **轻量交互**: 移动设备仅作为遥控器，无需本地存储

## 🏗️ 架构设计

```
[Android App] <--WebSocket--> [中转服务器] <--WebSocket--> [PC Python服务]
                                                                    |
                                                                    v
                                                           [Cursor/IDE]
```

## 📋 功能特性

### 当前功能 (MVP)
- ✅ WebSocket 双向通信
- ✅ 文本消息传输
- ✅ PC 端 Cursor 控制器集成
- ✅ Android 应用基础 UI

### 计划功能
- [ ] 多 IDE 支持（CodeBuddy、OpenCode）
- [ ] 语音输入支持
- [ ] 开发进度可视化
- [ ] 快捷指令模板
- [ ] 对话历史同步

## 🚀 快速开始

### 环境要求

- **PC**: Windows 11, Python 3.10+
- **移动端**: Android 8.0+ (API 26+)
- **IDE**: Cursor（MVP 阶段）

### PC 客户端设置

1. 进入 PC 客户端目录：
```bash
cd pc-client
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置设置（可选）：
```bash
# 编辑 config.py 自定义中转服务器 URL
```

4. 运行 PC 客户端：
```bash
python relay_client.py
```

### 中转服务器设置

1. 进入中转服务器目录：
```bash
cd relay-server
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行中转服务器：
```bash
python server.py
```

**注意**: 生产环境建议将中转服务器部署到云服务（如腾讯云 CloudBase）以实现公网访问。

### Android 应用设置

1. 在 Android Studio 中打开项目
2. 同步 Gradle 依赖
3. 在设备或模拟器上构建并运行

## 📁 项目结构

```
MobileAgentLivelink/
├── android-app/          # Android 应用 (Kotlin + Jetpack Compose)
├── pc-client/            # PC 端 Python 服务
├── relay-server/         # WebSocket 中转服务器
├── docs/                 # 项目文档
│   ├── CONTEXT.md        # 当前项目状态
│   ├── DECISIONS.md      # 架构决策记录
│   ├── ROADMAP.md        # 开发路线图
│   └── CHANGELOG.md      # 版本历史
└── CONTRIBUTING_AI.md    # AI 协作指南
```

## 🛠️ 技术栈

- **Android**: Kotlin, Jetpack Compose, OkHttp (WebSocket)
- **PC 客户端**: Python, websockets, pyautogui, pynput
- **中转服务器**: Python, FastAPI, uvicorn, websockets
- **通信协议**: 基于云中转的 WebSocket

## 📝 开发状态

**当前阶段**: Milestone 0.1 - MVP 核心通信

**进度**:
- [x] 项目初始化
- [x] PC 端 Python 服务
- [x] 中转服务器实现
- [x] Android 应用骨架
- [x] 本地通信测试（已验证）

**下一步**:
- [ ] 部署中转服务器到公网
- [ ] Android 应用编译测试
- [ ] 端到端公网测试

## 🤝 贡献指南

请阅读 [CONTRIBUTING_AI.md](CONTRIBUTING_AI.md) 了解协作规范和开发工作流。

## 📄 许可证

[在此添加许可证信息]

## 🙏 致谢

本项目旨在为 AI 驱动的 IDE 提供无缝的移动端到 PC 端开发工作流。

---

For English documentation, see [README.md](README.md).
