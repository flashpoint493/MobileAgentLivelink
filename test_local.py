"""本地测试脚本 - 在单台设备上测试完整链路"""
import asyncio
import json
import sys
from websockets import connect, serve

# ============== 模拟中转服务器 ==============
clients = {}

async def relay_handler(websocket, path=None):
    """简化的中转服务"""
    device_id = None
    device_type = None
    
    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "register":
                device_id = data.get("device_id")
                device_type = data.get("device_type")
                clients[device_id] = {"ws": websocket, "type": device_type}
                print(f"[Server] 设备注册: {device_type} - {device_id}")
                await websocket.send(json.dumps({"type": "registered", "device_id": device_id}))
                
            elif msg_type == "send_to_cursor":
                # 转发到 PC
                for cid, c in clients.items():
                    if c["type"] == "pc":
                        await c["ws"].send(message)
                        print(f"[Server] 转发消息到 PC: {data.get('content', '')[:30]}...")
                        
            elif msg_type == "ack":
                # 转发回手机
                for cid, c in clients.items():
                    if c["type"] == "mobile":
                        await c["ws"].send(message)
                        
    except Exception as e:
        print(f"[Server] 连接断开: {e}")
    finally:
        if device_id:
            clients.pop(device_id, None)


# ============== 模拟手机端 ==============
async def mobile_client(message_to_send: str):
    """模拟手机发送消息"""
    uri = "ws://localhost:8765"
    
    async with connect(uri) as ws:
        # 注册
        await ws.send(json.dumps({
            "type": "register",
            "device_id": "test-mobile",
            "device_type": "mobile"
        }))
        resp = await ws.recv()
        print(f"[Mobile] 注册响应: {resp}")
        
        # 等待 PC 连接
        await asyncio.sleep(1)
        
        # 发送消息
        await ws.send(json.dumps({
            "type": "send_to_cursor",
            "content": message_to_send,
            "message_id": "test-001"
        }))
        print(f"[Mobile] 已发送: {message_to_send}")
        
        # 等待 ACK
        try:
            resp = await asyncio.wait_for(ws.recv(), timeout=10)
            print(f"[Mobile] 收到响应: {resp}")
        except asyncio.TimeoutError:
            print("[Mobile] 等待响应超时")


async def run_server():
    """运行服务器"""
    server = await serve(relay_handler, "localhost", 8765)
    print("[Server] 中转服务已启动 ws://localhost:8765")
    await server.wait_closed()


async def run_test(message: str):
    """运行完整测试"""
    # 启动服务器
    server = await serve(relay_handler, "localhost", 8765)
    print("[Server] 中转服务已启动 ws://localhost:8765")
    print("-" * 50)
    
    # 导入并启动 PC 客户端
    sys.path.insert(0, "d:/Github/MobileAgentLivelink/pc-client")
    from relay_client import RelayClient
    
    pc_client = RelayClient()
    
    # 启动 PC 客户端连接（后台任务）
    pc_task = asyncio.create_task(pc_client.connect())
    await asyncio.sleep(1)  # 等待连接
    
    print("-" * 50)
    print(f"[Test] 准备发送测试消息: {message}")
    print("[Test] 请确保 Cursor 已打开...")
    input("[Test] 按 Enter 继续...")
    
    # 模拟手机发送
    await mobile_client(message)
    
    # 等待处理
    await asyncio.sleep(3)
    
    server.close()
    print("\n[Test] 测试完成!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        # 只运行服务器
        asyncio.run(run_server())
    else:
        # 运行完整测试
        test_msg = "hello world this is a test"
        if len(sys.argv) > 1:
            test_msg = " ".join(sys.argv[1:])
        asyncio.run(run_test(test_msg))
