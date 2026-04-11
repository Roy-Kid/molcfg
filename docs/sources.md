# Sources

A source loads configuration from one origin and returns a plain `dict`. `ConfigLoader` merges multiple sources in order.

## DictSource

Wraps an in-memory dict. Useful for defaults and test fixtures.

```python
from molcfg import DictSource

src = DictSource({"db": {"host": "localhost", "port": 5432}}, name="defaults")
data = src.load()
```

## JsonFileSource

Reads a JSON file from disk.

```python
from molcfg import JsonFileSource

src = JsonFileSource("config.json", name="file")
```

## TomlFileSource

Reads a TOML file from disk.

```python
from molcfg import TomlFileSource

src = TomlFileSource("config.toml", name="file")
```

## EnvSource

Reads environment variables and maps them into nested keys by splitting on `_`.

```python
from molcfg import EnvSource

src = EnvSource(
    prefix="APP",
    environ={
        "APP_DB_HOST": "prod-db",
        "APP_DB_PORT": "5432",
        "APP_DEBUG": "true",
    },
)

assert src.load() == {
    "db": {"host": "prod-db", "port": 5432},
    "debug": True,
}
```

`prefix` is stripped and not included in the output key. Keys are lowercased. Pass `environ=` to inject a custom env dict (useful in tests); omit it to read `os.environ`.

## CliSource

Parses a list of `--key=value` or `--key value` arguments.

```python
from molcfg import CliSource

src = CliSource(["--db.host=localhost", "--db.port", "5432", "--debug=true"])
assert src.load() == {"db": {"host": "localhost", "port": 5432}, "debug": True}
```

Dotted keys map directly to nested dicts.

## Coercion

`EnvSource` and `CliSource` coerce string values by default:

| Input | Result |
|-------|--------|
| `"true"` / `"false"` | `bool` |
| `"5432"` | `int` |
| `"3.14"` | `float` |
| `"null"` / `"none"` | `None` |
| `'["a","b"]'` | `list` |
| `'{"x":1}'` | `dict` |

Pass `coerce=False` to keep raw strings.

## Naming sources

All sources accept a `name` argument recorded in metadata:

```python
DictSource({"x": 1}, name="defaults")
EnvSource(prefix="APP", name="env")
```

Use stable, descriptive names. They appear in `Config.meta()` history.
