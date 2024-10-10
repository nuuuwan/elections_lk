from dataclasses import dataclass
from functools import cached_property

from elections_lk.core.result.PartyToVotes import PartyToVotes
from elections_lk.core.result.VoteSummary import VoteSummary


@dataclass
class Result:
    id: str
    vote_summary: VoteSummary
    party_to_votes: PartyToVotes

    @classmethod
    def from_dict(cls, d) -> 'Result':
        return cls(
            id=d['entity_id'],
            party_to_votes=PartyToVotes.from_dict(d),
            vote_summary=VoteSummary.from_dict(d),
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

    @cached_property
    def winning_party_id(self) -> str:
        return self.party_to_votes.winning_party_id
