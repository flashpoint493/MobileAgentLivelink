"""PC Client 配置"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 云中转服务器配置
# 从环境变量读取，或使用本地测试地址
# 生产环境请设置环境变量: RELAY_SERVER_URL=ws://<你的服务器IP>:8765/ws
RELAY_SERVER_URL = os.getenv("RELAY_SERVER_URL", "ws://localhost:8765/ws")
DEVICE_ID = os.getenv("DEVICE_ID", "default-pc")
# AUTH_TOKEN: 配对密钥，必填！用于安全配对，防止未授权访问
# 设置方式: 环境变量 AUTH_TOKEN=your_secret_token
# 警告: 未配置AUTH_TOKEN将导致无法配对
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")

# 项目根目录（用于读取上下文文件）
PROJECT_ROOT = os.getenv("PROJECT_ROOT", str(Path(__file__).resolve().parent.parent))

# Cursor 窗口配置
CURSOR_WINDOW_TITLE = "Cursor"
INPUT_DELAY = 0.05  # 模拟输入延迟(秒)

# New Chat 命令（通过命令面板触发）
NEW_CHAT_COMMAND = os.getenv("NEW_CHAT_COMMAND", "New Chat")

# 任务完成保底通知超时（秒）
TASK_DONE_TIMEOUT = float(os.getenv("TASK_DONE_TIMEOUT", "45"))

