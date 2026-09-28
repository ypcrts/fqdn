# Contributing

Thanks for taking the time to contribute. This document covers the setup and
the rules a change has to pass.

## Development setup

[uv](https://docs.astral.sh/uv/) creates the environment and locks the
dependency set:

```console
git clone git@github.com:ypcrts/fqdn.git
cd fqdn
uv sync --group dev
```

Then run the checks:

```console
uv run pytest --cov=fqdn
uv run ruff check fqdn tests
uv run ruff format --check fqdn tests
uv run mypy fqdn
```

`pre-commit` runs the linters and formatters on every commit:

```console
uv tool install pre-commit
pre-commit install
```

## Ground rules

### Supported Python versions

The published metadata advertises Python 2.7 and newer, so the source under
`fqdn/` must stay parseable by Python 2.7. That means:

- No f-strings, variable annotations, keyword-only arguments, or other syntax
  older interpreters cannot parse.
- Type information lives in `fqdn/__init__.pyi`, never as inline annotations.
  The stub is not executed, so it can use modern typing freely.
- The `UP` (pyupgrade) rules stay out of the ruff selection, because they would
  rewrite the source into syntax the advertised floor cannot parse.
- `fqdn/_compat.py` selects `functools.cached_property` on Python 3.8 and newer
  and falls back to the `cached-property` dependency below that.

The development toolchain (pytest, mypy, ruff and friends) only runs on modern
interpreters, which is what CI uses.

### Code style

- Match the style of the surrounding code and prefer self-documenting names to
  inline comments.
- Keep the public API on the `FQDN` class; the stub mirrors it.

### Tests

Add or update tests for behavior a user would notice. A bug fix should come with
a test that fails before the fix.

## Pull requests

- Branch from `develop`. `develop` is the integration branch; releases are
  tagged from it.
- Keep a pull request to one change, with a short description of the problem and
  the fix.
- Add a line to `CHANGELOG.md` under `Unreleased` for anything a user would
  notice.
- Make sure `uv run pytest`, `ruff check`, `ruff format --check` and `mypy` all
  pass. CI runs the same commands.

## Releasing

Maintainers cut a release by tagging:

1. In `CHANGELOG.md`, rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`,
   and add a fresh empty `## [Unreleased]` above it.
2. Commit that on `develop`.
3. Tag it and push the tag:

   ```console
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin vX.Y.Z
   ```

The tag starts the release workflow, which builds the distributions, publishes
them to PyPI over trusted publishing, and opens a GitHub release whose notes are
the changelog section for that version. `setuptools_scm` derives the package
version from the tag, so do not edit a version by hand.

## Reporting bugs

Open an issue with the Python version, the exact input, and what you expected to
happen. For security issues, follow [SECURITY.md](SECURITY.md) instead of
opening a public issue.
