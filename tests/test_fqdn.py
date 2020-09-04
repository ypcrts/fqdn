# coding=utf-8
import sys

import pytest

from fqdn import FQDN
from unittest import TestCase

def build_fqdn(domain, strict = True):
    return FQDN(domain, strict)

@pytest.fixture(params=(True, False))
def strict(request):
    return request.param

class TestFQDNValidation:
    def test_constructor(self, strict):
        with self.assertRaises(ValueError):
            build_fqdn(None, strict)

    # Python 3-specific tests
    if sys.version_info >= (3, 0):

        def test_constructor_raises_on_bytes(self, strict):
            with self.assertRaises(ValueError):
                build_fqdn(b"", strict)

            with self.assertRaises(ValueError):
                build_fqdn(b"helloworld", strict)

    def test_str(self):
        d = "greatdomain.com"
        f = build_fqdn(d, strict)
        assert f.absolute == str(f)

    def test_rfc_1035_s_2_3_4__label_max_length(self):
        self.__assert_valid(
            "www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com"
        )
        self.__assert_valid(
            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk"
        )

    def test_rfc_1035_s_2_3_4__label_too_long(self):
        self.__assert_invalid("A" * 64, "com")
        self.__assert_invalid("b" * 63, "A" * 64, "com")
        self.__assert_invalid("com", "b" * 63, "A" * 64)

    def test_rfc_1035_s_2_3_4__name_too_long_254_octets(self):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2) - 1)]
        parts.append("co")
        fqdn = ".".join(parts)
        assert len(fqdn) == 254
        self.__assert_invalid(fqdn)

    def test_rfc_1035_s_2_3_4__name_ok_253_octets(self):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts)
        assert len(fqdn) == 253
        self.__assert_valid(fqdn)

    def test_rfc_1035_s_3_1__trailing_byte(self):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts) + "."
        assert len(fqdn) == 254
        self.__assert_valid(fqdn)

    def test_rfc_3696_s_2__label_invalid_starts_or_ends_with_hyphen(self):
        self.__assert_invalid("-a", "com")
        self.__assert_invalid("a-", "com")
        self.__assert_invalid("-a-", "com")
        self.__assert_invalid("a", "-com")
        self.__assert_invalid("a", "com-")

    def test_rfc_3696_s_2__preferred_form_invalid_chars(self):
        # these should use punycode instead
        self.__assert_invalid("є", "com")
        self.__assert_invalid("le-tour-est-joué", "com")
        self.__assert_invalid("invalid", "cóm")
        self.__assert_invalid("ich-hätte-gern-ein-Umlaut", "de")
        self.__assert_invalid("\x01", "com")
        self.__assert_invalid("x", "\x01\x02\x01")

    def test_rfc_3696_s_2__valid(self):
        self.__assert_valid("shopping", "on", "the" "net")
        self.__assert_valid("who", "is")
        self.__assert_valid("bbc", "co", "uk")
        self.__assert_valid("example", "io")
        self.__assert_valid("sh4d05-7357", "c00-mm")

    def test_rfc_3696_s_2__tld_must_not_be_all_numeric(self):
        self.__assert_invalid("www.1")
        self.__assert_invalid("1.1")

        self.__assert_invalid("111")
        self.__assert_invalid("www.111")

        self.__assert_valid("1.a1")

        self.__assert_valid("1.1a")
        self.__assert_valid("www.1a")

    def __assert_invalid(self, *seq):
        self.assertFalse(self.__is_valid_fqdn_from_labels_sequence(seq))

    def __assert_valid(self, *seq):
        self.assertTrue(self.__is_valid_fqdn_from_labels_sequence(seq))

    def __is_valid_fqdn_from_labels_sequence(self, fqdn_labels_sequence):
        fqdn = ".".join(fqdn_labels_sequence)
        return build_fqdn(fqdn, strict).is_valid


class TestAbsoluteFQDN(TestCase):
    def test_absolute_fqdn(self):
        self.assertTrue(build_fqdn("trainwreck.com.").is_valid_absolute, strict)

    def test_absolute_fqdn__fail(self):
        self.assertFalse(build_fqdn("trainwreck.com").is_valid_absolute, strict)

    def test_to_absolute_fqdn_from_relative(self):
        self.assertEqual(build_fqdn("trainwreck.com").absolute, "trainwreck.com.", strict)

    def test_to_absolute_fqdn_from_absolute(self):
        self.assertEqual(
            build_fqdn("absolutetrainwreck.com.", strict).absolute, "absolutetrainwreck.com."
        )

    def test_to_absolute_fqdn__raises_ValueError(self):
        with self.assertRaises(ValueError):
            build_fqdn("trainwreckcom", strict).absolute

    def test_relative_fqdn_true(self):
        assert build_fqdn("relative.com", strict).is_valid_relative is True

    def test_relative_fqdn_false(self):
        assert build_fqdn("relative.com.", strict).is_valid_relative is False


class TestRelativeFQDN(TestCase):
    def test_relative_fqdn_from_relative(self):
        self.assertEqual(build_fqdn("trainwreck.com").relative, "trainwreck.com", strict)

    def test_relative_fqdn_from_absolute(self):
        self.assertEqual(build_fqdn("trainwreck.com.").relative, "trainwreck.com", strict)

    def test_relative_fqdn_from_invalid(self):
        with self.assertRaises(ValueError):
            build_fqdn("trainwreck..", strict).relative


class TestEquality(TestCase):
    def test_absolutes_are_equal(self):
        self.assertEqual(build_fqdn("trainwreck.com."), FQDN("trainwreck.com."), strict)

    def test_relatives_are_equal(self):
        self.assertEqual(build_fqdn("trainwreck.com"), FQDN("trainwreck.com"), strict)

    def test_mismatch_are_equal(self):
        self.assertEqual(build_fqdn("trainwreck.com."), FQDN("trainwreck.com"), strict)

    def test_equality_is_case_insensitive(self):
        self.assertEqual(
            build_fqdn("all-letters-were-created-equal.com.", strict),
            build_fqdn("ALL-LETTERS-WERE-CREATED-EQUAL.COM.", strict),
        )


class TestHash(TestCase):
    def test_is_hashable(self):
        self.assertTrue(hash(build_fqdn("trainwreck.com.")), strict)

    def test_absolutes_are_equal(self):
        self.assertEqual(hash(build_fqdn("trainwreck.com.")), hash(FQDN("trainwreck.com.")), strict)

    def test_relatives_are_equal(self):
        self.assertEqual(hash(build_fqdn("trainwreck.com")), hash(FQDN("trainwreck.com")), strict)

    def test_mismatch_are_equal(self):
        self.assertEqual(hash(build_fqdn("trainwreck.com.")), hash(FQDN("trainwreck.com")), strict)

    def test_equality_is_case_insensitive(self):
        self.assertEqual(
            hash(build_fqdn("all-letters-were-created-equal.com."), strict),
            hash(build_fqdn("ALL-LETTERS-WERE-CREATED-EQUAL.COM."), strict),
        )

    def test_not_equal_to_string(self):
        self.assertNotEqual(hash(build_fqdn("trainwreck.com.")), hash("trainwreck.com."), strict)

    def test_different_fqdns_are_not_equal(self):
        self.assertNotEqual(hash(build_fqdn("trainwreck.com.")), hash(FQDN("test.com.")), strict)
