from functools import total_ordering


@total_ordering
class Version():
    def __init__(self, string):
        self._tuple = self.tupelize(string)

    def __lt__(self, other):
        return self._tuple < self.tupelize(other)

    def __eq__(self, other):
        return self._tuple == self.tupelize(other)

    def __repr__(self):
        return f'{type(self).__name__}({repr(self._tuple)})'

    def __str__(self):
        return '.'.join(str(i) for i in self._tuple)

    @staticmethod
    def tupelize(version):
        if isinstance(version, (int, float, str, Version)):
            return tuple(int(i) for i in str(version).split('.'))
        elif type(version) == tuple:
            return version
        else:
            raise TypeError(type(version))
