# 7.49. cudaMemcpy3DOperand

**Source:** structcudaMemcpy3DOperand.html#structcudaMemcpy3DOperand


### Public Variables

cudaMemcpy3DOperand::@8::@10 array

size_t layerHeight

struct cudaMemLocation locHint

cudaMemcpy3DOperand::@8::@9 ptr

size_t rowLength


### Variables

cudaMemcpy3DOperand::@8::@10 cudaMemcpy3DOperand::array


Struct representing an operand when cudaMemcpy3DOperand::type is cudaMemcpyOperandTypeArray

size_t cudaMemcpy3DOperand::layerHeight


Height of each layer in elements.

struct cudaMemLocationcudaMemcpy3DOperand::locHint


Hint location for the operand. Ignored when the pointers are not managed memory or memory allocated outside CUDA.

cudaMemcpy3DOperand::@8::@9 cudaMemcpy3DOperand::ptr


Struct representing an operand when cudaMemcpy3DOperand::type is cudaMemcpyOperandTypePointer

size_t cudaMemcpy3DOperand::rowLength


Length of each row in elements.

* * *

!


Copyright © 2025 NVIDIA Corporation