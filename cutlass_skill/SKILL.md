---
name: cutlass-skill
description: "Write, debug, and optimize CUTLASS and CuTeDSL GPU kernels using local source code, examples, and header references. Use when the user mentions CUTLASS, CuTe, CuTeDSL, cute::Layout, cute::Tensor, TiledMMA, TiledCopy, CollectiveMainloop, CollectiveEpilogue, GEMM kernel, grouped GEMM, sparse GEMM, flash attention CUTLASS, blackwell GEMM, hopper GEMM, FP8 GEMM, blockwise scaling, MoE GEMM, StreamK, warp specialization CUTLASS, TMA CUTLASS, or asks about writing high-performance CUDA kernels with CUTLASS/CuTe templates."
---

# CUTLASS & CuTeDSL Development

## Source Code Locations

CUTLASS 源码本地路径（由 install.sh 从 GitHub clone）:

**CUTLASS_REPO**: `~/.cursor/skills/cutlass-skill/repos/cutlass/`

如果该路径不存在，运行:

```bash
# 在 cursor-gpu-skills 项目目录下运行
bash update-repos.sh cutlass
```

所有搜索路径基于 `CUTLASS_REPO` 变量。使用 Grep 工具时，替换为实际绝对路径。

### CuTeDSL (Python DSL for GPU Kernels)

```
CUTLASS_REPO/python/CuTeDSL/
├── cutlass/
│   ├── base_dsl/       # DSL 基础: 类型, 变量, 函数, PTX emit
│   ├── cute/           # CuTe Python 绑定: Layout, Tensor, TiledMMA, TiledCopy
│   ├── cutlass_dsl/    # CUTLASS DSL: GEMM builder, epilogue, pipeline
│   ├── pipeline/       # 流水线抽象: MainloopPipeline, PipelineAsync
│   ├── jax/            # JAX 集成
│   ├── utils/          # 编译工具, profiler, tensor 工具
│   └── torch.py        # PyTorch 集成
```

CuTeDSL 示例:

```
CUTLASS_REPO/examples/python/CuTeDSL/
├── ampere/             # Ampere: sgemm, tensorop_gemm, flash_attention_v2
├── hopper/             # Hopper: TMA gemm, FP8, grouped GEMM
├── blackwell/          # Blackwell: blockwise_gemm
├── blackwell_geforce/  # GeForce Blackwell
├── cute/               # CuTe tutorials (Python)
├── distributed/        # 分布式 GEMM
├── experimental/       # 实验性功能
├── jax/                # JAX 示例
├── notebooks/          # Jupyter notebooks (英文)
├── notebooks-zh/       # Jupyter notebooks (中文)
└── advanced_compiler_control/  # 高级编译控制
```

### CUTLASS C++ Examples (按架构分类)

```
CUTLASS_REPO/examples/
├── 00-47:  Ampere 及更早架构
├── 48-69:  Hopper (sm_90)
│   ├── 48_hopper_warp_specialized_gemm
│   ├── 49_hopper_gemm_with_collective_builder
│   ├── 54_hopper_fp8_warp_specialized_gemm
│   ├── 55_hopper_mixed_dtype_gemm
│   ├── 57_hopper_grouped_gemm
│   ├── 62_hopper_sparse_gemm
│   ├── 67_hopper_fp8..._blockwise_scaling
│   ├── 88_hopper_fmha
│   └── ...
├── 70-93:  Blackwell (sm_100)
│   ├── 70_blackwell_gemm
│   ├── 71_blackwell_gemm_with_collective_builder
│   ├── 72_blackwell_narrow_precision_gemm
│   ├── 77_blackwell_fmha
│   ├── 81_blackwell_gemm_blockwise
│   ├── 83_blackwell_sparse_gemm
│   ├── 92_blackwell_moe_gemm
│   ├── 93_blackwell_low_latency_gqa
│   └── ...
└── cute/tutorial/      # CuTe C++ tutorials (sgemm, tiled_copy, hopper, blackwell)
```

### CuTe C++ Headers

