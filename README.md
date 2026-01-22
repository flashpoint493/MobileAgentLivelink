# MobileAgentLivelink

A cross-platform application that enables mobile devices to remotely control PC Agent IDEs (Cursor, CodeBuddy, OpenCode). Send development requests from your phone and trigger Vibe Development workflows on your PC.

## 🎯 Core Value

- **Anytime, Anywhere**: Send development requests to your PC IDE from your mobile device
- **Remote Monitoring**: View development progress and AI conversations in real-time
- **Lightweight Interaction**: Mobile device acts as a remote control, no local storage required

## 🏗️ Architecture

```
[Web Client] <--WebSocket--> [Relay Server] <--WebSocket--> [PC Python Service]
                                                                    |
                                                                    v
                                                           [Cursor/IDE]
```

## 📋 Features

### Current (MVP)
- ✅ WebSocket bidirectional communication
- ✅ Text message transmission
- ✅ PC-side Cursor controller integration
- ✅ Web client (single HTML file)

### Planned
- [ ] Multi-IDE support (CodeBuddy, OpenCode)
- [ ] Voice input support
- [ ] Development progress visualization
- [ ] Quick command templates
- [ ] Conversation history sync

## 🚀 Quick Start

### Prerequisites

- **PC**: Windows 11, Python 3.10+
- **Browser**: Modern browser with WebSocket support (Chrome, Firefox, Edge, Safari)
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

3. Configure settings:
```bash
# Set environment variables (required for security):
# AUTH_TOKEN: Pairing token (required) - prevents unauthorized access
# RELAY_SERVER_URL: Relay server URL (default: ws://localhost:8765/ws)
# DEVICE_ID: Device identifier (default: default-pc)

# Example (Windows PowerShell):
$env:AUTH_TOKEN="your_secret_token_here"
$env:RELAY_SERVER_URL="ws://your-server-ip:8765/ws"
$env:DEVICE_ID="my-pc-001"

# Or create a .env file in pc-client/ directory:
# AUTH_TOKEN=your_secret_token_here
# RELAY_SERVER_URL=ws://your-server-ip:8765/ws
# DEVICE_ID=my-pc-001
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

**Note**: For production, deploy the relay server to a cloud service (e.g., Tencent Cloud Lighthouse) for public network access. See [Deployment Guide](docs/DEPLOYMENT.md) for details.

### Web Client Setup

Simply open `web-client.html` in your web browser:
```bash
# Double-click web-client.html or open in browser
web-client.html
```

Configure relay server URL and connect.

## 📁 Project Structure

```
MobileAgentLivelink/
├── web-client.html       # Single-file web client (HTML/CSS/JS)
├── pc-client/            # PC-side Python service
├── relay-server/         # WebSocket relay server
├── docs/                # Project documentation
│   ├── CONTEXT.md       # Current project state
│   ├── DECISIONS.md     # Architecture decisions
│   ├── ROADMAP.md       # Development roadmap
│   ├── CHANGELOG.md     # Version history
│   ├── DEPLOYMENT.md    # Deployment guide
│   └── QA_TEST_CASES.md # Test cases
└── CONTRIBUTING_AI.md    # AI collaboration guidelines
```

## 🛠️ Technology Stack

- **Web Client**: HTML, CSS, JavaScript (WebSocket API)
- **PC Client**: Python, websockets, pyautogui, pynput
- **Relay Server**: Python, FastAPI, uvicorn, websockets
- **Communication**: WebSocket over cloud relay

## 📝 Development Status

**Current Phase**: Milestone 0.1 - MVP Core Communication

**Progress**:
- [x] Project initialization
- [x] PC-side Python service
- [x] Relay server implementation
- [x] Web client (single HTML file)
- [x] Local communication test (verified)

**Next Steps**:
- [x] Create deployment documentation and scripts
- [x] Web client local testing
- [ ] End-to-end public network testing (see [Test Cases](docs/QA_TEST_CASES.md))

## 🤝 Contributing

Please read [CONTRIBUTING_AI.md](CONTRIBUTING_AI.md) for collaboration guidelines and development workflow.

## 📄 License

[Add license information here]

## 🙏 Acknowledgments

Built to enable seamless mobile-to-PC development workflows for AI-powered IDEs.

---

For Chinese documentation, see [README_zh.md](README_zh.md).
