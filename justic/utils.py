import logging
import pathlib
import shutil
import importlib.util

import jinja2

logger = logging.getLogger(__name__)


def defaults(root, target, config):
    """return config, content, meta"""
    dirs = {'root': pathlib.Path(root).absolute()}
    dirs['build'] = dirs['root'] / 'build'
    dirs['templates'] = dirs['root'] / 'templates'
    funcs = {
        'default': defaults,
        'analyze_current': analyze_current,
    }
    config.get('dirs', {}).update(dirs)
    config.get('funcs', {}).update(funcs)

    meta = {'current': pathlib.Path(target)}
    if not meta['current'].is_absolute():
        meta['current'] = dirs['root'] / meta['current']

    return config, {}, meta


def update_config(config, meta):
    result = config if isinstance(config, dict) else {}
    meta = meta if isinstance(meta, dict) else {}
    result['remove_build_prefix'] = config.get('remove_build_prefix', '.')
    for directory in meta.get('dirs', {}).values():
        if not isinstance(directory, pathlib.Path):
            directory = pathlib.Path(directory)
        if not directory.is_absolute():
            directory = result.get('dirs', {})['root'] / directory
    return result


def update_meta(config, meta):
    result = meta if isinstance(meta, dict) else {}
    config = config if isinstance(config, dict) else {}
    result['render'] = meta.get('render', True) and meta.get('current').is_file()
    result['template'] = meta.get('template') or config.get('default_template')
    result['build'] = meta.get('build')
    if isinstance(meta['build'], str):
        result['build'] = config['dirs']['build'] / pathlib.Path(meta['build'])
    else:
        output = result['current'].relative_to(config['dirs']['root'] / config['remove_build_prefix'])
        result['build'] = config['dirs']['build'] / output
        result['build'] = result['build'].with_suffix('.html')
    return result


def load_file(file):
    if not pathlib.Path(file).is_file():
        logger.warning('"%s" is no file, no conten load', file)
        return {}, {}, {}
    spec = importlib.util.spec_from_file_location('justic.data', file)
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    content = {name: getattr(data, name) for name in dir(data) if not name.startswith('__') and name.isupper()}
    return getattr(data, '__JUSTIC__', {}), content, getattr(data, '__META__', {})


def load_dir(directory):
    """directory could be string or pathlib.Path"""
    file = pathlib.Path(directory) / '__init__.py'
    if file.is_file():
        return load_file(file)
    return {}, {}, {}


def analyze_current(current):
    item = pathlib.Path(current)
    if item.is_file():
        return load_file(item)
    if item.is_dir():
        return load_dir(item)
    return {}, {}, {}


def get_targets(config, content, meta):
    targets = meta.get('targets', [])
    target = meta.get('target')
    if target:
        targets.append(target)
    if len(targets) > 0:
        for targ in map(pathlib.Path, targets):
            if not targ.is_absolute():
                target = meta['current'].parent / targ if meta['current'].is_file() else meta['current'] / targ
            yield target, config, content

    elif meta['current'].is_dir():
        for target in meta['current'].iterdir():
            if not target.name.startswith('__') and target.suffix in ['', '.py']:
                yield target, config, content


def render(config, content, meta):
    if not meta.get('render', True) or not isinstance(meta.get('template'), str):
        logger.debug('nothing to render')
        return
    tmpenv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=config['dirs']['templates']))
    template = tmpenv.get_template(meta['template'])
    data = template.render(**content)
    meta['build'].parent.mkdir(parents=True, exist_ok=True)
    meta['build'].write_text(data)
    logger.info('save file "%s"', meta['build'])


def copy_static(config, meta):
    if 'static' in meta:
        static = pathlib.Path(meta['static'])
        if not static.is_absolute():
            if meta['current'].is_file():
                static = meta['current'].parent / static
            else:
                static = meta['current'] / static
        staticbuild = config['dirs']['build'] / 'static'
        if staticbuild.is_dir():
            shutil.rmtree(staticbuild)
        shutil.copytree(static, staticbuild)
