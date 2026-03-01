# 7.53. cudaMemcpyNodeParams

**Source:** structcudaMemcpyNodeParams.html#structcudaMemcpyNodeParams


### Public Variables

struct cudaMemcpy3DParms copyParams

cudaExecutionContext_t ctx

int flags

int reserved


### Variables

struct cudaMemcpy3DParmscudaMemcpyNodeParams::copyParams


Parameters for the memory copy

cudaExecutionContext_tcudaMemcpyNodeParams::ctx


Context in which to run the memcpy. If NULL will try to use the current context.

int cudaMemcpyNodeParams::flags


Must be zero

int cudaMemcpyNodeParams::reserved


Must be zero

* * *

!


Copyright © 2025 NVIDIA Corporation