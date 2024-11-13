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
            Party("JVP", "#f00"),
            Party("NMPP", "#f00"),
            Party("NPP", "#f00"),
            Party("SLPP", "#800"),
            Party("PA", "#008"),
            Party("SLFP", "#008"),
            Party("UPFA", "#008"),
            Party("SLPP", "#008"),
            Party("NDF", "#080"),
            Party("UNP", "#080"),
            Party("SJB", "#080"),
            Party("SLMP", "#f08"),
            Party("IND16", "#f80"),
            Party("IND4", "#00c"),
            Party("dnv", "#880"),
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
        return Party(code, "#888")
