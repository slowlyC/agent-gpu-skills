# Triton & Gluon Quick Reference

所有路径相对于: `TRITON_REPO` (即 `~/.cursor/skills/triton-skill/repos/triton/`)

## Triton Language 常用操作

| 操作 | 说明 | 示例教程 |
|------|------|---------|
| `tl.load(ptr, mask)` | 从全局内存加载 | `tutorials/01-vector-add.py` |
| `tl.store(ptr, val, mask)` | 写入全局内存 | `tutorials/01-vector-add.py` |
| `tl.dot(a, b)` | 矩阵乘法 (Tensor Core) | `tutorials/03-matrix-multiplication.py` |
| `tl.dot_scaled(a, sa, b, sb)` | Block-scaled matmul (FP4/FP8) | `tutorials/10-block-scaled-matmul.py` |
| `tl.program_id(axis)` | 当前 program 的 ID | `tutorials/01-vector-add.py` |
| `tl.arange(start, end)` | 生成连续整数 | `tutorials/01-vector-add.py` |
| `tl.max(x, axis)` | 归约求最大值 | `tutorials/02-fused-softmax.py` |
| `tl.sum(x, axis)` | 归约求和 | `tutorials/02-fused-softmax.py` |
| `tl.exp(x)` | 指数运算 | `tutorials/02-fused-softmax.py` |
| `tl.rand(seed, offset)` | 伪随机数生成 | `tutorials/04-low-memory-dropout.py` |
| `tl.atomic_cas(ptr, cmp, val)` | 原子比较交换 | `tutorials/05-layer-norm.py` |
| `@triton.autotune` | 自动调优配置 | `tutorials/03-matrix-multiplication.py` |
| `@triton.jit` | JIT 编译装饰器 | `tutorials/01-vector-add.py` |

## Gluon 常用操作

| 操作 | 说明 | 示例教程 |
|------|------|---------|
| `@gluon.jit` | Gluon JIT 装饰器 | `tutorials/gluon/01-intro.py` |
| `BlockedLayout` | Tile 数据布局 | `tutorials/gluon/02-layouts.py` |
| `cp.async` / `async_copy` | 异步内存拷贝 | `tutorials/gluon/03-async-copy.py` |
| `tma.async_copy_*` | TMA 异步传输 | `tutorials/gluon/04-tma.py` |
| `wgmma` | Warp Group MMA (Hopper) | `tutorials/gluon/05-wgmma.py` |
| `tcgen05_mma` | 5th Gen Tensor Core (Blackwell) | `tutorials/gluon/06-tcgen05.py` |
| `tcgen05_copy` | Tensor Memory 拷贝 | `tutorials/gluon/10-tcgen05-copy.py` |
| `tcgen05_mma_scaled` | Block-scaled MMA | `tutorials/gluon/11-tcgen05-mma-scaled.py` |
| `mbarrier` | Memory barrier 同步 | `tutorials/gluon/04-tma.py` |
| `warp_specialize` | Warp 特化 | `tutorials/gluon/08-warp-specialization.py` |
| `async_gather/scatter` | TMA Gather/Scatter | `tutorials/gluon/09-tma-gather-scatter.py` |

## Triton Kernels 参考实现

| 内核 | 文件 | 特性 |
|------|------|------|
| Dense GEMM | `triton_kernels/triton_kernels/matmul_details/_matmul.py` | TMA, mxfp4/8, 融合激活 |
| Persistent GEMM | `triton_kernels/triton_kernels/matmul_details/_p_matmul.py` | Ragged TMA, 持久化 |
| Matmul API | `triton_kernels/triton_kernels/matmul.py` | FusedActivation, Epilogue, MoE |
| Reduction | `triton_kernels/triton_kernels/reduce.py` | mask, scale, mxfp, flexpoint |
| Top-K | `triton_kernels/triton_kernels/topk.py` | Streaming top-k, bitmatrix |
| SwiGLU | `triton_kernels/triton_kernels/swiglu.py` | SiLU(x)*linear(x), flexpoint |
| MXFP 量化 | `triton_kernels/triton_kernels/numerics_details/mxfp.py` | downcast/upcast mxfp4/8 |
| Flexpoint | `triton_kernels/triton_kernels/numerics_details/flexpoint.py` | FP8 scaling |
| Tensor/Layout | `triton_kernels/triton_kernels/tensor.py` | TMA descriptors, layout transforms |
| Roofline | `triton_kernels/triton_kernels/roofline.py` | 性能分析, CSV export |
| Testing | `triton_kernels/triton_kernels/testing.py` | assert_close, compute_sanitizer |

## Layout 布局详情

| 布局 | 文件 | 目标架构 |
|------|------|---------|
| Blackwell MX Scale | `triton_kernels/.../layout_details/blackwell_scale.py` | sm_100+ |
| Blackwell MX Value | `triton_kernels/.../layout_details/blackwell_value.py` | sm_100+ |
| Hopper MX Value | `triton_kernels/.../layout_details/hopper_value.py` | sm_90 |
| Hopper MX Scale | `triton_kernels/.../layout_details/hopper_scale.py` | sm_90 |
| CDNA4 Scale | `triton_kernels/.../layout_details/cdna4_scale.py` | AMD gfx1250 |
| Strided | `triton_kernels/.../layout_details/strided.py` | 通用 |

## 按架构分类

### Hopper (sm_90) 相关

- `tutorials/gluon/05-wgmma.py` — WGMMA
- `tutorials/gluon/04-tma.py` — TMA
- `tutorials/09-persistent-matmul.py` — 持久化 matmul
- `triton_kernels/.../layout_details/hopper_value.py` — Hopper MX 布局

### Blackwell (sm_100) 相关

- `tutorials/gluon/06-tcgen05.py` — tcgen05 MMA
- `tutorials/gluon/10-tcgen05-copy.py` — tcgen05 copy
- `tutorials/gluon/11-tcgen05-mma-scaled.py` — scaled MMA
- `tutorials/gluon/09-tma-gather-scatter.py` — TMA Gather/Scatter
- `tutorials/gluon/12-cluster-launch-control.py` — CLC
- `examples/gluon/01-attention-forward.py` — Flash Attention (Blackwell)
- `triton_kernels/.../layout_details/blackwell_scale.py` — Blackwell MX 布局
