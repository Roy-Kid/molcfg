# API Reference

## Config

```python
class Config(data: dict | None = None, *, metadata=None, prefix="")
```

Nested configuration container. Nested dicts are automatically wrapped into child `Config` instances.

### Access

| Operation | Example |
|-----------|---------|
| Attribute read | `cfg.db.host` |
| Dotted-path read | `cfg["db.host"]` |
| Attribute write | `cfg.db.host = "x"` |
| Dotted-path write | `cfg["db.host"] = "x"` |
| Containment | `"db.host" in cfg` |
| Delete | `del cfg.db.host` |

### Methods

- `get(path, default=None)` — safe dotted-path read
- `keys()`, `values()`, `items()` — top-level iteration
- `to_dict()` — recursive plain-dict export
- `to_json(**kwargs)` — JSON string; passes kwargs to `json.dumps`
- `to_toml()` — TOML string
- `to_yaml(**kwargs)` — YAML string; passes kwargs to `yaml.dump`
- `save_json(path, **kwargs)` / `save_toml(path)` / `save_yaml(path, **kwargs)` — write the config to a file
- `freeze()` — recursively freeze; raises `FrozenConfigError` on write
- `unfreeze()` — recursively unfreeze
- `snapshot()` — push current state onto the snapshot stack
- `rollback()` — pop and restore the last snapshot (raises `ConfigError` if the stack is empty)
- `on_change(callback)` — register `callback(path, new_value, old_value)`
- `meta(path="")` — return `{"source": str, "history": tuple}` for a dotted path, or `None` if the path has no recorded metadata
- `metadata()` — return the full metadata dict

### Properties

- `frozen` — `True` if the config is currently frozen

### Class-level loaders

```python
Config.load_json(path)   # -> Config
Config.load_toml(path)   # -> Config
Config.load_yaml(path)   # -> Config
```

Convenience shortcuts that read a single file. Source tracking is **not**
recorded — for provenance, load through `ConfigLoader` with the matching
`*FileSource` instead.

---

## Sources

All sources inherit from `Source` and expose a single method:

- `load() -> dict[str, Any]`

Every source accepts an optional `name`. When omitted (`None`), the source's class name is recorded in metadata; the name is what appears in `Config.meta()` history.

### DictSource

```python
DictSource(data: dict, name: str | None = None)
```

Wraps an in-memory dict.

### JsonFileSource

```python
JsonFileSource(path: str | Path, name: str | None = None)
```

### TomlFileSource

```python
TomlFileSource(path: str | Path, name: str | None = None)
```

### YamlFileSource

```python
YamlFileSource(path: str | Path, name: str | None = None)
```

Loads a YAML file (requires `pyyaml`). An empty file yields `{}`.

### EnvSource

```python
EnvSource(
    prefix: str = "",
    separator: str = "_",
    environ: dict | None = None,
    *,
    coerce: bool = True,
    name: str | None = None,
)
```

Reads environment variables and maps them to nested keys by splitting on `separator` (default `_`). `prefix` is stripped and not included in the output key.

### CliSource

```python
CliSource(args: list[str], *, coerce: bool = True, name: str | None = None)
```

Parses `--key=value` and `--key value` arguments. Dotted keys map to nested dicts.

---

## Merge

### merge()

```python
merge(base: dict, override: dict, strategy: MergeStrategy = DEEP_MERGE) -> dict
```

Returns a new dict. Neither input is mutated.

### MergeStrategy

```python
class MergeStrategy(enum.Enum):
    DEEP_MERGE = "deep_merge"
    OVERRIDE   = "override"
    APPEND     = "append"
```

### ConfigLoader

```python
ConfigLoader(sources: list[Source], strategy: MergeStrategy = DEEP_MERGE)
```

- `load() -> Config` — merge all sources in order, attach metadata

### ProfileLoader

