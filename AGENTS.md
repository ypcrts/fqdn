# AGENTS

## Supported Python versions

The package metadata advertises Python 2.7 and newer. The source under `fqdn/`
must stay parseable by Python 2.7:

- No f-strings, variable annotations, keyword-only arguments, or other syntax
  the floor cannot parse.
- Type information goes in `fqdn/__init__.pyi`, never as inline annotations.
  Update the stub whenever the public API changes.
- Keep `UP` (pyupgrade) out of the ruff selection.
- `fqdn/_compat.py` bridges `cached_property` down to Python 2.7.

The development toolchain only runs on modern interpreters, which is what CI
uses.

## Required engineering constraints

- Keep the public API on the `FQDN` class in sync with its stub.
- Prefer self-documenting names; add inline comments only when a maintainer
  needs context that the code cannot carry.
- Never bump a version by hand; `setuptools_scm` reads it from the git tag.
- Run `uv run pytest`, `uv run ruff check fqdn tests`,
  `uv run ruff format --check fqdn tests` and `uv run mypy fqdn` before
  declaring a change done.
- Add a `CHANGELOG.md` entry under `Unreleased` for user-visible changes.
