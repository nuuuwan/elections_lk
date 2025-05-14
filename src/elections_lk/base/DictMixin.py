from functools import cached_property


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

    def __getattr__(self, key: str):
        return self.idx[key]

    def __getitem__(self, key: str):
        return self.idx[key]

    def items(self):
        return self.idx.items()

    def keys(self):
        return self.idx.keys()

    def values(self):
        return self.idx.values()

    # Math

    @cached_property
    def total(self):
        return sum(self.idx.values())

    @cached_property
    def norm(self):
        return self.__class__(
            {k: v / self.total for k, v in self.idx.items()}
        )

    @cached_property
    def int(self):
        return self.__class__({k: int(v) for k, v in self.idx.items()})

    @cached_property
    def non_int(self):
        return self.__class__({k: v - int(v) for k, v in self.idx.items()})

    @cached_property
    def max_key(self) -> str:
        return next(iter(self.idx.keys()))

    def filter(self, func):
        return self.__class__(
            {k: v for k, v in self.idx.items() if func(k, v)}
        )

    @cached_property
    def nonzero(self):
        return self.__class__({k: v for k, v in self.idx.items() if v != 0})

    # Math - Operators
    def __mul__(self, other):
        return self.__class__({k: v * other for k, v in self.idx.items()})
