# This Python file uses the following encoding: utf-8
import unittest

from utensils.stringutils import to_latin, to_upper_first_chars
from utensils.stringutils import parse_price

class TestStringutils(unittest.TestCase):
    def test_to_upper_first_chars(self):
        text = u'guzellik & ask'
        self.assertEquals('Guzellik & Ask', to_upper_first_chars(text))

    def test_to_latin(self):
        text = u'güzellik'
        self.assertEqual('guzellik', to_latin(text))
        text = u'ruzgâr'
        self.assertEquals('ruzgar', to_latin(text))

    def test_parse_price(self):
        self.assertEquals(8.0, parse_price('3 for 24.00'))
        self.assertEquals(308.0, parse_price('$308.00 - $440.00', min))
        self.assertEquals(440.0, parse_price('$308.00 - $440.00'))

if __name__ == "__main__":
    unittest.main()
