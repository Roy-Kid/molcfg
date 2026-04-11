# Concurrency

## ThreadSafeConfig

`ThreadSafeConfig` wraps a `Config` and serializes all reads and writes through a shared `RLock`.

```python
from molcfg import Config, ThreadSafeConfig

cfg = ThreadSafeConfig(Config({"db": {"host": "localhost", "port": 5432}}))

cfg.db.host = "prod-db"
assert cfg["db.host"] == "prod-db"
```

Nested attribute access returns another `ThreadSafeConfig` holding the same lock, so operations across nested levels stay atomic.

Supports the full `Config` interface: item access, freeze, snapshot, rollback, `on_change`, `to_dict`, `to_json`.

### Sharing a lock

Pass an existing `RLock` to coordinate access across multiple wrappers:

```python
import threading

lock = threading.RLock()
cfg1 = ThreadSafeConfig(Config({"a": 1}), lock=lock)
cfg2 = ThreadSafeConfig(Config({"b": 2}), lock=lock)
```

## FileLock

`FileLock` provides a POSIX file lock via `fcntl.flock`. Use it when multiple processes may update the same file-backed state.

```python
from molcfg import FileLock

with FileLock("/var/run/myapp.lock"):
    # exclusive access across processes
    ...
```

The lock file is created if it does not exist. The lock is released on `__exit__` or when `release()` is called explicitly.

## Interpolation

`interpolate()` resolves `${...}` placeholders in string values before building a `Config`.

```python
from molcfg import interpolate

data = {
    "base_url": "https://example.com",
    "api_url": "${base_url}/api/v1",
    "secret": "${env:API_SECRET}",
}

resolved = interpolate(data)
# resolved["api_url"] == "https://example.com/api/v1"
# resolved["secret"]  == value of $API_SECRET from os.environ
```

Supported placeholder forms:

- `${path.to.key}` — reference another key in the same config dict
- `${env:VAR_NAME}` — read from the environment

Circular references raise `CircularReferenceError`. Unresolvable references are left unchanged.

Pass `environ=` to inject a custom env dict instead of reading `os.environ`.
