import logging
import unittest

from utensils.loggingutils import basicConfig

class TestConfig(unittest.TestCase):
    def test_basic_config(self):
        basicConfig(console=True)
        self.assertEquals(2, len(logging.getLogger().handlers))

if __name__ == "__main__":
    unittest.main()
