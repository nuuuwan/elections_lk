from functools import cache, cached_property


class DictMixin:

    # Assumes that self.idx exists, and that idx is sorted by value descending

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

    def __getitem__(self, key: str) -> int:
        return self.idx[key]

    def items(self):
        return self.idx.items()

    def keys(self):
        return self.idx.keys()

    def values(self):
        return self.idx.values()

    # Math

    @cached_property
    def total(self) -> int:
        return sum(self.idx.values())

    @cache
    def get_p(self, key: str) -> int:
        if key not in self.idx:
            return 0
        return self.idx[key] / self.total

    @cached_property
    def max_key(self) -> str:
        return next(iter(self.idx.keys()))
