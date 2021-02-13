import logging
import pathlib
import shutil
import importlib.util

import jinja2


def defaults(root):
    dirs = {
        'build': root / 'build',
        'templates': root / 'templates',
    }
    config = {'dirs': dirs}
    content = {}
    return config, content, {}


class Justic:
    """docstring for Justic."""

    def __init__(self, root='.', target='justiconf.py', config={}, content={}):
        self.logger = logging.getLogger('justic.Justic')

        self.root = pathlib.Path(root).absolute()
        self.target = pathlib.Path(target)
        if not self.target.is_absolute():
            self.target = self.root / self.target

        self.logger.debug('new root=%s, target=%s', self.root, self.target)
        self.config, self.content, self.meta = defaults(self.root)
        self.update(config, content)
        self.analyze_target()

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
                directory = self.root / directory

    def update_config(self):
        self.update_dirs()
        self.config['remove_build_prefix'] = self.config.get('remove_build_prefix', '.')

    def update_meta(self, meta):
        self.meta = meta
        self.meta['render'] = self.meta.get('render', True) and self.target.is_file()
        self.meta['template'] = self.meta.get('template') or self.config.get('default_template')
        self.meta['build'] = self.meta.get('build')
        if isinstance(self.meta['build'], str):
            self.meta['build'] = self.config['dirs']['build'] / pathlib.Path(self.meta['build'])
        else:
            self.meta['build'] = self.config['dirs']['build'] / self.target.relative_to(self.root / self.config['remove_build_prefix'])
            self.meta['build'] = self.meta['build'].with_suffix('.html')

    def analyze_target(self):
        if self.target.is_file():
            config, content, meta = self.load_file(self.target)
        elif self.target.is_dir():
            config, content, meta = self.load_dir(self.target)
        else:
            self.logger.warning('WTF?')
            return False
        self.update(config, content, meta)
        return True

    def load_file(self, file):
        spec = importlib.util.spec_from_file_location('justic.data', file)
        data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data)
        content = {name: getattr(data, name) for name in dir(data) if not name.startswith('__') and name.isupper()}
        return getattr(data, '__JUSTIC__', {}), content, getattr(data, '__META__', {})

    def load_dir(self, directory):
        file = self.target / '__init__.py'
        if file.is_file():
            return self.load_file(file)
        return {}, {}, {}

    def get_targets(self):
        targets = self.meta.get('targets', [])
        target = self.meta.get('target')
        if target:
            targets.append(target)
        if len(targets) > 0:
            for target in targets:
                target = pathlib.Path(target)
                if not target.is_absolute():
                    if self.target.is_file():
                        target = self.target.parent / target
                    else:
                        target = self.target / target
                yield Justic(self.root, target, self.config, self.config)

        elif self.target.is_dir():
            for target in self.target.iterdir():
                if not target.name.startswith('__') and target.suffix in ['', '.py']:
                    yield Justic(self.root, target, self.config, self.config)

    def render(self):
        if self.meta.get('render', True) and isinstance(self.meta['template'], str):
            tmpenv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.config['dirs']['templates']))
            template = tmpenv.get_template(self.meta['template'])
            data = template.render(**self.content)
            self.meta['build'].parent.mkdir(parents=True, exist_ok=True)
            self.meta['build'].write_text(data)

    def copy_static(self):
        if 'static' in self.meta:
            static = pathlib.Path(self.meta['static'])
            if not static.is_absolute():
                if self.target.is_file():
                    static = self.target.parent / static
                else:
                    static = self.target / static
            staticbuild = self.config['dirs']['build'] / 'static'
            if staticbuild.is_dir():
                shutil.rmtree(staticbuild)
            shutil.copytree(static, staticbuild)

    def run(self):
        self.logger.debug('run meta=%s', self.meta)
        # self.logger.debug('run content=%s', self.content)
        # self.logger.debug('run config=%s', self.config)
        self.render()
        for target in self.get_targets():
            target.run()
        self.copy_static()
