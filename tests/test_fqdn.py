# coding=utf-8
import sys
from unittest import TestCase

import pytest
from fqdn import FQDN


def build_fqdn(domain, strict=True):
    return FQDN(domain, strict=strict)


@pytest.fixture(params=(True, False))
def strict(request):
    return request.param


class TestFQDNValidation:
    def test_constructor(self, strict):
        with pytest.raises(ValueError):
            build_fqdn(None, strict)

    # Python 3-specific tests
    if sys.version_info >= (3, 0):

        def test_constructor_raises_on_bytes(self, strict):
            with pytest.raises(ValueError):
                build_fqdn(b"", strict)

            with pytest.raises(ValueError):
                build_fqdn(b"helloworld", strict)

    def test_str(self, strict):
        d = "greatdomain.com"
        f = build_fqdn(d, strict)
        assert f.absolute == str(f)

    def test_rfc_1035_s_2_3_4__label_max_length(self, strict):
        self.__assert_valid(
            "www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com",
            strict=strict,
        )
        self.__assert_valid(
            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk",
            strict=strict,
        )

    def test_rfc_1035_s_2_3_4__label_too_long(self, strict):
        self.__assert_invalid("A" * 64, "com", strict=strict)
        self.__assert_invalid("b" * 63, "A" * 64, "com", strict=strict)
        self.__assert_invalid("com", "b" * 63, "A" * 64, strict=strict)

    def test_rfc_1035_s_2_3_4__name_too_long_254_octets(self, strict):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2) - 1)]
        parts.append("co")
        fqdn = ".".join(parts)
        assert len(fqdn) == 254
        self.__assert_invalid(fqdn, strict=strict)

    def test_rfc_1035_s_2_3_4__name_ok_253_octets(self, strict):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts)
        assert len(fqdn) == 253
        self.__assert_valid(fqdn, strict=strict)

    def test_rfc_1035_s_3_1__trailing_byte(self, strict):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts) + "."
        assert len(fqdn) == 254
        self.__assert_valid(fqdn, strict=strict)

    def test_rfc_3696_s_2__label_invalid_starts_or_ends_with_hyphen(self, strict):
        self.__assert_invalid("-a", "com", strict=strict)
        self.__assert_invalid("a-", "com", strict=strict)
        self.__assert_invalid("-a-", "com", strict=strict)
        self.__assert_invalid("a", "-com", strict=strict)
        self.__assert_invalid("a", "com-", strict=strict)

    def test_rfc_3696_s_2__preferred_form_invalid_chars(self, strict):
        # these should use punycode instead
        self.__assert_invalid("є", "com", strict=strict)
        self.__assert_invalid("le-tour-est-joué", "com", strict=strict)
        self.__assert_invalid("invalid", "cóm", strict=strict)
        self.__assert_invalid("ich-hätte-gern-ein-Umlaut", "de", strict=strict)
        self.__assert_invalid("\x01", "com", strict=strict)
        self.__assert_invalid("x", "\x01\x02\x01", strict=strict)

    def test_rfc_3696_s_2__valid(self, strict):
        self.__assert_valid("shopping", "on", "the" "net", strict=strict)
        self.__assert_valid("who", "is", strict=strict)
        self.__assert_valid("bbc", "co", "uk", strict=strict)
        self.__assert_valid("example", "io", strict=strict)
        self.__assert_valid("sh4d05-7357", "c00-mm", strict=strict)

    def test_rfc_3696_s_2__tld_must_not_be_all_numeric(self, strict):
        self.__assert_invalid("www.1", strict=strict)
        self.__assert_invalid("1.1", strict=strict)

        self.__assert_invalid("111", strict=strict)
        self.__assert_invalid("www.111", strict=strict)

        self.__assert_valid("1.a1", strict=strict)

        self.__assert_valid("1.1a", strict=strict)
        self.__assert_valid("www.1a", strict=strict)

    def test_rfc_strictness_compliance(self):
        self.__assert_valid("test_test.test.com", strict=False)
        self.__assert_invalid("test_test.test.com", strict=True)
        self.__assert_invalid("test.test_test.com", strict=True)
        self.__assert_invalid("test.test_test.com", strict=False)

    def __assert_invalid(self, *seq, strict):
        assert self.__is_valid_fqdn_from_labels_sequence(seq, strict=strict) is False

    def __assert_valid(self, *seq, strict):
        assert self.__is_valid_fqdn_from_labels_sequence(seq, strict=strict) is True

    def __is_valid_fqdn_from_labels_sequence(self, fqdn_labels_sequence, strict):
        fqdn = ".".join(fqdn_labels_sequence)
        return FQDN(fqdn, strict=strict).is_valid


