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
    def from_dict(cls, d) -> "PartyToVotes":
        idx = {}
        for k, v in d.items():
            if k not in ["entity_id"] + VoteSummary.FIELDS:
                idx[k] = Votes.parse(v)
        idx = dict(sorted(idx.items(), key=lambda x: x[1], reverse=True))
        return cls.from_idx(idx)

    @cached_property
    def total(self) -> int:
        return sum(self.idx.values())

    @cache
    def p(self, key: str) -> int:
        if key not in self.idx:
            return 0
        return self.idx[key] / self.total

    @cached_property
    def winning_party_id(self) -> str:
        return next(iter(self.idx.keys()))

    @cache
    def get_party_to_votes_othered(self, threshold: float) -> "PartyToVotes":
        idx = {}
        total = self.total
        for party, votes in self.idx.items():
            if votes / total >= threshold:
                idx[party] = votes
            else:
                idx["other"] = idx.get("other", 0) + votes
        return PartyToVotes.from_idx(idx)

    @cached_property
    def party_to_pvotes(self) -> "PartyToVotes":
        return PartyToVotes.from_idx(
            {k: v / self.total for k, v in self.idx.items()}
        )
