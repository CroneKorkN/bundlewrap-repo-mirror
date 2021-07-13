class hdict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

class hlist(list):
    def __hash__(self):
        return hash(tuple(sorted(self)))
