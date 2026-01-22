"""自动测试脚本 - 无需交互"""
import asyncio
import json
import sys
sys.path.insert(0, "d:/Github/MobileAgentLivelink/pc-client")

from websockets import connect, serve
from cursor_controller import CursorController

async def main():
    print("=" * 50)
    print("MobileAgentLivelink 本地测试")
    print("=" * 50)
    
    # 1. 先测试 Cursor 控制器
    print("\n[1] 测试 Cursor 控制器...")
    ctrl = CursorController()
    status = ctrl.get_status()
    print(f"    Cursor 状态: {status}")
    
    if not status["running"]:
        print("    [ERROR] 未检测到 Cursor 窗口，请打开 Cursor")
        return
    
    print("    [OK] Cursor 已检测到")
    
    # 2. 测试打开对话面板
    print("\n[2] 测试打开 Cursor 对话面板 (Ctrl+L)...")
    await asyncio.sleep(1)
    
    success = ctrl.open_chat_panel()
    if success:
        print("    [OK] 对话面板已打开")
    else:
        print("    [WARN] 打开对话面板可能失败")
    
    # 3. 测试发送消息
    print("\n[3] 测试发送消息...")
    await asyncio.sleep(1)
    
    test_message = "hello this is a test from MobileAgentLivelink"
    success = ctrl.send_message(test_message)
    
    if success:
        print(f"    [OK] 消息已发送: {test_message}")
    else:
        print("    [ERROR] 发送消息失败")
    
    print("\n" + "=" * 50)
    print("测试完成！请查看 Cursor 窗口")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
