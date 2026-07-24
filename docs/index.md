---
title: molcfg
description: Configuration library for predictable loading, merging, validation, and source tracking.
hide:
  - navigation
  - toc
hero:
  title: molcfg
  description: Load configuration from dicts, files, environment variables, and CLI arguments; merge the layers into one immutable object; validate it against a schema; and ask any value where it came from. A single runtime dependency, and every operation returns an isolated copy.
  install:
    label: Install
    command: pip install molcrafts-molcfg
  badges:
    - img: https://img.shields.io/pypi/v/molcrafts-molcfg
      href: https://pypi.org/project/molcrafts-molcfg/
      alt: PyPI version
    - img: https://img.shields.io/badge/python-3.12%2B-blue.svg
      href: https://pypi.org/project/molcrafts-molcfg/
      alt: Python 3.12+
    - img: https://img.shields.io/badge/license-BSD--3--Clause-blue.svg
      href: https://github.com/MolCrafts/molcfg/blob/master/LICENSE
      alt: License BSD-3-Clause
  actions:
    - label: Get started
      href: getting-started/
      style: primary
    - label: Sources
      href: sources/
    - label: API reference
      href: api/
---

<h1 class="molcrafts-sr-only">molcfg</h1>

<div class="molcrafts-manual-home" markdown>

<!-- ────────────────────────────────────────────────────────────
     AT A GLANCE — compact frame: static label + one code block
     ──────────────────────────────────────────────────────────── -->

<section class="molcrafts-manual-section molcrafts-manual-section--compact" markdown>

<div class="molcrafts-manual-section__header" markdown>

<span class="molcrafts-manual-eyebrow">At a glance</span>

## Layers in, one explained config out

Stack sources lowest-priority first. `ConfigLoader` merges them into an
immutable `Config`, and `meta()` reports the winning source and the full
override history for any value.

</div>

```python
from molcfg import CliSource, ConfigLoader, DictSource, EnvSource

cfg = ConfigLoader([
    DictSource({"db": {"host": "localhost", "port": 5432}}, name="defaults"),
    EnvSource(prefix="APP", name="env"),
    CliSource(["--db.port=6432"], name="cli"),
]).load()

assert cfg["db.port"] == 6432
assert cfg.meta("db.port") == {"source": "cli", "history": ("defaults", "cli")}
```

</section>

<!-- ────────────────────────────────────────────────────────────
     CAPABILITIES — stack frame + 2-column grid of linked cards
     ──────────────────────────────────────────────────────────── -->

<section class="molcrafts-manual-section molcrafts-manual-section--stack" markdown>

<div class="molcrafts-manual-section__header" markdown>

<span class="molcrafts-manual-eyebrow">What molcfg gives you</span>

## Everything a config layer needs, nothing it doesn't

</div>

<div class="molcrafts-manual-grid molcrafts-manual-grid--cols-2">
  <a href="sources/">
    <strong>Layered sources</strong>
    <p>Load from dicts, JSON / TOML / YAML files, environment variables, and CLI arguments — each a named <code>Source</code> you can stack in priority order.</p>
  </a>
  <a href="merge/">
    <strong>Immutable merge</strong>
    <p>Deep-merge, override, and append strategies via <code>ConfigLoader</code> and <code>ProfileLoader</code>. Every result is an isolated copy — inputs are never mutated.</p>
  </a>
  <a href="validation/">
    <strong>Schema validation</strong>
    <p>Recursive schemas with defaults, strict unknown-field checks, and built-in constraints (<code>Range</code>, <code>OneOf</code>, …). Fail fast with a clear message.</p>
  </a>
  <a href="getting-started/">
    <strong>Source tracking</strong>
    <p><code>Config.meta()</code> answers "where did this value come from?" — the winning source plus the full override history for every key.</p>
  </a>
  <a href="registry/">
    <strong>Registry &amp; Build</strong>
    <p>Resolve config strings like <code>"silu"</code> into Python classes or instances, so config files can drive object construction.</p>
  </a>
  <a href="concurrency/">
    <strong>Concurrency &amp; interpolation</strong>
    <p>A thread-safe wrapper and cross-platform file lock for shared access, plus <code>${path.to.key}</code> / <code>${env:VAR}</code> interpolation with circular-reference detection.</p>
  </a>
</div>

</section>

<!-- ────────────────────────────────────────────────────────────
     MANUAL INDEX — stack frame, full-width numbered chapter list
     ──────────────────────────────────────────────────────────── -->

<section class="molcrafts-manual-section molcrafts-manual-section--stack" markdown>

<div class="molcrafts-manual-section__header" markdown>

<span class="molcrafts-manual-eyebrow">Find your page</span>

## The manual in seven chapters

</div>

<nav class="molcrafts-manual-index" aria-label="Manual chapters">
  <a href="getting-started/">
    <span>01</span>
    <strong>Getting Started</strong>
    <em>Install molcfg, load your first config, and stack layered sources end to end.</em>
  </a>
  <a href="sources/">
    <span>02</span>
    <strong>Sources</strong>
    <em>Dict, file, environment, and CLI sources — how each parses input and reports its origin.</em>
  </a>
  <a href="validation/">
    <span>03</span>
    <strong>Validation</strong>
    <em>Schemas, defaults, strict mode, and the constraint family that guards every value.</em>
  </a>
  <a href="merge/">
    <span>04</span>
    <strong>Merge</strong>
    <em>Merge strategies, <code>ConfigLoader</code>, and <code>ProfileLoader</code> — always returning isolated copies.</em>
  </a>
  <a href="registry/">
    <span>05</span>
    <strong>Registry</strong>
    <em>String tags to classes and instances for config-driven factories.</em>
  </a>
  <a href="concurrency/">
    <span>06</span>
    <strong>Concurrency</strong>
    <em>Thread-safe wrapper, file locks, and interpolation with circular-reference detection.</em>
  </a>
  <a href="api/">
    <span>07</span>
    <strong>API Reference</strong>
    <em>The complete exported surface, module by module.</em>
  </a>
</nav>

</section>

</div>
