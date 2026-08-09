"""Tests for molcfg.environment — the one door to the process environment.

Every molcrafts package reaches environment variables through this module, so
the set of variables the ecosystem depends on is always enumerable. Reading an
undeclared name is an error; that is what keeps :func:`describe` complete
rather than merely well-intentioned.
"""

from __future__ import annotations

import pytest

from molcfg.environment import (
    EnvVar,
    UndeclaredEnvVar,
    declare,
    declared,
    describe,
    get,
)


@pytest.fixture(autouse=True)
def _isolate_registry():
    """Each test starts from the declarations molcfg itself makes."""
    from molcfg import environment

    saved = dict(environment._DECLARED)
    try:
        yield
    finally:
        environment._DECLARED.clear()
        environment._DECLARED.update(saved)


class TestDeclare:
    def test_returns_the_declaration(self):
        var = declare("MY_VAR", purpose="a purpose", project="demo")
        assert var == EnvVar(name="MY_VAR", purpose="a purpose", project="demo")

    def test_declaration_shows_up_in_the_listing(self):
        declare("MY_VAR", purpose="a purpose", project="demo")
        assert any(v.name == "MY_VAR" for v in declared())

    def test_redeclaring_identically_is_idempotent(self):
        first = declare("MY_VAR", purpose="p", project="demo")
        second = declare("MY_VAR", purpose="p", project="demo")
        assert first == second
        assert [v.name for v in declared()].count("MY_VAR") == 1

    def test_redeclaring_differently_is_a_conflict(self):
        declare("MY_VAR", purpose="p", project="demo")
        with pytest.raises(ValueError, match="already declared"):
            declare("MY_VAR", purpose="something else", project="other")

    def test_empty_purpose_is_rejected(self):
        # A listing whose entries do not say what they are for is not a listing.
        with pytest.raises(ValueError, match="purpose"):
            declare("MY_VAR", purpose="  ", project="demo")


class TestGet:
    def test_reads_a_declared_variable(self):
        declare("MY_VAR", purpose="p", project="demo")
        assert get("MY_VAR", environ={"MY_VAR": "value"}) == "value"

    def test_missing_value_returns_the_default(self):
        declare("MY_VAR", purpose="p", project="demo")
        assert get("MY_VAR", default="fallback", environ={}) == "fallback"

    def test_undeclared_variable_cannot_be_read(self):
        with pytest.raises(UndeclaredEnvVar, match="SNEAKY"):
            get("SNEAKY", environ={"SNEAKY": "value"})

    def test_the_error_says_how_to_fix_it(self):
        with pytest.raises(UndeclaredEnvVar, match="declare"):
            get("SNEAKY", environ={})


class TestDescribe:
    def test_reports_whether_each_variable_is_set(self):
        declare("SET_VAR", purpose="p", project="demo")
        declare("UNSET_VAR", purpose="p", project="demo")
        rows = {r["name"]: r for r in describe(environ={"SET_VAR": "x"})}
        assert rows["SET_VAR"]["set"] is True
        assert rows["SET_VAR"]["value"] == "x"
        assert rows["UNSET_VAR"]["set"] is False
        assert rows["UNSET_VAR"]["value"] is None

    def test_carries_purpose_and_project(self):
        declare("MY_VAR", purpose="why it exists", project="demo")
        row = next(r for r in describe(environ={}) if r["name"] == "MY_VAR")
        assert row["purpose"] == "why it exists"
        assert row["project"] == "demo"

    def test_sorted_by_name_for_stable_output(self):
        declare("ZZZ", purpose="p", project="demo")
        declare("AAA", purpose="p", project="demo")
        names = [r["name"] for r in describe(environ={})]
        assert names == sorted(names)


class TestMolcfgDeclaresItsOwn:
    """molcfg's own reads are declarations like everyone else's."""

    def test_molcrafts_home_is_declared(self):
        assert "MOLCRAFTS_HOME" in {v.name for v in declared()}

    def test_home_is_declared(self):
        assert "HOME" in {v.name for v in declared()}

    def test_every_declaration_names_a_project_and_purpose(self):
        for var in declared():
            assert var.project.strip(), f"{var.name} has no project"
            assert var.purpose.strip(), f"{var.name} has no purpose"
