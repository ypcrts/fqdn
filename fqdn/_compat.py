import sys

if sys.version_info[:2] >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

if sys.version_info[0] >= 3:
    string_types = (str,)
else:
    string_types = (str, unicode)  # noqa: F821

__all__ = ["cached_property", "string_types"]
