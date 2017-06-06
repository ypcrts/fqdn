import re


class FQDN:
    FQDN_REGEX = re.compile('^((?!-)[-A-Z\d]{1,63}(?<!-)\.)+[A-Z]{1,63}\.?$',
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
        return self.__is_valid

    def __validate(self) -> bool:
        """
        Validates a fully-qualified domain name (FQDN), in full compliance with
        RFC 1035, and the "preferred form" specified in RFC 3686 s. 2.

        Tolerates both relative and absolute FQDNs.

        https://tools.ietf.org/html/rfc3696#section-2
        https://tools.ietf.org/html/rfc1035
        """
        if len(self.fqdn) > 255:
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
