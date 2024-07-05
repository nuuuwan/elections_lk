from dataclasses import dataclass

from elections_lk.core.result.PartyToVotes import PartyToVotes
from elections_lk.core.result.VoteSummary import VoteSummary


@dataclass
class Result:
    id: str
    vote_summary: VoteSummary
    party_to_votes: PartyToVotes

    @classmethod
    def from_gig_table_row(cls, gig_table_row) -> 'Result':
        return cls(
            id=gig_table_row.id,
            party_to_votes=PartyToVotes.from_gig_table_row(gig_table_row),
            vote_summary=VoteSummary.from_gig_table_row(gig_table_row),
        )

    @classmethod
    def from_list(cls, id, results_list) -> 'Result':
        return cls(
            id=id,
            party_to_votes=PartyToVotes.from_list(
                [result.party_to_votes for result in results_list]
            ),
            vote_summary=VoteSummary.from_list(
                [result.vote_summary for result in results_list]
            ),
        )
