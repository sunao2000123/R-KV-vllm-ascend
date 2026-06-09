# Codex 自动化测试反馈循环 SOP

本文档描述在 `sunao2000123/R-KV-vllm-ascend` 这个 fork 仓库里跑
"测试报错 → AI 修复 → 服务器再跑" 双端循环的完整流程。

## 1. 拓扑

```
┌──────────────────────┐                ┌──────────────────────┐
│ 服务器（跑测试）      │                │ 你的 Mac（AI 协作）   │
│                      │                │                      │
│ - 代码 clone 在此    │                │ - launchd 后台守护   │
│ - 真机 NPU / GPU     │                │ - 每 30s poll issue   │
│ - 报错时复制粘贴到    │ ───issue 评论──>│   评论               │
│   GitHub issue 评论  │                │ - AI 读评论改代码     │
│ - git pull 拉 commit │ <───commit──── │ - git push           │
│ - 再跑测试           │                │                      │
└──────────────────────┘                └──────────────────────┘
        ↕                                          ↕
        └────── GitHub: sunao2000123/R-KV-vllm-ascend ──────┘
              - Issue #1 "Codex 自动化测试反馈监控"
              - Branch: codex/issue-1-feedback
```

**关键不变量**：

- AI **永不**直接连服务器。服务器报错只能由你"手动"复制粘贴到 issue。
- AI **只能** push commit 到 GitHub。服务器**只能** `git pull` 拉。
- 唯一**双向**通信介质 = **GitHub Issue #1 的评论区**。

## 2. 一次性环境准备

### 2.1 服务器端
```bash
git clone git@github.com:sunao2000123/R-KV-vllm-ascend.git
cd R-KV-vllm-ascend
git checkout codex/issue-1-feedback
# 日常：git pull → 跑测试 → 报错复制粘贴
```

### 2.2 Mac 端
```bash
# 1. 装 gh CLI（一次性）
brew install gh
gh auth login   # 跟着向导，token 存钥匙串

# 2. 注册 feedback-monitor launchd 守护进程（一次性）
cd ~/Projects/R-KV-vllm-ascend
./tools/feedback-monitor/install_launchd.sh

# 3. 验证
launchctl list | grep feedback-monitor
tail -f .tmp/feedback-monitor/monitor.log
```

### 2.3 GitHub 端
- 在 `sunao2000123/R-KV-vllm-ascend` 创建 issue：
  - 标题：`Codex 自动化测试反馈监控`
  - 正文：
    ```
    这个 Issue 用于接收真实环境中的自动化测试反馈。

    请在评论中提供：
    - 失败现象或测试输出
    - 复现步骤
    - 期望行为
    - 相关环境信息
    ```
  - 记下 issue 编号（如 #1）

## 3. 一次完整循环

### 第 1 步：服务器报错

```bash
# 在服务器
pytest tests/test_rkv.py 2>&1 | tee /tmp/last_test.log
# 或
python -m vllm.entrypoints.openai.api_server ...
# 复制最后 ~50 行报错
```

### 第 2 步：你把报错贴到 issue 评论

去 https://github.com/sunao2000123/R-KV-vllm-ascend/issues/1
粘贴报错。**格式建议**：

```
[服务器] hostname=ascend-bj-1  commit=<git rev-parse HEAD>
[命令] pytest tests/test_rkv.py -x
[错误]
... (粘贴 stack trace) ...
[期望] step=5 should_compress=True 真的压缩
```

### 第 3 步：AI 拉评论

守护进程会在 30s 内检测到新评论，并写一行：
```
NEW_COMMENT repo=sunao2000123/R-KV-vllm-ascend issue=1 id=... author=sunao2000123 url=...
  body_preview: ...
```

**你**打开新的 Cursor AI 对话，把这条 `NEW_COMMENT` 贴进去，或者直接说
"我刚在 issue #1 发了新评论，去拉一下"。AI 读 `.tmp/feedback-monitor/updates.json` 拿到完整内容。

### 第 4 步：AI 改代码 + push

AI 在 `~/Projects/R-KV-vllm-ascend/` 里改代码、跑 verify_dependencies.py / 单元测试
（**注意：真机 NPU 部署测试只能在服务器上跑，本地只能跑逻辑测试**）、
commit、push（用 `gh-push-troubleshoot` skill 走 SSH）。

### 第 5 步：服务器拉

```bash
cd R-KV-vllm-ascend
git pull
pytest tests/test_rkv.py 2>&1 | tee /tmp/last_test.log
```

回到第 1 步。如果通过，AI 会在 issue 下回复"已修复 commit=xxx，建议服务器
重新部署"。如果还报错，回到第 2 步贴新日志。

## 4. 失败模式 / 排错

| 现象 | 原因 | 修复 |
|---|---|---|
| daemon 启动后立刻退出 | `gh` 没登录 | `gh auth login` |
| daemon 启动后立刻退出 | issue 编号错了 | 改 plist `--issue` 后 `install_launchd.sh` 重装 |
| 评论贴了但 daemon 没检测到 | GitHub 还没索引新评论 | 等等，或 `./run_once.sh` 手动跑一次 |
| `git push` 失败"127.0.0.1:7890" | 死代理，按 `gh-push-troubleshoot` skill 走 SSH |
| 守护进程 30s 一次但你嫌慢 | 改 `FEEDBACK_MONITOR_POLL=10` 环境变量，重装 plist |

## 5. 配套 Skill

| Skill | 路径 | 作用 |
|---|---|---|
| `gh-issue-comment-monitor` | `~/.cursor/skills-cursor/` + 项目内 `.cursor/skills/` | 拉评论、checkpoint 推进 |
| `gh-push-troubleshoot` | `~/.cursor/skills-cursor/` | push 失败时自动恢复 SSH 链路 |

两者都不修改 GitHub——前者只读，后者只诊断+建议。
