# https://manpages.debian.org/jessie/apt/sources.list.5.de.html

from urllib.parse import urlparse
from re import search, sub
from functools import total_ordering
from re import match


def render_apt_conf(section, depth=0):
    buffer = ""

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


@total_ordering
class AptSource():
    def __init__(self, string):
        # parse options, which are optional
        if search(r'\[.*\]', string):
            self.options = {
                k:v.split(',')
                    for k,v in (
                        e.split('=') for e in search(r'\[(.*)\]', string)[1].split()
                    )
            }
            string_without_options = sub(r'\[.*\]', '', string)
        else:
            self.options = {}
            string_without_options = string

        # parse rest of source, now in defined order
        parts = string_without_options.split()
        self.type = parts[0]
        self.url = urlparse(parts[1])
        self.suite = parts[2]
        self.components = parts[3:]

    def __str__(self):
        parts = [
            self.type,
            self.url.geturl(),
            self.suite,
            ' '.join(self.components),
        ]

        if self.options:
            parts.insert(
                1,
                "[{}]".format(
                    ' '.join(
                        '{}={}'.format(
                            k,
                            ','.join(v)
                        ) for k,v in self.options.items()
                    )
                )
            )

        return ' '.join(parts)


    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f"{type(self).__name__}('{str(self)}')"


# source = AptSource('deb [arch=amd64 trusted=true] http://deb.debian.org/debian buster-backports main contrib non-free')
# print(repr(source))
# print(source.type)
# print(source.options)
# source.options['test'] = ['was', 'ist', 'das']
# print(source.url)
# print(source.suite)
# print(source.components)
# print(str(source))
