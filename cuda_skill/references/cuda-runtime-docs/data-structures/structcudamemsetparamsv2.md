# 7.59. cudaMemsetParamsV2

**Source:** structcudaMemsetParamsV2.html#structcudaMemsetParamsV2


### Public Variables

cudaExecutionContext_t ctx

void * dst

unsigned int elementSize

size_t height

size_t pitch

unsigned int value

size_t width


### Variables

cudaExecutionContext_tcudaMemsetParamsV2::ctx


Context in which to run the memset. If NULL will try to use the current context.

void * cudaMemsetParamsV2::dst


Destination device pointer

unsigned int cudaMemsetParamsV2::elementSize


Size of each element in bytes. Must be 1, 2, or 4.

size_t cudaMemsetParamsV2::height


Number of rows

size_t cudaMemsetParamsV2::pitch


Pitch of destination device pointer. Unused if height is 1

unsigned int cudaMemsetParamsV2::value


Value to be set

size_t cudaMemsetParamsV2::width


Width of the row in elements

* * *

!


Copyright © 2025 NVIDIA Corporation