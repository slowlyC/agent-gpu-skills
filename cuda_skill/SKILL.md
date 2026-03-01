---
name: cuda-skill
description: "Query NVIDIA PTX ISA 9.1, CUDA Runtime API 13.1, Driver API 13.1, Programming Guide v13.1, Best Practices Guide, Nsight Compute, Nsight Systems local documentation. Debug and optimize GPU kernels with nsys/ncu/compute-sanitizer workflows. Use when writing, debugging, or optimizing CUDA code, GPU kernels, PTX instructions, inline PTX, TensorCore operations (WMMA, WGMMA, TMA, tcgen05), or when the user mentions CUDA API functions, error codes, device properties, memory management, profiling, GPU performance, compute capabilities, CUDA Graphs, Cooperative Groups, Unified Memory, dynamic parallelism, or CUDA programming model concepts."
---

# CUDA & PTX Reference

## Documentation Locations

All documentation is under a single base directory:

**CUDA_REFS**: `~/.cursor/skills/cuda-skill/references/`

```
references/
├── ptx-docs/              # PTX ISA 9.1 full spec (405 files, 2.3MB)
├── ptx-simple/            # PTX condensed quick-ref (13 files, 149KB)
├── cuda-runtime-docs/     # CUDA Runtime API 13.1 (107 files, 0.9MB)
├── cuda-driver-docs/      # CUDA Driver API 13.1 (128 files, 0.8MB)
├── cuda-guide/            # CUDA Programming Guide v13.1 (39 pages, 1.6MB)
│   ├── 01-introduction/   # Programming model, CUDA platform
│   ├── 02-basics/         # CUDA C++, kernels, async, memory, nvcc
│   ├── 03-advanced/       # Advanced APIs, kernel programming, driver API, multi-GPU
│   ├── 04-special-topics/ # Graphs, Unified Memory, Coop Groups, TMA, etc.
│   ├── 05-appendices/     # Compute Capabilities, C++ extensions, math funcs
│   └── INDEX.md
├── best-practices-guide/  # CUDA C++ Best Practices Guide
├── ncu-docs/              # Nsight Compute full docs (ProfilingGuide, CLI, etc.)
├── nsys-docs/             # Nsight Systems full docs (UserGuide, etc.)
├── ptx-isa.md             # PTX search guide
├── cuda-runtime.md        # Runtime API search guide
├── cuda-driver.md         # Driver API search guide
├── nsys-guide.md          # Nsight Systems quick reference
├── ncu-guide.md           # Nsight Compute quick reference
├── debugging-tools.md     # compute-sanitizer, cuda-gdb
├── nvtx-patterns.md       # NVTX instrumentation
└── performance-traps.md   # Bank conflicts, coalescing
```

### ptx-simple/ Contents (Condensed Quick-Ref)

```
ptx-simple/
├── ptx-isa-arithmetic.md       # add, sub, mul, mad, fma, div, min, max
├── ptx-isa-data-types.md       # Types, cvt, rounding, pack
├── ptx-isa-memory-spaces.md    # .reg, .global, .shared, fences
├── ptx-isa-load-store.md       # ld, st, prefetch
├── ptx-isa-control-flow.md     # @p, setp, bra, call, ret, exit
├── ptx-isa-tensor-cores.md     # mma.sync, ldmatrix, wgmma
├── ptx-isa-async-copy.md       # cp.async, cp.async.bulk, TMA
├── ptx-isa-barriers.md         # bar.sync, mbarrier
├── ptx-isa-warp-ops.md         # shfl, vote, match, redux
├── ptx-isa-cache-hints.md      # Cache control
├── ptx-isa-sm90-hopper.md      # Hopper-specific (sm_90)
├── ptx-isa-sm100-blackwell.md  # Blackwell-specific (sm_100, tcgen05)
└── ptx-isa-misc.md             # Other instructions
```

## Search Strategy

**Use Grep tool** to search documentation. Never load entire files into context.

### PTX Instruction Lookup

