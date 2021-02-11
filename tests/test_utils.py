import unittest
import pathlib

from justic.utils import Directories


class TestDirectories(unittest.TestCase):

    def test_items(self):
        directories = Directories()
        self.assertIn('work', directories)
        self.assertIn('build', directories)
        self.assertIn('content', directories)
        self.assertIn('templates', directories)
        self.assertIn('static', directories)

    def test_pathlib(self):
        directories = Directories()
        for item in directories.values():
            self.assertIsInstance(item, pathlib.Path)


if __name__ == '__main__':
    unittest.main()
