# Merge

## merge()

`merge(base, override, strategy)` merges two plain dicts and returns a new one. Neither input is mutated.

```python
from molcfg import MergeStrategy, merge

base = {"db": {"host": "localhost", "port": 5432}, "debug": False}
override = {"db": {"port": 6432}}

result = merge(base, override, MergeStrategy.DEEP_MERGE)
assert result == {"db": {"host": "localhost", "port": 6432}, "debug": False}
```

## Strategies

### DEEP_MERGE (default)

Recursively merges nested dicts. Scalar values in `override` replace those in `base`.

```python
base     = {"db": {"host": "a", "port": 5432}}
override = {"db": {"port": 6432}}
# result  = {"db": {"host": "a", "port": 6432}}
```

### OVERRIDE

Discards `base` entirely and returns a deep copy of `override`.

```python
base     = {"db": {"host": "a", "port": 5432}, "debug": True}
override = {"db": {"port": 6432}}
# result  = {"db": {"port": 6432}}
```

### APPEND

Like `DEEP_MERGE` for dicts, but concatenates lists instead of replacing them.

```python
base     = {"tags": ["web", "api"]}
override = {"tags": ["internal"]}
# result  = {"tags": ["web", "api", "internal"]}
```

## ConfigLoader

`ConfigLoader` applies merge incrementally across an ordered list of sources. Later sources override earlier ones.

```python
from molcfg import CliSource, ConfigLoader, DictSource, EnvSource, MergeStrategy

cfg = ConfigLoader(
    [
        DictSource({"db": {"host": "localhost", "port": 5432}}, name="defaults"),
        EnvSource(prefix="APP", name="env"),
        CliSource(["--db.port=6432"], name="cli"),
    ],
    strategy=MergeStrategy.DEEP_MERGE,
).load()
```

The resulting `Config` object carries full source metadata. `cfg.meta("db.port")` returns the last writer and the complete history.

## ProfileLoader

`ProfileLoader` adds named profile overlays on top of a base set of sources.

```python
from molcfg import DictSource, ProfileLoader, TomlFileSource

loader = ProfileLoader(
    base_sources=[
        DictSource({"db": {"host": "localhost", "port": 5432}}, name="defaults"),
        TomlFileSource("config.toml", name="file"),
    ],
    profiles={
        "prod": DictSource({"db": {"host": "prod-db.internal"}}, name="profile:prod"),
        "staging": DictSource({"db": {"host": "staging-db.internal"}}, name="profile:staging"),
    },
)

cfg = loader.load(profile="prod")
assert cfg["db.host"] == "prod-db.internal"
assert cfg["db.port"] == 5432  # from defaults
```

Call `loader.load()` without a profile to get the base config only.
