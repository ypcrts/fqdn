import re


class FQDN:
    """
    From https://tools.ietf.org/html/rfc1035#page-9,  RFC 1035 3.1. Name space
    definitions:

        Domain names in messages are expressed in terms of a sequence of labels.
        Each label is represented as a one octet length field followed by that
        number of octets.  Since every domain name ends with the null label of
        the root, a domain name is terminated by a length byte of zero.  The
        high order two bits of every length octet must be zero, and the
        remaining six bits of the length field limit the label to 63 octets or
        less.

        To simplify implementations, the total length of a domain name (i.e.,
        label octets and label length octets) is restricted to 255 octets or
        less.


    Therefore the max length of a domain name is actually 253 ASCII bytes
    without the trailing null byte or the leading length byte, and the max
    length of a label is 62 bytes without the leading length byte.
    """
    FQDN_REGEX = re.compile('^((?!-)[-A-Z\d]{1,62}(?<!-)\.)+[A-Z]{1,62}\.?$',
                            re.IGNORECASE)

    def __init__(self, fqdn: str):
        try:
            assert fqdn and isinstance(fqdn, str)
        except:
            raise ValueError("fqdn must be str")
        self.fqdn = fqdn
        self.__is_valid = self.__validate()

    def __str__(self):
        return self.fqdn

    @property
    def is_valid(self):
        """
        Validates a fully-qualified domain name (FQDN), in full compliance with
        RFC 1035, and the "preferred form" specified in RFC 3686 s. 2.

        Tolerates both relative and absolute FQDNs.

        https://tools.ietf.org/html/rfc3696#section-2
        https://tools.ietf.org/html/rfc1035
        """
        return self.__is_valid

    def __validate(self) -> bool:
        """
        Iff the fqdn ends with a dot (in place of the RFC1035 trailing null
        byte), it may have a total length of 254 bytes, still it must be
        less than 253 bytes.
        """
        length = len(self.fqdn)
        if self.fqdn.endswith('.'):
            length -= 1
        if length > 253:
            return False
        return bool(self.FQDN_REGEX.match(self.fqdn))

    @property
    def is_valid_absolute(self) -> bool:
        """
        Validates a fully-qualified domain name (FQDN) is RFC preferred-form
        compliant, and ends with a `.`. With relative FQDNS in DNS lookups,
        the current hosts domain name or search domains may be appended.
        """
        return self.fqdn.endswith('.') and self.is_valid

    @property
    def is_valid_relative(self) -> bool:
        """
        Validates a fully-qualified domain name (FQDN) is RFC preferred-form
        compliant, and does not ends with a `.`.
        """
        return not self.fqdn.endswith('.') and self.is_valid

    @property
    def absolute(self) -> str:
        if not self.is_valid:
            raise ValueError(f'invalid FQDN `{self.fqdn}`')

        if self.is_valid_absolute:
            return self.fqdn

        return f'{self.fqdn}.'

    @property
    def relative(self) -> str:
        if not self.is_valid:
            raise ValueError(f'invalid FQDN `{self.fqdn}`')

        if self.is_valid_absolute:
            return self.fqdn[:-1]

        return self.fqdn
