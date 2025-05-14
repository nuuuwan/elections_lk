from dataclasses import dataclass

from elections_lk.core.Votes import Votes


@dataclass
class VoteSummary:
    electors: int
    polled: int
    valid: int
    rejected: int

    FIELDS = ["electors", "polled", "valid", "rejected"]

    @classmethod
    def from_dict(cls, d) -> "VoteSummary":
        [electors, polled, valid, rejected] = [
            Votes.parse(d[field]) for field in cls.FIELDS
        ]

        return cls(electors, polled, valid, rejected)

    @property
    def p_turnout(self) -> float:
        return self.polled / self.electors

    @property
    def p_valid(self) -> float:
        return self.valid / self.polled

    @property
    def p_rejected(self) -> float:
        return self.rejected / self.polled
