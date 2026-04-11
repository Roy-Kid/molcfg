# Release Notes

## 1.0.0

Release date: `2026-04-11`

`1.0.0` is the first release positioned as stable for production use.

### Highlights

- Added recursive schema validation for nested structures.
- Added strict validation mode with `allow_extra=False`.
- Added default injection with `apply_defaults=True`.
- Added source metadata tracking with `Config.meta()`.
- Added automatic scalar and JSON-like coercion for `EnvSource` and `CliSource`.
- Fixed nested aliasing issues in merge and source-loading paths.
- Fixed nested thread-safe reads so they keep the same lock boundary.
- Added Zensical documentation and release engineering files.

### Upgrade Notes

- The PyPI package name is now `molcrafts-molcfg`.
  The Python import stays `molcfg`.
- `EnvSource` and `CliSource` now coerce values by default.
  Use `coerce=False` if your application requires raw strings.
- The package version is now `1.0.0`.
