@echo off
chcp 65001 >nul
title MobileAgentLivelink PC客户端

echo ========================================
echo   MobileAgentLivelink PC客户端启动器
echo ========================================
echo.

REM ==========================================
REM 配置区域 - 请修改以下参数
REM ==========================================

REM 中转服务器地址（IP或域名，不需要包含 ws:// 和端口）
REM 示例：SET SERVER_IP=123.456.789.012
REM 示例：SET SERVER_IP=your-server.com
SET SERVER_IP=localhost
SET SERVER_PORT=8765

REM 配对密钥（必填！用于安全配对，防止未授权访问）
REM 示例：SET AUTH_TOKEN=my_secret_password_123
SET AUTH_TOKEN=your_secret_token_here

REM 设备ID（可选，用于标识此PC）
SET DEVICE_ID=default-pc

REM 项目根目录（用于读取上下文文件，留空则使用默认值）
REM 默认值：当前目录的上一级（即项目根目录）
REM 示例：SET PROJECT_ROOT=D:\Github\MobileAgentLivelink
SET PROJECT_ROOT=

REM 任务完成保底通知超时（秒，可选）
SET TASK_DONE_TIMEOUT=45

REM ==========================================
REM 以下内容无需修改
REM ==========================================

echo [配置检查]
echo 中转服务器: %SERVER_IP%:%SERVER_PORT%
echo 配对密钥: %AUTH_TOKEN%
echo 设备ID: %DEVICE_ID%
if "%PROJECT_ROOT%"=="" (
    echo 项目根目录: 使用默认值（项目根目录）
) else (
    echo 项目根目录: %PROJECT_ROOT%
)
echo.

REM 检查配对密钥是否已配置
if "%AUTH_TOKEN%"=="your_secret_token_here" (
    echo [警告] 配对密钥未配置！
    echo 请在脚本中设置 AUTH_TOKEN 变量
    echo.
    pause
    exit /b 1
)

REM 构建完整的WebSocket URL
SET RELAY_SERVER_URL=ws://%SERVER_IP%:%SERVER_PORT%/ws

REM 设置环境变量
set RELAY_SERVER_URL=%RELAY_SERVER_URL%
set AUTH_TOKEN=%AUTH_TOKEN%
set DEVICE_ID=%DEVICE_ID%
if not "%PROJECT_ROOT%"=="" (
    set PROJECT_ROOT=%PROJECT_ROOT%
)
if not "%TASK_DONE_TIMEOUT%"=="" (
    set TASK_DONE_TIMEOUT=%TASK_DONE_TIMEOUT%
)

echo [环境变量已设置]
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.10+
    echo.
    pause
    exit /b 1
)

echo [Python环境检查通过]
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 检查relay_client.py是否存在
if not exist "relay_client.py" (
    echo [错误] 找不到 relay_client.py 文件
    echo 请确保在 pc-client 目录下运行此脚本
    echo.
    pause
    exit /b 1
)

echo [启动PC客户端...]
echo.
echo ========================================
echo   正在连接到: %RELAY_SERVER_URL%
echo   设备ID: %DEVICE_ID%
echo ========================================
echo.
echo 提示: 按 Ctrl+C 可停止服务
echo.

REM 启动Python客户端
python relay_client.py

REM 如果Python脚本异常退出，暂停以便查看错误信息
if errorlevel 1 (
    echo.
    echo [错误] PC客户端异常退出
    echo.
    pause
)

