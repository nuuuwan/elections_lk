from elections_lk.base.DictMixin import DictMixin


class FloatDict(DictMixin):
    def __init__(self, idx: dict[str, float]):
        self.idx = idx
