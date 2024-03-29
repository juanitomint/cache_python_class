# In memory cache implementation in python

This project implements a simple in memory cache implementation in python.
With least accessed or lru_cache (Least Recently Used) eviction and replacement policy.

```mermaid
graph TD
  
subgraph "ADD KEY"
        X[X:0]
end
subgraph "cache (key:hits)"
    A[A:1]
    B[B:5]
    C[C:7]
    D[D:10]
    E[E:13]
end


subgraph "cache2(key:hits)"

    J[X:0]
    K[B:5]
    L[C:7]
    M[D:10]
    N[E:13]
end

subgraph "Evict key"
    Y[A:1]
end
  X -->|Added new key with value 55| A
  A --> |Evicted key 1 with 1 hits |Y
  A --> J

  
```

## basic usage

Initializes a cache object of size 10 and using "id" as cache key
```python
cache = Cache(10,hash_key="id")
```
