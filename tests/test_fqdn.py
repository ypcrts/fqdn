# coding=utf-8
import sys
from fqdn import FQDN
from unittest import TestCase


class TestFQDNValidation(TestCase):
    def test_constructor(self):
        with self.assertRaises(ValueError):
            FQDN(None)

    # Python 3-specific tests
    if sys.version_info >= (3, 0):

        def test_constructor_raises_on_bytes(self):
            with self.assertRaises(ValueError):
                FQDN(b"")

            with self.assertRaises(ValueError):
                FQDN(b"helloworld")

    def test_str(self):
        d = "greatdomain.com"
        f = FQDN(d)
        assert f.absolute == str(f)

    def test_rfc_1035_s_2_3_4__label_max_length(self):
        self.assertTrue(
            FQDN(
                "www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com"
            ).is_valid
        )
        self.assertTrue(
            FQDN(
                "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk"
            ).is_valid
        )

    def test_rfc_1035_s_2_3_4__label_too_long(self):
        self.__assert_invalid_from_seq("A" * 64, "com")
        self.__assert_invalid_from_seq("b" * 63, "A" * 64, "com")
        self.__assert_invalid_from_seq("com", "b" * 63, "A" * 64)

    def test_rfc_1035_s_2_3_4__name_too_long_254_octets(self):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2) - 1)]
        parts.append("co")
        fqdn = ".".join(parts)
        assert len(fqdn) == 254
        self.__assert_invalid_from_seq(fqdn)

    def test_rfc_1035_s_2_3_4__name_ok_253_octets(self):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts)
        assert len(fqdn) == 253
        self.__assert_valid_from_seq(fqdn)

    def test_rfc_1035_s_3_1__trailing_byte(self):
        parts = [(chr(ord("A") + i % 26)) for i in range(int(254 / 2))]
        fqdn = ".".join(parts) + "."
        assert len(fqdn) == 254
        self.__assert_valid_from_seq(fqdn)

    def test_rfc_3696_s_2__label_invalid_starts_or_ends_with_hyphen(self):
        self.__assert_invalid_fwd_and_bkwd_from_seq("-a", "com")
        self.__assert_invalid_fwd_and_bkwd_from_seq("a-", "com")
        self.__assert_invalid_fwd_and_bkwd_from_seq("-a-", "com")

    def test_rfc_3696_s_2__preferred_form_invalid_chars(self):
        # these should use punycode instead
        self.__assert_invalid_fwd_and_bkwd_from_seq("є", "com")
        self.__assert_invalid_fwd_and_bkwd_from_seq("le-tour-est-joué", "com")
        self.__assert_invalid_fwd_and_bkwd_from_seq("invalid", "cóm")
        self.__assert_invalid_fwd_and_bkwd_from_seq("ich-hätte-gern-ein-Umlaut", "de")
        self.__assert_invalid_fwd_and_bkwd_from_seq("\x01", "com")
        self.__assert_invalid_fwd_and_bkwd_from_seq("x", "\x01\x02\x01")

    def test_rfc_3696_s_2__valid(self):
        self.assertTrue(FQDN("net", min_labels=1).is_valid)
        self.assertTrue(FQDN("who.is").is_valid)
        self.assertTrue(FQDN("bbc.co.uk").is_valid)
        self.__assert_valid_fwd_and_bkwd_from_seq("sh4d05-7357", "c00-mm")

    def test_rfc_1035_s_2_3_1__label_cannot_have_inital_digit(self):
        self.__assert_invalid_fwd_and_bkwd_from_seq("www", "1")
        self.__assert_invalid_fwd_and_bkwd_from_seq("1w", "1")
        self.__assert_invalid_fwd_and_bkwd_from_seq("1w", "a")
        self.__assert_invalid_fwd_and_bkwd_from_seq("1w1", "d")
        self.__assert_invalid_fwd_and_bkwd_from_seq("111", "a")
        self.__assert_invalid_fwd_and_bkwd_from_seq("www", "1a")

    def test_rfc_1035_s_2_3_1__label_can_have_medial_and_terminal_digits(self):
        self.__assert_valid_fwd_and_bkwd_from_seq("www1", "a")
        self.__assert_valid_fwd_and_bkwd_from_seq("ww1a", "c")

        self.assertTrue(FQDN("w1w", min_labels=1).is_valid)
        self.assertTrue(FQDN("a11", min_labels=1).is_valid)
        self.assertTrue(FQDN("a1", min_labels=1).is_valid)

        self.__assert_valid_fwd_and_bkwd_from_seq("w2w", "c")
        self.__assert_valid_fwd_and_bkwd_from_seq("a111", "a")
        self.__assert_valid_fwd_and_bkwd_from_seq("a1c1", "a")

    def __assert_valid_fwd_and_bkwd_from_seq(self, *seq):
        rseq = reversed(seq)
        self.__assert_valid_from_seq(*rseq)

    def __assert_invalid_fwd_and_bkwd_from_seq(self, *seq):
        rseq = reversed(seq)
        self.__assert_invalid_from_seq(*rseq)

    def __assert_invalid_from_seq(self, *seq):
        self.assertFalse(self.__is_valid_fqdn_from_labels_seq(seq))

    def __assert_valid_from_seq(self, *seq):
        self.assertTrue(self.__is_valid_fqdn_from_labels_seq(seq))

    def __is_valid_fqdn_from_labels_seq(self, fqdn_labels_seq):
        fqdn = ".".join(fqdn_labels_seq)
        return FQDN(fqdn).is_valid


