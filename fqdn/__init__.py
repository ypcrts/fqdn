import re

from fqdn._compat import cached_property, string_types


def _to_ascii(fqdn):
    try:
        return fqdn.encode("idna").decode("ascii")
    except UnicodeError:
        return fqdn


class FQDN:
    """
    From https://tools.ietf.org/html/rfc1035#page-9,  RFC 1035 3.1. Name space
    definitions:

        Domain names in messages are expressed in terms of a sequence of
        labels. Each label is represented as a one octet length field followed
        by that number of octets.  Since every domain name ends with the null
        label of the root, a domain name is terminated by a length byte of
        zero.  The high order two bits of every length octet must be zero, and
        the remaining six bits of the length field limit the label to 63 octets
        or less.

        To simplify implementations, the total length of a domain name (i.e.,
        label octets and label length octets) is restricted to 255 octets or
        less.


    Therefore the max length of a domain name is actually 253 ASCII bytes
    without the trailing null byte or the leading length byte, and the max
    length of a label is 63 bytes without the leading length byte.

    Internationalized domain names in Unicode are converted to their ASCII
    (IDNA/Punycode) form on construction, so they are validated and rendered
    against the same ASCII syntax described above.
    """

    PREFERRED_NAME_SYNTAX_REGEXSTR = (
        r"^((?![-])[-A-Z\d]{1,63}(?<!-)[.])*(?!-)[-A-Z\d]{1,63}(?<!-)[.]?$"
    )
    ALLOW_UNDERSCORES_REGEXSTR = (
        r"^((?![-])[-_A-Z\d]{1,63}(?<!-)[.])*(?!-)[-_A-Z\d]{1,63}(?<!-)[.]?$"
    )

    def __init__(self, fqdn, *nothing, **kwargs):
        if nothing:
            raise ValueError("got extra positional parameter, try kwargs")
        unknown_kwargs = set(kwargs.keys()) - {"allow_underscores", "min_labels"}
        if unknown_kwargs:
            raise ValueError("got extra kwargs: {}".format(unknown_kwargs))

        if not (fqdn and isinstance(fqdn, string_types)):
            raise ValueError("fqdn must be str")
        self._fqdn = _to_ascii(fqdn).lower()
        self._allow_underscores = kwargs.get("allow_underscores", False)
        self._min_labels = kwargs.get("min_labels", 2)

    def __str__(self):
        """
        The FQDN as a string in absolute form
        """
        return self.absolute

    @property
    def _regex(self):
        regexstr = (
            FQDN.PREFERRED_NAME_SYNTAX_REGEXSTR
            if not self._allow_underscores
            else FQDN.ALLOW_UNDERSCORES_REGEXSTR
        )
        return re.compile(regexstr, re.IGNORECASE)

    @cached_property
    def is_valid(self):
        """
        True for a validated fully-qualified domain name (FQDN), in full
        compliance with RFC 1035, and the "preferred form" specified in RFC
        3686 s. 2, whether relative or absolute.

        https://tools.ietf.org/html/rfc3696#section-2
        https://tools.ietf.org/html/rfc1035

        If and only if the FQDN ends with a dot (in place of the RFC1035
        trailing null byte), it may have a total length of 254 bytes, still it
        must be less than 253 bytes.
        """
        length = len(self._fqdn)
        if self._fqdn.endswith("."):
            length -= 1
        if length > 253:
            return False
        regex_pass = self._regex.match(self._fqdn)
        if not regex_pass:
            return False

        return self.labels_count >= self._min_labels

    @property
    def labels_count(self):
        has_terminal_dot = self._fqdn[-1] == "."
        count = self._fqdn.count(".") + (0 if has_terminal_dot else 1)
        return count

    @cached_property
    def is_valid_absolute(self):
        """
        True for a fully-qualified domain name (FQDN) that is RFC
        preferred-form compliant and ends with a `.`.

        With relative FQDNS in DNS lookups, the current hosts domain name or
        search domains may be appended.
        """
        return self._fqdn.endswith(".") and self.is_valid

    @cached_property
    def is_valid_relative(self):
        """
        True for a validated fully-qualified domain name that compiles with the
        RFC preferred-form and does not ends with a `.`.
        """
        return not self._fqdn.endswith(".") and self.is_valid

    @cached_property
    def absolute(self):
        """
        The FQDN as a string in absolute form
        """
        if not self.is_valid:
            raise ValueError("invalid FQDN `{0}`".format(self._fqdn))

        if self.is_valid_absolute:
            return self._fqdn

        return "{0}.".format(self._fqdn)

    @cached_property
    def relative(self):
        """
        The FQDN as a string in relative form
        """
        if not self.is_valid:
            raise ValueError("invalid FQDN `{0}`".format(self._fqdn))

        if self.is_valid_absolute:
            return self._fqdn[:-1]

        return self._fqdn

    def __eq__(self, other):
        if isinstance(other, FQDN):
            return self.absolute == other.absolute

    def __hash__(self):
        return hash(self.absolute) + hash("fqdn")


