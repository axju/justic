import sys
import pathlib
import shutil
import logging
import importlib.util

import jinja2


def check_file(file):
    spec = importlib.util.spec_from_file_location('justic.data', file)
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    content = {name: getattr(data, name) for name in dir(data) if not name.startswith('__')}
    return content.get('META', {}), content


class Directories(dict):
    """Manage the directories"""

    def __init__(self, **kwargs):
        super().__init__()
        self['work'] = pathlib.Path(kwargs.get('workdir', '.')).absolute()
        self['build'] = self['work'] / kwargs.get('build', 'build')
        self['content'] = self['work'] / kwargs.get('content', 'content')
        self['templates'] = self['work'] / kwargs.get('templates', 'templates')
        self['static'] = self['work'] / kwargs.get('static', 'static')


class Justic:

    def __init__(self, **kwargs):
        self.logger = logging.getLogger('justic.Justic')
        self.kwargs = kwargs
        self.directories = Directories(**kwargs)
        self.config = self.directories['work'] / kwargs.get('config', 'justiconf.py')

    def load_global(self):
        if self.config.is_file():
            return check_file(self.config)
        return 'base.html', {}

    def get_outputfile(self, file):
        return self.directories['build'] / file.relative_to(self.directories['content']).with_suffix('.html')

    def render(self):
        tmpenv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.directories['templates']))
        default_meta, global_content = self.load_global()
        for file in self.directories['content'].glob('**/*.py'):
            meta, content = check_file(file)
            template = tmpenv.get_template(meta.get('template') or default_meta.get('template', 'base.html'))
            content.update(global_content)
            data = template.render(**content)
            self.get_outputfile(file).write_text(data)
            self.logger.info('create file %s', self.get_outputfile(file))
            self.logger.debug('content %s', content)

    def copy_static(self):
        staticbuild = self.directories['build'] / 'static'
        if staticbuild.is_dir():
            shutil.rmtree(staticbuild)
        shutil.copytree(self.directories['static'], staticbuild)

    def run(self):
        self.logger.info('run')
        if self.kwargs.get('delete', False) and self.directories['build'].is_dir():
            shutil.rmtree(self.directories['build'])
        sys.path.append(str(self.directories['work']))
        self.directories['build'].mkdir(parents=True, exist_ok=True)
        self.copy_static()
        self.render()
