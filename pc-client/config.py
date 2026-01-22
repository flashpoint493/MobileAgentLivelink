"""PC Client 配置"""
import os
from dotenv import load_dotenv

load_dotenv()

# 云中转服务器配置
# 从环境变量读取，或使用本地测试地址
# 生产环境请设置环境变量: RELAY_SERVER_URL=ws://<你的服务器IP>:8765/ws
RELAY_SERVER_URL = os.getenv("RELAY_SERVER_URL", "ws://localhost:8765/ws")
DEVICE_ID = os.getenv("DEVICE_ID", "default-pc")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")

# Cursor 窗口配置
CURSOR_WINDOW_TITLE = "Cursor"
INPUT_DELAY = 0.05  # 模拟输入延迟(秒)
