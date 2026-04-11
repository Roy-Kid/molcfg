# Validation

## Basic Validation

```python
from molcfg import validate

class DbSchema:
    host: str
    port: int

validate({"host": "localhost", "port": 5432}, DbSchema)
```

## Defaults

Set `apply_defaults=True` to return a completed object:

```python
class DbSchema:
    host: str = "localhost"
    port: int = 5432

result = validate({}, DbSchema, apply_defaults=True)
assert result == {"host": "localhost", "port": 5432}
```

## Strict Unknown-Field Handling

Set `allow_extra=False` to reject keys not present in the schema:

```python
validate(
    {"host": "localhost", "debug": True},
    DbSchema,
    allow_extra=False,
)
```

## Nested Schemas

```python
class DbSchema:
    host: str
    port: int = 5432

class AppSchema:
    db: DbSchema

validated = validate({"db": {}}, AppSchema, apply_defaults=True)
```

`molcfg` also supports `list[Schema]` and `dict[K, V]`.

## Constraints

Built-in constraint helpers:

- `Range`
- `Length`
- `Pattern`
- `OneOf`

Example:

```python
from molcfg import Range

class DbSchema:
    port: int
    __constraints__ = {"port": [Range(1, 65535)]}
```
