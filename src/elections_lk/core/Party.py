from dataclasses import dataclass
from functools import cache


@dataclass
class Party:
    code: str
    color: str

    @staticmethod
    @cache
    def list_all():
        return [
            Party('JVP', '#f00'),
            Party('NDF', '#080'),
            Party('NMPP', '#f00'),
            Party('SLPP', '#800'),
            Party("PA", "#008"),
            Party("SLFP", "#008"),
            Party("SLMP", "#f08"),
            Party("UNP", "#080"),
            Party("UPFA", "#008"),
        ]

    @staticmethod
    @cache
    def idx():
        return {p.code: p for p in Party.list_all()}

    @staticmethod
    @cache
    def from_code(code: str):
        idx = Party.idx()
        if code in idx:
            return idx[code]
        return Party(code, 'gray')
