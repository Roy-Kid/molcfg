"""Tests for thread safety, file locking, and interpolation."""

import threading

import pytest

from molcfg import Config, FileLock, ThreadSafeConfig, interpolate
from molcfg.errors import CircularReferenceError


class TestThreadSafeConfig:
    def test_basic_access(self):
        cfg = Config({"x": 1})
        ts = ThreadSafeConfig(cfg)
        assert ts["x"] == 1
        ts["x"] = 2
        assert ts["x"] == 2

    def test_concurrent_writes(self):
        cfg = Config({"counter": 0})
        ts = ThreadSafeConfig(cfg)
        errors: list[Exception] = []

        def increment():
            try:
                for _ in range(100):
                    with ts._lock:
                        val = ts._config._data["counter"]
                        ts._config._data["counter"] = val + 1
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=increment) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert ts["counter"] == 400

    def test_freeze_unfreeze(self):
        ts = ThreadSafeConfig(Config({"a": 1}))
        ts.freeze()
        from molcfg.errors import FrozenConfigError

        with pytest.raises(FrozenConfigError):
            ts["a"] = 2
        ts.unfreeze()
        ts["a"] = 2
        assert ts["a"] == 2

    def test_to_dict(self):
        ts = ThreadSafeConfig(Config({"a": {"b": 1}}))
        assert ts.to_dict() == {"a": {"b": 1}}

    def test_to_json(self):
        ts = ThreadSafeConfig(Config({"a": 1}))
        assert '"a": 1' in ts.to_json()

    def test_contains(self):
        ts = ThreadSafeConfig(Config({"a": 1}))
        assert "a" in ts

    def test_snapshot_rollback(self):
        ts = ThreadSafeConfig(Config({"x": 1}))
        ts.snapshot()
        ts["x"] = 2
        ts.rollback()
        assert ts["x"] == 1

    def test_nested_reads_return_threadsafe_wrapper(self):
        ts = ThreadSafeConfig(Config({"db": {"host": "localhost"}}))

        child = ts["db"]

        assert isinstance(child, ThreadSafeConfig)
        child.host = "other"
        assert ts["db.host"] == "other"

    def test_nested_attr_reads_return_threadsafe_wrapper(self):
        ts = ThreadSafeConfig(Config({"db": {"host": "localhost"}}))

        child = ts.db

        assert isinstance(child, ThreadSafeConfig)
        child["host"] = "other"
        assert ts.db.host == "other"


class TestFileLock:
    def test_lock_and_unlock(self, tmp_path):
        lock_path = tmp_path / "test.lock"
        lock = FileLock(lock_path)
        lock.acquire()
        lock.release()

    def test_context_manager(self, tmp_path):
        lock_path = tmp_path / "test.lock"
        with FileLock(lock_path):
            assert lock_path.exists()

    def test_concurrent_file_access(self, tmp_path):
        lock_path = tmp_path / "counter.lock"
        data_path = tmp_path / "counter.txt"
        data_path.write_text("0")

        def increment():
            for _ in range(50):
                with FileLock(lock_path):
                    val = int(data_path.read_text())
                    data_path.write_text(str(val + 1))

        threads = [threading.Thread(target=increment) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert int(data_path.read_text()) == 200


class TestInterpolation:
    def test_config_self_reference(self):
        data = {"base": "/opt", "data": "${base}/data"}
        result = interpolate(data)
        assert result["data"] == "/opt/data"

    def test_env_reference(self):
        data = {"home": "${env:MY_HOME}"}
        result = interpolate(data, environ={"MY_HOME": "/Users/alice"})
        assert result["home"] == "/Users/alice"

    def test_nested_reference(self):
        data = {"a": {"b": "hello"}, "c": "${a.b} world"}
        result = interpolate(data)
        assert result["c"] == "hello world"

    def test_circular_reference(self):
        data = {"a": "${b}", "b": "${a}"}
        with pytest.raises(CircularReferenceError):
            interpolate(data)

    def test_no_interpolation_needed(self):
        data = {"a": 1, "b": "plain"}
        result = interpolate(data)
        assert result == {"a": 1, "b": "plain"}

    def test_chained_reference(self):
        data = {"x": "base", "y": "${x}-ext", "z": "${y}-final"}
        result = interpolate(data)
        assert result["z"] == "base-ext-final"

    def test_missing_reference_left_unchanged(self):
        data = {"a": "${nonexistent}"}
        result = interpolate(data)
        assert result["a"] == "${nonexistent}"
