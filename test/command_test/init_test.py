import sys
import unittest
import scape.command.init


class InitTest(unittest.TestCase):
    def test(self):
        scape.command.init.init(['test'])


if __name__ == '__main__':
    unittest.main()
