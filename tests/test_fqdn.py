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
                FQDN(b'')

            with self.assertRaises(ValueError):
                FQDN(b'helloworld')

    def test_str(self):
        d = 'greatdomain.com'
        assert d == str(FQDN(d))
        d += '.'
        assert d == str(FQDN(d))

    def test_rfc_1035_s_2_3_4__label_max_length(self):
        self.__assert_valid('www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com')
        self.__assert_valid('abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk')

    def test_rfc_1035_s_2_3_4__label_too_long(self):
        self.__assert_invalid('A' * 64, 'com')
        self.__assert_invalid('b' * 63, 'A' * 64, 'com')

    def test_rfc_1035_s_2_3_4__name_too_long_254_octets(self):
        parts = [(chr(ord('A') + i % 26))
                 for i in range(int(254 / 2) - 1)]
        parts.append('co')
        fqdn = '.'.join(parts)
        assert len(fqdn) == 254
        self.__assert_invalid(fqdn)

    def test_rfc_1035_s_2_3_4__name_ok_253_octets(self):
        parts = [(chr(ord('A') + i % 26)) for i in range(int(254 / 2))]
        fqdn = '.'.join(parts)
        assert len(fqdn) == 253
        self.__assert_valid(fqdn)

    def test_rfc_1035_s_3_1__trailing_byte(self):
        parts = [(chr(ord('A') + i % 26)) for i in range(int(254 / 2))]
        fqdn = '.'.join(parts) + '.'
        assert len(fqdn) == 254
        self.__assert_valid(fqdn)

    def test_rfc_3696_s_2__label_invalid_starts_or_ends_with_hyphen(self):
        self.__assert_invalid('-a', 'com')
        self.__assert_invalid('a-', 'com')
        self.__assert_invalid('-a-', 'com')
        self.__assert_invalid('a', '-com')
        self.__assert_invalid('a', 'com-')

    def test_rfc_3696_s_2__preferred_form_invalid_chars(self):
        # these should use punycode instead
        self.__assert_invalid('є', 'com')
        self.__assert_invalid('le-tour-est-joué', 'com')
        self.__assert_invalid('invalid', 'cóm')
        self.__assert_invalid('ich-hätte-gern-ein-Umlaut', 'de')
        self.__assert_invalid('\x01', 'com')
        self.__assert_invalid('x', '\x01\x02\x01')

    def test_rfc_3696_s_2__valid(self):
        self.__assert_valid(
            'shopping',
            'on',
            'the'
            'net')
        self.__assert_valid('who', 'is')
        self.__assert_valid('bbc', 'co', 'uk')
        self.__assert_valid('example', 'io')

    def __assert_invalid(self, *seq):
        self.assertFalse(self.__is_valid_fqdn_from_labels_sequence(seq))

    def __assert_valid(self, *seq):
        self.assertTrue(self.__is_valid_fqdn_from_labels_sequence(seq))

    def __is_valid_fqdn_from_labels_sequence(self, fqdn_labels_sequence):
        fqdn = '.'.join(fqdn_labels_sequence)
        return FQDN(fqdn).is_valid


class TestAbsoluteFQDN(TestCase):

    def test_absolute_fqdn(self):
        self.assertTrue(FQDN('trainwreck.com.').is_valid_absolute)

    def test_absolute_fqdn__fail(self):
        self.assertFalse(FQDN('trainwreck.com').is_valid_absolute)

    def test_to_absolute_fqdn_from_relative(self):
        self.assertEqual(FQDN('trainwreck.com').absolute,
                         'trainwreck.com.')

    def test_to_absolute_fqdn_from_absolute(self):
        self.assertEqual(FQDN('absolutetrainwreck.com.').absolute,
                         'absolutetrainwreck.com.')

    def test_to_absolute_fqdn__raises_ValueError(self):
        with self.assertRaises(ValueError):
            FQDN('trainwreckcom').absolute

    def test_relative_fqdn_true(self):
        assert FQDN('relative.com').is_valid_relative is True

    def test_relative_fqdn_false(self):
        assert FQDN('relative.com.').is_valid_relative is False


class TestRelativeFQDN(TestCase):

    def test_relative_fqdn_from_relative(self):
        self.assertEqual(FQDN('trainwreck.com').relative, 'trainwreck.com')

    def test_relative_fqdn_from_absolute(self):
        self.assertEqual(FQDN('trainwreck.com.').relative, 'trainwreck.com')

    def test_relative_fqdn_from_invalid(self):
        with self.assertRaises(ValueError):
            FQDN('trainwreck..').relative
