Fully-Qualified Domain Names
===================================
|Build Status| |Coverage Status| |Latest PyPI Version| |Downloads| |Monthly Downloads|

Validates fully-qualified domain names against `RFC 1123
<https://tools.ietf.org/html/rfc/1123>`_, so that they are acceptable to modern
browsers

This package can also convert between absolute and relative FQDNs, and test
equality irrespective of alphabetic case.


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



RFC1123 domain names to alphanumeric ASCII characters and hypens as follows:

1. Each label can have a maximum of 63 characters separated by dots.

2. The total length of the FQDN cannot exceed a total of 253 bytes, not
   including the implied null label at the end (a single dot in string
   representations).

This package adds only one additional restriction to those restrictions, that
there be a minimum of two labels, but this is configurable.

- `RFC 1123 s. 2.1 <https://tools.ietf.org/html/rfc1123#section-2>`_
  authoritative for Internet host names, and superseeds the older `RFC 1035
  <http://tools.ietf.org/html/rfc1035>`_

- `RFC 3696 s. 2 <https://tools.ietf.org/html/rfc3696#section-2>`_ (commentary
  about domain name validation history)

It's worth noting that `RFC2181 s. 11 <http://tools.ietf.org/html/rfc2181#section-11>`_
comments that RFC 1035 does not restrict domain names to the preferred name
syntax set out in `RFC 1035 <http://tools.ietf.org/html/rfc1035>`_. Instead
Internet hostnames are restricted more or less by a combination of tradition
and RFC2181, where this package finds itself.

This package Google Chrome and Mozilla Firefox adhere only loosely to the
preferred name syntax with minor deviations, adding underscores (`_`), and
allowing hyphens to appear at the end of a label, and sometimes also the
beginning. See `#14 <https://github.com/ypcrts/fqdn/issues/14>`_.
