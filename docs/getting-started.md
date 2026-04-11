# Getting Started

## Installation

```bash
pip install molcrafts-molcfg
```

The PyPI distribution name is `molcrafts-molcfg`, while the Python import remains `molcfg`.

For local development:

```bash
pip install -e ".[dev]"
```

For docs work:

```bash
pip install -e ".[docs]"
```

## First Config

```python
from molcfg import Config

cfg = Config({"app": {"name": "demo"}})

assert cfg.app.name == "demo"
assert cfg["app.name"] == "demo"
```

## Layered Loading

```python
from molcfg import CliSource, ConfigLoader, DictSource, EnvSource

loader = ConfigLoader(
    [
        DictSource({"db": {"host": "localhost", "port": 5432}}, name="defaults"),
        EnvSource(prefix="APP", name="env"),
        CliSource(["--db.port=6432"], name="cli"),
    ]
)

cfg = loader.load()
```

Later sources override earlier ones using `MergeStrategy.DEEP_MERGE` by default.

## Inspecting Source History

```python
cfg.meta("db.port")
```

Typical result:

```python
{"source": "cli", "history": ("defaults", "cli")}
```

This is useful when operators need to answer why a value changed.
