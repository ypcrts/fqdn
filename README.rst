===================================
Fully-Qualified Domain Names
===================================

|License Status| |Build Status| |Coverage Status| |Latest PyPI Version| |Downloads| |Monthly Downloads|

This package validates Fully Qualified Domain Names (FQDNs) conformant to the Internet Engineering Task Force specification [#spec]_. The design intent is to validate that a string would be traditionally acceptable as a public Internet hostname to RFC-conformant software, which is a strict subset of the logic in modern web browsers like Mozilla Firefox and Chromium that determines whether make a DNS lookup [#letsencrypt]_. Configuration options can relax the contraints so that host names consisting of a single label or continaing underscores will be valid, which is closer to how modern web browsers work [#browsers]_ .

>>> from fqdn import FQDN
>>> domain = 'bbc.co.uk'
>>> bbc_fqdn = FQDN(domain)
>>> bbc_fqdn.is_valid
True
>>> bbc_fqdn.absolute
'bbc.co.uk.'
>>> bbc_fqdn.relative
'bbc.co.uk'

Equality checks are implemented case insensitive conformant to to the IETF specification [#equality].
    
>>> FQDN('BBC.CO.UK.') == FQDN('BbC.Co.uK')
True
>>> hash(FQDN('BBC.CO.UK.')) == hash(FQDN('BbC.Co.uK'))
True
    
Licenses
===================================

|License Status Shield| 

Standards Conformance
========================================================

In the default configuration, this package adds only one additional constraint to the IETF specification, requiring a minimum of two labels, separated by periods. This extra restriction can be disabled. It is enabled by default to prevent breaking backwards compatibility. Review the tests for examples of the impact of this. 


IETF Specification
------------------------------------

The IETF specification restricts domain names to alphanumeric ASCII characters and hyphens as described below.

`RFC 1123 <https://tools.ietf.org/html/rfc1123>`_: Requirements for Internet Hosts - Application and Support, October 1989
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

   Status of This Memo

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


`RFC 952 <https://tools.ietf.org/html/rfc952>`_: DoD Internet host table specification, October 1985
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

   STATUS OF THIS MEMO

   This RFC is the official specification of the format of the Internet
   Host Table.

.. code:: text

    <hname> ::= <name>*["."<name>]
    <name>  ::= <let>[*[<let-or-digit-or-hyphen>]<let-or-digit>]


Commentary
------------------------------------

.. [RFC-1035] November 1987. https://tools.ietf.org/html/rfc1035

.. [RFC-2181] https://tools.ietf.org/html/rfc2181 
   s. 11 <http://tools.ietf.org/html/rfc2181#section-11>`_.
   comments that [RFC-1035]_ does not restrict domain names to the preferred name
   syntax set out in it. Instead Internet hostnames are restricted more or less
   by a combination of tradition and [RFC-2181]_, where this package finds itself.
   
.. [RFC-3696] Domain name validation history



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
   
