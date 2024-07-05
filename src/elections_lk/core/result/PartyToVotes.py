from dataclasses import dataclass

from elections_lk.core.result.VoteSummary import VoteSummary
from elections_lk.core.Votes import Votes


@dataclass
class PartyToVotes:
    idx: dict[str, int]

    @classmethod
    def from_gig_table_row(cls, gig_table_row) -> 'PartyToVotes':
        idx = {}
        for k, v in gig_table_row.dict.items():
            if k not in ['id'] + VoteSummary.FIELDS:
                idx[k] = Votes.parse(v)
        return cls(idx)

    def __getattr__(self, key: str) -> int:
        return self.idx[key]

    @property
    def total(self) -> int:
        return sum(self.idx.values())

    def get_p(self, key: str) -> int:
        return self.idx[key] / self.total
