Fully-Qualified Domain Names
===================================
|Build Status| |Coverage Status| |Latest PyPI Version| |Downloads| |Monthly Downloads|

Validates a fully-qualified domain name (FQDN), in full compliance with the
`RFC 1035 s. 2.3.1 <https://tools.ietf.org/html/rfc1035>` "preferred name
syntax". That form is comprised of alphanumeric ASCII characters as well as
hyphens, except at the beginning of labels, which are separated by dots in
human-readable representations.

The preferred name syntax is same as described in other RFCs including:

- `RFC 1123 s. 2.1 <https://tools.ietf.org/html/rfc1123#section-2>` (authoritative for Internet host names)

- `RFC 3696 s. 2 <https://tools.ietf.org/html/rfc3696#section-2>` (commentary about domain name validation history)

By contrast, `RFC2181 s. 11 <http://tools.ietf.org/html/rfc2181#section-11>`
comments that RFC 1035 does not restrict domain names to the preferred name
syntax set out in `RFC 1035 <http://tools.ietf.org/html/rfc1035>`.

Web browsers like Firefox and Chrome adhere to the preferred name syntax with
a minor deviation, adding underscores (`_`). See `#14 <https://github.com/ypcrts/fqdn/issues/14>`.


Can also convert between absolute and relative FQDNs.

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
