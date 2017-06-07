FQDN: Fully-Qualified Domain Name
=================================

[![Build Status](https://travis-ci.org/0x6768/fqdn.svg?branch=master)](https://travis-ci.org/0x6768/fqdn?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/0x6768/fqdn/badge.svg?branch=master)](https://coveralls.io/github/0x6768/fqdn?branch=master)
[![Latest PyPi Version](https://img.shields.io/pypi/v/fqdn.svg)](https://pypi.python.org/pypi/fqdn)

Validates a fully-qualified domain name (FQDN), in full compliance with
RFC 1035, and the "preferred form" specified in RFC 3686 s. 2.

Can also validate absolute and relative FQDNs.

```python
from fqdn import FQDN


domain = 'bbc.co.uk'
fqdn = FQDN(domain)

fqdn.is_valid
# True

fqdn.is_valid_absolute
# False

fqdn.is_valid_relative
# True
```

