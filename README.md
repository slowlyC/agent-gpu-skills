# cursor-gpu-skills

Cursor IDE 的 GPU 开发 Skill 集合，目前包含四个 Skill:

| Skill | 层级 | 使用场景 |
|:------|:-----|:---------|
| **cuda-skill** | 底层 (PTX/CUDA C++) | 查 PTX 指令、CUDA API、Programming Guide，nsys/ncu 分析 |
| **triton-skill** | 高层 (Python DSL) | 写 Triton/Gluon 内核，查教程和示例 |
| **cutlass-skill** | 中间层 (C++/CuTeDSL) | 写 CUTLASS/CuTe kernel，查 CuTeDSL 示例 |
| **sglang-skill** | 应用层 (LLM Serving) | SGLang 推理引擎开发，KV cache、Attention backend |

## 安装

```bash
git clone https://github.com/slowlyC/cursor-gpu-skills.git
cd cursor-gpu-skills

# 1. 获取外部源码 repo (sparse checkout, ~114MB)
bash update-repos.sh

# 2. 安装 skill 到 ~/.cursor/skills/
bash install.sh
```

脚本会创建软链接到 `~/.cursor/skills/`，自动同步更新。详细安装说明参考 [INSTALL.md](INSTALL.md)。

## 目录结构

```
cursor-gpu-skills/
├── README.md
├── INSTALL.md                       # 详细安装指南
├── install.sh                       # 安装脚本 (创建软链接到 ~/.cursor/skills/)
├── update-repos.sh                  # 克隆/更新外部 repo (triton, cutlass, sglang)
├── scrape_docs.py                   # 文档爬虫 (uv script)
├── cuda_skill/
│   ├── SKILL.md
│   └── references/                  # CUDA 文档库 (~700 files)
├── triton_skill/
│   ├── SKILL.md
│   ├── quick-reference.md
│   └── repos/triton/                # sparse checkout (~8MB, .gitignore)
├── cutlass_skill/
│   ├── SKILL.md
│   └── repos/cutlass/               # sparse checkout (~62MB, .gitignore)
└── sglang_skill/
    ├── SKILL.md
    └── repos/sglang/                # sparse checkout (~44MB, .gitignore)
```

`repos/` 目录通过 `.gitignore` 排除，用 `bash update-repos.sh` 重建。

## cuda-skill

NVIDIA CUDA 全套文档转换为可搜索的 Markdown:

| 文档 | 文件数 | 大小 | 来源 |
|:-----|:-------|:-----|:-----|
| PTX ISA 9.1 完整规范 | 405 | 2.3MB | [NVIDIA PTX ISA](https://docs.nvidia.com/cuda/parallel-thread-execution/) |
| PTX 精简参考 | 13 | 149KB | [triton/.claude/knowledge](https://github.com/facebookexperimental/triton) |
| CUDA Runtime API 13.1 | 107 | 0.9MB | [NVIDIA Runtime API](https://docs.nvidia.com/cuda/cuda-runtime-api/) |
| CUDA Driver API 13.1 | 128 | 0.8MB | [NVIDIA Driver API](https://docs.nvidia.com/cuda/cuda-driver-api/) |
| CUDA Programming Guide v13.1 | 39 | 1.6MB | [NVIDIA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/) |
| CUDA C++ Best Practices Guide | 73 | 585KB | [NVIDIA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) |
| Nsight Compute 文档 | 9 | 741KB | [NVIDIA Nsight Compute](https://docs.nvidia.com/nsight-compute/) |
| Nsight Systems 文档 | 5 | 833KB | [NVIDIA Nsight Systems](https://docs.nvidia.com/nsight-systems/) |
| 工具指南 (nsys/ncu/debug) | 6 | - | 手写参考 |

文档通过 `scrape_docs.py` 管理，用 `uv run scrape_docs.py all --force` 更新。

## triton-skill

直接引用 Triton 源码中的教程、示例和内核实现:

| 内容 | 路径 | 说明 |
|:-----|:-----|:-----|
| Triton 教程 (01-11) | `triton/python/tutorials/` | 从 vector add 到 block-scaled matmul |
| Gluon 教程 (01-12) | `triton/python/tutorials/gluon/` | layouts, TMA, wgmma, tcgen05, warp spec |
| Gluon 示例 | `triton/python/examples/gluon/` | Flash Attention (Blackwell) |
| 生产级内核 | `triton/python/triton_kernels/` | matmul, reduce, top-k, SwiGLU, MXFP |
| 语言定义 | `triton/python/triton/language/` | tl.* 操作语义 |

## cutlass-skill

引用 CUTLASS 源码:

| 内容 | 路径 |
|:-----|:-----|
| CuTeDSL Python 教程 | `cutlass/python/CuTeDSL/` |
| CuTe Python bindings | `cutlass/python/pycute/` |
| CUTLASS C++ 示例 | `cutlass/examples/` |
| CuTe 头文件 | `cutlass/include/cute/` |

## sglang-skill

引用 SGLang 源码:

| 内容 | 路径 |
|:-----|:-----|
| SRT 推理引擎 | `sglang/python/sglang/srt/` |
| JIT 内核 | `sglang/python/sglang/jit_kernel/` |
| SGL-Kernel (CUDA) | `sglang/sgl-kernel/` |

## 致谢

cuda-skill 的文档爬取方案受 [technillogue/ptx-isa-markdown](https://github.com/technillogue/ptx-isa-markdown) 启发。

## 许可

CUDA 文档内容 (c) NVIDIA Corporation. Triton、CUTLASS、SGLang 源码遵循其各自原始许可.
