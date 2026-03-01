---
name: triton-skill
description: "Write, debug, and optimize Triton and Gluon GPU kernels using local source code, tutorials, and kernel references. Use when the user mentions Triton, Gluon, tl.load, tl.store, tl.dot, triton.jit, gluon.jit, wgmma, tcgen05, TMA, tensor descriptor, persistent kernel, warp specialization, fused attention, matmul kernel, kernel fusion, tl.program_id, triton autotune, MXFP, FP8, FP4, block-scaled matmul, SwiGLU, top-k, or asks about writing GPU kernels in Python."
---

# Triton & Gluon Kernel Development

## Source Code Locations

Triton 源码本地路径（由 install.sh 从 GitHub clone）:

**TRITON_REPO**: `~/.cursor/skills/triton-skill/repos/triton/`

如果该路径不存在，运行:

```bash
# 在 cursor-gpu-skills 项目目录下运行
bash update-repos.sh triton
```

所有搜索路径基于 `TRITON_REPO` 变量。使用 Grep 工具时，将 `TRITON_REPO` 替换为实际绝对路径。
可通过以下命令获取实际路径:

```bash
readlink -f ~/.cursor/skills/triton-skill/repos/triton
```

### Triton Tutorials (入门到进阶)

```
TRITON_REPO/python/tutorials/
├── 01-vector-add.py             # Triton 基础: @triton.jit, program_id, load/store
├── 02-fused-softmax.py          # 内核融合, reduction, tl.max/tl.sum/tl.exp
├── 03-matrix-multiplication.py  # Block matmul, L2 cache, @triton.autotune
├── 04-low-memory-dropout.py     # 并行 PRNG, tl.rand, seed-based dropout
├── 05-layer-norm.py             # Backward pass, atomic ops, tl.atomic_cas
├── 06-fused-attention.py        # Flash Attention v2, causal mask, FP8, warp spec
├── 07-extern-functions.py       # libdevice 外部函数调用
├── 08-grouped-gemm.py           # Group GEMM, TMA, tensor descriptors
├── 09-persistent-matmul.py      # 持久化内核, TMA, warp specialization, FP8
├── 10-block-scaled-matmul.py    # FP4/FP8, MXFP4, tl.dot_scaled
└── 11-programmatic-dependent-launch.py  # PDL, gdc_wait, gdc_launch_dependents
```

### Gluon Tutorials (底层 GPU 编程)

```
TRITON_REPO/python/tutorials/gluon/
├── 01-intro.py                  # Gluon vs Triton, tile-based SPMD, @gluon.jit
├── 02-layouts.py                # BlockedLayout, size_per_thread, warps_per_cta
├── 03-async-copy.py             # cp.async, 流水线, shared memory
├── 04-tma.py                    # Tensor Memory Accelerator, tensor desc, mbarrier
├── 05-wgmma.py                  # Warp-Group MMA, Hopper Tensor Core, async MMA
├── 06-tcgen05.py                # Blackwell Tensor Core, Tensor Memory, tcgen05_mma
├── 07-persistence.py            # 持久化内核, work assignment, 多级流水线
├── 08-warp-specialization.py    # Warp 特化, 任务重叠
├── 09-tma-gather-scatter.py     # Native TMA Gather/Scatter (Blackwell)
├── 10-tcgen05-copy.py           # tcgen05_copy, shared→tensor memory
├── 11-tcgen05-mma-scaled.py     # tcgen05_mma_scaled, nvfp4/mxfp4/mxfp8
└── 12-cluster-launch-control.py # CLC, 动态 work distribution
```

### Gluon Examples (完整实现)

```
TRITON_REPO/python/examples/gluon/
└── 01-attention-forward.py      # Flash Attention forward (Blackwell)
                                 # 完整的 producer/consumer, TMA, tcgen05_mma
```

### Triton Kernels (生产级参考实现)

