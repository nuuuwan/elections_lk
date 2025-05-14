from dataclasses import dataclass

from elections_lk.core.result.PartyToSeats import PartyToSeats
from elections_lk.core.result.PartyToVotes import PartyToVotes
from elections_lk.core.result.Result import Result
from elections_lk.core.result.SeatSummary import SeatSummary
from elections_lk.core.result.VoteSummary import VoteSummary


@dataclass
class ResultWithSeats(Result):
    seat_summary: SeatSummary
    party_to_seats: PartyToSeats

    def __init__(
        self,
        id: str,
        vote_summary: VoteSummary,
        party_to_votes: PartyToSeats,
        seat_summary: SeatSummary,
        party_to_seats: PartyToSeats,
    ):
        super().__init__(id, vote_summary, party_to_votes)
        self.seat_summary = seat_summary
        self.party_to_seats = party_to_seats

    @classmethod
    def from_dict(cls, d) -> "Result":
        return cls(
            id=d["entity_id"],
            vote_summary=VoteSummary.from_dict(d),
            party_to_votes=PartyToVotes.from_dict(d),
            seat_summary=SeatSummary.from_dict(d),
            party_to_seats=PartyToSeats.from_dict(d),
        )
