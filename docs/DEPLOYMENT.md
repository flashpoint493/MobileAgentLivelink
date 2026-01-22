# MobileAgentLivelink 部署指南

## 概述

本文档描述如何将中转服务器部署到腾讯云，实现公网访问。

## 部署方案

根据 [DECISIONS.md](DECISIONS.md)，我们选择**腾讯云轻量应用服务器 (Lighthouse)** 作为部署方案。

### 方案优势
- ✅ 开通即用，5 分钟搞定
- ✅ 标准 Linux 环境，部署逻辑清晰
- ✅ 新用户首购价格优惠（约 ¥40-60/月）
- ✅ 完全控制，便于调试

## 部署步骤

### 1. 购买腾讯云服务器

1. 访问 [腾讯云轻量应用服务器](https://cloud.tencent.com/product/lighthouse)
2. 选择配置：
   - **地域**: 选择离你最近的地域（如：北京、上海、广州）
   - **镜像**: Ubuntu 22.04 LTS
   - **套餐**: 2核2G 或更高（推荐 2核4G）
   - **带宽**: 3Mbps 起步
3. 完成购买并获取：
   - 服务器公网 IP
   - SSH 登录密码（或密钥）

### 2. 服务器环境准备

#### 2.1 SSH 连接服务器

```bash
# 使用密码登录（IPv4）
ssh root@<你的服务器IP>

# 使用密码登录（IPv6）
ssh root@<你的IPv6地址>

# 或使用密钥登录
ssh -i <密钥路径> root@<你的服务器IP>
```

#### 2.2 安装 Python 环境

```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Python 3.10+ 和 pip
apt install -y python3 python3-pip python3-venv

# 验证安装
python3 --version  # 应显示 Python 3.10.x 或更高
```

#### 2.3 安装项目依赖

```bash
# 创建项目目录
mkdir -p /opt/mobileagentlivelink
cd /opt/mobileagentlivelink

# 上传项目文件（使用 scp 或 git clone）

# === 方式1: 使用 scp 上传（推荐，适用于 GitHub 无法访问的情况）===
# 在本地 Windows PowerShell 执行：
# scp -r relay-server root@<你的服务器IP>:/opt/mobileagentlivelink/
# 如果使用 scp，则不需要 cd MobileAgentLivelink，直接进入 relay-server 目录

# === 方式2: 使用 git clone（需要服务器能访问 GitHub）===
# 如果遇到 "Connection timed out" 错误，请使用方式1（scp）或方式3（代理）
#
# 重要说明：
# - 对于公开仓库（Public Repository）：不需要登录，可以直接 clone
# - 对于私有仓库（Private Repository）：需要配置认证
#   方式A: 使用 Personal Access Token
#     git clone https://<token>@github.com/flashpoint493/MobileAgentLivelink.git
#   方式B: 使用 SSH key（需要先配置 SSH key）
#     git clone git@github.com:flashpoint493/MobileAgentLivelink.git

# 检查是否已经 clone 过仓库
if [ -d "MobileAgentLivelink" ]; then
    echo "仓库已存在，更新到最新版本..."
    cd MobileAgentLivelink
    git pull
else
    echo "首次克隆仓库..."
    # 如果 GitHub 无法访问，请使用方式1（scp）上传文件
    # 公开仓库可以直接 clone，无需登录
    git clone https://github.com/flashpoint493/MobileAgentLivelink.git
    cd MobileAgentLivelink
fi

# === 方式3: 使用代理访问 GitHub（如果方式1和2都不可用）===
# 配置 Git 使用代理（需要先设置代理服务器）
# git config --global http.proxy http://<代理地址>:<端口>
# git config --global https.proxy https://<代理地址>:<端口>
# git clone https://github.com/flashpoint493/MobileAgentLivelink.git
# 使用完后取消代理：
# git config --global --unset http.proxy
# git config --global --unset https.proxy

# 进入中转服务器目录
cd relay-server

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# 更新 pip（推荐）
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

**重要提示**：

- **首次部署**：如果目录不存在，使用 `git clone` 克隆仓库
- **更新已有仓库**：如果目录已存在，使用 `git pull` 更新到最新版本
- **虚拟环境**：如果虚拟环境已存在，直接激活即可，无需重新创建
- **依赖更新**：每次更新代码后，建议运行 `pip install -r requirements.txt` 确保依赖是最新的

### 3. 配置服务器

#### 3.1 服务器地址信息

**注意**: 请将以下示例中的 `<你的服务器IP>` 替换为实际的服务器 IP 地址。

部署后的服务器地址：
- **IPv4 地址**: `<你的服务器IP>`
- **IPv6 地址**: `<你的IPv6地址>`
- **WebSocket 地址**: 
  - IPv4: `ws://<你的服务器IP>:8765/ws`
  - IPv6: `ws://[<你的IPv6地址>]:8765/ws`

#### 3.2 创建环境变量文件

```bash
# 在 relay-server 目录下创建 .env 文件
cat > .env << EOF
# 服务器配置
HOST=0.0.0.0
PORT=8765

# 安全配置（可选）
AUTH_TOKEN=<你的认证令牌>
EOF
```

#### 3.3 修改服务器代码支持环境变量

服务器代码已支持从环境变量读取配置（如果已实现），否则需要修改 `server.py`。

### 4. 配置防火墙

在腾讯云控制台配置防火墙规则：

1. 进入轻量应用服务器控制台
2. 选择你的服务器 → **防火墙** → **添加规则**
3. 添加规则：
   - **类型**: 自定义
   - **协议**: TCP
   - **端口**: 8765
   - **策略**: 允许
   - **来源**: 0.0.0.0/0（或限制为特定 IP）

### 5. 配置开机自启（使用 systemd）

#### 5.1 创建 systemd 服务文件

```bash
sudo cat > /etc/systemd/system/mobileagent-relay.service << EOF
[Unit]
Description=MobileAgentLivelink Relay Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/mobileagentlivelink/relay-server
Environment="PATH=/opt/mobileagentlivelink/relay-server/venv/bin"
ExecStart=/opt/mobileagentlivelink/relay-server/venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

#### 5.2 启动服务

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start mobileagent-relay

# 设置开机自启
sudo systemctl enable mobileagent-relay

# 查看服务状态
sudo systemctl status mobileagent-relay

# 查看日志
sudo journalctl -u mobileagent-relay -f
```

### 6. 验证部署

#### 6.1 检查服务运行状态

```bash
# 检查进程
ps aux | grep server.py

# 检查端口监听
netstat -tlnp | grep 8765
# 或
ss -tlnp | grep 8765
```

#### 6.2 测试健康检查接口

```bash
# 在服务器上测试
curl http://localhost:8765/health

# 从本地测试（替换为你的服务器IP）
curl http://<你的服务器IP>:8765/health
```

预期返回：
```json
{"status":"ok","pcs":0,"mobiles":0}
```

#### 6.3 测试 WebSocket 连接

可以使用在线 WebSocket 测试工具，或使用 Python 脚本：

```python
import asyncio
import websockets

async def test():
    # 使用 IPv4 地址（替换为你的服务器IP）
    uri = "ws://<你的服务器IP>:8765/ws"
    # 或使用 IPv6 地址（注意 IPv6 地址需要用方括号括起来）
    # uri = "ws://[<你的IPv6地址>]:8765/ws"
    async with websockets.connect(uri) as websocket:
        # 发送注册消息
        await websocket.send('{"type":"register","device_id":"test","device_type":"mobile"}')
        response = await websocket.recv()
        print(f"收到响应: {response}")

asyncio.run(test())
```

## 更新中转服务器（应用变更）

> 适用于已部署且使用 systemd 运行的场景。

当你在本地仓库提交并推送代码后，需要在服务器上更新并重启服务。以下是三种更新方式：

### 方式 A：使用自动化更新脚本（推荐）

**最简单快捷的方式**，一键完成所有更新步骤：

```bash
# 1. SSH 连接到服务器
ssh root@<你的服务器IP>

# 2. 进入项目目录
cd /opt/mobileagentlivelink/MobileAgentLivelink

# 3. 确保更新脚本有执行权限
chmod +x relay-server/update.sh

# 4. 运行更新脚本
sudo relay-server/update.sh
```

脚本会自动执行以下操作：
- ✅ 检查项目目录和服务状态
- ✅ 使用 `git pull` 拉取最新代码
- ✅ 更新 Python 依赖包
- ✅ 重启 systemd 服务
- ✅ 验证服务健康状态
- ✅ 显示服务状态和日志查看命令

**如果更新失败**，脚本会显示回滚命令，你可以手动执行回滚。

### 方式 B：使用 Git 手动更新

如果你需要更多控制，可以手动执行每个步骤：

```bash
# 1. SSH 连接到服务器
ssh root@<你的服务器IP>

# 2. 进入项目目录
cd /opt/mobileagentlivelink/MobileAgentLivelink

# 3. 拉取最新代码
git pull

# 4. 进入服务目录并激活虚拟环境
cd relay-server
source venv/bin/activate

# 5. 更新依赖（如果有 requirements.txt 变更）
pip install -r requirements.txt

# 6. 重启服务
sudo systemctl restart mobileagent-relay

# 7. 检查服务状态
sudo systemctl status mobileagent-relay

# 8. 验证服务健康（可选）
curl http://localhost:8765/health
```

### 方式 C：使用 scp 覆盖更新

如果服务器上没有 git 仓库，可以使用 scp 上传文件：

```bash
# 1. 在本地执行：上传 relay-server 目录
scp -r relay-server root@<你的服务器IP>:/opt/mobileagentlivelink/MobileAgentLivelink/

# 2. SSH 连接到服务器
ssh root@<你的服务器IP>

# 3. 进入服务目录
cd /opt/mobileagentlivelink/MobileAgentLivelink/relay-server

# 4. 激活虚拟环境并更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 5. 重启服务
sudo systemctl restart mobileagent-relay

# 6. 检查服务状态
sudo systemctl status mobileagent-relay
```

### 更新后验证

无论使用哪种方式，更新后都应该验证服务是否正常运行：

```bash
# 1. 检查服务状态
sudo systemctl status mobileagent-relay

# 2. 检查端口监听
ss -tlnp | grep 8765

# 3. 测试健康检查接口
curl http://localhost:8765/health

# 4. 查看服务日志（如有问题）
sudo journalctl -u mobileagent-relay -n 50 -f
```

### 回滚到之前的版本

如果更新后出现问题，可以回滚到之前的版本：

```bash
# 1. 进入项目目录
cd /opt/mobileagentlivelink/MobileAgentLivelink

# 2. 查看提交历史
git log --oneline -10

# 3. 回滚到指定提交（替换 <commit-hash> 为之前的提交哈希）
git checkout <commit-hash>

# 4. 进入服务目录
cd relay-server
source venv/bin/activate

# 5. 更新依赖（如果需要）
pip install -r requirements.txt

# 6. 重启服务
sudo systemctl restart mobileagent-relay

# 7. 验证服务
sudo systemctl status mobileagent-relay
```

### 更新注意事项

1. **备份重要数据**：更新前建议备份 `.env` 配置文件
2. **检查依赖变更**：如果 `requirements.txt` 有变更，务必运行 `pip install -r requirements.txt`
3. **服务重启**：代码更新后必须重启服务才能生效
4. **验证功能**：更新后建议执行端到端测试，确保功能正常
5. **查看日志**：如有问题，及时查看服务日志排查

## 客户端配置更新

### Web 客户端更新

**Web 客户端是单文件 HTML**，使用方式有两种：

#### 方式 1：本地文件（推荐）

直接下载 `web-client.html` 文件到本地，用浏览器打开即可：

```bash
# 从 GitHub 下载最新版本
# 访问: https://github.com/flashpoint493/MobileAgentLivelink/blob/master/web-client.html
# 点击 "Raw" 按钮，然后右键保存为 web-client.html
```

**更新方法**：
- 当仓库中的 `web-client.html` 有更新时，重新下载文件覆盖本地文件即可
- 配置信息（服务器地址、设备ID等）保存在浏览器 localStorage 中，不会丢失
- 建议定期检查仓库更新，获取最新功能和 bug 修复

#### 方式 2：部署到 Web 服务器（可选）

如果你希望通过 HTTP 访问 Web 客户端，可以部署到服务器：

```bash
# 1. 将 web-client.html 上传到服务器
scp web-client.html root@<你的服务器IP>:/var/www/html/

# 2. 配置 Nginx（示例）
# 在 /etc/nginx/sites-available/default 中添加：
#   location / {
#       root /var/www/html;
#       index web-client.html;
#   }

# 3. 重启 Nginx
sudo systemctl restart nginx
```

**更新方法**：
- 重新上传 `web-client.html` 文件覆盖服务器上的旧文件
- 如果使用 Git 部署，可以在服务器上执行 `git pull` 更新

**注意**：
- Web 客户端通过配置的服务器地址连接中转服务器，**中转服务器更新时，Web 客户端不需要更新**
- 只有 `web-client.html` 文件本身有更新（新功能、bug修复）时，才需要更新客户端文件
- 配置信息保存在浏览器中，更新文件不会丢失配置

### PC 客户端配置

更新 `pc-client/config.py` 或 `.env` 文件：

```python
# 使用 IPv4 地址（替换为你的服务器IP）
RELAY_SERVER_URL = "ws://<你的服务器IP>:8765/ws"

# 或使用 IPv6 地址（注意 IPv6 地址需要用方括号括起来）
# RELAY_SERVER_URL = "ws://[<你的IPv6地址>]:8765/ws"

# 或使用域名（如果已配置）
# RELAY_SERVER_URL = "ws://relay.yourdomain.com:8765/ws"
```

**更新方法**：
- 如果 PC 客户端代码有更新，重新下载 `pc-client/` 目录
- 如果只是中转服务器地址变更，只需修改配置文件

## 故障排查

### GitHub 连接超时（无法 clone 仓库）

如果遇到 `fatal: unable to access 'https://github.com/...': Connection timed out` 错误：

**解决方案 1：使用 scp 从本地上传（推荐）**

```bash
# 在本地 Windows PowerShell 执行
# 1. 进入项目根目录
cd D:\Github\MobileAgentLivelink

# 2. 上传整个项目到服务器
scp -r . root@<你的服务器IP>:/opt/mobileagentlivelink/MobileAgentLivelink

# 或者只上传 relay-server 目录（如果只需要部署中转服务器）
scp -r relay-server root@<你的服务器IP>:/opt/mobileagentlivelink/
```

**解决方案 2：配置 Git 代理（如果有代理服务器）**

```bash
# 在服务器上配置代理
git config --global http.proxy http://<代理地址>:<端口>
git config --global https.proxy https://<代理地址>:<端口>

# 然后重试 clone
git clone https://github.com/flashpoint493/MobileAgentLivelink.git

# 使用完后取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

**解决方案 3：检查网络连接**

```bash
# 测试是否能访问 GitHub
ping github.com

# 测试 HTTPS 连接
curl -I https://github.com

# 如果都无法访问，建议使用解决方案1（scp上传）
```

### Git 认证问题（私有仓库）

如果仓库是私有的，clone 时需要认证：

**方式 1：使用 Personal Access Token（推荐）**

```bash
# 在 GitHub 创建 Personal Access Token (Settings -> Developer settings -> Personal access tokens)
# 然后使用 token 克隆：
git clone https://<token>@github.com/flashpoint493/MobileAgentLivelink.git

# 或者在 URL 中嵌入 token
git clone https://ghp_xxxxxxxxxxxx@github.com/flashpoint493/MobileAgentLivelink.git
```

**方式 2：配置 SSH Key**

```bash
# 1. 在服务器上生成 SSH key（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 查看公钥
cat ~/.ssh/id_ed25519.pub

# 3. 将公钥添加到 GitHub (Settings -> SSH and GPG keys)

# 4. 使用 SSH URL 克隆
git clone git@github.com:flashpoint493/MobileAgentLivelink.git
```

**方式 3：配置 Git Credential Helper**

```bash
# 配置 Git 保存凭据
git config --global credential.helper store

# 首次 clone 时会提示输入用户名和密码/token
git clone https://github.com/flashpoint493/MobileAgentLivelink.git
# 输入用户名和 Personal Access Token（不是密码）
```

**注意**：
- **公开仓库不需要认证**，可以直接 clone
- 如果遇到认证错误，检查仓库是否为私有，或网络是否正常

### 服务无法启动

1. 检查 Python 环境：
   ```bash
   python3 --version
   which python3
   ```

2. 检查依赖安装：
   ```bash
   source venv/bin/activate
   pip list
   ```

3. 查看服务日志：
   ```bash
   sudo journalctl -u mobileagent-relay -n 50
   ```

### 无法连接服务器

1. 检查防火墙规则（腾讯云控制台）
2. 检查服务器防火墙（ufw/iptables）
3. 检查服务是否运行：
   ```bash
   sudo systemctl status mobileagent-relay
   ```

### WebSocket 连接失败

1. 检查服务器端口是否开放：
   ```bash
   # 测试 IPv4（替换为你的服务器IP）
   telnet <你的服务器IP> 8765
   
   # 或测试 IPv6（替换为你的IPv6地址）
   telnet <你的IPv6地址> 8765
   ```

2. 检查服务日志中的错误信息

3. 验证 WebSocket 路径是否正确：`/ws`

## 安全建议

1. **使用 HTTPS/WSS**（生产环境推荐）：
   - 配置 Nginx 反向代理
   - 使用 Let's Encrypt 免费 SSL 证书
   - 将 WebSocket 升级为 WSS

2. **认证机制**：
   - 实现设备认证（AUTH_TOKEN）
   - 限制连接来源 IP（如需要）

3. **监控和日志**：
   - 配置日志轮转
   - 设置监控告警

## 下一步

部署完成后：
1. 更新 PC 客户端配置
2. 更新 Android 应用配置
3. 执行端到端测试（参考 `docs/QA_TEST_CASES.md`）

---

*最后更新: 2026-01-22*