```bash
# Find specific instruction
rg "mbarrier.init" ~/.cursor/skills/cuda-skill/references/ptx-docs/9-instruction-set/

# Find WGMMA register fragments
rg "register fragment" ~/.cursor/skills/cuda-skill/references/ptx-docs/9-instruction-set/ | rg -i wgmma

# Find TMA swizzling modes
rg "swizzle_mode" ~/.cursor/skills/cuda-skill/references/ptx-docs/

# Quick PTX syntax lookup (condensed)
rg "wgmma" ~/.cursor/skills/cuda-skill/references/ptx-simple/ptx-isa-tensor-cores.md
```

### CUDA Runtime API Lookup

```bash
# Error code meaning
rg "cudaErrorInvalidValue" ~/.cursor/skills/cuda-skill/references/cuda-runtime-docs/

# Function documentation
rg -A 20 "cudaStreamSynchronize" ~/.cursor/skills/cuda-skill/references/cuda-runtime-docs/modules/group__cudart__stream.md

# Struct fields
rg "" ~/.cursor/skills/cuda-skill/references/cuda-runtime-docs/data-structures/structcudadeviceprop.md
```

### CUDA Driver API Lookup

```bash
# Context management
rg -A 20 "cuCtxCreate" ~/.cursor/skills/cuda-skill/references/cuda-driver-docs/modules/group__cuda__ctx.md

# Module loading
rg "cuModuleLoad" ~/.cursor/skills/cuda-skill/references/cuda-driver-docs/modules/group__cuda__module.md

# Virtual memory
rg "cuMemMap" ~/.cursor/skills/cuda-skill/references/cuda-driver-docs/modules/group__cuda__va.md
```

### CUDA Programming Guide Lookup

```bash
# Compute Capabilities table
rg -A 5 "sm_90" ~/.cursor/skills/cuda-skill/references/cuda-guide/05-appendices/compute-capabilities.md

# CUDA Graphs usage
rg "cudaGraph" ~/.cursor/skills/cuda-skill/references/cuda-guide/04-special-topics/cuda-graphs.md

# Cooperative Groups
rg "cooperative" ~/.cursor/skills/cuda-skill/references/cuda-guide/04-special-topics/cooperative-groups.md

# Unified Memory behavior
rg "managed" ~/.cursor/skills/cuda-skill/references/cuda-guide/04-special-topics/unified-memory.md

# Thread Block Clusters (Hopper+)
rg "cluster" ~/.cursor/skills/cuda-skill/references/cuda-guide/01-introduction/programming-model.md

# Programming Guide index (discover all topics)
cat ~/.cursor/skills/cuda-skill/references/cuda-guide/INDEX.md
```

### Best Practices Guide Lookup

```bash
# Memory coalescing best practices
rg -i "coalescing" ~/.cursor/skills/cuda-skill/references/best-practices-guide/

# Occupancy optimization
rg -i "occupancy" ~/.cursor/skills/cuda-skill/references/best-practices-guide/

# Shared memory usage patterns
rg -i "shared memory" ~/.cursor/skills/cuda-skill/references/best-practices-guide/
```

### Nsight Compute Lookup

```bash
# Metric meanings and collection
rg -i "metric" ~/.cursor/skills/cuda-skill/references/ncu-docs/ProfilingGuide.md

# CLI usage and options
rg -i "section" ~/.cursor/skills/cuda-skill/references/ncu-docs/NsightComputeCli.md

# Roofline analysis
rg -i "roofline" ~/.cursor/skills/cuda-skill/references/ncu-docs/ProfilingGuide.md
```

### Nsight Systems Lookup

```bash
# CLI profiling options
rg -i "nsys profile" ~/.cursor/skills/cuda-skill/references/nsys-docs/UserGuide.md

# CUDA trace analysis
rg -i "cuda.*trace" ~/.cursor/skills/cuda-skill/references/nsys-docs/UserGuide.md
```

## When to Use Each Source

