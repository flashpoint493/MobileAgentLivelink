# MobileAgentLivelink 决策记录

## 待确认决策

(暂无)

## 已确认决策

### [S-001] 公网通信架构
- **状态**: CONFIRMED
- **日期**: 2026-01-22
- **决策**: 必须支持公网访问（跨网络远程控制）
- **方案**: 使用云中转服务器，手机和 PC 都连接到中转服务
- **理由**: 
  - 用户场景需要在外出时控制家里/公司PC
  - 避免复杂的内网穿透配置
  - 统一的连接体验

### [S-002] 目标平台
- **状态**: CONFIRMED
- **日期**: 2026-01-22
- **决策**: 
  - 移动端: Android (Kotlin)
  - PC端: Windows 11
- **技术选型**:
  - Android: Kotlin + Jetpack Compose (原生，性能好)
  - PC: Python (跨平台易开发，后续可扩展 Mac/Linux)
  - 通信: WebSocket over 云中转服务

### [S-003] MVP IDE 范围
- **状态**: CONFIRMED
- **日期**: 2026-01-22
- **决策**: MVP 优先支持 Cursor
- **集成方式**: Windows API 模拟键盘输入 + 窗口控制
- **理由**: 用户量大，覆盖面广

### [A-001] 云服务供应商
- **状态**: CONFIRMED
- **日期**: 2026-01-22
- **决策**: 使用腾讯云作为云服务供应商
- **选项**:
  - A: CloudBase (免费额度，需学习) ✅
  - B: 轻量应用服务器 Lighthouse (简单直接，约 ¥40-60/月)
- **决策**: 优先考虑 Lighthouse，备选 CloudBase
- **理由**:
  - Lighthouse 开通即用，5 分钟搞定
  - 标准 Linux 环境，部署逻辑清晰
  - 新用户首购价格优惠
- **部署方案**: SSH 连接，安装 Python 环境，部署 relay-server，配置开机自启

### [A-002] Web客户端技术选型
- **状态**: CONFIRMED
- **日期**: 2026-01-22
- **决策**: 开发单文件HTML Web客户端
- **选项**:
  - A: 单文件HTML（零依赖，易分发）✅
  - B: React/Vue应用（需要构建工具）
- **理由**:
  - 零依赖，用户可直接打开使用
  - 便于通过文件分享、URL分享等方式分发
  - 快速部署，无需服务器
- **技术栈**: 原生HTML/CSS/JavaScript + WebSocket API

### [A-003] 废弃Android App方案
- **状态**: CONFIRMED
- **日期**: 2026-01-22
- **决策**: 废弃Android App开发，采用Web客户端作为唯一客户端
- **选项**:
  - A: 保留Android App
  - B: 废弃Android App，使用Web客户端 ✅
- **理由**:
  - Web客户端跨平台（PC/平板/手机），无需多个客户端
  - 零安装，直接打开浏览器即可使用
  - 更轻量，维护成本更低
  - 单文件分发更方便
- **影响**: 删除android-app目录及所有Android相关代码

---

## 公网通信方案说明

### 架构图
```
[Android App] <--WebSocket--> [云中转服务器] <--WebSocket--> [PC Python服务]
```

### 云中转服务选项（按难度排序）

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **1. 腾讯云 CloudBase** | 免费额度，WebSocket支持，已集成IDE | 需学习 | ⭐⭐⭐⭐⭐ |
| **2. Supabase Realtime** | 免费，实时数据库 | 国内速度一般 | ⭐⭐⭐⭐ |
| **3. 自建 VPS** | 完全控制 | 需购买服务器 | ⭐⭐⭐ |
| **4. Cloudflare Tunnel** | 免费内网穿透 | 配置复杂 | ⭐⭐ |

### 推荐: 腾讯云 CloudBase
- 免费额度足够 MVP 使用
- 支持 WebSocket 云函数
- CodeBuddy 有集成支持，部署方便

---
*决策记录格式见 CONTRIBUTING_AI.md*
