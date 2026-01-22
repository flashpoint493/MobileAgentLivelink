"""Cursor IDE 控制器 - 通过 Windows API 模拟输入"""
import time
import ctypes
import os
import psutil
from pathlib import Path
import pyautogui
import pygetwindow as gw
from config import CURSOR_WINDOW_TITLE, INPUT_DELAY, NEW_CHAT_COMMAND

# Windows API 常量
SW_RESTORE = 9
SW_SHOW = 5


class CursorController:
    """控制 Cursor IDE 窗口"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = INPUT_DELAY
        self.chat_open = False
    
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
    
    def open_chat_panel(self, force_open: bool = False) -> bool:
        """打开 Cursor AI 对话面板 (Ctrl+L)"""
        if not self.activate_cursor():
            return False
        
        if force_open or not self.chat_open:
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.5)
            self.chat_open = True
        return True
    
    def new_chat(self) -> bool:
        """通过命令面板触发 New Chat"""
        if not self.activate_cursor():
            return False
        
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'shift', 'p')
        time.sleep(0.2)
        self._type_text(NEW_CHAT_COMMAND)
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)
        self.chat_open = True
        return True
    
    def send_message(self, message: str, force_open: bool = False) -> bool:
        """向 Cursor 发送消息"""
        if not self.open_chat_panel(force_open=force_open):
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
    
    def get_workspace_path(self) -> Path | None:
        """获取 Cursor 当前打开的工作区路径"""
        window = self.find_cursor_window()
        if not window:
            return None
        
        try:
            # 方法1: 从窗口进程获取工作目录
            hwnd = window._hWnd
            process_id = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
            
            try:
                process = psutil.Process(process_id.value)
                cwd = process.cwd()
                # Cursor的工作目录通常是项目根目录
                if cwd and Path(cwd).exists():
                    return Path(cwd).resolve()
            except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                pass
            
            # 方法2: 从窗口标题解析（Cursor标题格式通常是 "项目名 - Cursor" 或包含路径）
            title = window.title
            if title and title != CURSOR_WINDOW_TITLE:
                # 尝试从标题中提取路径信息
                # 某些情况下标题可能包含路径
                pass
            
            # 方法3: 尝试从Cursor的配置文件获取
            # Cursor通常会在用户目录下存储工作区信息
            app_data = os.getenv('APPDATA')
            if app_data:
                cursor_config = Path(app_data) / 'Cursor' / 'User' / 'globalStorage' / 'storage.json'
                # 这里可以尝试解析配置文件，但比较复杂
            
            return None
        except Exception as e:
            print(f"[WARN] 获取工作区路径失败: {e}")
            return None
    
    def get_status(self) -> dict:
        """获取 Cursor 状态"""
        window = self.find_cursor_window()
        workspace_path = self.get_workspace_path()
        return {
            "running": window is not None,
            "title": window.title if window else None,
            "minimized": window.isMinimized if window else None,
            "workspace_path": str(workspace_path) if workspace_path else None,
        }



# 测试
if __name__ == "__main__":
    ctrl = CursorController()
    print("Cursor 状态:", ctrl.get_status())
