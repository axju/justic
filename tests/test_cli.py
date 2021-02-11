import unittest
import pathlib

from justic.__main__ import main


class TestMain(unittest.TestCase):

    def test_version(self):
        # main(['-V'])
        workdir = pathlib.Path(__file__).parent / 'test_project'
        main([str(workdir)])


if __name__ == '__main__':
    unittest.main()
