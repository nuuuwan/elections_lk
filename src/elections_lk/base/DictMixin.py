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
        return self.__class__({k: v / self.total for k, v in self.idx.items()})

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
        return self.__class__({k: v for k, v in self.idx.items() if func(k, v)})

    @cached_property
    def nonzero(self):
        return self.__class__({k: v for k, v in self.idx.items() if v != 0})

    def sort(self, custom_lambda=None):
        return self.__class__(
            dict(
                sorted(
                    self.idx.items(),
                    key=lambda x: (
                        x[1],
                        custom_lambda(x[0]) if custom_lambda else 0,
                    ),
                    reverse=True,
                )
            )
        )

    # Math - Operators
    def __add__(self, other):
        assert isinstance(other, DictMixin)
        union_keys = set(self.idx.keys()).union(other.idx.keys())
        return self.__class__(
            {k: self.idx.get(k, 0) + other.idx.get(k, 0) for k in union_keys}
        )

    def __mul__(self, other):
        return self.__class__({k: v * other for k, v in self.idx.items()})

    @staticmethod
    def concat(*items):
        print(items)
        sum_item = items[0]
        for item in items[1:]:
            sum_item += item
        return sum_item