class _K8sName:
    """
    Shared behavior for the Kubernetes name validators. The formats and limits
    mirror k8s.io/apimachinery/pkg/util/validation, the package the Kubernetes
    API server validates names with.
    """

    REGEXSTR = r""
    MAX_LENGTH = 0

    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError("name must be str")
        self._name = name

    @property
    def _regex(self):
        return re.compile(self.REGEXSTR)

    @cached_property
    def is_valid(self):
        if len(self._name) > self.MAX_LENGTH:
            return False
        return self._regex.match(self._name) is not None


class K8sLabel(_K8sName):
    """
    A Kubernetes DNS-1123 label, the format `IsDNS1123Label` accepts for
    Namespace and StatefulSet names. It is a lowercase alphanumeric string or
    '-', starts and ends with an alphanumeric character, and is at most 63
    characters.

    The Kubernetes names documentation says RFC 1123 labels must start with an
    alphabetic character, but the implementation has always accepted a leading
    digit; this class follows the implementation.

    https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-label-names
    """

    REGEXSTR = r"[a-z0-9]([-a-z0-9]*[a-z0-9])?\Z"
    MAX_LENGTH = 63


class K8sSubdomain(_K8sName):
    """
    A Kubernetes DNS-1123 subdomain, the format `IsDNS1123Subdomain` accepts
    for most object names, such as Pods and Deployments. It is a
    period-separated sequence of lowercase alphanumeric characters, '-' or '.',
    starts and ends with an alphanumeric character, and is at most 253
    characters.

    https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
    """

    REGEXSTR = r"[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*\Z"
    MAX_LENGTH = 253


class K8sLabelValue(_K8sName):
    """
    A Kubernetes label value, the format `IsValidLabelValue` accepts for
    `metadata.labels` values. It may be empty, starts and ends with an
    alphanumeric character, may contain '-', '_' and '.', and is at most 63
    characters.

    https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set
    """

    REGEXSTR = r"(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?\Z"
    MAX_LENGTH = 63


class K8sQualifiedName(_K8sName):
    """
    A Kubernetes qualified name, the format `IsQualifiedName` accepts for
    label and annotation keys. It is an optional DNS-1123 subdomain prefix and
    '/', followed by a name of at most 63 characters that starts and ends with
    an alphanumeric character and may contain '-', '_' and '.'.

    https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set
    """

    NAME_REGEXSTR = r"([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]\Z"
    MAX_NAME_LENGTH = 63

    @property
    def _name_regex(self):
        return re.compile(self.NAME_REGEXSTR)

    @cached_property
    def is_valid(self):
        parts = self._name.split("/")
        if len(parts) == 1:
            name = parts[0]
        elif len(parts) == 2 and K8sSubdomain(parts[0]).is_valid:
            name = parts[1]
        else:
            return False
        if not name or len(name) > self.MAX_NAME_LENGTH:
            return False
        return self._name_regex.match(name) is not None
