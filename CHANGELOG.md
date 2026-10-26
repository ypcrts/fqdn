# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-09-28

### Changed

- **Breaking:** `FQDN` now accepts Unicode input that it previously rejected as
  invalid, encoding it to ASCII (IDNA/Punycode) before validation. A non-ASCII
  hostname whose `is_valid` was `False` may now pass, and `absolute`,
  `relative` and `str()` return its Punycode form instead of raising.
  Applications that relied on non-ASCII hostnames being rejected — for example
  to enforce an ASCII-only or anti-homograph policy — must apply their own
  check to the input before constructing an `FQDN`. ASCII input is unaffected.

### Added

- IDN support: Unicode domain names are encoded to their ASCII (IDNA/Punycode)
  form in the constructor, so names such as `Bücher.example` validate and
  render as `xn--bcher-kva.example.` (#12, #25).
- `K8sLabel`, `K8sSubdomain`, `K8sLabelValue` and `K8sQualifiedName` validators
  for the DNS-1123 names, label values and qualified names Kubernetes enforces.

## [1.6.0] - 2026-09-28

### Added

- `fqdn/__init__.pyi` type stubs and a `py.typed` marker, so type checkers
  resolve the public API.
- A CI matrix over Linux, macOS and Windows on Python 3.10 through 3.14, plus a
  compatibility job that installs the built wheel on Python 3.8 and 3.9.
- CodeQL, OSSAR, OpenSSF Scorecard, Snyk and FOSSA scanning workflows.
- A `release` workflow that publishes to PyPI over trusted publishing when a
  `v*` tag is pushed, and opens a GitHub release from the matching changelog
  section.
- Read the Docs configuration and a Sphinx build for the existing docs.
- `CONTRIBUTING.md`, `AGENTS.md` and issue and pull request templates.
- Renovate configuration for security updates and lock file maintenance.

### Changed

- Packaging moved from `setup.py`/`setup.cfg`/bumpversion to `pyproject.toml`
  with `setuptools_scm`; the version is derived from the git tag.
- Linting moved from flake8, black and prospector to ruff, and mypy now checks
  the package.
- The README is Markdown and carries a full badge wall.
- `tests/test_fqdn.py` import block is sorted to satisfy ruff.

### Removed

- `setup.py`, `setup.cfg`, `.bumpversion.cfg`, `tox.ini`, `.flake8` and
  `.prospector.yml`.

### Notes

- The published metadata still advertises Python 2.7 and newer, and the wheel
  still installs there. The source distribution no longer builds on interpreters
  older than 3.9, which the build backend requires.

## [1.5.1] - 2021-03-11

### Added

- Continuous integration for coverage reporting and PyPy in GitHub Actions.

### Changed

- Python 3.9 is tested with no code changes.
- Restored the coverage report to 100%.

## [1.5.0] - 2020-10-04

### Added

- `min_labels` and rejection of hostnames with an initial digit.
- `allow_underscores` (renamed from `strict`), which relaxes validation toward
  browser behavior.

### Changed

- Support for RFC 1123 preferred-name syntax.
- Test suite converted to pytest.

## [1.4.0] - 2020-04-26

### Added

- `FQDN` is hashable and `__eq__` is case-insensitive per RFC 4343.
- `__str__` returns the absolute form.

### Changed

- `cached_property` is no longer required on Python 3.8 and newer.

## [1.3.1] - 2020-03-21

### Changed

- Python 3.8 support, and the code formatted with black.

## [1.3.0] - 2020-03-07

### Fixed

- Reject all-numeric top-level labels.

## [1.2.0] - 2019-12-22

### Added

- Earlier releases; see the repository history for details.