| Need | Source | Path shorthand |
|------|--------|----------------|
| PTX instruction syntax/semantics | Full PTX docs | `ptx-docs/9-instruction-set/` |
| Quick PTX syntax check | Condensed PTX | `ptx-simple/` |
| State spaces, data types | Full PTX docs | `ptx-docs/5-state-spaces-types-and-variables/` |
| Memory consistency model | Full PTX docs | `ptx-docs/8-memory-consistency-model/` |
| Special registers (%tid, etc.) | Full PTX docs | `ptx-docs/10-special-registers/` |
| Directives (.version, .target) | Full PTX docs | `ptx-docs/11-directives/` |
| CUDA Runtime functions | Runtime docs | `cuda-runtime-docs/modules/` |
| CUDA structs (cudaDeviceProp) | Runtime docs | `cuda-runtime-docs/data-structures/` |
| Driver API (cuCtx, cuModule) | Driver docs | `cuda-driver-docs/modules/` |
| sm_90 / Hopper specifics | Condensed PTX | `ptx-simple/ptx-isa-sm90-hopper.md` |
| sm_100 / Blackwell / tcgen05 | Condensed PTX | `ptx-simple/ptx-isa-sm100-blackwell.md` |
| CUDA C++ programming concepts | Programming Guide | `cuda-guide/02-basics/` |
| Thread/block/grid model | Programming Guide | `cuda-guide/01-introduction/programming-model.md` |
| Compute Capabilities table | Programming Guide | `cuda-guide/05-appendices/compute-capabilities.md` |
| CUDA Graphs usage | Programming Guide | `cuda-guide/04-special-topics/cuda-graphs.md` |
| Unified Memory | Programming Guide | `cuda-guide/04-special-topics/unified-memory.md` |
| Cooperative Groups | Programming Guide | `cuda-guide/04-special-topics/cooperative-groups.md` |
| Async barriers/pipelines (C++) | Programming Guide | `cuda-guide/04-special-topics/async-barriers.md` |
| L2 cache control | Programming Guide | `cuda-guide/04-special-topics/l2-cache-control.md` |
| Dynamic parallelism | Programming Guide | `cuda-guide/04-special-topics/dynamic-parallelism.md` |
| C++ language extensions | Programming Guide | `cuda-guide/05-appendices/cpp-language-extensions.md` |
| Math functions (device) | Programming Guide | `cuda-guide/05-appendices/mathematical-functions.md` |
| Multi-GPU programming | Programming Guide | `cuda-guide/03-advanced/multi-gpu-systems.md` |
| Environment variables | Programming Guide | `cuda-guide/05-appendices/environment-variables.md` |
| Memory optimization practices | Best Practices | `best-practices-guide/` |
| Performance profiling strategy | Best Practices | `best-practices-guide/` |
| ncu metrics, sections, roofline | Nsight Compute | `ncu-docs/ProfilingGuide.md` |
| ncu CLI options and workflows | Nsight Compute | `ncu-docs/NsightComputeCli.md` |
| nsys profiling and tracing | Nsight Systems | `nsys-docs/UserGuide.md` |

## Debugging Workflow

1. **Reproduce minimally** — Isolate failing kernel with smallest input
2. **Add printf** — `if (idx == 0) printf(...)` in device code
3. **Run compute-sanitizer**:
   ```bash
   compute-sanitizer --tool memcheck ./program
   compute-sanitizer --tool racecheck ./program
   ```
4. **cuda-gdb backtrace** (non-interactive):
   ```bash
   cuda-gdb -batch -ex "run" -ex "bt" ./program
   ```
5. **When tools fail** — Minimize diff between working/broken code, read it carefully

For detailed tool options, read `~/.cursor/skills/cuda-skill/references/debugging-tools.md`.

## Performance Optimization Workflow

**Never optimize without profiling.** GPU bottleneck intuition is almost always wrong.

1. **Establish baseline** timing
2. **nsys** — Where is time spent?
   ```bash
   nsys profile -o report ./program
   nsys stats report.nsys-rep --report cuda_gpu_kern_sum
   ```
3. **ncu** — Why is this kernel slow?
   ```bash
   ncu --kernel-name "myKernel" --set full -o report ./program
   ```
4. **Hypothesize** based on metrics, change ONE thing, verify

