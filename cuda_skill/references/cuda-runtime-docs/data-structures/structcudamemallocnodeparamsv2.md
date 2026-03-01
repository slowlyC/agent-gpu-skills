# 7.48. cudaMemAllocNodeParamsV2

**Source:** structcudaMemAllocNodeParamsV2.html#structcudaMemAllocNodeParamsV2


### Public Variables

size_t accessDescCount

cudaMemAccessDesc * accessDescs

size_t bytesize

void * dptr

struct cudaMemPoolProps poolProps


### Variables

size_t cudaMemAllocNodeParamsV2::accessDescCount


in: Number of `accessDescs`s

cudaMemAccessDesc * cudaMemAllocNodeParamsV2::accessDescs


in: number of memory access descriptors. Must not exceed the number of GPUs.

size_t cudaMemAllocNodeParamsV2::bytesize


in: size in bytes of the requested allocation

void * cudaMemAllocNodeParamsV2::dptr


out: address of the allocation returned by CUDA

struct cudaMemPoolPropscudaMemAllocNodeParamsV2::poolProps


in: location where the allocation should reside (specified in location). handleTypes must be cudaMemHandleTypeNone. IPC is not supported. in: array of memory access descriptors. Used to describe peer GPU access

* * *

!


Copyright © 2025 NVIDIA Corporation