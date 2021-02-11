import unittest

from justic.__main__ import main


class TestMain(unittest.TestCase):

    def test_version(self):
        # main(['-V'])
        main()


if __name__ == '__main__':
    unittest.main()
