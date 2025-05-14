from dataclasses import dataclass
from functools import cached_property

from elections_lk.base import NumDict
from elections_lk.core.raw_data import RawData
from elections_lk.core.result.VoteSummary import VoteSummary
from elections_lk.core.Votes import Votes


@dataclass
class PartyToVotes(NumDict):
    idx: dict[str, int]

    IGNORE_FIELDS = ["entity_id"] + VoteSummary.FIELDS

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
            if (
                k not in PartyToVotes.IGNORE_FIELDS
                and not RawData.is_extra_field(k)
            ):
                idx[k] = Votes.parse(v)
        idx = dict(sorted(idx.items(), key=lambda x: x[1], reverse=True))
        return cls.from_idx(idx)

    @cached_property
    def winning_party_id(self) -> str:
        return self.max_key
