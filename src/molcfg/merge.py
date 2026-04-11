"""Configuration merging: strategies, loader, and profile support."""

from __future__ import annotations

import copy
import enum
from collections.abc import Mapping, Sequence
from typing import Any

from molcfg.config import Config
from molcfg.source import Source


class MergeStrategy(enum.Enum):
    """Strategy for merging two config dicts."""

    OVERRIDE = "override"
    APPEND = "append"
    DEEP_MERGE = "deep_merge"


def merge(
    base: dict[str, Any],
    override: dict[str, Any],
    strategy: MergeStrategy = MergeStrategy.DEEP_MERGE,
) -> dict[str, Any]:
    """Merge *override* into *base* using the given strategy.

    Returns a new dict; neither input is mutated.
    """
    if strategy is MergeStrategy.OVERRIDE:
        return copy.deepcopy(override)

    if strategy is MergeStrategy.APPEND:
        result = copy.deepcopy(base)
        for key, value in override.items():
            if key in result and isinstance(result[key], list) and isinstance(value, list):
                result[key] = result[key] + copy.deepcopy(value)
            else:
                result[key] = copy.deepcopy(value)
        return result

    # DEEP_MERGE
    return _deep_merge(base, override)


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


class ConfigLoader:
    """Load and merge configuration from an ordered list of sources.

    Later sources override earlier ones using the specified merge strategy.
    """

    def __init__(
        self,
        sources: Sequence[Source],
        strategy: MergeStrategy = MergeStrategy.DEEP_MERGE,
    ) -> None:
        self._sources = sources
        self._strategy = strategy

    def load(self) -> Config:
        merged: dict[str, Any] = {}
        metadata: dict[str, dict[str, Any]] = {}
        for source in self._sources:
            data = source.load()
            merged = merge(merged, data, self._strategy)
            _record_source_metadata(metadata, data, source.name)
        return Config(merged, metadata=metadata)


class ProfileLoader:
    """Apply named profile overrides on top of a base config.

    Profiles are provided as a dict mapping profile names to sources.
    """

    def __init__(
        self,
        base_sources: Sequence[Source],
        profiles: Mapping[str, Source],
        strategy: MergeStrategy = MergeStrategy.DEEP_MERGE,
    ) -> None:
        self._base_sources = base_sources
        self._profiles = profiles
        self._strategy = strategy

    def load(self, profile: str | None = None) -> Config:
        loader = ConfigLoader(self._base_sources, self._strategy)
        cfg = loader.load()
        if profile is not None:
            if profile not in self._profiles:
                raise KeyError(f"Unknown profile: {profile!r}")
            overlay = self._profiles[profile].load()
            merged = merge(cfg.to_dict(), overlay, self._strategy)
            metadata = cfg.metadata()
            _record_source_metadata(metadata, overlay, self._profiles[profile].name)
            cfg = Config(merged, metadata=metadata)
        return cfg


def _record_source_metadata(
    metadata: dict[str, dict[str, Any]],
    data: dict[str, Any],
    source_name: str,
) -> None:
    for path in _iter_metadata_paths(data):
        entry = metadata.setdefault(path, {"history": []})
        history = entry.setdefault("history", [])
        if isinstance(history, tuple):
            history = list(history)
            entry["history"] = history
        if not history or history[-1] != source_name:
            history.append(source_name)
        entry["source"] = source_name


def _iter_metadata_paths(node: dict[str, Any], prefix: str = ""):
    if prefix:
        yield prefix
    for key, value in node.items():
        path = f"{prefix}.{key}" if prefix else key
        yield path
        if isinstance(value, dict):
            yield from _iter_metadata_paths(value, path)
