# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

# python setup.py install before running tests
from chandler.handler import SizedAndTimedRotatingHandler


class TestSizedAndTimedRotatignHandler(unittest.TestCase):

    def test_rotation_on_time(self):
        self.assertEqual(6, 6)

    def test_rotation_on_size(self):
        self.assertEqual(6, 6)


if __name__ == '__main__':
    unittest.main()