| Symptom | Likely Cause | Tool |
|---------|--------------|------|
| Low GPU utilization | Launch overhead, CPU bottleneck | nsys timeline |
| Memory bound | Poor coalescing, low cache hit | ncu memory section |
| Compute bound but slow | Low occupancy, register pressure | ncu occupancy |
| High sectors/request (>4) | Poor coalescing | ncu memory metrics |

For detailed guides, read:
- `~/.cursor/skills/cuda-skill/references/nsys-guide.md` (quick reference)
- `~/.cursor/skills/cuda-skill/references/ncu-guide.md` (quick reference)
- `~/.cursor/skills/cuda-skill/references/performance-traps.md`
- `~/.cursor/skills/cuda-skill/references/ncu-docs/ProfilingGuide.md` (full Nsight Compute profiling guide)
- `~/.cursor/skills/cuda-skill/references/nsys-docs/UserGuide.md` (full Nsight Systems user guide)
- `~/.cursor/skills/cuda-skill/references/best-practices-guide/` (CUDA C++ Best Practices)

## Compilation Reference

```bash
# Debug
nvcc -g -G -lineinfo -O0 program.cu -o program_debug

# Release with line info (always use -lineinfo for profiling)
nvcc -O3 -lineinfo program.cu -o program

# Target architecture
nvcc -arch=sm_80 program.cu   # Ampere
nvcc -arch=sm_90 program.cu   # Hopper
nvcc -arch=sm_100 program.cu  # Blackwell

# Generate PTX / inspect binary
nvcc -ptx program.cu
cuobjdump -ptx ./program
cuobjdump -sass ./program
nvcc --ptxas-options=-v program.cu  # Register usage
```

## Inline PTX in CUDA

```cuda
__device__ int myAdd(int a, int b) {
    int result;
    asm("add.s32 %0, %1, %2;"
        : "=r"(result)
        : "r"(a), "r"(b));
    return result;
}
// Constraint codes: r=32b reg, l=64b reg, f=f32, d=f64, n=immediate
```

## PTX Documentation Structure

```
ptx-docs/
├── 1-introduction/
├── 2-programming-model/          # Thread hierarchy, memory
├── 3-ptx-machine-model/          # SIMT architecture
├── 4-syntax/                     # PTX syntax rules
├── 5-state-spaces-types-and-variables/  # Memory spaces, data types
├── 6-instruction-operands/       # Operand types
├── 7-abstracting-the-abi/        # Functions, calling conventions
├── 8-memory-consistency-model/   # Memory ordering, atomics
├── 9-instruction-set/            # 186 instruction files
│   ├── 9.7.1-*   Integer arithmetic
│   ├── 9.7.3-*   Floating point
│   ├── 9.7.9-*   Data movement (includes TMA)
│   ├── 9.7.14-*  WMMA (sm_70+)
│   ├── 9.7.15-*  WGMMA (sm_90+)
│   └── 9.7.16-*  TensorCore Gen5 (sm_100+)
├── 10-special-registers/         # %tid, %ctaid, %clock64
├── 11-directives/                # .version, .target, .entry
├── 12-descriptions-ofpragmastrings/
└── 13-release-notes/
```

## Updating Documentation

```bash
cd /path/to/cursor-gpu-skills

# Update everything
uv run scrape_docs.py all --force

# Or update individually:
uv run scrape_docs.py ptx-simple --force    # Condensed PTX from triton repo
uv run scrape_docs.py ptx                    # Full PTX ISA from NVIDIA
uv run scrape_docs.py runtime                # CUDA Runtime API
uv run scrape_docs.py driver                 # CUDA Driver API
uv run scrape_docs.py guide --force          # CUDA Programming Guide v13.1
uv run scrape_docs.py best-practices --force # CUDA C++ Best Practices Guide
uv run scrape_docs.py ncu-docs --force       # Nsight Compute docs
uv run scrape_docs.py nsys-docs --force      # Nsight Systems docs
```

## Additional References

For deeper investigation, read the search guide files:
- PTX search workflow: `~/.cursor/skills/cuda-skill/references/ptx-isa.md`
- Runtime API guide: `~/.cursor/skills/cuda-skill/references/cuda-runtime.md`
- Driver API guide: `~/.cursor/skills/cuda-skill/references/cuda-driver.md`
