# https://manpages.debian.org/latest/apt/sources.list.5.de.html
# https://repolib.readthedocs.io/en/latest/deb822-format.html

from re import match
from glob import glob
from os.path import join, basename, exists


def format_variables(node, string):
    return string.format(
        codename=node.metadata.get('os_codename'),
        version=node.os_version[0],
    )


def find_keyfile_extension(node, key_name):
    formatted_key_name = format_variables(node, key_name)

    for extension in ('asc', 'gpg'):
        if exists(join(node.repo.path, 'data', 'apt', 'keys', f'{formatted_key_name}.{extension}')):
            return extension
    else:
        raise Exception(f"no keyfile '{formatted_key_name}.(asc|gpg)' found")


def render_apt_conf(section, depth=0):
    buffer = ''

    for k,v in sorted(section.items()):
        if isinstance(v, dict):
            # element is a sub section
            assert match(r'^[a-zA-Z/\-\:\.\_\+]*$', k) and not match(r'::', k)
            buffer += ' '*4*depth + k + ' {\n'
            buffer += render_apt_conf(v, depth=depth+1)
            buffer += ' '*4*depth + '}\n'
        elif isinstance(v, (set, list)):
            # element is a value list
            buffer += ' '*4*depth + k + ' {\n'
            for e in sorted(v):
                buffer += ' '*4*(depth+1) + '"' + e + '";\n'
            buffer += ' '*4*depth + '}\n'
        else:
            # element is a single value
            buffer += ' '*4*depth + k + ' "' + v + '";\n'

    return buffer



def render_source(node, source_name):
    config = node.metadata.get(f'apt/sources/{source_name}')
    lines = []

    # X-Repolib-Name
    lines.append(
        f'X-Repolib-Name: ' + source_name
    )

    # types
    lines.append(
        f'Types: ' + ' '.join(sorted(config.get('types', {'deb'})))
    )

    # url
    lines.append(
        f'URIs: ' + config['url']
    )

    # suites
    lines.append(
        f'Suites: ' + ' '.join(sorted(config['suites']))
    )

    # components
    if 'components' in config:
        lines.append(
            f'Components: ' + ' '.join(sorted(config['components']))
        )

    # options
    for key, value in sorted(config['options'].items()):
        if isinstance(value, (set, list)):
            value = ' '.join(value)

        lines.append(
            f'{key}: ' + value
        )

    # render to string and format variables
    return format_variables(node, '\n'.join(lines) + '\n')