```
CUTLASS_REPO/include/cute/
├── layout.hpp          # Layout 核心: Shape, Stride, 组合
├── tensor.hpp          # Tensor: make_tensor, local_tile, partition
├── swizzle.hpp         # Swizzle 模式
├── algorithm/          # copy, gemm, fill, clear
├── arch/               # 架构特定: copy_sm90, mma_sm90, copy_sm100
├── atom/               # MMA atom, Copy atom 定义
│   ├── mma_atom.hpp
│   ├── copy_atom.hpp
│   └── mma_traits_sm90_gmma.hpp  # WGMMA traits
├── numeric/            # 数值类型
└── container/          # tuple, array
```

### CUTLASS C++ Headers

```
CUTLASS_REPO/include/cutlass/
├── gemm/               # GEMM 设备层, collective, kernel
│   ├── collective/     # CollectiveMainloop, CollectiveEpilogue
│   ├── kernel/         # GemmUniversal
│   └── device/         # 设备启动接口
├── epilogue/           # Epilogue: bias, activation, scaling
├── conv/               # 卷积
├── arch/               # MMA 指令包装 (mma_sm90.h, mma_sm100.h)
├── pipeline/           # Pipeline: PipelineTmaAsync, PipelineAsync
├── experimental/       # 实验性 API
└── detail/             # 内部实现细节
```

### pycute (Python CuTe 绑定)

```
CUTLASS_REPO/python/pycute/
├── layout.py           # Layout, make_layout, complement, coalesce
├── int_tuple.py        # IntTuple 操作
├── swizzle.py          # Swizzle
└── typing.py           # 类型定义
```

## Search Strategy

**用 Grep 工具搜索**，不要整文件加载。

### CuTeDSL 用法

```bash
CUTLASS_REPO="$HOME/.cursor/skills/cutlass-skill/repos/cutlass"

# 查找 CuTeDSL GEMM 示例
rg "@jit" $CUTLASS_REPO/examples/python/CuTeDSL/

# 查找 TiledMMA 使用
rg "TiledMMA\|tiled_mma" $CUTLASS_REPO/python/CuTeDSL/cutlass/cute/

# 查找 pipeline 用法
rg "MainloopPipeline\|PipelineAsync" $CUTLASS_REPO/python/CuTeDSL/cutlass/pipeline/

# 查找 Blackwell CuTeDSL 示例
rg "sm_100\|blackwell" $CUTLASS_REPO/examples/python/CuTeDSL/blackwell/
```

### CuTe C++ 用法

```bash
# 查找 Layout 操作
rg "make_layout\|composition\|complement" $CUTLASS_REPO/include/cute/layout.hpp

# 查找 TiledCopy 使用
rg "TiledCopy\|make_tiled_copy" $CUTLASS_REPO/include/cute/

# 查找 MMA atom traits
rg "MMA_Traits" $CUTLASS_REPO/include/cute/atom/

# 查找 Hopper WGMMA
rg "SM90_64x" $CUTLASS_REPO/include/cute/atom/mma_traits_sm90_gmma.hpp

# 查找 TMA copy
rg "SM90_TMA" $CUTLASS_REPO/include/cute/arch/
```

### CUTLASS Collective Builder

```bash
# 查找 CollectiveBuilder 使用
rg "CollectiveBuilder" $CUTLASS_REPO/examples/49_hopper_gemm_with_collective_builder/

# 查找 Collective Mainloop
rg "CollectiveMainloop" $CUTLASS_REPO/include/cutlass/gemm/collective/

# 查找 Epilogue 融合
rg "fusion\|EVT" $CUTLASS_REPO/include/cutlass/epilogue/

# 查找 kernel 启动模板
rg "GemmUniversal" $CUTLASS_REPO/include/cutlass/gemm/device/
```

### GEMM 示例搜索

```bash
# 查找 FP8 GEMM 配置
rg "float_e4m3\|float_e5m2\|fp8" $CUTLASS_REPO/examples/54_hopper_fp8_warp_specialized_gemm/

# 查找 blockwise scaling
rg "blockwise\|block_scale" $CUTLASS_REPO/examples/67_hopper_fp8_warp_specialized_gemm_with_blockwise_scaling/

# 查找 grouped GEMM
rg "grouped\|ProblemShape::Group" $CUTLASS_REPO/examples/57_hopper_grouped_gemm/

# 查找 sparse GEMM
rg "sparse\|Sparse" $CUTLASS_REPO/examples/62_hopper_sparse_gemm/

# 查找 StreamK
rg "StreamK\|stream_k" $CUTLASS_REPO/examples/47_ampere_gemm_universal_streamk/
```

