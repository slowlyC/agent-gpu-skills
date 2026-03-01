# 安装指南

## 首次安装

```bash
cd cursor-gpu-skills

# 1. 获取源码 repo（sparse checkout 从 GitHub，约 114MB）
bash update-repos.sh

# 2. 安装 skill 到 Cursor
bash install.sh
```

## 安装方式

默认使用**混合模式**安装到 `~/.cursor/skills/`:

- skill 目录: 真实目录（Cursor 不识别软链接目录）
- `SKILL.md`: 复制真实文件（Cursor 不识别软链接的 SKILL.md）
- 其余文件: 软链接到项目目录（repo、references 等）

## 目录结构

```
cursor-gpu-skills/              # 项目目录（统一维护）
├── cuda_skill/                 # CUDA/PTX 文档 skill
│   └── references/             # CUDA 文档库 (~6.5MB)
├── triton_skill/               # Triton/Gluon skill
│   └── repos/triton/           # sparse checkout (~8MB)
├── cutlass_skill/              # CUTLASS/CuTeDSL skill
│   └── repos/cutlass/          # sparse checkout (~62MB)
├── sglang_skill/               # SGLang skill
│   └── repos/sglang/           # sparse checkout (~44MB)
├── install.sh                  # 安装到 ~/.cursor/skills/
├── update-repos.sh             # 获取/更新源码 repo
├── scrape_cuda_docs.py         # CUDA 文档爬虫
└── INSTALL.md
```

## 更新

```bash
# 更新所有源码 repo
bash update-repos.sh

# 只更新某个 repo
bash update-repos.sh triton
bash update-repos.sh cutlass
bash update-repos.sh sglang

# 更新 CUDA 文档库
uv run scrape_cuda_docs.py all --force

# 同步 SKILL.md（修改源文件后重新安装）
bash install.sh
```

## 验证

```bash
bash install.sh   # 安装时自动验证 19 项检查
```

## Cursor Skill 发现规则

| 层级 | 要求 | 可用软链接 |
|------|------|-----------|
| skill 目录 | 必须是真实目录 | 否 |
| SKILL.md | 必须是真实文件 | 否 |
| 其他内容 | 无限制 | 是 |
