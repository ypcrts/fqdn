Fully-Qualified Domain Names
===================================
|Build Status| |Coverage Status| |Latest PyPI Version|

`PyPI Stats`_

Validates a fully-qualified domain name (FQDN), in full compliance with
`RFC 1035 <https://tools.ietf.org/html/rfc1035>`, and the "preferred form" 
specified in `RFC 3696 section 2 <https://tools.ietf.org/html/rfc3696#section-2>`_.

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


.. |Build Status| image:: https://travis-ci.org/ypcrts/fqdn.svg?branch=master
   :target: https://travis-ci.org/ypcrts/fqdn?branch=master
.. |Coverage Status| image:: https://coveralls.io/repos/github/ypcrts/fqdn/badge.svg?branch=master
   :target: https://coveralls.io/github/ypcrts/fqdn?branch=master
.. |Latest PyPI Version| image:: https://img.shields.io/pypi/v/fqdn.svg
   :target: https://pypi.python.org/pypi/fqdn
.. _PyPI Stats: https://pypistats.org/packages/fqdn
