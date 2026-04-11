"""Exception types for molcfg."""


class ConfigError(Exception):
    """Base exception for all molcfg errors."""


class FrozenConfigError(ConfigError):
    """Raised when attempting to modify a frozen Config."""


class CircularReferenceError(ConfigError):
    """Raised when interpolation detects a circular reference."""


class ValidationError(ConfigError):
    """Raised when config validation fails."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        msg = "; ".join(errors)
        super().__init__(msg)
