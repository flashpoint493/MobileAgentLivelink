# MobileAgentLivelink

一个跨平台应用，支持移动设备远程控制 PC 端的 Agent IDE（Cursor、CodeBuddy、OpenCode）。从手机发送开发需求，在 PC 端触发 Vibe Development 工作流。

## 🎯 核心价值

- **随时发起**: 在移动设备上随时向 PC IDE 发送开发需求
- **远程监控**: 实时查看开发进度和 AI 对话
- **轻量交互**: 移动设备仅作为遥控器，无需本地存储

## 🏗️ 架构设计

```
[Web客户端] <--WebSocket--> [中转服务器] <--WebSocket--> [PC Python服务]
                                                                    |
                                                                    v
                                                           [Cursor/IDE]
```

## 📋 功能特性

### 当前功能 (MVP)
- ✅ WebSocket 双向通信
- ✅ 文本消息传输
- ✅ PC 端 Cursor 控制器集成
- ✅ Web客户端（单文件HTML）

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

3. 配置设置（必填）：
```bash
# 设置环境变量（安全要求）：
# AUTH_TOKEN: 配对密钥（必填）- 防止未授权访问
# RELAY_SERVER_URL: 中转服务器地址（默认: ws://localhost:8765/ws）
# DEVICE_ID: 设备标识（默认: default-pc）

# 示例（Windows PowerShell）：
$env:AUTH_TOKEN="your_secret_token_here"
$env:RELAY_SERVER_URL="ws://your-server-ip:8765/ws"
$env:DEVICE_ID="my-pc-001"

# 或在 pc-client/ 目录创建 .env 文件：
# AUTH_TOKEN=your_secret_token_here
# RELAY_SERVER_URL=ws://your-server-ip:8765/ws
# DEVICE_ID=my-pc-001
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

**注意**: 生产环境建议将中转服务器部署到云服务（如腾讯云轻量应用服务器）以实现公网访问。详细部署指南请参考 [部署文档](docs/DEPLOYMENT.md)。

### Web客户端设置

直接在浏览器中打开 `web-client.html` 文件：
```bash
# 双击 web-client.html 或在浏览器中打开
web-client.html
```

配置中转服务器地址并连接。在配对时，需要输入PC端配置的AUTH_TOKEN。

## 📁 项目结构

```
MobileAgentLivelink/
├── web-client.html       # 单文件Web客户端（HTML/CSS/JS）
├── pc-client/            # PC 端 Python 服务
├── relay-server/         # WebSocket 中转服务器
├── docs/                 # 项目文档
│   ├── CONTEXT.md        # 当前项目状态
│   ├── DECISIONS.md      # 架构决策记录
│   ├── ROADMAP.md        # 开发路线图
│   ├── CHANGELOG.md      # 版本历史
│   ├── DEPLOYMENT.md     # 部署指南
│   └── QA_TEST_CASES.md  # 测试用例手册
└── CONTRIBUTING_AI.md    # AI 协作指南
```

## 🛠️ 技术栈

- **Web客户端**: HTML, CSS, JavaScript (WebSocket API)
- **PC 客户端**: Python, websockets, pyautogui, pynput
- **中转服务器**: Python, FastAPI, uvicorn, websockets
- **通信协议**: 基于云中转的 WebSocket

## 📝 开发状态

**当前阶段**: Milestone 0.1 - MVP 核心通信

**进度**:
- [x] 项目初始化
- [x] PC 端 Python 服务
- [x] 中转服务器实现
- [x] Web客户端（单文件HTML）
- [x] 本地通信测试（已验证）
- [x] 安全验证机制（AUTH_TOKEN强制要求）

**下一步**:
- [x] 创建部署文档和脚本
- [x] 部署中转服务器到公网（参考 [部署指南](docs/DEPLOYMENT.md)）
- [ ] 端到端公网测试（参考 [测试用例](docs/QA_TEST_CASES.md)）

## 🤝 贡献指南

请阅读 [CONTRIBUTING_AI.md](CONTRIBUTING_AI.md) 了解协作规范和开发工作流。

## 📄 许可证

[在此添加许可证信息]

## 🙏 致谢

本项目旨在为 AI 驱动的 IDE 提供无缝的移动端到 PC 端开发工作流。

---

For English documentation, see [README.md](README.md).