```
TRITON_REPO/python/triton_kernels/triton_kernels/
├── matmul.py                    # 矩阵乘法 API (融合激活/MoE/ragged)
├── matmul_details/
│   ├── _matmul.py               # Dense GEMM kernel (TMA, mxfp4/8)
│   ├── _p_matmul.py             # Persistent GEMM kernel (ragged TMA)
│   └── _common.py               # 偏移计算, XCD swizzle
├── reduce.py                    # Reduction kernel (mask/scale/mxfp/flexpoint)
├── topk.py                      # Top-K selection (forward/backward, bitmatrix)
├── swiglu.py                    # SwiGLU activation kernel
├── compaction.py                # Masked compaction kernel
├── numerics.py                  # FP8/MXFP 数值配置
├── numerics_details/
│   ├── mxfp.py                  # MXFP 量化/反量化
│   └── flexpoint.py             # Flexpoint 缩放
├── tensor.py                    # Tensor/Layout 抽象 (TMA descriptors)
├── tensor_details/
│   └── layout_details/          # Blackwell/Hopper/CDNA4 MX 布局
├── distributed.py               # 分布式 MoE, SymmetricMemory
├── testing.py                   # 测试工具 (assert_close, compute_sanitizer)
└── roofline.py                  # Roofline 性能分析
```

### Triton 语言源码

```
TRITON_REPO/python/triton/language/           # tl.* 操作的定义和语义
TRITON_REPO/python/triton/experimental/gluon/ # gluon.* 操作的定义
TRITON_REPO/python/triton/runtime/            # JIT 编译, 缓存, 解释器
TRITON_REPO/python/triton/compiler/           # 代码生成
TRITON_REPO/python/triton/tools/              # Tensor descriptor 工具
```

### C++ 编译器 (IR 定义和 Passes)

```
TRITON_REPO/include/triton/
├── Dialect/
│   ├── Triton/           # Triton IR dialect 定义 (.td, .h)
│   ├── TritonGPU/        # TritonGPU dialect (layouts, encodings)
│   ├── TritonNvidiaGPU/  # NVIDIA 特定 ops (wgmma, tma, tcgen05)
│   └── Gluon/            # Gluon dialect
├── Conversion/           # IR lowering passes (TritonGPU -> LLVM)
├── Analysis/             # Alias, Allocation, AxisInfo, Membar
└── Tools/                # 工具类

TRITON_REPO/lib/
├── Dialect/
│   ├── Triton/           # Triton ops 实现, canonicalize
│   ├── TritonGPU/        # GPU layout 优化 passes
│   ├── TritonNvidiaGPU/  # NVIDIA lowering
│   └── Gluon/            # Gluon ops 实现
├── Conversion/           # Lowering pass 实现 (TritonGPU -> LLVM IR)
├── Analysis/             # 分析 pass 实现
└── Target/               # 代码生成目标
```

## Search Strategy

**用 Grep 工具搜索**，不要整文件加载。

先确定 TRITON_REPO 的实际路径，然后用绝对路径搜索。

### Triton API 用法

```bash
# 设置路径变量（替换为实际路径）
TRITON_REPO="$HOME/.cursor/skills/triton-skill/repos/triton"

# 查找 tl.dot 的使用方式
rg "tl\.dot" $TRITON_REPO/python/tutorials/

# 查找 autotune 配置示例
rg "@triton.autotune" $TRITON_REPO/python/tutorials/

# 查找 tensor descriptor 创建
rg "TensorDescriptor" $TRITON_REPO/python/tutorials/

# 查找特定 tl 操作的定义
rg "def (load|store|dot)" $TRITON_REPO/python/triton/language/
```

### Gluon API 用法

```bash
# 查找 gluon.jit 使用
rg "@gluon.jit" $TRITON_REPO/python/tutorials/gluon/

# 查找 wgmma 用法
rg "wgmma" $TRITON_REPO/python/tutorials/gluon/05-wgmma.py

# 查找 tcgen05 用法 (Blackwell)
rg "tcgen05" $TRITON_REPO/python/tutorials/gluon/

# 查找 TMA 异步拷贝模式
rg "async_copy" $TRITON_REPO/python/tutorials/gluon/

# 查找 mbarrier 使用
rg "mbarrier" $TRITON_REPO/python/tutorials/gluon/
```

