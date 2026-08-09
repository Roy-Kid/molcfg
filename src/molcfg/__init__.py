"""molcfg — configuration library for the molcrafts ecosystem."""

from molcfg.concurrency import FileLock, ThreadSafeConfig, interpolate
from molcfg.config import Config
from molcfg.environment import EnvVar, UndeclaredEnvVar
from molcfg.environment import declare as declare_env_var
from molcfg.environment import declared as declared_env_vars
from molcfg.environment import describe as describe_env
from molcfg.environment import get as get_env_var
from molcfg.errors import (
    CircularReferenceError,
    ConfigError,
    FrozenConfigError,
    ValidationError,
)
from molcfg.merge import ConfigLoader, MergeStrategy, ProfileLoader, merge
from molcfg.paths import project_config_dir
from molcfg.registry import Registry
from molcfg.source import (
    CliSource,
    DictSource,
    EnvSource,
    JsonFileSource,
    Source,
    TomlFileSource,
    YamlFileSource,
)
from molcfg.validation import Build, Length, OneOf, Pattern, Range, validate

__all__ = [
    # Config
    "Config",
    # Errors
    "ConfigError",
    "CircularReferenceError",
    "FrozenConfigError",
    "ValidationError",
    # Sources
    "Source",
    "CliSource",
    "DictSource",
    "EnvSource",
    "JsonFileSource",
    "TomlFileSource",
    "YamlFileSource",
    # Merge
    "ConfigLoader",
    "MergeStrategy",
    "ProfileLoader",
    "merge",
    # Validation
    "Build",
    "Length",
    "OneOf",
    "Pattern",
    "Range",
    "validate",
    # Registry
    "Registry",
    # Concurrency
    "FileLock",
    "ThreadSafeConfig",
    "interpolate",
    # Paths
    "project_config_dir",
    # Environment — the one door to os.environ
    "EnvVar",
    "UndeclaredEnvVar",
    "declare_env_var",
    "declared_env_vars",
    "describe_env",
    "get_env_var",
]
