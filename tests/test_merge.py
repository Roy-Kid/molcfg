"""Tests for merge strategies, ConfigLoader, and profiles."""

import pytest

from molcfg import (
    ConfigLoader,
    DictSource,
    MergeStrategy,
    ProfileLoader,
    merge,
)


class TestMerge:
    def test_deep_merge(self):
        base = {"db": {"host": "a", "port": 5432}}
        override = {"db": {"host": "b"}}
        result = merge(base, override, MergeStrategy.DEEP_MERGE)
        assert result == {"db": {"host": "b", "port": 5432}}

    def test_override_strategy(self):
        base = {"db": {"host": "a", "port": 5432}}
        override = {"db": {"host": "b"}}
        result = merge(base, override, MergeStrategy.OVERRIDE)
        assert result == {"db": {"host": "b"}}

    def test_append_strategy_lists(self):
        base = {"tags": ["a", "b"]}
        override = {"tags": ["c"]}
        result = merge(base, override, MergeStrategy.APPEND)
        assert result == {"tags": ["a", "b", "c"]}

    def test_append_strategy_scalars(self):
        base = {"x": 1}
        override = {"x": 2}
        result = merge(base, override, MergeStrategy.APPEND)
        assert result == {"x": 2}

    def test_deep_merge_nested(self):
        base = {"a": {"b": {"c": 1, "d": 2}}}
        override = {"a": {"b": {"c": 10, "e": 3}}}
        result = merge(base, override)
        assert result == {"a": {"b": {"c": 10, "d": 2, "e": 3}}}

    def test_does_not_mutate_inputs(self):
        base = {"a": {"b": 1}}
        override = {"a": {"c": 2}}
        merge(base, override)
        assert base == {"a": {"b": 1}}
        assert override == {"a": {"c": 2}}

    def test_result_does_not_share_nested_state_with_inputs(self):
        base = {"a": {"b": 1}}
        override = {"a": {"c": 2}}

        result = merge(base, override)
        result["a"]["b"] = 99
        result["a"]["c"] = 100

        assert base == {"a": {"b": 1}}
        assert override == {"a": {"c": 2}}

    def test_override_strategy_returns_isolated_copy(self):
        override = {"db": {"host": "b"}}

        result = merge({}, override, MergeStrategy.OVERRIDE)
        result["db"]["host"] = "changed"

        assert override == {"db": {"host": "b"}}

    def test_append_strategy_returns_isolated_copy(self):
        base = {"tags": ["a"]}
        override = {"tags": ["b"]}

        result = merge(base, override, MergeStrategy.APPEND)
        result["tags"].append("c")

        assert base == {"tags": ["a"]}
        assert override == {"tags": ["b"]}


class TestConfigLoader:
    def test_load_multiple_sources(self):
        defaults = DictSource({"db": {"host": "localhost", "port": 5432}})
        overrides = DictSource({"db": {"host": "production"}})
        loader = ConfigLoader([defaults, overrides])
        cfg = loader.load()
        assert cfg["db.host"] == "production"
        assert cfg["db.port"] == 5432

    def test_empty_sources(self):
        loader = ConfigLoader([])
        cfg = loader.load()
        assert cfg.to_dict() == {}

    def test_tracks_config_value_sources(self):
        defaults = DictSource(
            {"db": {"host": "localhost", "port": 5432}},
            name="defaults",
        )
        env = DictSource({"db": {"host": "prod-db"}}, name="env")

        cfg = ConfigLoader([defaults, env]).load()

        assert cfg.meta("db.host") == {
            "source": "env",
            "history": ("defaults", "env"),
        }
        assert cfg.meta("db.port") == {
            "source": "defaults",
            "history": ("defaults",),
        }


class TestProfileLoader:
    def test_load_with_profile(self):
        base = [DictSource({"db": {"host": "localhost"}})]
        profiles = {
            "prod": DictSource({"db": {"host": "prod-db"}}),
        }
        loader = ProfileLoader(base, profiles)
        cfg = loader.load("prod")
        assert cfg["db.host"] == "prod-db"

    def test_load_without_profile(self):
        base = [DictSource({"db": {"host": "localhost"}})]
        loader = ProfileLoader(base, {})
        cfg = loader.load()
        assert cfg["db.host"] == "localhost"

    def test_unknown_profile_raises(self):
        loader = ProfileLoader([], {})
        with pytest.raises(KeyError, match="unknown"):
            loader.load("unknown")

    def test_profile_load_updates_source_history(self):
        loader = ProfileLoader(
            [DictSource({"db": {"host": "localhost"}}, name="defaults")],
            {"prod": DictSource({"db": {"host": "prod-db"}}, name="profile:prod")},
        )

        cfg = loader.load("prod")

        assert cfg.meta("db.host") == {
            "source": "profile:prod",
            "history": ("defaults", "profile:prod"),
        }
