import logging
import unittest

from utensils.enum import Enum
from utensils.options import define
from utensils.options import Error
from utensils.options import options
from utensils.options import parse_command_line

TestTypes = Enum([
    'type1',
    'type2',
    ])

class OptionsTest(unittest.TestCase):
    def _clear_options(self):
        return dict([(k, v) for (k, v) in options.items() if k != 'help'])

    def setUp(self):
        self._clear_options()
        # these are currently required
        define("logging", default="none")
        define("port", default=80, type=int)

    def test_required(self):
        define("required_field", type=int, required=True)

        # Test required field passed
        parse_command_line(["main.py", "--required_field=10"])
        self.assertTrue(True, 'required field passed')

        # Test parse required not passed
        try:
            # We have to clear options here again :( since, each time we
            # parse_command_line options sets global state
            self._clear_options()
            define("required_field", type=int, required=True)
            define("port", default=80, type=int)

            parse_command_line(["main.py", '--port=80'])
            self.assertFalse(True, 'fail if we got here')
        except Error:
            logging.exception('exception')
            self.assertTrue(True, 'raised exception')

if __name__ == "__main__":
    unittest.main()
