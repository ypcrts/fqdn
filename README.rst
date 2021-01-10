.. .............................................................................
.. AMAZING REFERENCES
.. .............................................................................
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/fqdn.svg
   :target: https://pypi.org/project/fqdn/

.. |Build Status| image:: https://travis-ci.org/ypcrts/fqdn.svg?branch=master
   :target: https://travis-ci.org/ypcrts/fqdn?branch=master

.. |Coverage Status| image:: https://coveralls.io/repos/github/ypcrts/fqdn/badge.svg?branch=master
   :target: https://coveralls.io/github/ypcrts/fqdn?branch=master

.. |Latest PyPI Version| image:: https://img.shields.io/pypi/v/fqdn.svg
   :target: https://pypi.python.org/pypi/fqdn

.. |Downloads| image:: https://pepy.tech/badge/fqdn
   :target: https://pepy.tech/project/fqdn

.. |Monthly Downloads| image:: https://pepy.tech/badge/fqdn/month
   :target: https://pepy.tech/project/fqdn/month

.. |License Status| image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn.svg?type=shield
   :target: https://app.fossa.com/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn?ref=badge_shield

.. |License Status Shield| image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn.svg?type=large
   :target: https://app.fossa.com/projects/git%2Bgithub.com%2Fypcrts%2Ffqdn

================================================================================
Python FQDN Fully-Qualified Domain Names
================================================================================

|License Status| |Build Status| |Coverage Status| |Latest PyPI Version|
|Downloads| |Monthly Downloads|

This package validates Fully Qualified Domain Names (FQDNs) conformant to the
Internet Engineering Task Force specification [#spec]_. The design intent is to
validate that a string would be traditionally acceptable as a public Internet
hostname to RFC-conformant software, which is a strict subset of the logic in
modern web browsers like Mozilla Firefox and Chromium that determines whether
make a DNS lookup [#letsencrypt]_. Configuration options can relax contraints
so that short hostnames without periods or others with underscores will
be valid. These relaxations are closer to how modern web browsers work [#browsers]_ .

>>> from fqdn import FQDN
>>> domain = 'bbc.co.uk'
>>> bbc_fqdn = FQDN(domain)
>>> bbc_fqdn.is_valid
True
>>> bbc_fqdn.absolute
'bbc.co.uk.'
>>> bbc_fqdn.relative
'bbc.co.uk'

Equality checks are implemented case insensitive conformant to to the IETF
specification [#equality].

>>> FQDN('BBC.CO.UK.') == FQDN('BbC.Co.uK')
True
>>> hash(FQDN('BBC.CO.UK.')) == hash(FQDN('BbC.Co.uK'))
True


.. [#spec] See `IETF Specification`_.
.. [#letsencrypt] Certificate Authorities like Let's Encrypt run a narrower set
  of string validation logic to determine validity for issuance. This package
  is not intended to achieve functional parity with CA issuance, because they
  may have proprietary or custom login. `Boulder's code
  <https://github.com/letsencrypt/boulder/blob/8139c8fe28d873c2f772827be30426d075103002/policy/pa.go#L218>`
  is starkly different from Chromium's, as outlined in `Issue #14
  <https://github.com/ypcrts/fqdn/issues/14#issuecomment-688604160>`.
.. [#browsers] See `Issue #14
  <https://github.com/ypcrts/fqdn/issues/14#issuecomment-688604160>`.


Standards Conformance
================================================================================

In the default configuration, this package adds only one additional constraint
to the IETF specification, requiring a minimum of two labels, separated by
periods. This extra restriction can be disabled. It is enabled by default to
prevent breaking backwards compatibility. Review the tests for examples of the
impact of this.


IETF Specification
--------------------------------------------------------------------------------

The IETF specification restricts domain names to alphanumeric ASCII characters
and hyphens as described below.

`RFC 1123 <https://tools.ietf.org/html/rfc1123>`_: Requirements for Internet
Hosts - Application and Support, October 1989
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   This RFC is an official specification for the Internet community.  It
   incorporates by reference, amends, corrects, and supplements the
   primary protocol standards documents relating to hosts.

..

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


`RFC 952 <https://tools.ietf.org/html/rfc952>`_: DoD Internet host table
specification, October 1985
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  This RFC is the official specification of the format of the Internet Host Table.

..
.. code:: text

    <hname> ::= <name>*["."<name>]
    <name>  ::= <let>[*[<let-or-digit-or-hyphen>]<let-or-digit>]


Commentary
--------------------------------------------------------------------------------

`RFC-1034 <https://tools.ietf.org/html/rfc1035>`_: Domain Name Concepts and
Facilities, November 1987
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Section 3.5 specifies a "preferred name syntax", which is non-compulsory.

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

`RFC-1035 <https://tools.ietf.org/html/rfc1035>`_: Domain Names
- Implementation and Specification, November 1987
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Section 2.3.1 repeats the "preferred name syntax" proposal from RFC-1034.

`RFC-2181 <https://tools.ietf.org/html/rfc2181>`_: Clarification to the DNS
Specification, July 1997
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Section 11 comments that RFC-1035 does not restrict domain names to the
preferred name syntax set out in it. Instead Internet hostnames are
restricted more or less by a combination of tradition and RFC-2181, where
this package finds itself.

`RFC-3696 <https://tools.ietf.org/html/rfc3696>`_: Application Techniques for
Checking and Transformation of Names, February 2004
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This memo provides *fascinating* commentary of the history of string validation
for domain names.

Licenses
===================================

|License Status Shield|
