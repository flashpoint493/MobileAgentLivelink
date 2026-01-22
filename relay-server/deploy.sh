#!/bin/bash
# MobileAgentLivelink 中转服务器部署脚本
# 用于在腾讯云服务器上快速部署

set -e

echo "=========================================="
echo "MobileAgentLivelink Relay Server 部署脚本"
echo "=========================================="

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "错误: 请使用 root 用户运行此脚本"
    exit 1
fi

# 项目目录
PROJECT_DIR="/opt/mobileagentlivelink"
SERVICE_DIR="$PROJECT_DIR/relay-server"
SERVICE_NAME="mobileagent-relay"

echo ""
echo "[1/5] 检查系统环境..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "安装 Python 3..."
    apt update
    apt install -y python3 python3-pip python3-venv
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python 版本: $PYTHON_VERSION"

# 检查项目目录
if [ ! -d "$SERVICE_DIR" ]; then
    echo "错误: 未找到项目目录 $SERVICE_DIR"
    echo "请先上传项目文件或使用 git clone"
    exit 1
fi

echo ""
echo "[2/5] 设置 Python 虚拟环境..."

cd "$SERVICE_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 创建虚拟环境"
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ 安装依赖完成"

echo ""
echo "[3/5] 创建 systemd 服务..."

# 创建 systemd 服务文件
cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=MobileAgentLivelink Relay Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${SERVICE_DIR}
Environment="PATH=${SERVICE_DIR}/venv/bin"
ExecStart=${SERVICE_DIR}/venv/bin/python ${SERVICE_DIR}/server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✓ 服务文件已创建"

echo ""
echo "[4/5] 启动服务..."

systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl restart ${SERVICE_NAME}

# 等待服务启动
sleep 2

if systemctl is-active --quiet ${SERVICE_NAME}; then
    echo "✓ 服务启动成功"
else
    echo "✗ 服务启动失败，查看日志:"
    journalctl -u ${SERVICE_NAME} -n 20 --no-pager
    exit 1
fi

echo ""
echo "[5/5] 验证部署..."

# 检查端口
if netstat -tlnp 2>/dev/null | grep -q ":8765" || ss -tlnp 2>/dev/null | grep -q ":8765"; then
    echo "✓ 端口 8765 正在监听"
else
    echo "⚠ 警告: 端口 8765 未监听，请检查服务日志"
fi

# 测试健康检查
sleep 1
if curl -s http://localhost:8765/health > /dev/null; then
    echo "✓ 健康检查通过"
    curl -s http://localhost:8765/health | python3 -m json.tool
else
    echo "⚠ 警告: 健康检查失败"
fi

echo ""
echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "服务管理命令:"
echo "  查看状态: systemctl status ${SERVICE_NAME}"
echo "  查看日志: journalctl -u ${SERVICE_NAME} -f"
echo "  重启服务: systemctl restart ${SERVICE_NAME}"
echo "  停止服务: systemctl stop ${SERVICE_NAME}"
echo ""
echo "重要提示:"
echo "  1. 请在腾讯云控制台配置防火墙，开放 8765 端口"
echo "  2. 更新 PC 客户端和 Android 应用的服务器地址"
echo "  3. 执行端到端测试验证功能"
echo ""
