from dataclasses import dataclass

from elections_lk.core.result.PartyToVotes import PartyToVotes
from elections_lk.core.result.VoteSummary import VoteSummary


@dataclass
class ResultPD:
    id: str
    vote_summary: VoteSummary
    party_to_votes: PartyToVotes

    @classmethod
    def from_gig_table_row(cls, gig_table_row) -> 'ResultPD':
        return cls(
            id=gig_table_row.id,
            party_to_votes=PartyToVotes.from_gig_table_row(gig_table_row),
            vote_summary=VoteSummary.from_gig_table_row(gig_table_row),
        )
