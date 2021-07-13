import json

class hdict(dict):
    def __hash__(self):
        return hash(json.dumps(self, sorted=True))

class hlist(list):
    def __hash__(self):
        return hash(json.dumps(self, sorted=True))
