# 7.10. cudaDevResource

**Source:** structcudaDevResource.html#structcudaDevResource


### Public Variables

struct cudaDevSmResource sm

enumcudaDevResourceType type

struct cudaDevWorkqueueResource wq

struct cudaDevWorkqueueConfigResource wqConfig


### Variables

struct cudaDevSmResourcecudaDevResource::sm


Resource corresponding to cudaDevResourceTypeSm `type`.

enumcudaDevResourceTypecudaDevResource::type


Type of resource, dictates which union field was last set

struct cudaDevWorkqueueResourcecudaDevResource::wq


Resource corresponding to cudaDevResourceTypeWorkqueue `type`.

struct cudaDevWorkqueueConfigResourcecudaDevResource::wqConfig


Resource corresponding to cudaDevResourceTypeWorkqueueConfig `type`.

* * *

!


Copyright © 2025 NVIDIA Corporation