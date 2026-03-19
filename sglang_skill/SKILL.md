---
name: sglang-skill
description: "Develop, debug, and optimize SGLang LLM serving engine. Use when the user mentions SGLang, sglang, srt, sgl-kernel, LLM serving, model inference, KV cache, attention backend, FlashInfer backend, MLA, MoE routing, MoE dispatch, expert parallelism SGLang, speculative decoding, disaggregated serving, TP/PP/EP, radix cache, continuous batching, chunked prefill, CUDA graph SGLang, model loading, quantization FP8/GPTQ/AWQ, JIT kernel, triton kernel SGLang, DeepSeek serving, EPLB (expert load balancing), HiCache, launch_server, sglang Engine API, LoRA inference, torch.compile SGLang, or asks about serving LLMs with SGLang. Also use when the user wants to add a new model to SGLang, add a new attention backend, debug SGLang serving issues, or optimize SGLang throughput/latency."
---

# SGLang Development

## Source Code Locations

SGLang 源码位于此 skill 安装目录下的 `repos/sglang/`。
实际路径取决于所用工具:
- Cursor: `~/.cursor/skills/sglang-skill/repos/sglang/`
- Claude Code: `~/.claude/skills/sglang-skill/repos/sglang/`
- Codex: `~/.agents/skills/sglang-skill/repos/sglang/`

**SGLANG_REPO**: 下文示例用 `~/.cursor/skills/sglang-skill/repos/sglang/` 作占位符，**替换为实际路径**。

如果该路径不存在，在项目目录下运行 `bash update-repos.sh sglang`。

### Core Runtime (SRT)

```
SGLANG_REPO/python/sglang/srt/
├── layers/
│   ├── attention/          # Attention backends
│   │   ├── flashinfer_backend.py      # FlashInfer (默认)
│   │   ├── flashinfer_mla_backend.py  # FlashInfer MLA (DeepSeek)
│   │   ├── cutlass_mla_backend.py     # CUTLASS MLA
│   │   ├── flashattention_backend.py  # FlashAttention
│   │   ├── triton_backend.py          # Triton attention
│   │   ├── flashmla_backend.py        # FlashMLA
│   │   ├── nsa_backend.py             # Native Sparse Attention
│   │   ├── tbo_backend.py             # TBO
│   │   ├── fla/                       # Flash Linear Attention
│   │   ├── triton_ops/                # Triton attention ops
│   │   └── wave_ops/                  # Wave attention ops
│   ├── moe/                # MoE routing and dispatch
│   ├── quantization/       # FP8, GPTQ, AWQ, Marlin, etc.
│   ├── deep_gemm_wrapper/  # DeepGEMM 集成
│   └── utils/
├── models/                 # 模型实现 (LLaMA, DeepSeek, Qwen, etc.)
│   └── deepseek_common/    # DeepSeek V2/V3 共享组件
├── managers/               # Scheduler, TokenizerManager, Detokenizer
├── mem_cache/              # KV cache, Radix cache
├── model_executor/         # 模型执行器, forward batch
├── model_loader/           # 模型加载, 权重映射
├── entrypoints/            # 启动入口: Engine, OpenAI API server
├── speculative/            # Speculative decoding
├── disaggregation/         # Disaggregated prefill/decode
├── distributed/            # TP/PP/EP 分布式
├── compilation/            # CUDA Graph, Torch.compile
├── configs/                # 模型配置
├── lora/                   # LoRA 推理
├── eplb/                   # Expert-level load balancing
├── hardware_backend/       # 硬件适配 (CUDA, ROCm, XPU)
└── utils/                  # 工具函数
```

### JIT Kernels (Python CUDA/Triton Kernels)