class TestAbsoluteFQDN:
    def test_absolute_fqdn(self, strict):
        assert build_fqdn("trainwreck.com.", strict).is_valid_absolute is True

    def test_absolute_fqdn__fail(self, strict):
        assert build_fqdn("trainwreck.com", strict).is_valid_absolute is False

    def test_to_absolute_fqdn_from_relative(self, strict):
        assert build_fqdn("trainwreck.com", strict).absolute == "trainwreck.com."

    def test_to_absolute_fqdn_from_absolute(self, strict):
        assert (
            build_fqdn("absolutetrainwreck.com.", strict).absolute
            == "absolutetrainwreck.com."
        )

    def test_to_absolute_fqdn__raises_ValueError(self, strict):
        with pytest.raises(ValueError):
            build_fqdn("trainwreckcom", strict).absolute

    def test_relative_fqdn_true(self, strict):
        assert build_fqdn("relative.com", strict).is_valid_relative is True

    def test_relative_fqdn_false(self, strict):
        assert build_fqdn("relative.com.", strict).is_valid_relative is False


class TestRelativeFQDN:
    def test_relative_fqdn_from_relative(self, strict):
        assert build_fqdn("trainwreck.com", strict).relative == "trainwreck.com"

    def test_relative_fqdn_from_absolute(self, strict):
        assert build_fqdn("trainwreck.com.", strict).relative == "trainwreck.com"

    def test_relative_fqdn_from_invalid(self, strict):
        with pytest.raises(ValueError):
            build_fqdn("trainwreck..", strict).relative


class TestEquality:
    def test_absolutes_are_equal(self, strict):
        assert build_fqdn("trainwreck.com.", strict) == build_fqdn(
            "trainwreck.com.", strict
        )

    def test_relatives_are_equal(self, strict):
        assert build_fqdn("trainwreck.com", strict) == build_fqdn(
            "trainwreck.com", strict
        )

    def test_mismatch_are_equal(self, strict):
        assert build_fqdn("trainwreck.com.", strict) == build_fqdn(
            "trainwreck.com", strict
        )

    def test_equality_is_case_insensitive(self, strict):
        assert build_fqdn("all-letters-were-created-equal.com.", strict) == build_fqdn(
            "ALL-LETTERS-WERE-CREATED-EQUAL.COM.", strict
        )

    def test_strict_and_loose_can_be_equal(self):
        assert FQDN("trainwreck.com.", strict=True) == FQDN("trainwreck.com", strict=False)


class TestHash:
    def test_is_hashable(self, strict):
        assert hash(build_fqdn("trainwreck.com."))

    def test_absolutes_are_equal(self, strict):
        assert hash(build_fqdn("trainwreck.com.", strict)) == hash(
            FQDN("trainwreck.com.", strict=strict)
        )

    def test_relatives_are_equal(self, strict):
        assert hash(build_fqdn("trainwreck.com", strict)) == hash(
            FQDN("trainwreck.com", strict=strict)
        )

    def test_mismatch_are_equal(self, strict):
        assert hash(build_fqdn("trainwreck.com.", strict)) == hash(
            FQDN("trainwreck.com", strict=strict)
        )

    def test_equality_is_case_insensitive(self, strict):
        assert hash(build_fqdn("all-letters-were-created-equal.com.", strict)) == hash(
            build_fqdn("ALL-LETTERS-WERE-CREATED-EQUAL.COM.", strict)
        )

    def test_not_equal_to_string(self, strict):
        assert hash(build_fqdn("trainwreck.com.", strict)) != hash("trainwreck.com.")

    def test_different_fqdns_are_not_equal(self, strict):
        assert hash(build_fqdn("trainwreck.com.")) != hash(FQDN("test.com."))

    def test_strict_and_loose_hashs_are_equal(self):
        assert hash(FQDN("trainwreck.com.", strict=True)) == hash(
            FQDN("trainwreck.com", strict=False)
        )
