"""WebSocket 中转服务器 - 连接手机和 PC"""
import asyncio
import json
from typing import Dict, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MobileAgentLivelink Relay Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """管理 WebSocket 连接"""
    
    def __init__(self):
        # device_id -> WebSocket
        self.pc_clients: Dict[str, WebSocket] = {}
        self.mobile_clients: Dict[str, WebSocket] = {}
        # mobile_id -> pc_id 配对关系
        self.pairings: Dict[str, str] = {}
        # pc_id -> token
        self.pc_tokens: Dict[str, str] = {}
    
    async def register(self, ws: WebSocket, device_id: str, device_type: str, token: str | None = None):
        """注册设备"""
        if device_type == "pc":
            self.pc_clients[device_id] = ws
            # 存储token，只有非空字符串才视为有效配置
            # None或空字符串都视为未配置，配对时将拒绝
            if token and token.strip():
                self.pc_tokens[device_id] = token.strip()
                print(f"[PC] 已注册: {device_id}, Token: 已配置")
            else:
                # 如果未提供token或为空，设置为None，配对时将拒绝
                self.pc_tokens[device_id] = None
                print(f"[PC] 已注册: {device_id}, Token: 未配置（配对将被拒绝）")
        else:
            self.mobile_clients[device_id] = ws
            print(f"[Mobile] 已注册: {device_id}")
    
    def disconnect(self, device_id: str, device_type: str):
        """断开连接"""
        if device_type == "pc":
            self.pc_clients.pop(device_id, None)
            self.pc_tokens.pop(device_id, None)
        else:
            self.mobile_clients.pop(device_id, None)
            self.pairings.pop(device_id, None)
    
    def pair(self, mobile_id: str, pc_id: str, token: str | None) -> tuple[bool, str | None]:
        """配对手机和 PC"""
        if pc_id not in self.pc_clients:
            return False, "pc_offline"
        
        # 获取PC注册时设置的token
        required_token = self.pc_tokens.get(pc_id)
        
        # 强制要求PC必须配置AUTH_TOKEN（非空字符串）
        if not required_token:
            print(f"[Pair] 配对失败: PC {pc_id} 未配置AUTH_TOKEN，拒绝配对")
            return False, "pc_token_not_configured"
        
        # 如果PC设置了token，则必须验证
        provided_token = (token.strip() if token else "") if token is not None else ""
        if provided_token != required_token:
            print(f"[Pair] 配对失败: PC {pc_id} token验证失败（期望: {required_token[:4]}..., 提供: {provided_token[:4] if provided_token else '空'}...）")
            return False, "invalid_token"
        
        self.pairings[mobile_id] = pc_id
        print(f"[Pair] {mobile_id} <-> {pc_id} (Token验证通过)")
        return True, None

    
    async def relay_to_pc(self, mobile_id: str, message: dict) -> bool:
        """转发消息到 PC"""
        pc_id = self.pairings.get(mobile_id)
        if not pc_id or pc_id not in self.pc_clients:
            return False
        
        pc_ws = self.pc_clients[pc_id]
        await pc_ws.send_json(message)
        return True
    
    async def relay_to_mobile(self, pc_id: str, message: dict):
        """转发消息到手机"""
        for mobile_id, paired_pc in self.pairings.items():
            if paired_pc == pc_id and mobile_id in self.mobile_clients:
                await self.mobile_clients[mobile_id].send_json(message)
    
    def get_online_pcs(self) -> list:
        """获取在线 PC 列表"""
        return list(self.pc_clients.keys())


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 入口"""
    await websocket.accept()
    device_id = None
    device_type = None
    
    try:
        async for message in websocket.iter_text():
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "register":
                # 设备注册
                device_id = data.get("device_id")
                device_type = data.get("device_type")
                token = data.get("token")
                await manager.register(websocket, device_id, device_type, token=token)
                await websocket.send_json({
                    "type": "registered",
                    "device_id": device_id
                })
            
            elif msg_type == "pair":
                # 手机请求配对 PC
                pc_id = data.get("pc_id")
                token = data.get("token")
                success, reason = manager.pair(device_id, pc_id, token)
                await websocket.send_json({
                    "type": "pair_result",
                    "success": success,
                    "pc_id": pc_id,
                    "reason": reason
                })

            
            elif msg_type == "list_pcs":
                # 获取在线 PC 列表
                pcs = manager.get_online_pcs()
                await websocket.send_json({
                    "type": "pc_list",
                    "pcs": pcs
                })
            
            elif msg_type == "send_to_cursor":
                # 手机发送消息到 Cursor
                success = await manager.relay_to_pc(device_id, data)
                if not success:
                    await websocket.send_json({
                        "type": "error",
                        "message": "PC 未连接或未配对"
                    })
            
            elif msg_type in ["ack", "status", "pong", "context_result", "task_started", "task_done", "new_chat_result", "set_chat_state_result"]:
                # PC 回复，转发给手机
                await manager.relay_to_mobile(device_id, data)

            
            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        pass
    finally:
        if device_id:
            manager.disconnect(device_id, device_type)
            print(f"[Disconnect] {device_type}: {device_id}")


@app.get("/health")
async def health():
    return {"status": "ok", "pcs": len(manager.pc_clients), "mobiles": len(manager.mobile_clients)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
