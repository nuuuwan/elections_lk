from dataclasses import dataclass

from elections_lk.core.raw_data import RawData
from elections_lk.core.Votes import Votes


@dataclass
class SeatSummary:
    total_seats: int

    @classmethod
    def from_dict(cls, d) -> "SeatSummary":
        seats = [
            Votes.parse(v)
            for k, v in d.items()
            if RawData.is_extra_field(k, "seats")
        ]
        return cls(total_seats=sum(seats))