```
SGLANG_REPO/python/sglang/jit_kernel/
├── flash_attention/        # Flash Attention 自定义实现
├── flash_attention_v4.py   # Flash Attention v4
├── cutedsl_gdn.py          # CuTeDSL GDN kernel
├── concat_mla.py           # MLA concat kernel
├── norm.py                 # Normalization kernels
├── rope.py                 # RoPE position encoding
├── pos_enc.py              # Position encoding
├── per_tensor_quant_fp8.py # FP8 量化
├── kvcache.py              # KV cache kernels
├── hicache.py              # HiCache kernels
├── gptq_marlin.py          # GPTQ Marlin kernel
├── cuda_wait_value.py      # CUDA sync primitives
└── diffusion/              # Diffusion model kernels
```

### sgl-kernel (C++/CUDA Custom Kernels)

```
SGLANG_REPO/sgl-kernel/
├── csrc/
│   ├── attention/          # Custom attention CUDA kernels
│   ├── cutlass_extensions/ # CUTLASS GEMM extensions
│   ├── gemm/               # GEMM kernels
│   ├── moe/                # MoE dispatch/combine kernels
│   ├── quantization/       # Quantization CUDA kernels
│   ├── allreduce/          # AllReduce CUDA kernels
│   ├── speculative/        # Speculative decoding kernels
│   ├── kvcacheio/          # KV cache I/O
│   ├── mamba/              # Mamba SSM kernels
│   ├── memory/             # Memory management
│   └── grammar/            # Grammar-guided generation
├── include/                # C++ headers
├── python/                 # Python bindings
├── tests/                  # Kernel tests
└── benchmark/              # Kernel benchmarks
```

### Frontend Language

```
SGLANG_REPO/python/sglang/lang/   # SGLang 前端 DSL
SGLANG_REPO/examples/             # 使用示例
SGLANG_REPO/benchmark/            # 性能基准
SGLANG_REPO/test/                 # 测试套件
SGLANG_REPO/docs/                 # 文档
```

## Search Strategy

**用 Grep 工具搜索**，不要整文件加载。

### Attention 和 MLA

```bash
SGLANG_REPO="$HOME/.cursor/skills/sglang-skill/repos/sglang"

# 查找 attention backend 注册
rg "register\|Backend" $SGLANG_REPO/python/sglang/srt/layers/attention/attention_registry.py

# 查找 FlashInfer MLA 实现
rg "forward\|mla" $SGLANG_REPO/python/sglang/srt/layers/attention/flashinfer_mla_backend.py

# 查找 CUTLASS MLA
rg "cutlass\|mla" $SGLANG_REPO/python/sglang/srt/layers/attention/cutlass_mla_backend.py

# 查找 attention 通用接口
rg "class.*Backend\|def forward" $SGLANG_REPO/python/sglang/srt/layers/attention/base_attn_backend.py
```

### Scheduler 和 Batching

```bash
# Scheduler 核心逻辑
rg "class Scheduler\|def get_next_batch" $SGLANG_REPO/python/sglang/srt/managers/

# Continuous batching 和 chunked prefill
rg "chunk\|prefill\|extend" $SGLANG_REPO/python/sglang/srt/managers/

# CUDA Graph
rg "cuda_graph\|CudaGraph" $SGLANG_REPO/python/sglang/srt/compilation/
```

### KV Cache 和 Memory

```bash
# Radix cache 实现
rg "RadixCache\|radix" $SGLANG_REPO/python/sglang/srt/mem_cache/

# KV cache 管理
rg "class.*Pool\|allocate\|free" $SGLANG_REPO/python/sglang/srt/mem_cache/

# HiCache (hierarchical cache)
rg "HiCache\|hicache" $SGLANG_REPO/python/sglang/srt/mem_cache/
```

### 模型相关

```bash
# 查找特定模型实现
rg "class.*ForCausalLM" $SGLANG_REPO/python/sglang/srt/models/

# DeepSeek V2/V3 实现
rg "DeepSeek\|MLA\|MoE" $SGLANG_REPO/python/sglang/srt/models/deepseek_v2.py

# 模型加载和权重映射
rg "load_weight\|weight_map" $SGLANG_REPO/python/sglang/srt/model_loader/
```

### MoE

```bash
# MoE routing
rg "TopK\|router\|expert" $SGLANG_REPO/python/sglang/srt/layers/moe/

# MoE CUDA kernels
rg "moe" $SGLANG_REPO/sgl-kernel/csrc/moe/
```

