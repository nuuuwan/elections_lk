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

    @cached_property
    def p_dict(self):
        return dict(self.p_items())

    @cached_property
    def dict(self):
        return self.idx

    @cache
    def get_parties(self, min_p_votes: float = 0) -> list[str]:
        return [k for k, v in self.p_items() if v >= min_p_votes]
