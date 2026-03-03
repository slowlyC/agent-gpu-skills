# 安装指南

## 首次安装

```bash
# 1. 获取源码 repo（sparse checkout 从 GitHub，约 114MB）
bash update-repos.sh

# 2. 安装 skill (默认 Cursor，用 --agent claude/codex/gemini 安装到其他工具)
bash install.sh
```

## 安装目标

```bash
bash install.sh                    # Cursor (默认，已验证)
bash install.sh --agent claude     # Claude Code
bash install.sh --agent codex      # Codex
bash install.sh --agent gemini     # Gemini CLI
```

| 工具 | Skill 安装路径 | 验证状态 | 官方文档 |
|:-----|:---------------|:---------|:---------|
| Cursor | `~/.cursor/skills/` | 已验证 | [Cursor Skills](https://cursor.com/docs/context/skills) |
| Claude Code | `~/.claude/skills/` | 未验证 | [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) |
| Codex | `~/.agents/skills/` | 未验证 | [Codex Skills](https://developers.openai.com/codex/skills) |
| Gemini CLI | `~/.gemini/skills/` | 未验证 | [Gemini CLI Skills](https://geminicli.com/docs/cli/skills/) |

注: SKILL.md 格式是跨工具通用的，但 skill 发现机制和搜索工具的行为可能因工具而异。Cursor 以外的工具如遇问题，建议让对应 AI 协助排查。

## 安装方式

默认使用**混合模式**安装:

- skill 目录: 真实目录（多数工具不识别软链接目录）
- `SKILL.md`: 复制真实文件（多数工具不识别软链接的 SKILL.md）
- 其余文件: 软链接到项目目录（repo、references 等）

使用 `--copy` 进行全量复制（适用于无法软链接的场景）。

## 更新

```bash
# 更新所有源码 repo
bash update-repos.sh

# 只更新某个 repo
bash update-repos.sh triton
bash update-repos.sh cutlass
bash update-repos.sh sglang

# 更新 CUDA 文档库
uv run scrape_docs.py all --force

# 同步 SKILL.md（修改源文件后重新安装）
bash install.sh                    # 或 --agent claude 等
```

## 验证

```bash
bash install.sh   # 安装时自动运行验证
```

## Skill 发现规则

| 层级 | 要求 | 可用软链接 |
|:-----|:-----|:----------|
| skill 目录 | 必须是真实目录 | 否 |
| SKILL.md | 必须是真实文件 | 否 |
| 其他内容 | 无限制 | 是 |

注: 以上规则在 Cursor 上验证通过。其他工具的 SKILL.md 发现和软链接行为可能不同，遇到问题可以让对应工具的 AI 协助排查。
