#!/bin/bash
# MobileAgentLivelink 中转服务器更新脚本
# 用于在仓库更新后快速更新并重启服务

set -e

echo "=========================================="
echo "MobileAgentLivelink Relay Server 更新脚本"
echo "=========================================="

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "错误: 请使用 root 用户运行此脚本"
    exit 1
fi

# 项目目录
PROJECT_DIR="/opt/mobileagentlivelink"
REPO_DIR="$PROJECT_DIR/MobileAgentLivelink"
SERVICE_DIR="$PROJECT_DIR/MobileAgentLivelink/relay-server"
SERVICE_NAME="mobileagent-relay"

echo ""
echo "[1/4] 检查项目目录..."

# 检查项目目录是否存在
if [ ! -d "$REPO_DIR" ]; then
    echo "错误: 未找到项目目录 $REPO_DIR"
    echo "请先使用 git clone 部署项目"
    exit 1
fi

if [ ! -d "$SERVICE_DIR" ]; then
    echo "错误: 未找到服务目录 $SERVICE_DIR"
    exit 1
fi

echo "✓ 项目目录检查通过"

echo ""
echo "[2/4] 更新代码..."

cd "$REPO_DIR"

# 检查是否为 git 仓库
if [ ! -d ".git" ]; then
    echo "⚠ 警告: 当前目录不是 git 仓库，跳过 git pull"
    echo "请手动更新代码或使用 scp 上传新文件"
else
    # 保存当前提交哈希（用于回滚）
    OLD_COMMIT=$(git rev-parse HEAD)
    echo "当前提交: $OLD_COMMIT"
    
    # 拉取最新代码
    echo "正在拉取最新代码..."
    git pull
    
    NEW_COMMIT=$(git rev-parse HEAD)
    echo "更新后提交: $NEW_COMMIT"
    
    if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
        echo "✓ 代码已是最新版本，无需更新"
    else
        echo "✓ 代码更新成功"
    fi
fi

echo ""
echo "[3/4] 更新依赖..."

cd "$SERVICE_DIR"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "⚠ 警告: 虚拟环境不存在，正在创建..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ 依赖更新完成"

echo ""
echo "[4/4] 重启服务..."

# 检查服务是否存在
if ! systemctl list-unit-files | grep -q "${SERVICE_NAME}.service"; then
    echo "⚠ 警告: 服务 ${SERVICE_NAME} 不存在"
    echo "请先运行 deploy.sh 进行初始部署"
    exit 1
fi

# 重启服务
systemctl daemon-reload
systemctl restart ${SERVICE_NAME}

# 等待服务启动
sleep 2

# 检查服务状态
if systemctl is-active --quiet ${SERVICE_NAME}; then
    echo "✓ 服务重启成功"
else
    echo "✗ 服务重启失败，查看日志:"
    journalctl -u ${SERVICE_NAME} -n 20 --no-pager
    echo ""
    echo "如需回滚，请执行:"
    echo "  cd $REPO_DIR"
    echo "  git checkout $OLD_COMMIT"
    echo "  cd $SERVICE_DIR"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  systemctl restart ${SERVICE_NAME}"
    exit 1
fi

echo ""
echo "=========================================="
echo "更新完成！"
echo "=========================================="
echo ""
echo "服务状态:"
systemctl status ${SERVICE_NAME} --no-pager -l | head -n 10

echo ""
echo "验证服务:"
sleep 1
if curl -s http://localhost:8765/health > /dev/null; then
    echo "✓ 健康检查通过"
    curl -s http://localhost:8765/health | python3 -m json.tool
else
    echo "⚠ 警告: 健康检查失败，请查看日志"
    echo "查看日志: journalctl -u ${SERVICE_NAME} -f"
fi

echo ""
echo "查看实时日志:"
echo "  journalctl -u ${SERVICE_NAME} -f"
echo ""