### 编译器 IR 和 Passes

```bash
# 查找 Triton IR op 定义 (TableGen)
rg "def.*Op" $TRITON_REPO/include/triton/Dialect/Triton/IR/

# 查找 TritonGPU layout encoding
rg "Encoding" $TRITON_REPO/include/triton/Dialect/TritonGPU/IR/

# 查找 NVIDIA 特定 ops (wgmma, tma)
rg "wgmma\|tma\|tcgen05" $TRITON_REPO/include/triton/Dialect/TritonNvidiaGPU/

# 查找 lowering pass 实现
rg "Pattern\|Rewrite" $TRITON_REPO/lib/Conversion/TritonGPUToLLVM/

# 查找 Gluon dialect ops
rg "def.*Op" $TRITON_REPO/include/triton/Dialect/Gluon/

# 查找特定 pass (如 coalesce, pipeline, prefetch)
rg "coalesce\|pipeline\|prefetch" $TRITON_REPO/lib/Dialect/TritonGPU/Transforms/
```

### 生产内核参考

```bash
# 查找 matmul 内核的 TMA 使用
rg "tma" $TRITON_REPO/python/triton_kernels/triton_kernels/matmul_details/

# 查找 MXFP 量化实现
rg "mxfp" $TRITON_REPO/python/triton_kernels/triton_kernels/numerics_details/

# 查找 persistent kernel 模式
rg "persistent" $TRITON_REPO/python/triton_kernels/triton_kernels/matmul_details/_p_matmul.py

# 查找 layout swizzle
rg "swizzle" $TRITON_REPO/python/triton_kernels/triton_kernels/tensor_details/layout_details/
```

## When to Use Each Source

| Need | Source | Path |
|------|--------|------|
| Triton 基础语法和模式 | Tutorials 01-05 | `python/tutorials/01-*.py` ~ `05-*.py` |
| 矩阵乘法优化 | Tutorial 03, 09, 10 | `python/tutorials/03-*.py`, `09-*.py`, `10-*.py` |
| Attention 内核 | Tutorial 06, Gluon example | `python/tutorials/06-*.py`, `python/examples/gluon/` |
| Gluon 入门 | Gluon tutorials 01-02 | `python/tutorials/gluon/01-intro.py`, `02-layouts.py` |
| TMA 异步拷贝 | Gluon tutorials 03-04 | `python/tutorials/gluon/03-*.py`, `04-*.py` |
| WGMMA (Hopper) | Gluon tutorial 05 | `python/tutorials/gluon/05-wgmma.py` |
| tcgen05 (Blackwell) | Gluon tutorials 06, 10, 11 | `python/tutorials/gluon/06-*.py`, `10-*.py`, `11-*.py` |
| 持久化内核模式 | Gluon tutorial 07 | `python/tutorials/gluon/07-persistence.py` |
| Warp 特化模式 | Gluon tutorial 08 | `python/tutorials/gluon/08-warp-specialization.py` |
| FP4/FP8/MXFP 量化 | Tutorial 10, triton_kernels | `python/tutorials/10-*.py`, `triton_kernels/numerics_details/` |
| 生产级 GEMM | triton_kernels matmul | `triton_kernels/triton_kernels/matmul_details/` |
| MoE / Ragged tensor | triton_kernels | `triton_kernels/triton_kernels/distributed.py`, `tensor_details/ragged_tensor.py` |
| Top-K / SwiGLU 内核 | triton_kernels | `triton_kernels/triton_kernels/topk.py`, `swiglu.py` |
| Roofline 性能分析 | triton_kernels | `triton_kernels/triton_kernels/roofline.py` |
| tl.* 操作语义/签名 | Language source | `python/triton/language/` |
| 布局和 swizzle | triton_kernels layouts | `triton_kernels/triton_kernels/tensor_details/layout_details/` |
| Triton IR op 定义 | include | `include/triton/Dialect/Triton/IR/` |
| GPU layout encoding | include | `include/triton/Dialect/TritonGPU/IR/` |
| NVIDIA ops (wgmma/tma) | include | `include/triton/Dialect/TritonNvidiaGPU/` |
| Gluon dialect 定义 | include | `include/triton/Dialect/Gluon/` |
| 编译 pass 实现 | lib | `lib/Dialect/TritonGPU/Transforms/` |
| IR lowering (GPU->LLVM) | lib | `lib/Conversion/TritonGPUToLLVM/` |

