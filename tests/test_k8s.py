# coding=utf-8
import sys

import pytest

from fqdn import K8sLabel, K8sLabelValue, K8sQualifiedName, K8sSubdomain


@pytest.mark.parametrize(
    "cls", [K8sLabel, K8sSubdomain, K8sLabelValue, K8sQualifiedName]
)
@pytest.mark.parametrize("name", [None, 0, False, ["a"], ("a",)])
def test_non_str_raises(cls, name):
    with pytest.raises(ValueError):
        cls(name)


@pytest.mark.skipif(sys.version_info < (3, 0), reason="bytes are str on Python 2")
@pytest.mark.parametrize(
    "cls", [K8sLabel, K8sSubdomain, K8sLabelValue, K8sQualifiedName]
)
@pytest.mark.parametrize("name", [b"", b"abc"])
def test_bytes_raise(cls, name):
    with pytest.raises(ValueError):
        cls(name)


class TestK8sLabel:
    @pytest.mark.parametrize(
        "name",
        [
            "a",
            "0",
            "abc",
            "a0c",
            "a-0c",
            "test-name",
            "01010",
            "0-0",
            "0--0",
            "xn--80ak6aa92e",
            "a" * 63,
        ],
    )
    def test_valid(self, name):
        assert K8sLabel(name).is_valid

    @pytest.mark.parametrize(
        "name",
        [
            "",
            " ",
            "A",
            "A0c",
            "-a",
            "a-",
            "-",
            "a.b",
            "a_b",
            "a b",
            "ab\ncd",
            "abc\n",
            "abc\n\n",
            "a" * 64,
        ],
    )
    def test_invalid(self, name):
        assert not K8sLabel(name).is_valid


class TestK8sSubdomain:
    @pytest.mark.parametrize(
        "name",
        [
            "a",
            "example.com",
            "svc.cluster.local",
            "a-b.c-d",
            "0.0.0.0",
            "a" * 63,
            ".".join(["a" * 63, "a" * 63, "a" * 63, "a" * 61]),
            # Kubernetes checks only the total length, not each label.
            "a" * 64,
        ],
    )
    def test_valid(self, name):
        assert K8sSubdomain(name).is_valid

    @pytest.mark.parametrize(
        "name",
        [
            "",
            "A.com",
            ".com",
            "com.",
            "a..b",
            "a_b.com",
            "a b.com",
            "-a.com",
            "a-.com",
            "abc\n",
            "a.\n",
            ".".join(["a" * 63, "a" * 63, "a" * 63, "a" * 62]),
        ],
    )
    def test_invalid(self, name):
        assert not K8sSubdomain(name).is_valid


class TestK8sLabelValue:
    @pytest.mark.parametrize(
        "name",
        [
            "",
            "a",
            "A",
            "0",
            "A.B_c-d",
            "a-b",
            "a_b",
            "a.b",
            "a..b",
            "a" * 63,
        ],
    )
    def test_valid(self, name):
        assert K8sLabelValue(name).is_valid

    @pytest.mark.parametrize(
        "name",
        [
            "-a",
            "a-",
            "_a",
            "a_",
            ".a",
            "a.",
            "a b",
            "a\n",
            "a" * 64,
        ],
    )
    def test_invalid(self, name):
        assert not K8sLabelValue(name).is_valid


class TestK8sQualifiedName:
    @pytest.mark.parametrize(
        "name",
        [
            "name",
            "Name",
            "A.B_c-d",
            "a/b",
            "example.com/name",
            "a" * 63,
            "example.com/" + "a" * 63,
        ],
    )
    def test_valid(self, name):
        assert K8sQualifiedName(name).is_valid

    @pytest.mark.parametrize(
        "name",
        [
            "",
            "/name",
            "example.com/",
            "a/b/c",
            "Example.com/name",
            "-a/name",
            "example..com/name",
            "-name",
            "_name",
            "name-",
            "name\n",
            "example.com/name\n",
            "a" * 64,
        ],
    )
    def test_invalid(self, name):
        assert not K8sQualifiedName(name).is_valid
