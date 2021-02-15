import logging

from justic import utils


class Justic:
    """docstring for Justic."""

    def __init__(self, config={}, content={}, **kwargs):
        self.logger = logging.getLogger('justic.Justic')

        # first we get the default values
        root = config.get('dirs', {}).get('root') or kwargs.get('root', '.')
        target = config.get('target') or kwargs.get('target', 'justiconf.py')
        self.config, self.content, self.meta = utils.defaults(root, target, config)

        # then update with the arguments (from the perant item)
        self.logger.debug('new root=%s, current=%s', self.config['dirs']['root'], self.meta['current'])
        self.update(config, content)

        # now analyze the current target and update
        target_config, target_content, meta = self.config['funcs']['analyze_current'](self.meta['current'])
        self.update(target_config, target_content, meta)

    def update(self, config=None, content=None, meta=None):
        self.content.update(content)
        self.config.update(config)
        self.config = utils.update_config(self.config, meta)
        if meta is not None:
            self.meta.update(meta)
            self.meta = utils.update_meta(self.config, self.meta)

    def get_targets(self):
        for target, config, content in utils.get_targets(self.config, self.content, self.meta):
            yield Justic(config, content, target=target)

    def run(self):
        self.logger.debug('run target=%s', self.meta['current'])
        self.logger.debug('run meta=%s', self.meta)
        self.logger.debug('run config=%s', self.config)
        utils.render(self.config, self.content, self.meta)
        for target in self.get_targets():
            target.run()
        utils.copy_static(self.config, self.meta)
