# Getting Started

## Installation

```bash
pip install molcrafts-molcfg
```

The PyPI distribution name is `molcrafts-molcfg`; the import name is `molcfg`.

For local development:

```bash
pip install -e ".[dev]"
pip install -e ".[docs]"
```

## First Config

```python
from molcfg import Config

cfg = Config({"app": {"name": "demo", "debug": False}})

# attribute access
assert cfg.app.name == "demo"

# dotted-path access
assert cfg["app.name"] == "demo"

# containment check
assert "app.debug" in cfg
```

## Mutating a Config

```python
cfg.app.name = "updated"
cfg["app.debug"] = True
```

Nested dicts are automatically wrapped into child `Config` objects.

## Freezing and rollback

```python
cfg.freeze()
# cfg.app.name = "x"  # raises FrozenConfigError

cfg.unfreeze()
cfg.snapshot()
cfg.app.name = "temporary"
cfg.rollback()
assert cfg.app.name == "updated"
```

## Layered loading

Later sources win using `DEEP_MERGE` by default:

```python
from molcfg import CliSource, ConfigLoader, DictSource, EnvSource

cfg = ConfigLoader([
    DictSource({"db": {"host": "localhost", "port": 5432}}, name="defaults"),
    EnvSource(prefix="APP", name="env"),
    CliSource(["--db.port=6432"], name="cli"),
]).load()

assert cfg["db.port"] == 6432
```

## Source tracking

```python
info = cfg.meta("db.port")
# {"source": "cli", "history": ("defaults", "cli")}
```

`source` is the last writer. `history` lists every source that touched the key, in order.

## Serialization

```python
d = cfg.to_dict()
s = cfg.to_json()
s = cfg.to_json(indent=2)
```

## Change callbacks

```python
def on_change(path: str, new_value, old_value) -> None:
    print(f"{path}: {old_value!r} -> {new_value!r}")

cfg.on_change(on_change)
cfg.app.name = "watched"
# app.name: 'demo' -> 'watched'
```
