from dataclasses import dataclass

from elections_lk.core.Votes import Votes


@dataclass
class VoteSummary:
    electors: int
    polled: int
    valid: int
    rejected: int

    FIELDS = ['electors', 'polled', 'valid', 'rejected']

    @classmethod
    def from_gig_table_row(cls, gig_table_row) -> 'VoteSummary':
        [electors, polled, valid, rejected] = [
            Votes.parse(gig_table_row.dict[field]) for field in cls.FIELDS
        ]

        # assert electors >= 0
        # assert polled >= 0
        # assert valid >= 0
        # assert rejected >= 0

        # assert electors >= polled
        # assert polled == valid + rejected

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
