class DictMixin:

    def __init__(self, *args, **kwargs):
        self._dict = {}
        for key, value in dict(*args, **kwargs).items():
            self[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __getattr__(self, key: str) -> int:
        return self.idx[key]

    def items(self):
        return self.idx.items()

    def keys(self):
        return self.idx.keys()

    def values(self):
        return self.idx.values()
