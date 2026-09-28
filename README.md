# Python FQDN — Fully-Qualified Domain Names

[![CI](https://github.com/ypcrts/fqdn/actions/workflows/ci.yml/badge.svg)](https://github.com/ypcrts/fqdn/actions/workflows/ci.yml)
[![CodeQL](https://github.com/ypcrts/fqdn/actions/workflows/codeql.yml/badge.svg)](https://github.com/ypcrts/fqdn/actions/workflows/codeql.yml)
[![OSSAR](https://github.com/ypcrts/fqdn/actions/workflows/ossar.yml/badge.svg)](https://github.com/ypcrts/fqdn/actions/workflows/ossar.yml)
[![codecov](https://codecov.io/gh/ypcrts/fqdn/branch/develop/graph/badge.svg?token=cavArywW2X)](https://codecov.io/gh/ypcrts/fqdn)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/ypcrts/fqdn/badge)](https://securityscorecards.dev/viewer/?uri=github.com/ypcrts/fqdn)
[![PyPI version](https://img.shields.io/pypi/v/fqdn)](https://pypi.org/project/fqdn/)
[![PyPI downloads](https://img.shields.io/pypi/dm/fqdn)](https://pepy.tech/projects/fqdn)
[![License: MPL-2.0](https://img.shields.io/pypi/l/fqdn)](LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/fqdn)](https://pypi.org/project/fqdn/)
[![Snyk](https://snyk.io/test/github/ypcrts/fqdn/badge.svg)](https://snyk.io/test/github/ypcrts/fqdn)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn?ref=shield)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-blue)](https://github.com/python/mypy)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Read the Docs](https://readthedocs.org/projects/fqdn/badge/?version=stable)](https://fqdn.readthedocs.io/)

This package validates Fully Qualified Domain Names (FQDNs) conforming to the
Internet Engineering Task Force specification (see
[IETF Specification](#ietf-specification)). The design intent is to validate
that a string would be traditionally acceptable as a public Internet hostname
to RFC-conforming software, which is a strict subset of the logic in modern web
browsers like Mozilla Firefox and Chromium that determines whether to make a DNS
lookup. Configuration options can relax constraints so that short hostnames
without periods or others with underscores will be valid. These relaxations are
closer to how modern web browsers work (see [Notes](#notes)).

```python
>>> from fqdn import FQDN
>>> domain = 'bbc.co.uk'
>>> bbc_fqdn = FQDN(domain)
>>> bbc_fqdn.is_valid
True
>>> bbc_fqdn.absolute
'bbc.co.uk.'
>>> bbc_fqdn.relative
'bbc.co.uk'
```

Equality checks are implemented case insensitive conforming to the IETF
specification:

```python
>>> FQDN('BBC.CO.UK.') == FQDN('BbC.Co.uK')
True
>>> hash(FQDN('BBC.CO.UK.')) == hash(FQDN('BbC.Co.uK'))
True
```

Internationalized domain names (IDNs) are converted to their ASCII
(IDNA/Punycode) form, so they validate and render like any other FQDN:

```python
>>> from fqdn import FQDN
>>> idn = FQDN('Bücher.example')
>>> idn.is_valid
True
>>> idn.absolute
'xn--bcher-kva.example.'
```

## Kubernetes names

Kubernetes validates object names against DNS-1123 formats. `K8sLabel`,
`K8sSubdomain`, `K8sLabelValue` and `K8sQualifiedName` mirror the functions the
API server calls, so a name can be checked before it is submitted. Unlike
`FQDN`, the DNS-1123 labels are case-sensitive and reject uppercase.

```python
>>> from fqdn import K8sLabel, K8sSubdomain
>>> K8sLabel('web-1').is_valid
True
>>> K8sLabel('Web-1').is_valid
False
>>> K8sSubdomain('svc.cluster.local').is_valid
True
```

Each class matches a function in
[`k8s.io/apimachinery/pkg/util/validation`](https://github.com/kubernetes/apimachinery/blob/master/pkg/util/validation/validation.go),
the package the API server validates names with:

| Class | Kubernetes function | Example |
| --- | --- | --- |
| `K8sLabel` | `IsDNS1123Label` | Namespace and StatefulSet names |
| `K8sSubdomain` | `IsDNS1123Subdomain` | Pod and Deployment names |
| `K8sLabelValue` | `IsValidLabelValue` | `metadata.labels` values |
| `K8sQualifiedName` | `IsQualifiedName` | label and annotation keys |

The rules come from the Kubernetes [Object
Names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)
documentation and the labels [syntax and character
set](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set),
which cite [RFC 1123](https://tools.ietf.org/html/rfc1123) and [RFC
1035](https://tools.ietf.org/html/rfc1035). Two details are worth knowing:

- `IsDNS1123Label` accepts a leading digit. The names documentation currently
  says RFC 1123 labels must start with an alphabetic character, but the
  implementation has always matched `[a-z0-9]`; `K8sLabel` follows the
  implementation.
- Service names use the stricter RFC 1035 label form and are therefore out of
  scope. The `RelaxedServiceNameValidation` feature gate switches newly created
  Services to `IsDNS1123Label`.

## Notes

- **Certificate authorities.** Certificate authorities like Let's Encrypt run a
  narrower set of string validation logic to determine validity for issuance.
  This package is not intended to achieve functional parity with CA issuance,
  because they may have proprietary or custom logic.
  [`boulder`'s code](https://github.com/letsencrypt/boulder/blob/8139c8fe28d873c2f772827be30426d075103002/policy/pa.go#L218)
  is starkly different from Chromium's, as outlined in
  [issue #14](https://github.com/ypcrts/fqdn/issues/14#issuecomment-688604160).
- **Browsers.** See
  [issue #14](https://github.com/ypcrts/fqdn/issues/14#issuecomment-688604160).
- **Internationalized domain names.** Unicode input is encoded with the
  standard library `idna` codec, which implements IDNA2003. Browsers apply the
  newer UTS #46 / IDNA2008 rules, which differ for characters such as `ß`
  (`straße.de` becomes `strasse.de` here, but `xn--strae-oqa.de` in a browser).

## Standards Conformance

In the default configuration, this package adds only one additional constraint
to the IETF specification, requiring a minimum of two labels, separated by
periods. This extra restriction can be disabled. It is enabled by default to
prevent breaking backwards compatibility. Review the tests for examples of the
impact of this.

### IETF Specification

The IETF specification restricts domain names to alphanumeric ASCII characters
and hyphens as described below.

[RFC 1123](https://tools.ietf.org/html/rfc1123): Requirements for Internet
Hosts - Application and Support, October 1989

> This RFC is an official specification for the Internet community. It
> incorporates by reference, amends, corrects, and supplements the primary
> protocol standards documents relating to hosts.

```
2.1  Host Names and Numbers

The syntax of a legal Internet host name was specified in RFC-952
[DNS:4].  One aspect of host name syntax is hereby changed: the
restriction on the first character is relaxed to allow either a
letter or a digit.  Host software MUST support this more liberal
syntax.

Host software MUST handle host names of up to 63 characters and
SHOULD handle host names of up to 255 characters.

Whenever a user inputs the identity of an Internet host, it SHOULD
be possible to enter either (1) a host domain name or (2) an IP
address in dotted-decimal ("#.#.#.#") form.  The host SHOULD check
the string syntactically for a dotted-decimal number before
looking it up in the Domain Name System.
```

[RFC 952](https://tools.ietf.org/html/rfc952): DoD Internet host table
specification, October 1985

> This RFC is the official specification of the format of the Internet Host
> Table.

```text
<hname> ::= <name>*["."<name>]
<name>  ::= <let>[*[<let-or-digit-or-hyphen>]<let-or-digit>]
```

### Commentary

[RFC 1034](https://tools.ietf.org/html/rfc1035): Domain Name Concepts and
Facilities, November 1987

- Section 3.5 specifies a "preferred name syntax", which is non-compulsory.

  ```
  3.5. Preferred name syntax

  The DNS specifications attempt to be as general as possible in the rules
  for constructing domain names.  The idea is that the name of any
  existing object can be expressed as a domain name with minimal changes.
  However, when assigning a domain name for an object, the prudent user
  will select a name which satisfies both the rules of the domain system
  and any existing rules for the object, whether these rules are published
  or implied by existing programs.

  For example, when naming a mail domain, the user should satisfy both the
  rules of this memo and those in RFC-822.  When creating a new host name,
  the old rules for HOSTS.TXT should be followed.  This avoids problems
  when old software is converted to use domain names.
  ```

[RFC 1035](https://tools.ietf.org/html/rfc1035): Domain Names -
Implementation and Specification, November 1987

- Section 2.3.1 repeats the "preferred name syntax" proposal from RFC 1034.

[RFC 2181](https://tools.ietf.org/html/rfc2181): Clarification to the DNS
Specification, July 1997

- Section 11 comments that RFC 1035 does not restrict domain names to the
  preferred name syntax set out in it. Instead Internet hostnames are
  restricted more or less by a combination of tradition and RFC 2181, where
  this package finds itself.

[RFC 3696](https://tools.ietf.org/html/rfc3696): Application Techniques for
Checking and Transformation of Names, February 2004

- This memo provides *fascinating* commentary of the history of string
  validation for domain names.

## Licenses

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn)
