class DictMixin:

    # Assumes that self.idx exists

    def __hash__(self):
        return hash(tuple(self.idx.items()))

    def __contains__(self, key):
        return key in self.idx

    def __iter__(self):
        return iter(self.idx)

    def __len__(self):
        return len(self.idx)

    def __getattr__(self, key: str) -> int:
        return self.idx[key]

    def items(self):
        return self.idx.items()

    def keys(self):
        return self.idx.keys()

    def values(self):
        return self.idx.values()
