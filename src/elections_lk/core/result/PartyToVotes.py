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
    def from_idx(cls, idx):
        sorted_idx = dict(
            sorted(idx.items(), key=lambda x: x[1], reverse=True)
        )
        return cls(sorted_idx)

    @classmethod
    def from_dict(cls, d) -> 'PartyToVotes':
        idx = {}
        for k, v in d.items():
            if k not in ['entity_id'] + VoteSummary.FIELDS:
                idx[k] = Votes.parse(v)
        idx = dict(sorted(idx.items(), key=lambda x: x[1], reverse=True))
        return cls.from_idx(idx)

    @classmethod
    def from_list(cls, party_to_votes_list) -> 'PartyToVotes':
        idx = {}
        for party_to_votes in party_to_votes_list:
            for party, votes in party_to_votes.items():
                idx[party] = idx.get(party, 0) + votes
        return cls.from_idx(idx)

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

    @cached_property
    def total(self) -> int:
        return sum(self.idx.values())

    @cache
    def p(self, key: str) -> int:
        return self.idx[key] / self.total

    @cached_property
    def winning_party_id(self) -> str:
        return next(iter(self.idx.keys()))
