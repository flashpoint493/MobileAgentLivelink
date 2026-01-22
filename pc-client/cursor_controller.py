"""Cursor IDE 控制器 - 通过 Windows API 模拟输入"""
import time
import ctypes
import pyautogui
import pygetwindow as gw
from config import CURSOR_WINDOW_TITLE, INPUT_DELAY

# Windows API 常量
SW_RESTORE = 9
SW_SHOW = 5


class CursorController:
    """控制 Cursor IDE 窗口"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = INPUT_DELAY
    
    def find_cursor_window(self):
        """查找 Cursor 窗口"""
        windows = gw.getWindowsWithTitle(CURSOR_WINDOW_TITLE)
        if not windows:
            return None
        return windows[0]
    
    def activate_cursor(self) -> bool:
        """激活 Cursor 窗口到前台"""
        window = self.find_cursor_window()
        if not window:
            print(f"[ERROR] 未找到 {CURSOR_WINDOW_TITLE} 窗口")
            return False
        
        try:
            hwnd = window._hWnd
            
            # 使用 Windows API 直接激活窗口
            if window.isMinimized:
                ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
            else:
                ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)
            
            # 强制设置前台窗口
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"[ERROR] 激活窗口失败: {e}")
            return False
    
    def open_chat_panel(self) -> bool:
        """打开 Cursor AI 对话面板 (Ctrl+L)"""
        if not self.activate_cursor():
            return False
        
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        return True
    
    def send_message(self, message: str) -> bool:
        """向 Cursor 发送消息"""
        if not self.open_chat_panel():
            return False
        
        time.sleep(0.3)
        
        # 使用剪贴板输入（支持中文）
        self._type_text(message)
        time.sleep(0.2)
        
        # 发送 (Enter)
        pyautogui.press('enter')
        return True
    
    def _type_text(self, text: str):
        """通过剪贴板输入文本（支持中文）"""
        import pyperclip
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
    
    def get_status(self) -> dict:
        """获取 Cursor 状态"""
        window = self.find_cursor_window()
        return {
            "running": window is not None,
            "title": window.title if window else None,
            "minimized": window.isMinimized if window else None,
        }


# 测试
if __name__ == "__main__":
    ctrl = CursorController()
    print("Cursor 状态:", ctrl.get_status())
