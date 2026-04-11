# Concurrency

## ThreadSafeConfig

`ThreadSafeConfig` wraps a `Config` and keeps reads and writes behind the same `RLock`.

```python
from molcfg import Config, ThreadSafeConfig

cfg = ThreadSafeConfig(Config({"db": {"host": "localhost"}}))
cfg.db.host = "prod-db"
```

Nested reads return another `ThreadSafeConfig`, not a raw `Config`, so lock boundaries remain intact.

## FileLock

`FileLock` provides a simple POSIX file lock:

```python
from molcfg import FileLock

with FileLock("/tmp/molcfg.lock"):
    ...
```

Use it when multiple processes might update the same file-backed state.

## Interpolation

`interpolate()` resolves config placeholders:

- `${path.to.value}`
- `${env:VAR_NAME}`

Circular references raise `CircularReferenceError`.
