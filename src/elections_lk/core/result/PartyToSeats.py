from dataclasses import dataclass

from elections_lk.base import DictMixin
from elections_lk.core.raw_data import RawData
from elections_lk.core.result.VoteSummary import VoteSummary
from elections_lk.core.Votes import Votes


@dataclass
class PartyToSeats(DictMixin):
    idx: dict[str, int]

    IGNORE_FIELDS = ["entity_id"] + VoteSummary.FIELDS

    @classmethod
    def from_idx(cls, idx):
        sorted_idx = dict(
            sorted(idx.items(), key=lambda x: x[1], reverse=True)
        )
        return cls(sorted_idx)

    @classmethod
    def from_dict(cls, d) -> "PartyToSeats":
        idx = {}
        for k, v in d.items():
            if (
                k not in PartyToSeats.IGNORE_FIELDS
                and RawData.is_extra_field(k, "seats")
            ):
                idx[RawData.remove_extra_field(k)] = Votes.parse(v)
        idx = dict(sorted(idx.items(), key=lambda x: x[1], reverse=True))
        return cls.from_idx(idx)