## When to Use Each Source

| Need | Source | Path |
|------|--------|------|
| CuTeDSL 入门 | CuTeDSL examples | `examples/python/CuTeDSL/ampere/` |
| CuTeDSL Hopper GEMM | CuTeDSL examples | `examples/python/CuTeDSL/hopper/` |
| CuTeDSL Blackwell GEMM | CuTeDSL examples | `examples/python/CuTeDSL/blackwell/` |
| CuTeDSL API 定义 | CuTeDSL source | `python/CuTeDSL/cutlass/` |
| CuTe Layout 语义 | CuTe headers | `include/cute/layout.hpp` |
| CuTe Tensor 操作 | CuTe headers | `include/cute/tensor.hpp` |
| MMA atom traits | CuTe atom | `include/cute/atom/` |
| TMA copy 架构 | CuTe arch | `include/cute/arch/copy_sm90*` |
| CUTLASS GEMM 模板 | CUTLASS examples | `examples/48-93_*` |
| Collective Builder | CUTLASS examples | `examples/49_hopper_gemm_with_collective_builder/` |
| Collective Mainloop | CUTLASS headers | `include/cutlass/gemm/collective/` |
| Epilogue 融合 | CUTLASS headers | `include/cutlass/epilogue/` |
| Pipeline 抽象 | CUTLASS headers | `include/cutlass/pipeline/` |
| pycute Layout 操作 | pycute | `python/pycute/` |
| Hopper FMHA | CUTLASS examples | `examples/88_hopper_fmha/` |
| Blackwell FMHA | CUTLASS examples | `examples/77_blackwell_fmha/` |
| MoE GEMM | CUTLASS examples | `examples/92_blackwell_moe_gemm/` |

## CuTeDSL 编写模式

### 基本 Elementwise Kernel

```python
from cutlass import jit, Int32, Float32

@jit
def add_kernel(x: Float32, y: Float32) -> Float32:
    return x + y
```

参考 `examples/python/CuTeDSL/ampere/elementwise_add.py` 获取完整示例。

### CuTeDSL GEMM

参考 `examples/python/CuTeDSL/ampere/sgemm.py` 获取基础 SGEMM。
参考 `examples/python/CuTeDSL/hopper/` 获取 Hopper TMA GEMM。

### CuTe C++ GEMM 模式

参考 `examples/cute/tutorial/sgemm_1.cu` ~ `sgemm_sm80.cu` 获取 CuTe SGEMM 渐进教程。

## Compilation Reference

```bash
# 编译 CUTLASS example
cd CUTLASS_REPO && mkdir -p build && cd build
cmake .. -DCUTLASS_NVCC_ARCHS=90a  # Hopper
cmake --build . --target 49_hopper_gemm_with_collective_builder

# 编译特定架构
cmake .. -DCUTLASS_NVCC_ARCHS="80;90a;100a"

# CuTeDSL 运行
pip install -e python/CuTeDSL/
python examples/python/CuTeDSL/ampere/sgemm.py
```

## 常见问题排查

| 问题 | 可能原因 | 查找参考 |
|------|---------|---------|
| GEMM 精度不对 | Epilogue 未配置正确的 accumulator 类型 | `rg "ElementAccumulator" examples/49_*` |
| TMA 报错 | Tensor alignment 不满足 128B | `rg "Alignment\|alignment" examples/48_*` |
| Collective Builder 编译失败 | 架构不匹配或 pipeline 配置错误 | `rg "KernelSchedule\|EpilogueSchedule" examples/49_*` |
| CuTeDSL 类型错误 | DSL 类型与 CUDA 类型不匹配 | `rg "dtype\|element_type" examples/python/CuTeDSL/` |
| Layout swizzle 错误 | Swizzle 模式与数据排布不兼容 | `include/cute/swizzle.hpp` |

## 更新 CUTLASS 源码

```bash
# 在 cursor-gpu-skills 项目目录下
bash update-repos.sh cutlass
```

## Additional References

- CUTLASS 官方文档: https://github.com/NVIDIA/cutlass
- CuTe 文档: `CUTLASS_REPO/media/docs/cute/` (如果使用 --full 模式安装)
- CuTeDSL notebooks: `examples/python/CuTeDSL/notebooks/`
