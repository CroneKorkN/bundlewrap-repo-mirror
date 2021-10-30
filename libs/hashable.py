import json
from functools import total_ordering

from bundlewrap.metadata import MetadataJSONEncoder


@total_ordering
class Hashable():
    def _json(self):
        return json.dumps(
            self,
            sort_keys=True,
            cls=MetadataJSONEncoder,
        )

    def __lt__(self, other):
        return self._json() < other._json()

    def __eq__(self, other):
        return self._json() == other._json()

    def __hash__(self):
        return hash(self._json())


class HashableDict(Hashable, dict):
    pass


class HashableSet(Hashable, set):
    pass


def hashable(object):
    return {
        dict: HashableDict,
        set: HashableSet,
    }[type(object)](object)
