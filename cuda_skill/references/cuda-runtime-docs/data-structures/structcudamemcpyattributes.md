# 7.52. cudaMemcpyAttributes

**Source:** structcudaMemcpyAttributes.html#structcudaMemcpyAttributes


### Public Variables

struct cudaMemLocation dstLocHint

unsigned int flags

enumcudaMemcpySrcAccessOrder srcAccessOrder

struct cudaMemLocation srcLocHint


### Variables

struct cudaMemLocationcudaMemcpyAttributes::dstLocHint


Hint location for the destination operand. Ignored when the pointers are not managed memory or memory allocated outside CUDA.

unsigned int cudaMemcpyAttributes::flags


Additional flags for copies with this attribute. See cudaMemcpyFlags.

enumcudaMemcpySrcAccessOrdercudaMemcpyAttributes::srcAccessOrder


Source access ordering to be observed for copies with this attribute.

struct cudaMemLocationcudaMemcpyAttributes::srcLocHint


Hint location for the source operand. Ignored when the pointers are not managed memory or memory allocated outside CUDA.

* * *

!


Copyright © 2025 NVIDIA Corporation