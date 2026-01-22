"""WebSocket 中转服务客户端"""
import asyncio
import json
from pathlib import Path
from websockets import connect, ConnectionClosed
from config import RELAY_SERVER_URL, DEVICE_ID, AUTH_TOKEN, PROJECT_ROOT, TASK_DONE_TIMEOUT
from cursor_controller import CursorController


class RelayClient:
    """连接云中转服务，接收手机端指令"""
    
    def __init__(self):
        self.cursor = CursorController()
        self.ws = None
        self.running = False
        self.last_message = None
        # 优先使用Cursor当前打开的项目路径，否则使用配置的PROJECT_ROOT
        self.project_root = self._get_project_root()
    
    def _get_project_root(self) -> Path:
        """获取项目根目录：优先使用Cursor当前工作区，否则使用配置的PROJECT_ROOT"""
        # 尝试从Cursor获取当前工作区路径
        workspace_path = self.cursor.get_workspace_path()
        if workspace_path and workspace_path.exists():
            print(f"[INFO] 使用Cursor当前工作区: {workspace_path}")
            return workspace_path
        
        # 回退到配置的PROJECT_ROOT
        fallback_root = Path(PROJECT_ROOT).resolve()
        print(f"[INFO] 使用配置的项目根目录: {fallback_root}")
        return fallback_root
    
    async def connect(self):
        """连接到中转服务器"""
        print(f"[INFO] 正在连接: {RELAY_SERVER_URL}")
        
        # 检查AUTH_TOKEN是否配置
        if not AUTH_TOKEN or not AUTH_TOKEN.strip():
            print("[WARN] AUTH_TOKEN 未配置或为空！")
            print("[WARN] 请设置环境变量 AUTH_TOKEN 以确保安全配对")
            print("[WARN] 未配置AUTH_TOKEN将导致无法配对，请尽快配置")
        
        try:
            self.ws = await connect(RELAY_SERVER_URL)
            self.running = True
            
            # 注册设备（即使AUTH_TOKEN为空也发送，让服务器知道需要验证）
            await self.send({
                "type": "register",
                "device_id": DEVICE_ID,
                "device_type": "pc",
                "token": AUTH_TOKEN if AUTH_TOKEN else ""
            })
            
            print(f"[INFO] 已连接，设备ID: {DEVICE_ID}")
            if AUTH_TOKEN and AUTH_TOKEN.strip():
                print(f"[INFO] Pair Token: {AUTH_TOKEN}")
            else:
                print("[WARN] AUTH_TOKEN 未配置，配对将失败")
            return True
        except Exception as e:
            print(f"[ERROR] 连接失败: {e}")
            return False
    
    async def send(self, data: dict):
        """发送消息"""
        if self.ws:
            await self.ws.send(json.dumps(data))
    
    def _resolve_path(self, raw_path: str) -> Path | None:
        try:
            candidate = (self.project_root / raw_path).resolve()
            if candidate == self.project_root or self.project_root in candidate.parents:
                return candidate
        except Exception:
            return None
        return None
    
    def _read_context_files(self, paths: list) -> list:
        items = []
        for raw in paths:
            if not raw:
                continue
            target = self._resolve_path(raw)
            if not target:
                items.append({"path": raw, "ok": False, "error": "invalid_path"})
                continue
            if not target.exists() or not target.is_file():
                items.append({"path": raw, "ok": False, "error": "not_found"})
                continue
            try:
                content = target.read_text(encoding="utf-8", errors="ignore")
                truncated = False
                if len(content) > 4000:
                    content = content[:4000]
                    truncated = True
                items.append({"path": raw, "ok": True, "content": content, "truncated": truncated})
            except Exception as e:
                items.append({"path": raw, "ok": False, "error": str(e)})
        return items
    
    async def _send_task_done(self, message_id: int, timeout: float):
        await asyncio.sleep(timeout)
        await self.send({
            "type": "task_done",
            "message_id": message_id,
            "estimated": True,
            "timeout": timeout
        })
    
    async def _send_context_result(self, context_request: dict, message_id: int | None = None, request_id: int | None = None):
        paths = context_request.get("paths", []) if isinstance(context_request, dict) else []
        if isinstance(paths, str):
            paths = [paths]
        items = self._read_context_files(paths)
        payload = {
            "type": "context_result",
            "items": items,
            "project_root": str(self.project_root),
        }
        if message_id is not None:
            payload["message_id"] = message_id
        if request_id is not None:
            payload["request_id"] = request_id
        await self.send(payload)
    
    async def handle_message(self, message: str):
        """处理收到的消息"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "send_to_cursor":
                # 收到手机发来的消息，转发给 Cursor
                content = data.get("content", "")
                force_open = data.get("force_open", False)
                print(f"[RECV] 收到指令: {content[:50]}...")
                
                success = self.cursor.send_message(content, force_open=force_open)
                if success:
                    self.last_message = content
                await self.send({
                    "type": "ack",
                    "success": success,
                    "message_id": data.get("message_id")
                })
                if success:
                    await self.send({
                        "type": "task_started",
                        "message_id": data.get("message_id")
                    })
                    done_timeout = float(data.get("done_timeout", TASK_DONE_TIMEOUT))
                    asyncio.create_task(self._send_task_done(data.get("message_id"), done_timeout))
                if data.get("context_request"):
                    await self._send_context_result(data.get("context_request"), message_id=data.get("message_id"))
                
            elif msg_type == "get_status":
                # 返回状态，并更新项目根目录（Cursor可能切换了工作区）
                status = self.cursor.get_status()
                # 如果Cursor工作区路径可用，更新project_root
                if status.get("workspace_path"):
                    new_root = Path(status["workspace_path"])
                    if new_root.exists() and new_root != self.project_root:
                        print(f"[INFO] 检测到Cursor切换工作区: {new_root}")
                        self.project_root = new_root
                await self.send({
                    "type": "status",
                    **status,
                    "project_root": str(self.project_root),
                    "last_message": self.last_message
                })
                
            elif msg_type == "get_context":
                context_request = data.get("context_request", {})
                await self._send_context_result(context_request, request_id=data.get("request_id"))
                
            elif msg_type == "new_chat":
                success = self.cursor.new_chat()
                await self.send({
                    "type": "new_chat_result",
                    "success": success,
                    "request_id": data.get("request_id")
                })
                
            elif msg_type == "set_chat_state":
                self.cursor.chat_open = bool(data.get("open"))
                await self.send({
                    "type": "set_chat_state_result",
                    "success": True,
                    "open": self.cursor.chat_open,
                    "request_id": data.get("request_id")
                })
                
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

