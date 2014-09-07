__author__ = 'Antony Cherepanov'

import unittest


class FakeTest(unittest.TestCase):
    def setUp(self):
        print("!-- In setUp()")

    def test_fake(self):
        print("!-- In test_fake()")


if __name__ == "__main__":
    unittest.main()
