import logging


import jinja2

from justic.settings import Settings


class Justic:

    def __init__(self, **kwargs):
        self.logger = logging.getLogger('justic.Justic')
        self.settings = Settings(**kwargs)
        self.tmpenv = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=self.settings['workdir'] / 'templates')
        )

    def run(self):
        self.logger.info('run')
        self.settings['builddir'].mkdir(parents=True, exist_ok=True)
        for file in self.settings['contentdir'].glob('**/*'):
            print(file)
            template = self.tmpenv.get_template('index.html')
            data = template.render()
            outputfile = self.settings['builddir'] / file.relative_to(self.settings['contentdir']).with_suffix('.html')
            print(outputfile)
            outputfile.write_text(data)
