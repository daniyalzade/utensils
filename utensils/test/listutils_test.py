import unittest

from utensils.listutils import batch
from utensils.listutils import merge
from utensils.listutils import find
from utensils.listutils import push_to_front
from utensils.listutils import dedup
from utensils.listutils import shuffle_multi
from utensils.listutils import to_multilist

class TestListutils(unittest.TestCase):
    def test_batch(self):
        print [b for b in batch([1], 10)]

    def test_find(self):
        self.assertEquals(None, find(range(5), lambda i: i>4))
        self.assertEquals(4, find(range(5), lambda i: i>3))

    def test_push_to_front(self):
        self.assertEquals([0, 1, 2, 3, 4], push_to_front(range(5), lambda i: i>-1))
        self.assertEquals([0, 1, 2, 3, 4], push_to_front(range(5), lambda i: i>6))
        self.assertEquals([4, 0, 1, 2, 3], push_to_front(range(5), lambda i: i>3))
        self.assertEquals([3, 0, 1, 2, 4], push_to_front(range(5), lambda i: i>2))

    def test_merge(self):
        merged = merge(range(0, 10), range(100, 110), mix_percentage=0)
        merged = [m for m in merged[:10] if m <= 100]
        self.assertEquals(10, len(merged))
        merged = merge(range(0, 10), range(100, 110), mix_percentage=100)
        merged = [m for m in merged[:10] if m >= 100]
        self.assertEquals(10, len(merged))

    def test_dedup(self):
        self.assertEquals(2, len(dedup([
            {'foo': 'bar'},
            {'bar': 'bar'},
            {'foo': 'bar'},
            ], fn=lambda k: tuple(k.items()))))

    def test_shuffle_multi(self):
        v, k = shuffle_multi(range(10), range(10))
        self.assertEquals(v, k)
        self.assertTrue(v != range(10))

        try:
            v, k = shuffle_multi(range(5), range(5), range(10))
            self.assertTrue(False, 'we should never get here')
        except AssertionError:
            pass

        self.assertEquals(([], []), shuffle_multi([], []))

    def test_to_multilist(self):
        self.assertEquals(5, len(to_multilist(range(25), 5)))
        self.assertEquals(3, len(to_multilist(range(25), 5, 3)))
        self.assertEquals(14, to_multilist(range(25), 5, 3)[-1][-1])

if __name__ == "__main__":
    unittest.main()
