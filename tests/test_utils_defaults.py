import unittest
import pathlib

from justic import utils


class TestUtilsDefaults(unittest.TestCase):

    def defaults_basic(self, root, target):
        config, content, meta = utils.defaults(root, target)
        self.assertIsInstance(config, dict)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(meta, dict)
        for directory in config['dirs'].values():
            self.assertIsInstance(directory, pathlib.Path)

    def test_defaults(self):
        self.defaults_basic('root', 'target')
        self.defaults_basic(pathlib.Path('root'), pathlib.Path('target'))

    def test_defaults_meta_current_relative(self):
        target = 'target'
        _, _, meta = utils.defaults('root', target)
        self.assertNotEqual(str(meta['current']), target)
        self.assertIsInstance(meta['current'], pathlib.Path)

    def test_defaults_meta_current_absolute(self):
        target = '/target'
        _, _, meta = utils.defaults('root', target)
        self.assertEqual(str(meta['current']), target)
        self.assertIsInstance(meta['current'], pathlib.Path)


if __name__ == '__main__':
    unittest.main()
