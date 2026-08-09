"""The one door to the process environment for the molcrafts ecosystem.

Every molcrafts package reads environment variables through this module rather
than touching :data:`os.environ` directly. The point is not indirection — it is
that a variable must be *declared* before it can be read, so the set of
variables the ecosystem depends on can always be listed.

That matters because a setting which lives only in one shell cannot be reported
by any ``… config list`` command, and two processes launched differently will
silently disagree about it. Declaring makes the invisible enumerable::

    from molcfg.environment import declare, get

    declare("USER", purpose="whose jobs to list", project="molq")
    name = get("USER", default="")

:func:`get` refuses an undeclared name, which is what keeps :func:`describe`
complete rather than merely well-intentioned. Configuration still belongs in a
config file; what belongs here is what only the environment can answer —
where the config root lives, and who the current user is.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

__all__ = [
    "EnvVar",
    "UndeclaredEnvVar",
    "declare",
    "declared",
    "describe",
    "get",
]


class UndeclaredEnvVar(LookupError):
    """Raised when reading an environment variable nobody declared."""


@dataclass(frozen=True)
class EnvVar:
    """A single environment variable the ecosystem knows it depends on."""

    name: str
    purpose: str
    project: str


_DECLARED: dict[str, EnvVar] = {}


def declare(name: str, *, purpose: str, project: str) -> EnvVar:
    """Register *name* as a variable *project* reads, and say why.

    Idempotent for an identical declaration so import order does not matter.
    Re-declaring the same name with a different purpose or project is a
    conflict: two packages disagreeing about one variable is exactly the
    confusion this module exists to prevent.

    Args:
        name: The environment variable name.
        purpose: What it is for. Must be non-empty — a listing whose entries
            do not say what they are for is not a listing.
        project: The package that reads it (e.g. ``"molq"``).

    Returns:
        The registered :class:`EnvVar`.

    Raises:
        ValueError: If *purpose* or *project* is blank, or if *name* was
            already declared differently.
    """
    if not purpose.strip():
        raise ValueError(f"{name}: purpose must be non-empty")
    if not project.strip():
        raise ValueError(f"{name}: project must be non-empty")
    var = EnvVar(name=name, purpose=purpose, project=project)
    existing = _DECLARED.get(name)
    if existing is not None and existing != var:
        raise ValueError(
            f"{name} is already declared by {existing.project} "
            f"({existing.purpose!r}); one variable, one meaning"
        )
    _DECLARED[name] = var
    return var


def declared() -> tuple[EnvVar, ...]:
    """Every declared variable, sorted by name."""
    return tuple(sorted(_DECLARED.values(), key=lambda v: v.name))


def get(
    name: str,
    *,
    default: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> str | None:
    """Read a declared environment variable.

    Args:
        name: The variable to read. Must have been passed to :func:`declare`.
        default: Returned when the variable is unset.
        environ: Environment mapping to read. Defaults to :data:`os.environ`;
            pass one to isolate a caller from the real environment.

    Raises:
        UndeclaredEnvVar: If *name* was never declared. Declare it so it shows
            up in :func:`describe` — an undeclared read is invisible to every
            command that reports configuration.
    """
    if name not in _DECLARED:
        raise UndeclaredEnvVar(
            f"{name} is not declared; call "
            f"molcfg.environment.declare({name!r}, purpose=..., project=...) "
            f"so it can be listed alongside the rest"
        )
    env = environ if environ is not None else os.environ
    value = env.get(name)
    return default if value is None else value


def describe(
    environ: Mapping[str, str] | None = None,
) -> list[dict[str, object]]:
    """List every declared variable with its current state.

    This is the reportable form the declaration requirement buys: one row per
    variable, whether it is set, and what it is for.

    Returns:
        One dict per variable, sorted by name, with keys ``name``,
        ``purpose``, ``project``, ``set``, and ``value``.
    """
    env = environ if environ is not None else os.environ
    rows: list[dict[str, object]] = []
    for var in declared():
        value = env.get(var.name)
        rows.append(
            {
                "name": var.name,
                "purpose": var.purpose,
                "project": var.project,
                "set": value is not None,
                "value": value,
            }
        )
    return rows


declare(
    "MOLCRAFTS_HOME",
    purpose="Base directory for all molcrafts config; defaults to ~/.molcrafts",
    project="molcfg",
)
declare(
    "HOME",
    purpose="User home, used to resolve the default config base and expand ~",
    project="molcfg",
)
