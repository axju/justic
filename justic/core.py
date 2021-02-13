import logging
import pathlib

from justic import utils


class Justic:
    """docstring for Justic."""

    def __init__(self, config={}, content={}, **kwargs):
        self.logger = logging.getLogger('justic.Justic')

        root = config.get('dirs', {}).get('root') or kwargs.get('root', '.')
        target = config.get('target') or kwargs.get('target', 'justiconf.py')
        self.config, self.content, self.meta = utils.defaults(root, target)

        self.logger.debug('new root=%s, current=%s', self.config['dirs']['root'], self.meta['current'])
        self.update(config, content)

        target_config, target_content, meta = utils.analyze_current(self.meta['current'])
        self.update(target_config, target_content, meta)

    def update(self, justic, content, meta=None):
        self.config.update(justic)
        self.content.update(content)
        self.update_config()
        if isinstance(meta, dict):
            self.update_meta(meta)

    def update_dirs(self):
        for directory in self.config['dirs'].values():
            if not isinstance(directory, pathlib.Path):
                directory = pathlib.Path(directory)
            if not directory.is_absolute():
                directory = self.config['dirs']['root'] / directory

    def update_config(self):
        self.update_dirs()
        self.config['remove_build_prefix'] = self.config.get('remove_build_prefix', '.')

    def update_meta(self, meta):
        self.meta.update(meta)
        self.meta['render'] = self.meta.get('render', True) and self.meta['current'].is_file()
        self.meta['template'] = self.meta.get('template') or self.config.get('default_template')
        self.meta['build'] = self.meta.get('build')
        if isinstance(self.meta['build'], str):
            self.meta['build'] = self.config['dirs']['build'] / pathlib.Path(self.meta['build'])
        else:
            output = self.meta['current'].relative_to(self.config['dirs']['root'] / self.config['remove_build_prefix'])
            self.meta['build'] = self.config['dirs']['build'] / output
            self.meta['build'] = self.meta['build'].with_suffix('.html')

    def get_targets(self):
        for target, config, content in utils.get_targets(self.config, self.content, self.meta):
            yield Justic(config, content, target=target)

    def run(self):
        self.logger.debug('run meta=%s', self.meta)
        # self.logger.debug('run content=%s', self.content)
        # self.logger.debug('run config=%s', self.config)
        utils.render(self.config, self.content, self.meta)
        for target in self.get_targets():
            target.run()
        utils.copy_static(self.config, self.meta)