### 量化

```bash
# FP8 量化
rg "fp8\|float8" $SGLANG_REPO/python/sglang/srt/layers/quantization/

# GPTQ/AWQ/Marlin
rg "gptq\|awq\|marlin" $SGLANG_REPO/python/sglang/srt/layers/quantization/
```

### Speculative Decoding

```bash
rg "speculative\|draft\|verify" $SGLANG_REPO/python/sglang/srt/speculative/
```

### 分布式

```bash
# TP/PP/EP
rg "tensor_parallel\|pipeline_parallel\|expert_parallel" $SGLANG_REPO/python/sglang/srt/distributed/

# Disaggregated serving
rg "disagg\|prefill_worker\|decode_worker" $SGLANG_REPO/python/sglang/srt/disaggregation/
```

## When to Use Each Source

| Need | Source | Path |
|------|--------|------|
| Attention backend 接口 | SRT layers | `srt/layers/attention/base_attn_backend.py` |
| FlashInfer attention | SRT layers | `srt/layers/attention/flashinfer_backend.py` |
| MLA (DeepSeek) | SRT layers | `srt/layers/attention/*mla*.py` |
| MoE routing/dispatch | SRT layers | `srt/layers/moe/` |
| 量化 (FP8/GPTQ/AWQ) | SRT layers | `srt/layers/quantization/` |
| Scheduler | SRT managers | `srt/managers/` |
| KV cache / Radix cache | SRT mem_cache | `srt/mem_cache/` |
| 模型实现 | SRT models | `srt/models/` |
| DeepSeek V2/V3 | SRT models | `srt/models/deepseek_v2.py`, `deepseek_common/` |
| Speculative decoding | SRT speculative | `srt/speculative/` |
| Disaggregated serving | SRT disagg | `srt/disaggregation/` |
| TP/PP/EP 分布式 | SRT distributed | `srt/distributed/` |
| CUDA Graph | SRT compilation | `srt/compilation/` |
| 模型加载 | SRT model_loader | `srt/model_loader/` |
| 启动入口 | SRT entrypoints | `srt/entrypoints/` |
| JIT Triton kernels | jit_kernel | `jit_kernel/` |
| Custom CUDA kernels | sgl-kernel | `sgl-kernel/csrc/` |
| CUTLASS extensions | sgl-kernel | `sgl-kernel/csrc/cutlass_extensions/` |
| 前端 DSL | lang | `python/sglang/lang/` |
| 使用示例 | examples | `examples/` |

## 常见开发场景

### 添加新 Attention Backend

1. 继承 `base_attn_backend.py` 中的 `AttnBackend`
2. 实现 `forward()` 方法
3. 在 `attention_registry.py` 注册
4. 参考 `flashinfer_backend.py` 作为模板

### 添加新模型

1. 在 `srt/models/` 创建模型文件
2. 实现 `ForCausalLM` 类
3. 实现 `load_weights()` 方法
4. 参考 `srt/models/llama.py` 作为模板

### 添加新量化方法

1. 在 `srt/layers/quantization/` 添加量化模块
2. 注册到量化工厂
3. 参考 `fp8_kernel.py` 或 `gptq.py`

## 启动和调试

```bash
# 启动 OpenAI 兼容 API server
python -m sglang.launch_server --model-path meta-llama/Meta-Llama-3-8B-Instruct --tp 1

# 使用 Engine API (Python)
from sglang import Engine
engine = Engine(model_path="meta-llama/Meta-Llama-3-8B-Instruct")

# Profiling
python -m sglang.launch_server --model-path ... --enable-torch-compile
nsys profile -o report python -m sglang.launch_server ...
```

## 更新 SGLang 源码

```bash
# 在 cursor-gpu-skills 项目目录下
bash update-repos.sh sglang
```

## Additional References

- SGLang 文档: https://docs.sglang.ai/
- GitHub: https://github.com/sgl-project/sglang
