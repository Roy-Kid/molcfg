# Sources

## Available Sources

- `DictSource`
- `JsonFileSource`
- `TomlFileSource`
- `EnvSource`
- `CliSource`

## Environment Variables

`EnvSource` splits variables into nested config objects.

```python
from molcfg import EnvSource

src = EnvSource(
    prefix="APP",
    environ={
        "APP_DB_HOST": "localhost",
        "APP_DB_PORT": "5432",
        "APP_DEBUG": "true",
    },
)

assert src.load() == {
    "db": {"host": "localhost", "port": 5432},
    "debug": True,
}
```

## CLI Arguments

```python
from molcfg import CliSource

src = CliSource(["--db.host=localhost", "--db.port", "5432", "--debug=true"])
```

`CliSource` supports both `--key=value` and `--key value`.

## Coercion Rules

By default, environment and CLI sources convert common string values:

- `true` and `false` to booleans
- integers like `5432` to `int`
- floats like `3.14` to `float`
- `null` and `none` to `None`
- JSON-style values like `["a", "b"]` or `{"x": 1}` to Python values

Use `coerce=False` when exact strings matter.

## Naming Sources

All sources accept a `name` that is recorded in metadata:

```python
from molcfg import DictSource

defaults = DictSource({"db": {"host": "localhost"}}, name="defaults")
```

Use stable names like `defaults`, `env`, `file`, `profile:prod`, or `cli`.
