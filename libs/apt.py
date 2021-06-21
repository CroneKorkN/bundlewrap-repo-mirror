# https://manpages.debian.org/jessie/apt/sources.list.5.de.html
from urllib.parse import urlparse
from re import match, search, sub


class AptSource():
    def __init__(self, string):
        if match(r'\[.*\]', string):
            self.options = {
                k:v.split('=') for k,v in (
                    e.split('=') for e in search(r'\[(.*)\]', string)[1].split()
                )
            }
        else:
            self.options = {}
        parts = sub(r'\[.*\]', '', string).split()
        self.type = parts[0]
        self.url = urlparse(parts[1])
        self.suite = parts[2]
        self.components = parts[3:]
    
    def render(self):
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

# source = AptSource('deb [arch=amd64 trusted=true] http://deb.debian.org/debian buster-backports main contrib non-free')
# print(repr(source))
# print(source.type)
# print(source.options)
# source.options['test'] = ['was', 'ist', 'das']
# print(source.url)
# print(source.suite)
# print(source.components)
# print(source.render())
