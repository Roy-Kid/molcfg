# Release Notes

## 1.4.1

Release date: 2026-05-11

### Added

- **`project_config_dir(name, *, environ=None)`** — resolves and creates
  `~/.molcrafts/<name>/config/` so downstream tools (e.g. `molq` writing a
  SQLite database) share a stable user-level configuration directory.
  `MOLCRAFTS_HOME` overrides the base; empty or whitespace-only values fall
  back to the default. Pass `environ=` to inject a mapping for full isolation
  from `os.environ` in tests.

### Breaking changes

None.

## 1.4.0

Release date: 2026-04-18

Release-suite version bump — no functional changes beyond 1.3.0.

## 1.3.0

Release date: 2026-04-18

### Added

- **`Registry[T]`** — tag-to-factory container. `registry.build("silu")`
  returns an instance; `registry.get("silu")` returns the registered class
  itself (for APIs that take `type[T]`). Decorator registration via
  `@registry("key")`.
- **Long-form specs with kwargs** — `registry.build({"type": "leaky_relu",
  "negative_slope": 0.1})` constructs `LeakyReLU(negative_slope=0.1)`.
- **`Build(registry)` marker** for `typing.Annotated` — declare
  `activation: Annotated[nn.Module, Build(activations)] = "silu"` in a
  schema and `validate()` resolves the config string into an instance
  before type-checking. Works the same across JSON/TOML/YAML sources, on
  explicit values and defaults alike.
- `docs/registry.md` guide covering short vs. long form, build vs. get,
  and `validate()` integration.

### Changed

- `validate()` now calls `get_type_hints(..., include_extras=True)` so
  `Annotated` metadata is visible to the new `Build` marker. No impact
  on existing schemas.

### Breaking changes

None.

## 1.2.0

Release date: 2026-04-13

### Added

- **`YamlFileSource`** — load configuration from YAML files, alongside the
  existing JSON and TOML file sources.

### Changed

- PyYAML is now a required runtime dependency (previously molcfg had no
  runtime dependencies). The "zero-dependency" framing was dropped from the
  package description and docs.

### Breaking changes

None.

## 1.0.0

Release date: 2026-04-11

First stable release.

### What's included

- `Config` with attribute access, dotted-path access, freeze, snapshot, rollback, and change callbacks
- `ConfigLoader` and `ProfileLoader` with source metadata tracking via `Config.meta()`
- `DictSource`, `JsonFileSource`, `TomlFileSource`, `EnvSource`, `CliSource`
- Automatic scalar and JSON-like coercion for `EnvSource` and `CliSource` (disable with `coerce=False`)
- `merge()` with `DEEP_MERGE`, `OVERRIDE`, and `APPEND` strategies — all paths return isolated copies
- Recursive schema validation with defaults, strict mode, and built-in constraints (`Range`, `Length`, `Pattern`, `OneOf`)
- `ThreadSafeConfig` with shared lock support; `FileLock` for cross-process coordination
- `interpolate()` with `${path.to.key}` and `${env:VAR}` resolution and circular-reference detection

### Breaking changes

None — this is the initial stable release.