class TestMinLabels(TestCase):
    def test_labels_count(self):
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
        with self.assertRaises(ValueError):
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


class TestAbsoluteFQDN(TestCase):
    def test_absolute_fqdn(self):
        self.assertTrue(FQDN("trainwreck.com.").is_valid_absolute)

    def test_absolute_fqdn__fail(self):
        self.assertFalse(FQDN("trainwreck.com").is_valid_absolute)

    def test_to_absolute_fqdn_from_relative(self):
        self.assertEqual(FQDN("trainwreck.com").absolute, "trainwreck.com.")

    def test_to_absolute_fqdn_from_absolute(self):
        self.assertEqual(
            FQDN("absolutetrainwreck.com.").absolute, "absolutetrainwreck.com."
        )

    def test_to_absolute_fqdn__raises_ValueError(self):
        with self.assertRaises(ValueError):
            FQDN("trainwreckcom").absolute

    def test_relative_fqdn_true(self):
        assert FQDN("relative.com").is_valid_relative is True

    def test_relative_fqdn_false(self):
        assert FQDN("relative.com.").is_valid_relative is False


class TestRelativeFQDN(TestCase):
    def test_relative_fqdn_from_relative(self):
        self.assertEqual(FQDN("trainwreck.com").relative, "trainwreck.com")

    def test_relative_fqdn_from_absolute(self):
        self.assertEqual(FQDN("trainwreck.com.").relative, "trainwreck.com")

    def test_relative_fqdn_from_invalid(self):
        with self.assertRaises(ValueError):
            FQDN("trainwreck..").relative


class TestEquality(TestCase):
    def test_absolutes_are_equal(self):
        self.assertEqual(FQDN("trainwreck.com."), FQDN("trainwreck.com."))

    def test_relatives_are_equal(self):
        self.assertEqual(FQDN("trainwreck.com"), FQDN("trainwreck.com"))

    def test_mismatch_are_equal(self):
        self.assertEqual(FQDN("trainwreck.com."), FQDN("trainwreck.com"))

    def test_equality_is_case_insensitive(self):
        self.assertEqual(
            FQDN("all-letters-were-created-equal.com."),
            FQDN("ALL-LETTERS-WERE-CREATED-EQUAL.COM."),
        )


class TestHash(TestCase):
    def test_is_hashable(self):
        self.assertTrue(hash(FQDN("trainwreck.com.")))

    def test_absolutes_are_equal(self):
        self.assertEqual(hash(FQDN("trainwreck.com.")), hash(FQDN("trainwreck.com.")))

    def test_relatives_are_equal(self):
        self.assertEqual(hash(FQDN("trainwreck.com")), hash(FQDN("trainwreck.com")))

    def test_mismatch_are_equal(self):
        self.assertEqual(hash(FQDN("trainwreck.com.")), hash(FQDN("trainwreck.com")))

    def test_equality_is_case_insensitive(self):
        self.assertEqual(
            hash(FQDN("all-letters-were-created-equal.com.")),
            hash(FQDN("ALL-LETTERS-WERE-CREATED-EQUAL.COM.")),
        )

    def test_not_equal_to_string(self):
        self.assertNotEqual(hash(FQDN("trainwreck.com.")), hash("trainwreck.com."))

    def test_different_fqdns_are_not_equal(self):
        self.assertNotEqual(hash(FQDN("trainwreck.com.")), hash(FQDN("test.com.")))
