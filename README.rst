Fully-Qualified Domain Names
===================================
|Build Status| |Coverage Status| |Latest PyPI Version|

Validates a fully-qualified domain name (FQDN), in full compliance with
`RFC 1035 <https://tools.ietf.org/html/rfc1035>`, and the "preferred form" 
specified in `RFC 3696 section 2 <https://tools.ietf.org/html/rfc3696#section-2>`_.

Can also convert between absolute and relative FQDNs.

.. code:: python

    from fqdn import FQDN


    domain = 'bbc.co.uk'
    fqdn = FQDN(domain)

    fqdn.is_valid
    # True

    fqdn.is_valid_absolute
    # False

    fqdn.is_valid_relative
    # True

    fqdn.absolute
    # bbc.co.uk.

.. |Build Status| image:: https://travis-ci.org/guyhughes/fqdn.svg?branch=master
   :target: https://travis-ci.org/guyhughes/fqdn?branch=master
.. |Coverage Status| image:: https://coveralls.io/repos/github/guyhughes/fqdn/badge.svg?branch=master
   :target: https://coveralls.io/github/guyhughes/fqdn?branch=master
.. |Latest PyPI Version| image:: https://img.shields.io/pypi/v/fqdn.svg
   :target: https://pypi.python.org/pypi/fqdn
