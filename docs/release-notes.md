# Release Notes

## 1.0.0

Release date: 2026-04-12

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
