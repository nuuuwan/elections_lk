from dataclasses import dataclass
from functools import cache, cached_property

from elections_lk.core.result.VoteSummary import VoteSummary
from elections_lk.core.Votes import Votes


@dataclass
class PartyToVotes:
    idx: dict[str, int]

    def __hash__(self):
        return hash(tuple(self.idx.items()))

    @classmethod
    def from_gig_table_row(cls, gig_table_row) -> 'PartyToVotes':
        idx = {}
        for k, v in gig_table_row.dict.items():
            if k not in ['id'] + VoteSummary.FIELDS:
                idx[k] = Votes.parse(v)
        return cls(idx)

    def __getattr__(self, key: str) -> int:
        return self.idx[key]

    @cached_property
    def total(self) -> int:
        return sum(self.idx.values())

    @cache
    def get_p(self, key: str) -> int:
        return self.idx[key] / self.total

    def items(self):
        return self.idx.items()

    @cache
    def p_items(self):
        return [(k, v / self.total) for k, v in self.idx.items()]
