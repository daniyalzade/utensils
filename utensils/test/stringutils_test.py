# This Python file uses the following encoding: utf-8
import unittest

from utensils.stringutils import to_latin, to_upper_first_chars
from utensils.stringutils import unformat_phone_number, parse_price

class TestStringutils(unittest.TestCase):
    def test_to_upper_first_chars(self):
        text = u'guzellik & ask'
        self.assertEquals('Guzellik & Ask', to_upper_first_chars(text))

    def test_to_latin(self):
        text = u'güzellik'
        self.assertEqual('guzellik', to_latin(text))
        text = u'ruzgâr'
        self.assertEquals('ruzgar', to_latin(text))

    def test_unformat_phone(self):
        self.assertEquals('2788733380', unformat_phone_number('278.873.3380'))
        self.assertEquals('5168737380', unformat_phone_number('516-873-7380'))
        self.assertEquals('2124312686', unformat_phone_number('(212) 431-2686'))
        self.assertEquals('2124312686', unformat_phone_number('212431-2686'))
        self.assertEquals('2788733380', unformat_phone_number('please call 278 873 3380'))
        self.assertEquals('5168737380', unformat_phone_number('5168737380'))

    def test_parse_price(self):
        self.assertEquals(8.0, parse_price('3 for 24.00'))
        self.assertEquals(308.0, parse_price('$308.00 - $440.00', min))
        self.assertEquals(440.0, parse_price('$308.00 - $440.00'))

if __name__ == "__main__":
    unittest.main()