```python
ProfileLoader(base_sources: list[Source], profiles: dict[str, Source], strategy: MergeStrategy = DEEP_MERGE)
```

- `load(profile: str | None = None) -> Config` — load base sources and optionally apply a named profile overlay

---

## Validation

### validate()

```python
validate(
    data: dict,
    schema: type,
    prefix: str = "",
    *,
    allow_extra: bool = True,
    apply_defaults: bool = False,
) -> dict
```

Raises `ValidationError` on type mismatch, missing required fields, or constraint failure. Returns the input dict unchanged unless `apply_defaults=True`, in which case a new dict with defaults filled in is returned. `prefix` prefixes reported error paths and is mainly used for nested validation.

### Constraints

```python
Range(min_val: int | float, max_val: int | float)   # inclusive [min_val, max_val]
Length(min_len: int = 0, max_len: int | None = None)
Pattern(pattern: str)                                # re.search against the value
OneOf(*values)
```

Attach via `__constraints__ = {"field": [constraint, ...]}` on the schema class.

### Build

```python
Build(registry: Registry)
```

`typing.Annotated` metadata marker. When `validate()` encounters
`field: Annotated[T, Build(reg)]`, the raw value is passed through
`reg.build(...)` before the field's type is checked. Works on default
values too.

---

## Registry

```python
Registry(name: str, *, discriminator: str = "type")
```

String-tag → factory container. Generic: `Registry[T]("name")`.

### Registration

```python
reg.register("silu", nn.SiLU)     # direct
@reg("leaky_relu")                # decorator
class MyLeakyReLU(nn.Module): ...
```

Keys are lowercased. Duplicate registration raises `ValueError`.

### Access

- `reg.build(spec) -> T | None` — resolve into an instance. Accepts
  `str` (short form), `dict` with a `type` key + kwargs (long form),
  `None` (pass-through), or an existing instance (idempotent).
- `reg.get(name) -> type[T] | callable | None` — return the registered
  factory/class without instantiating. `None` pass-through. For APIs
  that take `type[T]` and construct later.
- `reg.keys() -> list[str]` — sorted list of registered keys.
- `"key" in reg` — containment check (case-insensitive).

See the [Registry guide](registry.md) for the full tutorial.

---

## Concurrency

### ThreadSafeConfig

```python
ThreadSafeConfig(config: Config, lock: threading.RLock | None = None)
```

Wraps all reads and writes in the provided lock (or a new `RLock`). Exposes the same interface as `Config`.

### FileLock

```python
FileLock(path: str | Path)
```

Context manager. Acquires an exclusive lock on entry (`fcntl.LOCK_EX` on POSIX, `msvcrt.locking` on Windows) and releases it on exit.

- `acquire()` / `release()` for manual management

### interpolate()

```python
interpolate(data: dict, environ: dict | None = None) -> dict
```

Resolves `${path.to.key}` and `${env:VAR}` placeholders. Raises `CircularReferenceError` on circular references.

---

## Paths

### project_config_dir()

```python
project_config_dir(name: str, *, environ: Mapping[str, str] | None = None) -> Path
```

Returns `~/.molcrafts/<name>/config/`, creating it (and any missing parents)
if absent, so downstream tools share a stable user-level configuration
directory. `name` must be a single path segment — not empty, `.`, `..`, or
containing `/`, `\`, or `os.sep` (otherwise `ValueError` is raised and no
directory is created). If the `MOLCRAFTS_HOME` environment variable is set to
a non-empty value it overrides the `~/.molcrafts` base; empty or
whitespace-only values fall back to the default. Pass `environ=` to inject a
mapping instead of reading `os.environ`.

---

## Errors

All errors inherit from `ConfigError`.

| Exception | Raised when |
|-----------|-------------|
| `ConfigError` | Base class |
| `FrozenConfigError` | Writing to a frozen `Config` |
| `ValidationError` | Schema validation fails |
| `CircularReferenceError` | Interpolation detects a cycle |
