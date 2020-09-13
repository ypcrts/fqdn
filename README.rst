Fully-Qualified Domain Names
===================================
|Build Status| |Coverage Status| |Latest PyPI Version| |Downloads| |Monthly Downloads|

Validates a fully-qualified domain name (FQDN)'s compliance with the
`RFC 1035 s. 2.3.1 <https://tools.ietf.org/html/rfc1035>`_ "preferred name
syntax".

Can also convert between absolute and relative FQDNs, and test equality
irrespective of alphabetic case.

The preferred name syntax restricts domain names to alphanumeric ASCII
characters and hypens as follows:

1. Each label can have a maximum of 63 characters separated by dots.

2. The total length of the FQDN cannot exceed a total of 253 bytes, not
   including the implied null label at the end (a single dot in string
   representations).

3. hyphens (`-`) may not appear at the beginning or end of a label, and

4. digits (`[0-9]`) may not appear at the beginning of a label.


This repo adds only one additional restriction in its validation code path:

5. by default, there must be a minimum of two labels, but this is configurable.

The preferred name syntax is same as described in other RFCs including:

- `RFC 1123 s. 2.1 <https://tools.ietf.org/html/rfc1123#section-2>`_ (authoritative for Internet host names)

- `RFC 3696 s. 2 <https://tools.ietf.org/html/rfc3696#section-2>`_ (commentary about domain name validation history)

By contrast, `RFC2181 s. 11 <http://tools.ietf.org/html/rfc2181#section-11>`_
comments that RFC 1035 does not restrict domain names to the preferred name
syntax set out in `RFC 1035 <http://tools.ietf.org/html/rfc1035>`_.

Web browsers like Google Chrome and Mozilla Firefox adhere only loosely to the
preferred name syntax with minor deviations, adding underscores (`_`), and
allowing hyphens to appear at the end of a label, and sometimes also the
beginning. See `#14 <https://github.com/ypcrts/fqdn/issues/14>`_.



.. code:: python

    from fqdn import FQDN

    domain = 'bbc.co.uk'
    bbc_fqdn = FQDN(domain)

    bbc_fqdn.is_valid
    # True

    bbc_fqdn.is_valid_absolute
    # False

    bbc_fqdn.is_valid_relative
    # True

    bbc_fqdn.absolute
    # bbc.co.uk.

    FQDN("bbc.co.uk") == FQDN("BBC.CO.UK.")
    # True


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
