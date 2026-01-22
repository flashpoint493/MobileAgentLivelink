# MobileAgentLivelink

A cross-platform application that enables mobile devices to remotely control PC Agent IDEs (Cursor, CodeBuddy, OpenCode). Send development requests from your phone and trigger Vibe Development workflows on your PC.

## 🎯 Core Value

- **Anytime, Anywhere**: Send development requests to your PC IDE from your mobile device
- **Remote Monitoring**: View development progress and AI conversations in real-time
- **Lightweight Interaction**: Mobile device acts as a remote control, no local storage required

## 🏗️ Architecture

```
[Android App] <--WebSocket--> [Relay Server] <--WebSocket--> [PC Python Service]
                                                                    |
                                                                    v
                                                           [Cursor/IDE]
```

## 📋 Features

### Current (MVP)
- ✅ WebSocket bidirectional communication
- ✅ Text message transmission
- ✅ PC-side Cursor controller integration
- ✅ Android app with basic UI

### Planned
- [ ] Multi-IDE support (CodeBuddy, OpenCode)
- [ ] Voice input support
- [ ] Development progress visualization
- [ ] Quick command templates
- [ ] Conversation history sync

## 🚀 Quick Start

### Prerequisites

- **PC**: Windows 11, Python 3.10+
- **Mobile**: Android 8.0+ (API 26+)
- **IDE**: Cursor (for MVP)

### PC Client Setup

1. Navigate to the PC client directory:
```bash
cd pc-client
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure settings (optional):
```bash
# Edit config.py to customize relay server URL
```

4. Run the PC client:
```bash
python relay_client.py
```

### Relay Server Setup

1. Navigate to the relay server directory:
```bash
cd relay-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the relay server:
```bash
python server.py
```

**Note**: For production, deploy the relay server to a cloud service (e.g., Tencent CloudBase) for public network access.

### Android App Setup

1. Open the project in Android Studio
2. Sync Gradle dependencies
3. Build and run on your device or emulator

## 📁 Project Structure

```
MobileAgentLivelink/
├── android-app/          # Android application (Kotlin + Jetpack Compose)
├── pc-client/            # PC-side Python service
├── relay-server/         # WebSocket relay server
├── docs/                 # Project documentation
│   ├── CONTEXT.md        # Current project state
│   ├── DECISIONS.md      # Architecture decisions
│   ├── ROADMAP.md        # Development roadmap
│   └── CHANGELOG.md      # Version history
└── CONTRIBUTING_AI.md    # AI collaboration guidelines
```

## 🛠️ Technology Stack

- **Android**: Kotlin, Jetpack Compose, OkHttp (WebSocket)
- **PC Client**: Python, websockets, pyautogui, pynput
- **Relay Server**: Python, FastAPI, uvicorn, websockets
- **Communication**: WebSocket over cloud relay

## 📝 Development Status

**Current Phase**: Milestone 0.1 - MVP Core Communication

**Progress**:
- [x] Project initialization
- [x] PC-side Python service
- [x] Relay server implementation
- [x] Android app skeleton
- [x] Local communication test (verified)

**Next Steps**:
- [ ] Deploy relay server to public network
- [ ] Android app compilation testing
- [ ] End-to-end public network testing

## 🤝 Contributing

Please read [CONTRIBUTING_AI.md](CONTRIBUTING_AI.md) for collaboration guidelines and development workflow.

## 📄 License

[Add license information here]

## 🙏 Acknowledgments

Built to enable seamless mobile-to-PC development workflows for AI-powered IDEs.

---

For Chinese documentation, see [README_zh.md](README_zh.md).
