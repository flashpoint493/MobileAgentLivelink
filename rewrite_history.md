# Git 历史重写指南

## 目标
移除提交 `8e59882` 和 `65b27f6` 中的真实 IP 地址。

## 方法：使用交互式 Rebase

### 步骤 1: 开始交互式 Rebase

```bash
# 从包含敏感信息之前的提交开始 rebase
git rebase -i 9b873d6
```

### 步骤 2: 在编辑器中

将包含敏感信息的提交标记为 `edit`:
- `8e59882` → 改为 `edit`
- `65b27f6` → 改为 `edit`

其他提交保持 `pick`。

### 步骤 3: 编辑每个提交

当 rebase 停在 `8e59882` 时：

```bash
# 修复 docs/DEPLOYMENT.md 中的 IP 地址
# 使用占位符替换真实 IP
# 然后：
git add docs/DEPLOYMENT.md
git commit --amend --no-edit
git rebase --continue
```

当 rebase 停在 `65b27f6` 时：

```bash
# 修复 pc-client/config.py 中的 IP 地址
# 使用占位符替换真实 IP
# 然后：
git add pc-client/config.py
git commit --amend --no-edit
git rebase --continue
```

### 步骤 4: 完成

完成后，所有后续提交的 hash 会改变，但内容已经修复。

## 自动化脚本（可选）

如果需要自动化，可以使用 git filter-branch，但更复杂。
