# molcfg

[![CI](https://github.com/MolCrafts/molcfg/actions/workflows/ci.yml/badge.svg)](https://github.com/MolCrafts/molcfg/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/molcrafts-molcfg.svg)](https://pypi.org/project/molcrafts-molcfg/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python](https://img.shields.io/badge/python-3.12%2B-3776AB.svg?logo=python&logoColor=white)](./pyproject.toml)
[![Typed](https://img.shields.io/badge/typing-py.typed-0F766E.svg)](./src/molcfg/py.typed)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-16A34A.svg)](./LICENSE)
[![Runtime](https://img.shields.io/badge/runtime-zero%20deps-4F46E5.svg)](#highlights)

`molcfg` is a zero-dependency Python configuration library for applications that need predictable config loading, merging, validation, interpolation, and safe in-memory mutation.

PyPI distribution name: `molcrafts-molcfg`
Import name: `molcfg`

Version `1.0.0` stabilizes the public API around four core areas:

- layered loading from dictionaries, files, environment variables, and CLI arguments
- nested configuration access with freeze, snapshot, rollback, and change callbacks
- schema validation with recursive nested schemas, defaults, and unknown-field control
- source tracking via `Config.meta()` so callers can explain where a value came from

## Why molcfg

- Runtime dependency free
- Python `3.12+`
- Small surface area
- Works well for services, CLIs, and internal tooling

## Install

```bash
pip install molcrafts-molcfg
```

Optional local workflows:

```bash
pip install "molcrafts-molcfg[dev]"
pip install "molcrafts-molcfg[docs]"
pip install "molcrafts-molcfg[release]"
```

## Quick Start

```python
from molcfg import CliSource, ConfigLoader, DictSource, EnvSource, Range, validate

defaults = DictSource(
    {
        "app": {"name": "molcfg-demo"},
        "db": {"host": "localhost", "port": 5432},
    },
    name="defaults",
)

env = EnvSource(prefix="APP", name="env")
cli = CliSource(["--db.port=6432", "--app.debug=true"], name="cli")

cfg = ConfigLoader([defaults, env, cli]).load()

class DbSchema:
    host: str
    port: int
    __constraints__ = {"port": [Range(1, 65535)]}

validated_db = validate(
    cfg["db"].to_dict(),
    DbSchema,
    allow_extra=False,
    apply_defaults=True,
)

assert cfg["db.port"] == 6432
assert cfg.meta("db.port") == {
    "source": "cli",
    "history": ("defaults", "cli"),
}
assert validated_db == {"host": "localhost", "port": 6432}
```

## Feature Overview

### Sources

- `DictSource`
- `JsonFileSource`
- `TomlFileSource`
- `EnvSource`
- `CliSource`

`EnvSource` and `CliSource` coerce values by default:

- `"true"` / `"false"` -> `bool`
- `"5432"` -> `int`
- `"3.14"` -> `float`
- `"null"` / `"none"` -> `None`
- JSON-looking values like `["a", "b"]` -> parsed Python objects

Pass `coerce=False` to keep raw strings.

### Config Container

`Config` supports:

- attribute access: `cfg.db.host`
- dotted access: `cfg["db.host"]`
- freezing: `cfg.freeze()`
- rollback: `cfg.snapshot()` and `cfg.rollback()`
- serialization: `cfg.to_dict()` and `cfg.to_json()`
- metadata lookup: `cfg.meta("db.host")`

### Validation

`validate()` supports:

- primitive types
- `Literal`
- `list[T]`
- `dict[K, V]`
- nested class-based schemas
- optional fields
- defaults via `apply_defaults=True`
- extra field rejection via `allow_extra=False`
- built-in constraints: `Range`, `Length`, `Pattern`, `OneOf`

### Merging

Strategies:

- `MergeStrategy.DEEP_MERGE`
- `MergeStrategy.OVERRIDE`
- `MergeStrategy.APPEND`

All merge paths return isolated data structures and do not share nested mutable state with the inputs.

## Documentation

This repository includes a Zensical documentation site in `docs/`.

Common commands:

```bash
pip install ".[docs]"
zensical serve
zensical build
```

Deployment is expected to happen from Cloudflare Pages rather than GitHub Actions.

## Development

```bash
pip install ".[dev]"
pytest -q
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution workflow and [RELEASING.md](RELEASING.md) for the `1.x` release process.
