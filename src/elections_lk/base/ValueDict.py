from utils import Dict


class ValueDict(Dict):
    OTHERS = 'others'

    def __len__(self):
        return len(self.keys())

    @property
    def total(self):
        return sum(self.values())

    @property
    def d(self):
        return self.x

    @property
    def dict(self):
        return self.x

    @property
    def dict_p(self):
        return {k: v / self.total for k, v in self.items()}

    def keys_sorted(self):
        return [item[0] for item in self.items_sorted()]

    def items_sorted(self):
        return sorted(self.items(), key=lambda x: x[1], reverse=True)

    def items_othered(self, max_p_other=0.001):
        p_other = 0
        n_other = 0
        items = []
        for item in self.items_sorted():
            v = item[1]
            p = v / self.total
            if p < max_p_other:
                p_other += p
                n_other += v
            else:
                items.append(item)
        items.append((self.OTHERS, n_other))
        return items

    def get_othered_dict(self, keys):
        d = {}
        others = 0
        for k, v in self.items():
            if k in keys:
                d[k] = v
            else:
                others += v
        d[self.OTHERS] = others
        return d

    @classmethod
    def concat(cls, dict_list):
        d = {}
        for _dict in dict_list:
            for k, v in _dict.items():
                d[k] = d.get(k, 0) + v
        return cls(d)
