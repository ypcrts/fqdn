# coding=utf-8
import sys

import pytest
from fqdn import FQDN


@pytest.fixture(params=(True, False))
def strict(request):
    return request.param


class TestFQDNValidation:
    def test_constructor(self, strict):
        with pytest.raises(ValueError):
            FQDN(None, strict=strict)

    # Python 3-specific tests
    if sys.version_info >= (3, 0):

        def test_constructor_raises_on_bytes(self, strict):
            with pytest.raises(ValueError):
                FQDN(b"", strict=strict)

            with pytest.raises(ValueError):
                FQDN(b"helloworld", strict=strict)

    def test_str(self, strict):
        d = "greatdomain.com"
        f = FQDN(d, strict=strict)
        assert f.absolute == str(f)

    def test_rfc_1035_s_2_3_4__label_max_length(self, strict):
        assert FQDN(
            "www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com",
            strict=strict,
        ).is_valid
        assert FQDN(
            "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk",
            strict=strict,
        ).is_valid

    def test_rfc_1035_s_2_3_4__label_too_long(self, strict):
        self.__assert_invalid_from_seq("A" * 64, "com", strict=strict)
        self.__assert_invalid_from_seq("b" * 63, "A" * 64, "com", strict=strict)
        self.__assert_invalid_from_seq("com", "b" * 63, "A" * 64, strict=strict)

    def test_rfc_1035_s_2_3_4__name_too_long_254_octets(self, strict):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2) - 1)]
        parts.append("co")
        fqdn = ".".join(parts)
        assert len(fqdn) == 254
        self.__assert_invalid_from_seq(fqdn, strict=strict)

    def test_rfc_1035_s_2_3_4__name_ok_253_octets(self, strict):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts)
        assert len(fqdn) == 253
        self.__assert_valid_from_seq(fqdn, strict=strict)

    def test_rfc_1035_s_3_1__trailing_byte(self, strict):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts) + "."
        assert len(fqdn) == 254
        self.__assert_valid_from_seq(fqdn, strict=strict)

    def test_rfc_3696_s_2__label_invalid_starts_or_ends_with_hyphen(self):
        self.__assert_invalid_fwd_and_bkwd_from_seq("-a", "com", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("a-", "com", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("-a-", "com", strict=strict)

    def test_rfc_3696_s_2__preferred_form_invalid_chars(self, strict):
        # these should use punycode instead
        self.__assert_invalid_fwd_and_bkwd_from_seq("є", "com", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq(
            "le-tour-est-joué", "com", strict=strict
        )
        self.__assert_invalid_fwd_and_bkwd_from_seq("invalid", "cóm", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq(
            "ich-hätte-gern-ein-Umlaut", "de", strict=strict
        )
        self.__assert_invalid_fwd_and_bkwd_from_seq("\x01", "com", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("x", "\x01\x02\x01", strict=strict)

    def test_underscores_extra_mode(self):
        self.__assert_valid_fwd_and_bkwd_from_seq("_", "dog", strict=False)
        self.__assert_valid_fwd_and_bkwd_from_seq("i_", "dog", strict=False)
        self.__assert_valid_fwd_and_bkwd_from_seq("o_o", "dog", strict=False)

        self.__assert_invalid_fwd_and_bkwd_from_seq("_", "dog", strict=True)
        self.__assert_invalid_fwd_and_bkwd_from_seq("i_", "dog", strict=True)
        self.__assert_invalid_fwd_and_bkwd_from_seq("o_o", "dog", strict=True)

    def test_rfc_3696_s_2__valid(self):
        assert FQDN("net", min_labels=1, strict=strict).is_valid
        assert FQDN("who.is", strict=strict).is_valid
        assert FQDN("bbc.co.uk", strict=strict).is_valid
        self.__assert_valid_fwd_and_bkwd_from_seq(
            "sh4d05-7357", "c00-mm", strict=strict
        )

    def test_rfc_1035_s_2_3_1__label_cannot_have_inital_digit(self, strict):
        self.__assert_invalid_fwd_and_bkwd_from_seq("www", "1", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("1w", "1", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("1w", "a", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("1w1", "d", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("111", "a", strict=strict)
        self.__assert_invalid_fwd_and_bkwd_from_seq("www", "1a", strict=strict)

    def test_rfc_1035_s_2_3_1__label_can_have_medial_and_terminal_digits(self, strict):
        self.__assert_valid_fwd_and_bkwd_from_seq("www1", "a", strict=strict)
        self.__assert_valid_fwd_and_bkwd_from_seq("ww1a", "c", strict=strict)

        self.__assert_valid_fwd_and_bkwd_from_seq("w2w", "c", strict=strict)
        self.__assert_valid_fwd_and_bkwd_from_seq("a111", "a", strict=strict)
        self.__assert_valid_fwd_and_bkwd_from_seq("a1c1", "a", strict=strict)

    def __assert_valid_fwd_and_bkwd_from_seq(self, *seq, **kwargs):
        rseq = reversed(seq)
        self.__assert_valid_from_seq(*rseq, **kwargs)

    def __assert_invalid_fwd_and_bkwd_from_seq(self, *seq, **kwargs):
        rseq = reversed(seq)
        self.__assert_invalid_from_seq(*rseq, **kwargs)

    def __assert_invalid_from_seq(self, *seq, **kwargs):
        assert not (self.__is_valid_fqdn_from_labels_seq(seq, **kwargs))

    def __assert_valid_from_seq(self, *seq, **kwargs):
        assert self.__is_valid_fqdn_from_labels_seq(seq, **kwargs)

    def __is_valid_fqdn_from_labels_seq(self, fqdn_labels_seq, **kwargs):
        fqdn = ".".join(fqdn_labels_seq)
        return FQDN(fqdn, **kwargs).is_valid


class TestMinLabels:
    def test_labels_count(self, strict):
        assert FQDN("label").labels_count == 1
        assert FQDN("label.").labels_count == 1
        assert FQDN("label.babel").labels_count == 2
        assert FQDN("label.babel.").labels_count == 2
        assert FQDN(".label.babel.").labels_count == 3

    def test_min_labels_defaults_to_require_2(self):
        dn = FQDN("label")
        assert dn._min_labels == 2
        assert dn.labels_count == 1
        assert not dn.is_valid

    def test_min_labels_valid_set_to_1(self):
        with pytest.raises(ValueError):
            FQDN("", min_labels=1).is_valid
        assert FQDN("label", min_labels=1).is_valid
        assert not FQDN(".label", min_labels=1).is_valid
        assert FQDN("label.babel", min_labels=1).is_valid
        assert FQDN("label.babel.", min_labels=1).is_valid
        assert not FQDN(".label.babel", min_labels=1).is_valid

    def test_min_labels_valid_set_to_3(self):
        assert not FQDN("label", min_labels=3).is_valid
        assert not FQDN("label.babel", min_labels=3).is_valid
        assert not FQDN(".babel", min_labels=3).is_valid
        assert not FQDN("babel.", min_labels=3).is_valid
        assert not FQDN(".babel.", min_labels=3).is_valid
        assert not FQDN("label.babel.", min_labels=3).is_valid
        assert not FQDN(".label.babel.", min_labels=3).is_valid
        assert FQDN("fable.label.babel.", min_labels=3).is_valid
        assert FQDN("fable.label.babel", min_labels=3).is_valid


class TestAbsoluteFQDN:
    def test_absolute_fqdn(self, strict):
        assert FQDN("trainwreck.com.", strict=strict).is_valid_absolute is True

    def test_absolute_fqdn__fail(self, strict):
        assert FQDN("trainwreck.com", strict=strict).is_valid_absolute is False

    def test_to_absolute_fqdn_from_relative(self, strict):
        assert FQDN("trainwreck.com", strict=strict).absolute == "trainwreck.com."

    def test_to_absolute_fqdn_from_absolute(self, strict):
        assert (
            FQDN("absolutetrainwreck.com.", strict=strict).absolute
            == "absolutetrainwreck.com."
        )

    def test_to_absolute_fqdn__raises_ValueError(self, strict):
        with pytest.raises(ValueError):
            FQDN("trainwreckcom", strict=strict).absolute

    def test_relative_fqdn_true(self, strict):
        assert FQDN("relative.com", strict=strict).is_valid_relative is True

    def test_relative_fqdn_false(self, strict):
        assert FQDN("relative.com.", strict=strict).is_valid_relative is False


class TestRelativeFQDN:
    def test_relative_fqdn_from_relative(self, strict):
        assert FQDN("trainwreck.com", strict=strict).relative == "trainwreck.com"

    def test_relative_fqdn_from_absolute(self, strict):
        assert FQDN("trainwreck.com.", strict=strict).relative == "trainwreck.com"

    def test_relative_fqdn_from_invalid(self, strict):
        with pytest.raises(ValueError):
            FQDN("trainwreck..", strict=strict).relative


class TestEquality:
    def test_absolutes_are_equal(self, strict):
        assert FQDN("trainwreck.com.", strict=strict) == FQDN(
            "trainwreck.com.", strict=strict
        )

    def test_relatives_are_equal(self, strict):
        assert FQDN("trainwreck.com", strict=strict) == FQDN(
            "trainwreck.com", strict=strict
        )

    def test_mismatch_are_equal(self, strict):
        assert FQDN("trainwreck.com.", strict=strict) == FQDN(
            "trainwreck.com", strict=strict
        )

    def test_equality_is_case_insensitive(self, strict):
        assert FQDN("all-letters-were-created-equal.com.", strict=strict) == FQDN(
            "ALL-LETTERS-WERE-CREATED-EQUAL.COM.", strict=strict
        )

    def test_strict_and_loose_can_be_equal(self):
        assert FQDN("trainwreck.com.", strict=True) == FQDN(
            "trainwreck.com", strict=False
        )


class TestHash:
    def test_is_hashable(self, strict):
        assert hash(FQDN("trainwreck.com."))

    def test_absolutes_are_equal(self, strict):
        assert hash(FQDN("trainwreck.com.", strict=strict)) == hash(
            FQDN("trainwreck.com.", strict=strict)
        )

    def test_relatives_are_equal(self, strict):
        assert hash(FQDN("trainwreck.com", strict=strict)) == hash(
            FQDN("trainwreck.com", strict=strict)
        )

    def test_mismatch_are_equal(self, strict):
        assert hash(FQDN("trainwreck.com.", strict=strict)) == hash(
            FQDN("trainwreck.com", strict=strict)
        )

    def test_equality_is_case_insensitive(self, strict):
        assert hash(FQDN("all-letters-were-created-equal.com.", strict=strict)) == hash(
            FQDN("ALL-LETTERS-WERE-CREATED-EQUAL.COM.", strict=strict)
        )

    def test_not_equal_to_string(self, strict):
        assert hash(FQDN("trainwreck.com.", strict=strict)) != hash("trainwreck.com.")

    def test_different_fqdns_are_not_equal(self, strict):
        assert hash(FQDN("trainwreck.com.")) != hash(FQDN("test.com."))

    def test_strict_and_loose_hashs_are_equal(self):
        assert hash(FQDN("trainwreck.com.", strict=True)) == hash(
            FQDN("trainwreck.com", strict=False)
        )
