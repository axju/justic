import unittest
import pathlib
import shutil

from justic import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        path = pathlib.Path(__file__).parent / 'test_project' / 'build'
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=False, onerror=None)

    def test_load_file(self):
        file = pathlib.Path(__file__).parent / 'test_project' / 'content' / 'index.py'
        utils.load_file(file)

    def test_load_dir(self):
        utils.load_dir('file')

    def test_analyze_current(self):
        utils.analyze_current('file')

    def test_get_targets(self):
        config, content, meta = utils.defaults('root', 'target')
        utils.get_targets(config, content, meta)

    def test_render(self):
        config, content, meta = utils.defaults(pathlib.Path(__file__).parent / 'test_project', 'justiconf.py')
        meta['template'] = 'index.html'
        meta['build'] = pathlib.Path(__file__).parent / 'test_project' / 'build' / 'foo.html'
        self.assertFalse(meta['build'].is_file())
        utils.render(config, content, meta)

    def test_copy_static(self):
        config, _, meta = utils.defaults('test_project', 'justiconf.py')
        utils.copy_static(config, meta)


if __name__ == '__main__':
    unittest.main()
