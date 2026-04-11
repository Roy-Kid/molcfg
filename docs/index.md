# molcfg

`molcfg` is a compact Python configuration library for projects that want a predictable, dependency-free runtime core.

It focuses on four things:

- loading configuration from multiple sources
- merging layered settings without accidental aliasing
- validating nested structures with explicit rules
- keeping runtime behavior understandable through source tracking

## What ships in 1.0

- `Config` with attribute and dotted-path access
- `ConfigLoader` and `ProfileLoader`
- environment and CLI sources with type coercion
- merge strategies for override, append, and deep merge
- interpolation with circular-reference detection
- recursive validation with defaults and strict unknown-field checks
- thread-safe config wrapping and file locks

## Example

```python
from molcfg import CliSource, ConfigLoader, DictSource, EnvSource

cfg = ConfigLoader(
    [
        DictSource({"db": {"host": "localhost", "port": 5432}}, name="defaults"),
        EnvSource(prefix="APP", name="env"),
        CliSource(["--db.port=6432"], name="cli"),
    ]
).load()

assert cfg["db.port"] == 6432
assert cfg.meta("db.port") == {
    "source": "cli",
    "history": ("defaults", "cli"),
}
```

## Documentation Map

- Start with [Getting Started](getting-started.md) for installation and first usage.
- See [Sources](sources.md) for file, env, and CLI loading details.
- See [Validation](validation.md) for defaults, strict mode, and nested schemas.
- See [Concurrency](concurrency.md) for lock-related APIs.
- See [Release Notes](release-notes.md) for `1.0.0` changes.
