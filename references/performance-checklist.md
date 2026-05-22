# Performance Checklist

Use during `performance-optimization` skill execution.

## Before Changes

- [ ] Target metric is defined (latency P50/P95/P99, throughput, error rate, memory).
- [ ] Baseline is measured under realistic load.
- [ ] Binding constraint is identified (CPU, memory, IO, network, lock, GC).

## Common Constraints

- **CPU**: hot loops, expensive parsing, unnecessary serialization.
- **Memory**: object allocation churn, large in-memory caches, leaks.
- **IO**: synchronous filesystem, blocking network calls, N+1 queries.
- **Network**: chatty protocols, missing connection pooling, no keep-alive.
- **Lock contention**: coarse-grained locks, lock around IO.
- **GC**: large short-lived allocations, fragmented heap, finalizer storms.

## Change Discipline

- [ ] One change per measurement.
- [ ] Same setup for before and after.
- [ ] Effect attributed to the change (not other variables).
- [ ] Improvement worth the complexity introduced.

## Anti-Patterns

- "Add a cache" without measuring miss rate.
- Async-everything when the constraint isn't IO.
- Parallelize before profiling.
- Micro-optimize cold paths.
