"""WebSocket 中转服务客户端"""
import asyncio
import json
from websockets import connect, ConnectionClosed
from config import RELAY_SERVER_URL, DEVICE_ID, AUTH_TOKEN
from cursor_controller import CursorController


class RelayClient:
    """连接云中转服务，接收手机端指令"""
    
    def __init__(self):
        self.cursor = CursorController()
        self.ws = None
        self.running = False
    
    async def connect(self):
        """连接到中转服务器"""
        print(f"[INFO] 正在连接: {RELAY_SERVER_URL}")
        
        try:
            self.ws = await connect(RELAY_SERVER_URL)
            self.running = True
            
            # 注册设备
            await self.send({
                "type": "register",
                "device_id": DEVICE_ID,
                "device_type": "pc",
                "token": AUTH_TOKEN
            })
            
            print(f"[INFO] 已连接，设备ID: {DEVICE_ID}")
            return True
        except Exception as e:
            print(f"[ERROR] 连接失败: {e}")
            return False
    
    async def send(self, data: dict):
        """发送消息"""
        if self.ws:
            await self.ws.send(json.dumps(data))
    
    async def handle_message(self, message: str):
        """处理收到的消息"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "send_to_cursor":
                # 收到手机发来的消息，转发给 Cursor
                content = data.get("content", "")
                print(f"[RECV] 收到指令: {content[:50]}...")
                
                success = self.cursor.send_message(content)
                await self.send({
                    "type": "ack",
                    "success": success,
                    "message_id": data.get("message_id")
                })
                
            elif msg_type == "get_status":
                # 返回状态
                status = self.cursor.get_status()
                await self.send({"type": "status", **status})
                
            elif msg_type == "ping":
                await self.send({"type": "pong"})
                
        except json.JSONDecodeError:
            print(f"[WARN] 无效消息: {message}")
    
    async def listen(self):
        """监听消息循环"""
        try:
            async for message in self.ws:
                await self.handle_message(message)
        except ConnectionClosed:
            print("[WARN] 连接已断开")
            self.running = False
    
    async def run(self):
        """主运行循环（带自动重连）"""
        while True:
            if await self.connect():
                await self.listen()
            
            print("[INFO] 5秒后重连...")
            await asyncio.sleep(5)


async def main():
    client = RelayClient()
    await client.run()


if __name__ == "__main__":
    print("=" * 50)
    print("MobileAgentLivelink PC Client")
    print("=" * 50)
    asyncio.run(main())