## Triton Kernel 编写模式

### 基本模式

```python
import triton
import triton.language as tl

@triton.jit
def kernel(x_ptr, y_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements
    x = tl.load(x_ptr + offsets, mask=mask)
    y = x * 2  # 计算
    tl.store(y_ptr + offsets, y, mask=mask)

# 启动
grid = lambda meta: (triton.cdiv(n, meta['BLOCK_SIZE']),)
kernel[grid](x, y, n, BLOCK_SIZE=1024)
```

### Autotune 模式

```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 64}, num_stages=3, num_warps=8),
        triton.Config({'BLOCK_M': 64, 'BLOCK_N': 256, 'BLOCK_K': 32}, num_stages=4, num_warps=4),
    ],
    key=['M', 'N', 'K'],
)
@triton.jit
def matmul_kernel(a_ptr, b_ptr, c_ptr, M, N, K, ...):
    ...
```

参考 `python/tutorials/03-matrix-multiplication.py` 获取完整 autotune matmul 示例。

### Gluon 基本模式

```python
from triton.experimental import gluon

@gluon.jit
def kernel(x: gluon.tensor[M, N, tl.float16]):
    # 直接使用 tile 操作
    y = x + 1.0
    return y
```

参考 `python/tutorials/gluon/01-intro.py` 获取 Gluon 入门示例。

## 常见问题排查

| 问题 | 可能原因 | 查找参考 |
|------|---------|---------|
| tl.dot 结果错误 | 输入类型不匹配 (需要 float16/bfloat16) | `rg "tl.dot" tutorials/03-*.py` |
| CUDA OOM | BLOCK_SIZE 过大, num_stages 过多 | `rg "num_stages" tutorials/09-*.py` |
| autotune 无效 | key 参数未对齐实际变化维度 | `rg "key=" tutorials/03-*.py` |
| TMA descriptor 错误 | tensor 不连续或维度不匹配 | `rg "TensorDescriptor" tutorials/gluon/04-*.py` |
| wgmma 精度问题 | 需要 float32 累加器 | `rg "accumulator" tutorials/gluon/05-wgmma.py` |
| 性能低 | 未用 persistent kernel 或 warp spec | `tutorials/gluon/07-persistence.py`, `08-warp-specialization.py` |

## Triton 编译和调试

```bash
# 查看生成的 PTX
TRITON_PRINT_AUTOTUNING=1 python your_script.py

# 启用 IR dump
MLIR_ENABLE_DUMP=1 python your_script.py

# 使用 Triton 的 compute-sanitizer
from triton_kernels.testing import compute_sanitizer
# 参考: python/triton_kernels/triton_kernels/testing.py

# 性能分析
from triton_kernels.roofline import compute_roofline
# 参考: python/triton_kernels/triton_kernels/roofline.py
```

## 更新 Triton 源码

```bash
# 在 cursor-gpu-skills 项目目录下
bash update-repos.sh triton
```

## Additional References

- Triton 官方文档: https://triton-lang.org
- Triton Language API: `TRITON_REPO/python/triton/language/`
- Gluon Experimental API: `TRITON_REPO/python/triton/experimental/gluon/`
