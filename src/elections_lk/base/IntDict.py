from elections_lk.base.DictMixin import DictMixin


class IntDict(DictMixin):
    def __init__(self, idx: dict[str, int]):
        self.idx = idx
