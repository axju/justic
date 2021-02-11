import pathlib

DEFAULT = {
    'BUILD_DIR': 'build',
}


class Settings(dict):
    """docstring for Settings."""

    def __init__(self, **kwargs):
        super(Settings, self).__init__()
        self['workdir'] = pathlib.Path(kwargs.get('workdir', '.')).absolute()
        self['contentdir'] = self['workdir'] / kwargs.get('contentdir', 'content')
        self['builddir'] = self['workdir'] / kwargs.get('builddir', 'build')
