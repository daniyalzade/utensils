from datetime import datetime
import unittest

from utensils.dictutils import get_dotted
from utensils.dictutils import get_value_for_key


class TestDictutils(unittest.TestCase):
    def test_get_dotted(self):
        dict_ = {u'_id': {u'loc': {u'y': 2147, u'x': 14}, u't': datetime(2012, 4, 30, 14, 35)}}
        self.assertEquals(14, get_dotted(dict_, '_id.loc.x'))

    def test_get_dotted_array(self):
        dict_ = {
                '_id': {
                    'loc': {
                        'y': 2147, 'x': 14
                        },
                    't': datetime(2012, 4, 30, 14, 35),
                    'foo': [1, 2, {'bla':'la'}, 4, 5],
                    },
                }
        self.assertEquals(1, get_dotted(dict_, '_id.foo[0]'))
        self.assertEquals('la', get_dotted(dict_, '_id.foo[2].bla'))
        self.assertEquals(None, get_dotted(dict_, '_id.foo[3].bla'))

    def test_get_dotted_dict(self):
        dict_ = {
                'foo': [
                    {
                    'bar': 1,
                    'bla': 3,
                    },
                    {
                    'bar': 2,
                    'bla': 4,
                    },
                    {
                    'bar': 3,
                    'bla': 5,
                    },
                    ]
                }
        self.assertTrue(isinstance(get_dotted(dict_, 'foo[@bla=3]'), dict))
        self.assertEquals(1, get_dotted(dict_, 'foo[@bla=3].bar'))
        self.assertEquals(5, get_dotted(dict_, 'foo[@bar=3].bla'))

    def test_get_dotted_complex_dict(self):
        dict_ = {
                'foo': [
                    {
                    'bar': 1,
                    'bla': 3,
                    'foo': 3,
                    },
                    {
                    'bar': 2,
                    'bla': 4,
                    'foo': 3,
                    },
                    {
                    'bar': 3,
                    'bla': 5,
                    'foo': 3,
                    },
                    ]
                }
        self.assertEquals(2, get_dotted(dict_, 'foo[@bla=4@foo=3].bar'))

    def test_get_value_for_key(self):
        dict_ = {
                'foo': [
                    {
                    'bar': 1,
                    'bla': 3,
                    'gar': 3,
                    },
                    {
                    'bar': 2,
                    'bla': 4,
                    'foo': 3,
                    },
                    {
                    'bar': 3,
                    'bla': 5,
                    'foo': 3,
                    },
                    ]
                }
        self.assertEquals(3, get_value_for_key(dict_, 'gar'))

if __name__ == "__main__":
    unittest.main()
